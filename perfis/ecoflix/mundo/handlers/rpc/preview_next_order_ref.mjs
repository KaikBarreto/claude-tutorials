// Número de exibição do próximo pedido pelo modelo da empresa (padrão "#{NUM}" -> "#1634").
import { proximoNumero } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const tpl = store.rows('companies').find((c) => c.id === cid)?.order_number_template || '#{NUM}';
  const n = proximoNumero(store, cid);
  return tpl.replace(/\{NUM:(\d)\}/g, (_, w) => String(n).padStart(Number(w), '0')).replace('{NUM}', String(n));
};
