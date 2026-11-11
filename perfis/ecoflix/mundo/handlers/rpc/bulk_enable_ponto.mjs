// bulk_enable_ponto (Configurações de Ponto > "Ativar ponto eletrônico" > "Ativar ponto (n)", T19 cap08), como a função da 1.59.154
// (migration 20260903000000_bulk_enable_ponto_and_slug_guard.sql): liga o ponto de cada funcionário e gera o link pessoal de quem não
// tem. Devolve uma linha por funcionário: { employee_id, ok, error }.
import { slugPessoal } from './generate_ponto_slug.mjs';

export default (a, { store, companyId }) => {
  const out = [];
  for (const id of a.p_employee_ids || []) {
    const emp = store.rows('employees').find((e) => e.id === id && (!companyId || e.company_id === companyId));
    if (!emp) { out.push({ employee_id: id, ok: false, error: 'Funcionário não encontrado ou não pertence à sua empresa.' }); continue; }
    emp.ponto_enabled = true;
    if (!emp.ponto_slug || !String(emp.ponto_slug).trim()) emp.ponto_slug = slugPessoal(store, emp);
    out.push({ employee_id: id, ok: true, error: null });
  }
  store.table('employees').touch();
  return out;
};
