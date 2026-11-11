// generate_ponto_slug (EmployeeFormDialog.tsx: funcionário com o ponto ligado, T19 cap02; bulk_enable_ponto, cap08), como a função
// da 1.59.154 (migration 20260926140000_ponto_slug_primeiro_nome.sql): grava e devolve employees.ponto_slug no formato
// {empresa}-{primeiro nome}-{CÓDIGO12} (base32 sem 0 O 1 I L). No banco falso o código sai do nome (sha1), não do acaso: a
// mesma pessoa ganha o mesmo link em todo ensaio (rec/t19/t19_sementes.py usa a mesma conta para os slugs da semente).
import crypto from 'node:crypto';

const ALFA = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
const rotulo = (s) => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-+|-+$)/g, '');
export const codigo = (chave) => [...crypto.createHash('sha1').update(chave).digest().subarray(0, 12)].map((b) => ALFA[b % ALFA.length]).join('');

export function slugPessoal(store, emp) {
  const empresa = store.rows('companies').find((c) => c.id === emp.company_id);
  let primeiro = rotulo(String(emp.name || '').trim().split(/\s+/)[0]).slice(0, 20).replace(/-+$/, '') || 'ponto';
  const label = [rotulo(empresa?.name).slice(0, 48 - primeiro.length - 1).replace(/-+$/, ''), primeiro].filter(Boolean).join('-');
  return `${label}-${codigo('t19-ponto:' + String(emp.name || '').trim())}`;
}

export default (a, { store, RpcError }) => {
  const emp = store.rows('employees').find((e) => e.id === a.p_employee_id);
  if (!emp) throw new RpcError(`Funcionário ${a.p_employee_id} não encontrado`);
  emp.ponto_slug = slugPessoal(store, emp);
  store.table('employees').touch();
  return emp.ponto_slug;
};
