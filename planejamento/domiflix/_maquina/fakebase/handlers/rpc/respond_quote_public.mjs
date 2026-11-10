// RPC respond_quote_public(_token, _status) · 20260919230000_aprovacao_publica_usa_categoria_renomeada.sql:161-337
// O cliente aprova/rejeita pelo link. Só sai de 'enviado' (senão devolve ok:false, 'not_pending'). Muda SÓ o status; a conta a receber só
// nasce se company_settings.quote_public_approval_creates_receivable estiver ligada (padrão: desligada). Nada de OS, estoque ou custo.
import { nowIso } from '../../core/util.mjs';

const r2 = (n) => Math.round((n + Number.EPSILON) * 100) / 100;

function somaMeses(iso, k) {
  const [y, m, d] = iso.split('-').map(Number);
  const alvo = new Date(Date.UTC(y, m - 1 + k, 1));
  const ultimo = new Date(Date.UTC(alvo.getUTCFullYear(), alvo.getUTCMonth() + 1, 0)).getUTCDate();
  alvo.setUTCDate(Math.min(d, ultimo));
  return alvo.toISOString().slice(0, 10);
}

export default async function respondQuotePublic({ _token, _status }, { db }) {
  if (!['aprovado', 'rejeitado'].includes(_status)) return { ok: false, error: 'invalid_status' };
  const q = db.first('quotes', { token: _token });
  if (!q) return { ok: false, error: 'not_found' };
  if (q.status !== 'enviado') return { ok: false, status: q.status, error: 'not_pending', receivable_created: false };
  db.update('quotes', { id: q.id }, { status: _status });
  if (_status !== 'aprovado') return { ok: true, status: _status, receivable_created: false };
  const cfg = db.first('company_settings', { company_id: q.company_id });
  const bruto = Number(q.total_value || 0);
  if (q.financial_generated_at || !cfg?.quote_public_approval_creates_receivable || bruto <= 0) return { ok: true, status: _status, receivable_created: false };
  const n = Math.max(1, Math.min(60, q.receivable_installments || 1));
  const base = q.receivable_first_due_date || nowIso().slice(0, 10);
  const grupo = crypto.randomUUID();
  const parte = r2(bruto / n);
  let primeiro = null;
  for (let i = 1; i <= n; i++) {
    const valor = i === n ? r2(bruto - parte * (n - 1)) : parte;
    const venc = somaMeses(base, i - 1);
    const t = db.insert('financial_transactions', {
      company_id: q.company_id, transaction_type: 'entrada', category: 'Vendas de Serviços',
      description: `Orçamento #${q.quote_number}${n > 1 ? ` (${i}/${n})` : ''}`, amount: valor,
      transaction_date: venc, due_date: venc, paid_date: null, is_paid: false, customer_id: q.customer_id, account_id: null,
      installment_group_id: n > 1 ? grupo : null, installment_number: n > 1 ? i : null, installment_total: n > 1 ? n : null,
    });
    if (i === 1) primeiro = t.id;
  }
  db.update('quotes', { id: q.id }, { financial_generated_at: nowIso(), financial_transaction_id: primeiro });
  return { ok: true, status: _status, receivable_created: true, installments: n };
}
