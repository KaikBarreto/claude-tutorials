// Trigger de customers: o banco numera o código do cliente por empresa ao criar (o app não manda `code`; a lista mostra
// "<código> · <nome>"). Sem isto o cliente novo do T4 (a serralheria como cliente, cap05) saía sem número. Molde comum a suppliers.mjs.
export function codigoParceiro(store, tabela, row) {
  if (row.code !== undefined && row.code !== null && row.code !== '') return;
  const maior = Math.max(0, ...store.rows(tabela).filter((r) => r.company_id === row.company_id).map((r) => Number(r.code) || 0));
  row.code = String(maior + 1);
}

export default {
  beforeInsert(row, { store }) {
    codigoParceiro(store, 'customers', row);
  },
};
