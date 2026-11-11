// Estoque fiscal (T17): o livro de movimentos que as RPCs do banco montam em `_get_fiscal_inventory_movements`
// (migration 20261023221000_fiscal_inventory_ledger_and_kardex.sql) e o recorte pelo saldo inicial ativo. Usado por
// get_fiscal_inventory_position, get_fiscal_inventory_position_at e get_fiscal_inventory_history_paged.
//  - NF-e emitidas e canceladas (não homologação, não arquivadas, `computa_estoque_fiscal`), um movimento por item, com o sinal do
//    CFOP (1102/2102/1202/1910 entram; 5102/6102/6101/5502/6502/5927/5151/5152/6151/6152 saem; o resto "unclassified");
//    a cancelada ganha o estorno ("reversal") na data do cancelamento.
//  - Saldo inicial e ajustes de `fiscal_inventory_entries` (tabela dinâmica: a 1.59.154 ainda não a tem no types.ts).
//  - O saldo inicial ATIVO (o mais recente por material, sem estorno) vira a base: só entram os movimentos depois dele.
import crypto from 'node:crypto';

const ENTRA = new Set(['1102', '2102', '1202', '1910']);
const SAI = new Set(['5102', '6102', '6101', '5502', '6502', '5927', '5151', '5152', '6151', '6152']);
export const efeitoCfop = (cfop) => (ENTRA.has(String(cfop)) ? 1 : SAI.has(String(cfop)) ? -1 : 0);
const uuidMd5 = (s) => {
  const h = crypto.createHash('md5').update(s).digest('hex');
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20, 32)}`;
};
const ms = (v) => (v ? new Date(v).getTime() : NaN);

export function movimentos(store, cid, cfgId = null) {
  const mats = new Map(store.rows('materials').filter((m) => m.company_id === cid).map((m) => [m.id, m]));
  const nomeDe = (tab, id) => (id ? store.rows(tab).find((r) => r.id === id)?.name ?? null : null);
  const perfil = (id) => (id ? store.rows('profiles').find((p) => p.id === id)?.full_name ?? null : null);
  const notas = new Map(store.rows('invoices').filter((i) => i.company_id === cid && ['emitida', 'cancelada'].includes(i.status)
    && i.environment !== 'homologacao' && !i.archived_at && i.computa_estoque_fiscal !== false
    && (!cfgId || i.fiscal_config_id === cfgId)).map((i) => [i.id, i]));
  const out = [];
  for (const it of store.rows('invoice_items')) {
    const n = notas.get(it.invoice_id);
    if (!n) continue;
    const m = mats.get(it.material_id) || null;
    const ef = efeitoCfop(it.cfop);
    const base = {
      source_type: 'invoice', source_id: n.id, fiscal_config_id: n.fiscal_config_id, material_id: m ? m.id : null,
      material_name: (m && ((m.fiscal_name || '').trim() || m.name)) || it.material_name || 'Sem material vinculado',
      material_code: m ? m.code : null, unit: (m && m.unit) || it.unit, invoice_id: n.id, invoice_number: String(n.invoice_number),
      nfe_key: n.nfe_key || null, cfop: it.cfop, partner_name: nomeDe('customers', n.customer_id) || nomeDe('suppliers', n.supplier_id),
      created_by_name: perfil(n.created_by),
    };
    out.push({ ...base, movement_id: uuidMd5(`outbound:issued:${n.id}:${it.id}`), movement_type: ef === 1 ? 'entry' : ef === -1 ? 'exit' : 'unclassified',
      occurred_at: n.issue_date, quantity_delta: Number(it.quantity) * ef, reason: null });
    if (n.status === 'cancelada') {
      out.push({ ...base, movement_id: uuidMd5(`outbound:cancelled:${n.id}:${it.id}`), movement_type: 'reversal',
        occurred_at: n.cancelled_at || n.updated_at || n.issue_date, quantity_delta: -Number(it.quantity) * ef,
        reason: (n.cancellation_reason || '').trim() || 'Cancelamento da NF-e' });
    }
  }
  for (const e of store.rows('fiscal_inventory_entries')) {
    if (e.company_id !== cid || (cfgId && e.fiscal_config_id !== cfgId)) continue;
    const m = mats.get(e.material_id) || null;
    out.push({
      movement_id: e.id, movement_type: e.entry_type === 'opening_balance' ? 'opening_balance' : e.entry_type === 'manual_adjustment' ? 'adjustment' : 'reversal',
      source_type: 'manual_entry', source_id: e.id, fiscal_config_id: e.fiscal_config_id, material_id: e.material_id,
      material_name: (m && ((m.fiscal_name || '').trim() || m.name)) || 'Material sem nome', material_code: m ? m.code : null, unit: m ? m.unit : null,
      occurred_at: e.effective_at, quantity_delta: Number(e.quantity_delta), invoice_id: null, invoice_number: null, nfe_key: null, cfop: null,
      partner_name: null, reason: e.reason || null, created_by_name: perfil(e.created_by),
    });
  }
  return out;
}

/** saldos iniciais ativos por `config|material` (o mais recente, sem estorno), até `ate` (ms) se dado */
export function aberturas(store, cid, cfgId = null, ate = Infinity) {
  const todas = store.rows('fiscal_inventory_entries').filter((e) => e.company_id === cid && (!cfgId || e.fiscal_config_id === cfgId));
  const estornadas = new Set(todas.filter((e) => e.reverses_entry_id).map((e) => e.reverses_entry_id));
  const out = new Map();
  for (const e of todas) {
    if (e.entry_type !== 'opening_balance' || estornadas.has(e.id) || ms(e.effective_at) > ate) continue;
    const k = `${e.fiscal_config_id}|${e.material_id}`;
    const cur = out.get(k);
    if (!cur || ms(e.effective_at) > ms(cur.effective_at) || (ms(e.effective_at) === ms(cur.effective_at) && String(e.created_at) > String(cur.created_at))) out.set(k, e);
  }
  return out;
}

/** movimentos dentro do recorte do saldo inicial (o próprio saldo inicial + o que veio depois dele) */
export function recortados(store, cid, cfgId = null, ate = Infinity) {
  const ab = aberturas(store, cid, cfgId, ate);
  return movimentos(store, cid, cfgId).filter((mv) => {
    if (ms(mv.occurred_at) > ate) return false;
    const a = ab.get(`${mv.fiscal_config_id}|${mv.material_id}`);
    return !a || mv.movement_id === a.id || ms(mv.occurred_at) > ms(a.effective_at);
  });
}

const ordem = (a, b) => ms(a.occurred_at) - ms(b.occurred_at) || String(a.movement_id).localeCompare(String(b.movement_id));

/** linhas da posição (RETURNS TABLE de get_fiscal_inventory_position), ordenadas por nome */
export function posicao(store, cid, cfgId = null, ate = Infinity) {
  const ab = aberturas(store, cid, cfgId, ate);
  const mvs = recortados(store, cid, cfgId, ate);
  const grupos = new Map();
  const chave = (c, m) => `${c}|${m}`;
  for (const mv of mvs) {
    const k = chave(mv.fiscal_config_id, mv.material_id);
    if (!grupos.has(k)) grupos.set(k, { cfg: mv.fiscal_config_id, mat: mv.material_id, mvs: [] });
    grupos.get(k).mvs.push(mv);
  }
  for (const [k, a] of ab) if (!grupos.has(k)) grupos.set(k, { cfg: a.fiscal_config_id, mat: a.material_id, mvs: [] });
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const out = [];
  for (const [k, g] of grupos) {
    const a = ab.get(k) || null;
    const m = mats.get(g.mat) || null;
    const soma = (f) => g.mvs.filter(f).reduce((s, x) => s + x.quantity_delta, 0);
    out.push({
      fiscal_config_id: g.cfg, material_id: g.mat,
      material_name: (m && ((m.fiscal_name || '').trim() || m.name)) || g.mvs[0]?.material_name || 'Sem material vinculado',
      material_code: m ? m.code : null, unit: (m && m.unit) || g.mvs[0]?.unit || null,
      opening_quantity: a ? Number(a.quantity_delta) : 0, opening_date: a ? a.effective_at : null,
      entradas_qtd: soma((x) => x.movement_type === 'entry' || (x.movement_type === 'reversal' && x.invoice_id && x.quantity_delta < 0)),
      saidas_qtd: -soma((x) => x.movement_type === 'exit' || (x.movement_type === 'reversal' && x.invoice_id && x.quantity_delta > 0)),
      ajustes_qtd: soma((x) => !x.invoice_id && (['adjustment', 'reversal'].includes(x.movement_type) || (x.movement_type === 'opening_balance' && !a))),
      current_quantity: soma(() => true), has_opening_balance: !!a, is_archived: !!(m && m.is_archived),
    });
  }
  return out.sort((x, y) => x.material_name.localeCompare(y.material_name, 'pt-BR') || String(x.fiscal_config_id).localeCompare(String(y.fiscal_config_id)));
}

/** Kardex (get_fiscal_inventory_history_paged): saldo contínuo antes dos filtros e da paginação */
export function kardex(store, cid, a) {
  const mvs = recortados(store, cid, a.p_fiscal_config_id || null).sort(ordem);
  const saldo = new Map();
  const com = mvs.map((mv) => {
    const k = `${mv.fiscal_config_id}|${mv.material_id}`;
    const antes = saldo.get(k) || 0;
    const depois = antes + mv.quantity_delta;
    saldo.set(k, depois);
    return { ...mv, balance_before: antes, balance_after: depois };
  });
  const busca = (a.p_search || '').trim().toLowerCase();
  const ini = a.p_start_date ? ms(a.p_start_date) : -Infinity;
  const fim = a.p_end_date ? ms(a.p_end_date) : Infinity;
  const filt = com.filter((x) => ms(x.occurred_at) >= ini && ms(x.occurred_at) <= fim
    && (!a.p_material_id || x.material_id === a.p_material_id)
    && (!(a.p_movement_type || '').trim() || x.movement_type === a.p_movement_type.trim())
    && (!busca || [x.invoice_number, x.nfe_key, x.partner_name, x.material_name, x.material_code, x.reason].some((v) => v && String(v).toLowerCase().includes(busca))));
  filt.sort((x, y) => -ordem(x, y));
  const tam = Number(a.p_page_size) || 50;
  const pag = Math.max(1, Number(a.p_page) || 1);
  return { items: filt.slice((pag - 1) * tam, pag * tam), total_count: filt.length };
}
