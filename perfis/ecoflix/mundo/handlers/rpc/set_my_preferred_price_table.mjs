// "Fixar para meus pedidos e tickets" (20261112162947): grava profiles.preferred_price_table_id do usuário logado (nulo = remover). Devolve o id ou null.
// T03 (cap11).
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const id = a.p_price_table_id ?? null;
  if (id && !store.rows('price_tables').some((t) => t.id === id && t.company_id === ctx.companyId)) throw new RpcError('Tabela de preco nao pertence a empresa do usuario', '42501');
  db.update('profiles', (r) => r.id === ctx.userId, { preferred_price_table_id: id });
  return id;
};
