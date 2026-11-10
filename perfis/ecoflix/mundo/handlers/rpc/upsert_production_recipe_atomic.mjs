// Ficha técnica numa transação só (T11): cabeçalho (UPDATE com trava por empresa ou INSERT) e as linhas refeitas (insumos com a
// perda padrão, coprodutos com qty_per_output 0). Como a função SQL da 1.59.154 (20260911150100); devolve o id da ficha.
import { agoraMs } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, db, RpcError, userId } = ctx;
  const cid = a.p_company_id;
  if (!cid) throw new RpcError('p_company_id é obrigatório');
  const h = a.p_header || {};
  const saida = h.output_material_id;
  if (!saida) throw new RpcError('header.output_material_id é obrigatório');
  const agora = new Date(agoraMs()).toISOString();
  const vazio = (v) => (v === undefined || v === null || String(v) === '' ? null : v);
  const cab = {
    output_material_id: saida,
    name: vazio(h.name),
    production_unit: vazio(h.production_unit) || 'peça',
    output_qty_per_batch: vazio(h.output_qty_per_batch) != null ? Number(h.output_qty_per_batch) : 1,
    pieces_per_commercial_unit: vazio(h.pieces_per_commercial_unit) != null ? Number(h.pieces_per_commercial_unit) : null,
    is_active: true,
    updated_at: agora,
  };
  let id = a.p_recipe_id || null;
  if (id) {
    const r = store.rows('production_recipes').find((x) => x.id === id && x.company_id === cid);
    if (!r) throw new RpcError(`Ficha ${id} não encontrada para esta empresa`);
    Object.assign(r, cab);
    store.table('production_recipes').touch();
  } else {
    id = db.insert('production_recipes', { company_id: cid, ...cab, created_by: userId, created_at: agora }, { companyId: cid }).id;
  }
  db.remove('production_recipe_inputs', (x) => x.recipe_id === id && x.company_id === cid);
  db.remove('production_recipe_outputs', (x) => x.recipe_id === id && x.company_id === cid);
  const nome = (mid) => store.rows('materials').find((m) => m.id === mid && m.company_id === cid)?.name || null;
  for (const i of Array.isArray(a.p_inputs) ? a.p_inputs : []) {
    if (!i?.material_id) continue;
    const perda = vazio(i.loss_pct) != null ? Number(i.loss_pct) : null;
    const sobra = vazio(i.scrap_material_id);
    const insumo = nome(i.material_id) || i.material_id;
    if (perda != null && (perda < 0 || perda >= 100)) throw new RpcError(`Perda padrão inválida no insumo "${insumo}": informe um valor de 0% a 99,999% (recebido ${perda}%).`);
    if (sobra) {
      const destino = nome(sobra);
      if (!destino) throw new RpcError(`No insumo "${insumo}": o material de destino da perda não existe nesta empresa (scrap_material_id=${sobra}).`);
      if (sobra === saida) throw new RpcError(`No insumo "${insumo}": a perda não pode virar "${destino}", que é o próprio produto da ficha. Escolha outro material ou deixe como perda pura.`);
      if (perda == null) throw new RpcError(`No insumo "${insumo}": você escolheu "${destino}" como destino da perda mas não informou a porcentagem. Preencha a % de perda ou remova o material de destino.`);
    }
    db.insert('production_recipe_inputs', {
      recipe_id: id, company_id: cid, material_id: i.material_id, qty_per_output: Number(i.qty_per_output) || 0, loss_pct: perda, scrap_material_id: sobra, created_at: agora,
    }, { companyId: cid });
  }
  for (const o of Array.isArray(a.p_outputs) ? a.p_outputs : []) {
    if (!o?.material_id) continue;
    db.insert('production_recipe_outputs', {
      recipe_id: id, company_id: cid, material_id: o.material_id, qty_per_output: Number(o.qty_per_output) || 0, created_at: agora,
    }, { companyId: cid });
  }
  return id;
};
