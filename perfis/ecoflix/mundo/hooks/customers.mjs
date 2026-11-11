// Trigger de customers: o banco numera o código do cliente por empresa ao criar (o app não manda `code`; a lista mostra
// "<código> · <nome>"). Sem isto o cliente novo do T4 (a serralheria como cliente, cap05) saía sem número. Molde comum a suppliers.mjs.
export function codigoParceiro(store, tabela, row) {
  if (row.code !== undefined && row.code !== null && row.code !== '') return;
  const maior = Math.max(0, ...store.rows(tabela).filter((r) => r.company_id === row.company_id).map((r) => Number(r.code) || 0));
  row.code = String(maior + 1);
}

// Cadastro duplo (cliente + fornecedor ligados): o banco espelha no outro lado o que o aviso azul do "Editar" promete ("Mudanças em
// nome, CPF/CNPJ, contato, endereço e tabela de preços padrão refletem automaticamente no cadastro ... vinculado"): T4 cap06, a
// "Tabela Depósitos" do Depósito Irmãos Siqueira vale também no cliente. Cópia direta na linha do outro lado (sem disparar o gatilho dele).
const ESPELHO = ['name', 'cpf_cnpj', 'phone', 'phone_unavailable', 'email', 'contact_name', 'address', 'logradouro', 'numero', 'complemento',
  'bairro', 'cidade', 'uf', 'cep', 'codigo_ibge', 'default_price_table_id'];
export function espelhaParceiro(store, row, tabelaOutra, colunaLigacao) {
  const id = row[colunaLigacao];
  if (!id) return;
  const outro = store.rows(tabelaOutra).find((r) => r.id === id);
  if (!outro) return;
  let mudou = false;
  for (const k of ESPELHO) if (row[k] !== undefined && outro[k] !== row[k]) { outro[k] = row[k]; mudou = true; }
  if (mudou) { outro.updated_at = row.updated_at || outro.updated_at; store.table(tabelaOutra).touch(); }
}

export default {
  beforeInsert(row, { store }) {
    codigoParceiro(store, 'customers', row);
  },
  afterUpdate(row, { store }) {
    espelhaParceiro(store, row, 'suppliers', 'linked_supplier_id');
  },
};
