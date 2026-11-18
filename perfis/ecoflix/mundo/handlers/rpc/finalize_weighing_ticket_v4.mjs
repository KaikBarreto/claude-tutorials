// Salvar o Ticket de Pesagem no app 1.59.163+ (T8): espelha finalize_weighing_ticket_v4 da migration
// 20261111193000_standalone_weighing_financial_charge.sql. Finaliza pela v3 (na avulsa o payment_intent não vai para a v3) e, em pesagem
// avulsa NOVA com tarifa, aplica a cobrança (apply_standalone_weighing_charge_v1) na mesma chamada. Devolve o resultado da v3 mais
// standalone_charge_status ('none' | 'charged') e standalone_charge.
import v3 from './finalize_weighing_ticket_v3.mjs';
import { cobrarPesagemAvulsa } from './apply_standalone_weighing_charge_v1.mjs';

export default (a, ctx) => {
  const cid = a.p_company_id || ctx.companyId;
  const kind = a.p_ticket_kind || 'standard';
  const r = v3({ ...a, p_ticket_kind: kind, p_payment_intent: kind === 'standalone' ? null : a.p_payment_intent ?? null }, ctx);
  let cobranca;
  if (kind === 'standalone' && Number(a.p_weighing_fee || 0) > 0 && !r.already_existed) {
    cobranca = cobrarPesagemAvulsa(ctx, a.p_ticket_id, cid, a.p_payment_intent);
  } else {
    const t = ctx.store.rows('weighing_tickets').find((x) => x.id === a.p_ticket_id && x.company_id === cid);
    const st = t?.standalone_charge_status || 'none';
    cobranca = { charge_status: st, already_existed: st === 'charged' };
  }
  return { ...r, standalone_charge_status: cobranca.charge_status || 'none', standalone_charge: cobranca };
};
