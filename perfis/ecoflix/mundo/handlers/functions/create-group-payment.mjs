// Edge create-group-payment (supabase/functions/create-group-payment/index.ts), o "Pagar tudo de uma vez" do Gerencial, SEM Asaas: a cobrança
// única do total do grupo na matriz. PIX recorrente (o padrão do checkout) = o ramo "Pix Automático" do edge: devolve a autorização com o QR
// e o Pix Copia e Cola FICTÍCIOS (chave inventada, nada sai daqui) e grava a cobrança em subscription_payments (status PENDING) para o
// check-asaas-payment responder. Depois, a centralização do edge: billing_managed_by_group_id em todas as unidades e o ponteiro de
// assinatura das filiais limpo. Ciclos misturados = GROUP_MIXED_CYCLE. Cartão e boleto não fazem parte da aula: recusa sem cobrança.
import { exigeDono, empresasDoGrupo } from '../../lib/grupo.mjs';
import { esperado } from '../rpc/group_expected_payment.mjs';
import { agoraMs } from '../../lib/eco.mjs';

function crc16(s) {
  let c = 0xffff;
  for (const ch of Buffer.from(s, 'utf8')) {
    c ^= ch << 8;
    for (let i = 0; i < 8; i++) c = c & 0x8000 ? ((c << 1) ^ 0x1021) & 0xffff : (c << 1) & 0xffff;
  }
  return c.toString(16).toUpperCase().padStart(4, '0');
}
const f = (id, v) => id + String(v.length).padStart(2, '0') + v;
/** BR Code estático de demonstração (EMV): chave aleatória inventada, valor do grupo; o app desenha o QR a partir dele */
function brcode(valor, txid) {
  const conta = f('00', 'br.gov.bcb.pix') + f('01', '7d3f1c2a-9e45-4b8d-a6f0-3c2b1e8d5a90');
  const corpo = f('00', '01') + f('26', conta) + f('52', '0000') + f('53', '986') + f('54', valor.toFixed(2)) + f('58', 'BR') + f('59', 'ASSINATURA ECOSISTEMA')
    + f('60', 'SAO PAULO') + f('62', f('05', txid)) + '6304';
  return corpo + crc16(corpo);
}
// PNG 1x1 branco: o app gera o QR "com a marca" a partir do Copia e Cola; este é só o reserva do encodedImage
const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII=';

export default (body, ctx) => {
  const { store, db, FunctionError } = ctx;
  const gid = body?.group_id;
  const g = store.rows('company_groups').find((x) => x.id === gid);
  if (!g) throw new FunctionError(404, 'Grupo não encontrado');
  try { exigeDono({ ...ctx, RpcError: class extends Error {} }, gid); } catch { throw new FunctionError(403, 'Apenas a matriz do grupo pode pagar a fatura única'); }
  const exp = esperado(store, gid);
  if (exp.mixed_cycle) return { success: false, error: 'GROUP_MIXED_CYCLE', message: 'As unidades do grupo têm ciclos de cobrança diferentes.' };
  if (body?.billing_type !== 'PIX') return { success: false, error: 'Forma de pagamento indisponível no ambiente de demonstração' };
  const total = exp.total;
  const agora = agoraMs();
  const n = store.rows('subscription_payments').filter((p) => String(p.asaas_payment_id || '').startsWith('t22-auth-')).length + 1;
  const authId = `t22-auth-${String(n).padStart(4, '0')}-ecoflix`;
  const venc = new Date(agora).toISOString().slice(0, 10);
  const copia = brcode(total, `GRUPORECICLAVALE${n}`);
  const expira = new Date(agora + 24 * 3600000).toISOString();
  db.insert('subscription_payments', { company_id: g.owner_company_id, asaas_payment_id: authId, amount: total, billing_type: 'PIX', payment_method: 'pix',
    status: 'PENDING', due_date: venc, pix_copy_paste: copia, pix_qr_code: PNG, pix_expiration_date: expira, created_at: new Date(agora).toISOString(),
    updated_at: new Date(agora).toISOString() }, { companyId: g.owner_company_id });
  const ids = empresasDoGrupo(store, gid);
  for (const c of store.rows('companies')) {
    if (!ids.includes(c.id)) continue;
    c.billing_managed_by_group_id = gid;
    if (c.id !== g.owner_company_id) c.asaas_subscription_id = null;
  }
  store.table('companies').touch();
  return {
    success: true, group_id: gid, matriz_company_id: g.owner_company_id, total, external_reference: `group:${gid}`, mode: 'authorization', billing_type: 'PIX',
    is_recurring: body?.recurring !== false, pix_automatic: true, authorization_id: authId, payment_id: authId, status: 'PENDING', pix_qr_code: PNG,
    pix_copy_paste: copia, pix_expiration_date: expira, due_date: venc,
    centralization: { subscriptions_cancelled: [], companies_marked: ids, errors: [] },
  };
};
