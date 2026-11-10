// Padrao da coluna is_active em customer_origins (T1 · "Origens dos clientes"): o app so manda name, icon, color e
// company_id ao criar uma origem, e o banco real grava is_active = true. Sem este gancho a origem recem-criada
// aparecia como "Inativa" na lista da aba Usabilidade. Se o app mandar o valor (true/false), ele e respeitado.
export default {
  beforeInsert(row) {
    if (row.is_active === null || row.is_active === undefined) row.is_active = true;
  },
};
