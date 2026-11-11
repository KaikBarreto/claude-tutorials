// RPC push_group_assets_to_company (20260528001000), o "Enviar Ativos" da aba Unidades: só a dona, para uma filial ATIVA. 1) Materiais do
// catálogo: o de mesmo nome na filial só é atualizado (e contado) se estiver arquivado, sem preço, sem código ou sem NCM, ou com "Sobrescrever
// preços"; o que falta é criado com os preços da tabela padrão do grupo; os dois casos ganham o vínculo. 2) Com "Tabelas de Preço" (ou
// materiais + sobrescrever): a tabela PRINCIPAL da filial recebe os preços da tabela padrão do grupo e, com "Tabelas de Preço", os materiais
// também (como o SQL faz, mesmo sem a chave). 3) Categorias que faltam (nome + tipo). 4) As outras tabelas do grupo (cria as que faltam).
// 5/6) Clientes e fornecedores compartilhados que faltam (pelo nome). 7) group_push_audit. Devolve as contagens ("n novo(s)").
import { exigeDono, agora } from '../../lib/grupo.mjs';
import { num } from '../../lib/eco.mjs';
const k = (s) => String(s ?? '').trim().toLowerCase();
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const g = exigeDono(ctx, a._group_id);
  const alvo = a._target_company_id;
  if (!store.rows('company_group_members').some((m) => m.group_id === g.id && m.company_id === alvo && m.status === 'active')) {
    throw new RpcError('Target company is not an active member of this group');
  }
  const flag = (v) => v === undefined || v === null ? true : !!v;
  const sobrescreve = !!a._overwrite_prices;
  const pMat = flag(a._push_materials), pCat = flag(a._push_categories), pTab = flag(a._push_price_tables), pCli = flag(a._push_customers), pFor = flag(a._push_suppliers);
  const iso = new Date(agora()).toISOString();
  const tabelasGrupo = store.rows('group_price_tables').filter((t) => t.group_id === g.id);
  const padrao = tabelasGrupo.find((t) => t.is_default === true) || [...tabelasGrupo].sort((x, y) => String(x.created_at).localeCompare(String(y.created_at)))[0] || null;
  const itensGrupo = (tid) => store.rows('group_price_table_items').filter((i) => i.group_price_table_id === tid);
  const gmPorId = new Map(store.rows('group_materials').filter((m) => m.group_id === g.id).map((m) => [m.id, m]));
  const n = { materials: 0, categories: 0, price_tables: 0, customers: 0, suppliers: 0 };
  const matsAlvo = () => store.rows('materials').filter((m) => m.company_id === alvo);
  const linka = (mid, gmid) => {
    if (!store.rows('material_group_links').some((l) => l.company_material_id === mid || (l.group_material_id === gmid && l.company_id === alvo))) {
      db.insert('material_group_links', { company_material_id: mid, group_material_id: gmid, company_id: alvo, created_at: iso });
    }
  };
  if (pMat) {
    for (const gm of gmPorId.values()) {
      const it = padrao ? itensGrupo(padrao.id).find((i) => i.group_material_id === gm.id) : null;
      const bc = num(it?.purchase_price), bv = num(it?.sale_price);
      let code = String(gm.code ?? '').trim() || null;
      if (code && matsAlvo().some((m) => m.code === code && !m.is_archived && k(m.name) !== k(gm.name))) code = null;
      if (!code) code = 'M-' + Math.random().toString(16).slice(2, 10);
      const ex = matsAlvo().find((m) => k(m.name) === k(gm.name));
      if (!ex) {
        const novo = db.insert('materials', { company_id: alvo, name: gm.name, code, ncm: gm.ncm ?? null, unit: gm.unit || 'KG', purchase_price: bc, sale_price: bv,
          current_stock: 0, is_archived: false, created_at: iso, updated_at: iso }, { companyId: alvo });
        linka(novo.id, gm.id);
        n.materials += 1;
      } else {
        let final = String(ex.code ?? '').trim() || code;
        if (matsAlvo().some((m) => m.code === final && !m.is_archived && m.id !== ex.id)) final = 'M-' + Math.random().toString(16).slice(2, 10);
        const mexe = ex.is_archived || sobrescreve || !num(ex.purchase_price) || !num(ex.sale_price) || !String(ex.code ?? '').trim() || !String(ex.ncm ?? '').trim();
        if (mexe) {
          ex.is_archived = false;
          ex.purchase_price = sobrescreve || !num(ex.purchase_price) ? bc : ex.purchase_price;
          ex.sale_price = sobrescreve || !num(ex.sale_price) ? bv : ex.sale_price;
          ex.code = final;
          ex.ncm = String(ex.ncm ?? '').trim() ? ex.ncm : gm.ncm ?? null;
          ex.updated_at = iso;
          n.materials += 1;
        }
        linka(ex.id, gm.id);
      }
    }
    store.table('materials').touch();
  }
  const upsertItem = (tabId, mat, pc, pv) => {
    const ex = store.rows('price_table_items').find((i) => i.price_table_id === tabId && i.material_id === mat.id);
    if (ex) Object.assign(ex, { purchase_price: pc, sale_price: pv, updated_at: iso });
    else db.insert('price_table_items', { price_table_id: tabId, material_id: mat.id, purchase_price: pc, sale_price: pv, is_override: false, created_at: iso, updated_at: iso });
  };
  if (padrao && (pTab || (pMat && sobrescreve))) {
    const principal = store.rows('price_tables').find((t) => t.company_id === alvo && t.is_default);
    if (principal) {
      for (const it of itensGrupo(padrao.id)) {
        const gm = gmPorId.get(it.group_material_id);
        for (const m of matsAlvo().filter((x) => gm && k(x.name) === k(gm.name))) upsertItem(principal.id, m, it.purchase_price, it.sale_price);
      }
    }
    if (pTab) {
      for (const it of itensGrupo(padrao.id)) {
        const gm = gmPorId.get(it.group_material_id);
        for (const m of matsAlvo().filter((x) => gm && k(x.name) === k(gm.name) && !x.is_archived)) { m.purchase_price = it.purchase_price; m.sale_price = it.sale_price; }
      }
    }
    store.table('price_table_items').touch();
    store.table('materials').touch();
  }
  if (pCat) {
    for (const c of store.rows('group_financial_categories').filter((x) => x.group_id === g.id)) {
      if (store.rows('financial_categories').some((f) => f.company_id === alvo && k(f.name) === k(c.name) && f.type === c.type)) continue;
      ctx.db.insert('financial_categories', { company_id: alvo, name: c.name, type: c.type, color: c.color, created_at: iso, updated_at: iso }, { companyId: alvo });
      n.categories += 1;
    }
  }
  if (pTab) {
    for (const t of tabelasGrupo.filter((x) => !padrao || x.id !== padrao.id)) {
      let tab = store.rows('price_tables').find((p) => p.company_id === alvo && k(p.name) === k(t.name));
      if (!tab) {
        tab = db.insert('price_tables', { company_id: alvo, name: t.name, is_default: false, created_at: iso, updated_at: iso }, { companyId: alvo });
        n.price_tables += 1;
      }
      for (const it of itensGrupo(t.id)) {
        const gm = gmPorId.get(it.group_material_id);
        for (const m of matsAlvo().filter((x) => gm && k(x.name) === k(gm.name))) upsertItem(tab.id, m, it.purchase_price, it.sale_price);
      }
    }
  }
  const CLI = ['name', 'cpf_cnpj', 'email', 'phone', 'contact_name', 'address', 'nome_fantasia', 'razao_social', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep', 'codigo_ibge', 'inscricao_estadual', 'indicador_ie'];
  const parceiros = (tipo, tab, extra, cont) => {
    for (const s of store.rows('group_shared_entities').filter((x) => x.group_id === g.id && x.entity_type === tipo)) {
      const e = store.rows(tab).find((x) => x.id === s.source_entity_id);
      if (!e || store.rows(tab).some((x) => x.company_id === alvo && k(x.name) === k(e.name))) continue;
      const linha = { company_id: alvo, created_at: iso, updated_at: iso };
      for (const c of [...CLI, ...extra]) linha[c] = e[c] ?? null;
      db.insert(tab, linha, { companyId: alvo });
      n[cont] += 1;
    }
  };
  if (pCli) parceiros('customer', 'customers', ['is_industry', 'is_intermediary'], 'customers');
  if (pFor) parceiros('supplier', 'suppliers', [], 'suppliers');
  db.insert('group_push_audit', { group_id: g.id, pushed_by: ctx.userId, target_company_id: alvo, pushed_at: iso, ...n, overwrite_prices: sobrescreve,
    included_materials: pMat, included_categories: pCat, included_price_tables: pTab, included_customers: pCli, included_suppliers: pFor });
  return n;
};
