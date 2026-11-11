// Fiscal × operacional, lado fiscal (Estoque Fiscal > "Fiscal × operacional", T17 cap10), como a RPC do banco
// (migrations 20260920234500 e anteriores): por material, entrada e saída das NF-e EMITIDAS no período (quantidade e valor pelo
// CFOP do item; CFOP sem efeito vai para "não classificado"); mov_fiscal = entrada - saída. O lado operacional é a
// get_inventory_report_data (o app junta os dois e calcula o Delta).
import { efeitoCfop } from '../../lib/estoque_fiscal.mjs';

export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const ini = new Date(a.p_start_date).getTime();
  const fim = new Date(a.p_end_date).getTime();
  const notas = new Map(store.rows('invoices').filter((i) => i.company_id === cid && i.status === 'emitida' && i.environment !== 'homologacao'
    && !i.archived_at && i.computa_estoque_fiscal !== false && (!a.p_fiscal_config_id || i.fiscal_config_id === a.p_fiscal_config_id)
    && new Date(i.issue_date).getTime() >= ini && new Date(i.issue_date).getTime() <= fim).map((i) => [i.id, i]));
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const por = new Map();
  for (const it of store.rows('invoice_items')) {
    if (!notas.has(it.invoice_id)) continue;
    const k = it.material_id || null;
    if (!por.has(k)) {
      const m = mats.get(k) || null;
      por.set(k, { material_id: k, material_name: (m && ((m.fiscal_name || '').trim() || m.name)) || it.material_name || null,
        material_code: m ? m.code : null, unit: (m && m.unit) || it.unit, entrada_qtd: 0, entrada_valor: 0, saida_qtd: 0, saida_valor: 0,
        mov_fiscal_qtd: 0, nao_class_qtd: 0, nao_class_valor: 0, _un: new Set(), is_archived: !!(m && m.is_archived) });
    }
    const r = por.get(k);
    const q = Number(it.quantity) || 0;
    const v = Number(it.total_price) || 0;
    const ef = efeitoCfop(it.cfop);
    if (ef === 1) { r.entrada_qtd += q; r.entrada_valor += v; r.mov_fiscal_qtd += q; }
    else if (ef === -1) { r.saida_qtd += q; r.saida_valor += v; r.mov_fiscal_qtd -= q; }
    else { r.nao_class_qtd += q; r.nao_class_valor += v; }
    r._un.add(String(it.unit || '').toUpperCase());
  }
  const r2 = (n) => Math.round(n * 100) / 100;
  return [...por.values()].map(({ _un, ...r }) => ({ ...r, entrada_valor: r2(r.entrada_valor), saida_valor: r2(r.saida_valor),
    nao_class_valor: r2(r.nao_class_valor), distinct_units: _un.size }))
    .sort((x, y) => String(x.material_name).localeCompare(String(y.material_name), 'pt-BR'));
};
