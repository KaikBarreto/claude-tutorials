// Extratos OFX importados da conta (conciliação): nenhum no mundo base (o T14 importa o arquivo na tela).
export default (a, { store }) => store.rows('bank_statement_imports').filter((i) => i.bank_account_id === a.p_bank_account_id);
