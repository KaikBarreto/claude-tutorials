// Margem automática da tabela (20261119190000_price_table_auto_margin.sql): grava a chave, o alcance e a margem nas colunas `auto_margin_*`
// de price_tables e troca TODAS as linhas de price_table_material_margins pelas do payload (p_margins nulo = só a chave). Tabela vinculada recusa.
// T03 (cap07 a cap09). Devolve null (a função SQL devolve void).
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const cid = ctx.companyId;
  const t = store.rows('price_tables').find((x) => x.id === a.p_price_table_id && x.company_id === cid);
  if (!a.p_price_table_id) throw new RpcError('Tabela de preços não informada.', '22023');
  if (!t) throw new RpcError('Tabela de preços não encontrada.', 'P0002');
  if (t.is_linked) throw new RpcError('Tabela vinculada não tem margem automática: ela acompanha os preços da tabela principal.', '22023');
  if (!['table', 'material'].includes(a.p_scope)) throw new RpcError(`Alcance da margem inválido: ${a.p_scope}.`, '22023');
  if (a.p_type != null && !['percentage', 'value'].includes(a.p_type)) throw new RpcError(`Tipo da margem inválido: ${a.p_type}.`, '22023');
  db.update('price_tables', (r) => r.id === t.id, {
    auto_margin_enabled: !!a.p_enabled, auto_margin_scope: a.p_scope, auto_margin_type: a.p_type ?? null,
    auto_margin_amount: a.p_amount ?? null,
  });
  if (a.p_margins == null) return null;
  if (!Array.isArray(a.p_margins)) throw new RpcError('Margens por material devem vir numa lista.', '22023');
  const vistos = new Set();
  for (const m of a.p_margins) {
    if (!m.material_id) throw new RpcError('Margem sem material informado.', '22023');
    if (vistos.has(m.material_id)) throw new RpcError('O mesmo material veio repetido na lista de margens.', '22023');
    vistos.add(m.material_id);
    if (!['percentage', 'value', 'none'].includes(m.margin_type)) throw new RpcError('Tipo de margem por material inválido.', '22023');
    if (m.margin_type !== 'none' && m.margin_amount == null) throw new RpcError('Margem por material sem valor informado.', '22023');
  }
  db.remove('price_table_material_margins', { price_table_id: t.id });
  for (const m of a.p_margins) {
    db.insert('price_table_material_margins', {
      price_table_id: t.id, material_id: m.material_id, margin_type: m.margin_type,
      margin_amount: m.margin_type === 'none' ? null : Number(m.margin_amount),
    }, { companyId: cid });
  }
  return null;
};
