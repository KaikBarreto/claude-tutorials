// "Duplicar tabela" (20261111192000_duplicate_price_table_atomic.sql): cria "<nome> (cópia)" INDEPENDENTE (is_linked falso, sem variação), com os
// preços que valiam na origem na hora (tabela vinculada: o preço já calculado, salvo o item com sobrescrita). Devolve o id da cópia. T03 (cap11).
import { r3, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const cid = ctx.companyId;
  const src = store.rows('price_tables').find((t) => t.id === a.p_source_table_id && t.company_id === cid);
  if (!src) throw new RpcError('Tabela de preco nao pertence a empresa do usuario', '42501');
  const nomes = new Set(store.rows('price_tables').filter((t) => t.company_id === cid).map((t) => t.name));
  let n = 1, nome;
  for (;;) { nome = `${src.name} (cópia${n === 1 ? ')' : ' ' + n + ')'}`; if (!nomes.has(nome)) break; n += 1; }
  const nova = db.insert('price_tables', { company_id: cid, name: nome, is_default: false, is_linked: false, linked_to_table_id: null,
    variation_type: 'percentage', variation_amount: 0, variation_direction: 'positive' }, { companyId: cid });
  const itens = store.rows('price_table_items').filter((i) => i.price_table_id === src.id);
  const fator = (v, preco) => {
    if (!(src.is_linked && !src.is_default)) return preco;
    const k = num(src.variation_amount);
    const s = src.variation_direction === 'positive' ? 1 : -1;
    return r3(src.variation_type === 'percentage' ? preco * (1 + s * k / 100) : preco + s * k);
  };
  for (const m of store.rows('materials').filter((x) => x.company_id === cid && !x.is_archived)) {
    const it = itens.find((i) => i.material_id === m.id);
    const ov = it && it.is_override;
    db.insert('price_table_items', {
      price_table_id: nova.id, material_id: m.id,
      purchase_price: ov ? num(it.purchase_price) : fator('c', num(m.purchase_price)),
      sale_price: ov ? num(it.sale_price) : fator('v', num(m.sale_price)),
      is_override: false, variation_type: null, variation_amount: null, variation_direction: null,
    }, { companyId: cid });
  }
  return nova.id;
};
