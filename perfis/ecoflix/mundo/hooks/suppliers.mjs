// Trigger de suppliers: o banco numera o código do fornecedor por empresa ao criar (o app não manda `code`; a lista mostra
// "<código> · <nome>"). Sem isto o cadastro novo do T4 (Rogério, cap02; serralheria, cap04) saía sem número na lista. Depois de
// editar um fornecedor ligado a um cliente, espelha no cliente (customers.mjs, espelhaParceiro).
import { codigoParceiro, espelhaParceiro } from './customers.mjs';

export default {
  beforeInsert(row, { store }) {
    codigoParceiro(store, 'suppliers', row);
  },
  afterUpdate(row, { store }) {
    espelhaParceiro(store, row, 'customers', 'linked_customer_id');
  },
};
