// Itens de uma tabela de preço gravados de uma vez, como a função SQL (20260918210000_save_price_table_items_atomico.sql): confere a tabela e
// os materiais da empresa, recusa material repetido ou preço vazio e troca TODOS os itens da tabela pelos do payload (delete + insert). O
// "Editar Preços em Massa" manda a lista inteira (T03 cap06: a Principal com o cobre reajustado). Devolve {saved: n}.
import { num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  if (!a.p_price_table_id) throw new RpcError('price_table_id obrigatorio', '22023');
  if (!Array.isArray(a.p_rows)) throw new RpcError('p_rows deve ser um array json', '22023');
  const cid = ctx.companyId;
  if (!store.rows('price_tables').some((t) => t.id === a.p_price_table_id && t.company_id === cid)) {
    throw new RpcError('Tabela de preco nao pertence a empresa do usuario', '42501');
  }
  const vistos = new Set();
  for (const r of a.p_rows) {
    if (!r.material_id) throw new RpcError('Linha sem material_id no payload', '22023');
    if (vistos.has(r.material_id)) throw new RpcError(`Material repetido no payload: ${r.material_id}`, '22023');
    vistos.add(r.material_id);
    if (!store.rows('materials').some((m) => m.id === r.material_id && m.company_id === cid)) {
      throw new RpcError(`Material nao pertence a empresa do usuario: ${r.material_id}`, '42501');
    }
    if (r.purchase_price === null || r.purchase_price === undefined || r.sale_price === null || r.sale_price === undefined) {
      throw new RpcError(`purchase_price e sale_price sao obrigatorios (material ${r.material_id})`, '22023');
    }
  }
  db.remove('price_table_items', { price_table_id: a.p_price_table_id });
  for (const r of a.p_rows) {
    db.insert('price_table_items', {
      price_table_id: a.p_price_table_id, material_id: r.material_id, purchase_price: num(r.purchase_price), sale_price: num(r.sale_price),
      is_override: !!r.is_override, variation_type: r.variation_type ?? null, variation_amount: r.variation_amount ?? null,
      variation_direction: r.variation_direction ?? null,
    }, { companyId: cid });
  }
  return { saved: a.p_rows.length };
};
