// create_recurring_bill_template (app 1.59.154: supabase/migrations/20261027133000_recurring_bill_template_idempotency.sql) + o gerador
// _generate_bills_for_template (20260903130100; regra de 20260626130000): grava o molde e as contas. Com "Repetir até" (end_date) gera
// TODAS as contas até a data de parar; sem data, as da janela de hoje + 3 meses. next_due_date fica na primeira data depois da última
// gerada (o generate_due_recurring_bills do mundo continua dali). Mês a mês como o Postgres (date + interval: dia 31 vira o último do mês).
// Idempotente por client_request_id (o modal manda a mesma chave a cada tentativa). Devolve o molde. T13 cap07.
import { hojeBR, num } from '../../lib/eco.mjs';

const ultimoDia = (y, m) => new Date(Date.UTC(y, m, 0)).getUTCDate();   // m 1..12
function soma(d, freq, n) {
  const [y, m, dd] = d.split('-').map(Number);
  if (freq === 'weekly') return new Date(Date.UTC(y, m - 1, dd + 7 * n)).toISOString().slice(0, 10);
  const meses = freq === 'yearly' ? 12 * n : n;
  const t = (m - 1) + meses;
  const ny = y + Math.floor(t / 12), nm = (t % 12) + 1;
  return `${ny}-${String(nm).padStart(2, '0')}-${String(Math.min(dd, ultimoDia(ny, nm))).padStart(2, '0')}`;
}

export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const cid = ctx.companyId;
  if (!['payable', 'receivable'].includes(a.p_direction)) throw new RpcError('Direção inválida.');
  if (!a.p_description || !String(a.p_description).trim()) throw new RpcError('Informe a descrição.');
  if (!(num(a.p_amount) > 0)) throw new RpcError('O valor deve ser maior que zero.');
  if (!['weekly', 'monthly', 'yearly'].includes(a.p_frequency)) throw new RpcError(`Frequência inválida: ${a.p_frequency}`);
  const intervalo = num(a.p_interval);
  if (intervalo < 1) throw new RpcError('O intervalo deve ser >= 1.');
  if (!a.p_start_date) throw new RpcError('Informe a data do primeiro vencimento.');
  if (a.p_client_request_id) {
    const ja = store.rows('recurring_bill_templates').find((t) => t.company_id === cid && t.client_request_id === a.p_client_request_id);
    if (ja) return ja;
  }
  const t = db.insert('recurring_bill_templates', {
    company_id: cid, direction: a.p_direction, description: a.p_description, category_id: a.p_category_id || null, amount: num(a.p_amount),
    partner_type: a.p_partner_type || null, partner_id: a.p_partner_id || null, notes: a.p_notes || null, frequency: a.p_frequency,
    interval: intervalo, start_date: a.p_start_date, end_date: a.p_end_date || null, next_due_date: a.p_start_date, is_active: true,
    created_by: ctx.userId || null, expected_payment_method: a.p_expected_payment_method || null,
    expected_bank_account_id: a.p_expected_bank_account_id || null, client_request_id: a.p_client_request_id || null,
  }, { companyId: cid });
  const janela = soma(hojeBR(), 'monthly', 3);
  const fim = t.end_date ? (t.end_date < soma(hojeBR(), 'monthly', 60) ? t.end_date : soma(hojeBR(), 'monthly', 60)) : janela;
  let prox = t.next_due_date;
  while (prox <= fim) {
    const existe = store.rows('financial_bills').some((b) => b.recurring_template_id === t.id && b.due_date === prox);
    if (!existe) {
      db.insert('financial_bills', {
        company_id: cid, direction: t.direction, description: t.description, category_id: t.category_id, amount: t.amount, paid_amount: 0,
        currency: 'BRL', due_date: prox, status: 'pending', partner_type: t.partner_type, partner_id: t.partner_id, notes: t.notes,
        recurring_template_id: t.id, created_by: t.created_by, expected_payment_method: t.expected_payment_method,
        expected_bank_account_id: t.expected_bank_account_id,
      }, { companyId: cid });
    }
    prox = soma(prox, t.frequency, t.interval);
  }
  db.update('recurring_bill_templates', { id: t.id }, { next_due_date: prox });
  return t;
};
