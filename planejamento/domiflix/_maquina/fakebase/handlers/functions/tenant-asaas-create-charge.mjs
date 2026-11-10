// Edge function `tenant-asaas-create-charge` falsa (T19 · caps. 6 e 12). Espelha supabase/functions/tenant-asaas-create-charge (1.38.19):
//   POST { customer_id, value, due_date, billing_type, description, fine_*, interest_percent, discount_*, installment_count, fee_payer,
//          source_type, source_id, category, cost_center_id, post_to_finance }
//     -> { charge: { id, public_short_code, checkout_url, invoice_url, pix_copy_paste, boleto_url, value, due_date, status }, finance_warning? }
// Sem a Asaas: o pagamento e o boleto são FICTÍCIOS (códigos e endereços de exemplo; nada sai da máquina). O que o servidor real faz no banco
// e aqui também:
//  - grava `tenant_charges` (PENDING) com `public_short_code` curto (12 caracteres, base32 sem i, o, 0 e 1: `extractShortCode` do app recusa outro formato);
//  - "avulso"/orçamento/OS: com `post_to_finance` (padrão da conta: `auto_post_to_finance`) cria a conta a receber como a RPC
//    `create_tenant_charge_receivable` (entrada, não paga, competência de hoje, conta de destino e categoria da conta Asaas ou a da cobrança);
//  - `contract_installment`: NÃO cria conta a receber; liga a parcela que já existe (`financial_transactions.tenant_charge_id`);
//  - `receivable` ("Cobrar o saldo"): liga a conta a receber que já existe;
//  - dedupe pela origem (orçamento/parcela/OS/conta): a mesma cobrança viva volta em vez de criar outra.
import { FunctionError } from '../../http/functions.mjs';
import { uuid, dateBR, now } from '../../core/util.mjs';

// códigos fixos das três primeiras cobranças (o robô do T19 abre o link do capítulo 8 por eles); as seguintes saem aleatórias
const CODIGOS = ['hn7xq3rmk4vp', 'w4tn8kpzc6dj', 'm3zsb6yhq9ft'];
const ALFA = 'abcdefghjkmnpqrstuvwxyz23456789';
const MORTAS = ['CANCELLED', 'DELETED', 'REFUNDED', 'CHARGEBACK', 'REFUND_REQUESTED'];

function codigoNovo(db) {
  const usados = new Set(db.rows('tenant_charges').map((c) => c.public_short_code));
  const fixo = CODIGOS.find((c) => !usados.has(c));
  if (fixo) return fixo;
  let c;
  do c = Array.from({ length: 12 }, () => ALFA[Math.floor(Math.random() * ALFA.length)]).join('');
  while (usados.has(c));
  return c;
}

const r2 = (n) => Math.round(Number(n) * 100) / 100;

export default async function tenantAsaasCreateCharge(b, { db, userId, companyId }) {
  const conta = db.first('tenant_payment_accounts', (r) => String(r.company_id) === String(companyId));
  if (!conta || conta.status !== 'active') throw new FunctionError('Ative os recebimentos antes de gerar cobranças.', 400);
  const cliente = db.first('customers', { id: b.customer_id });
  if (!cliente) throw new FunctionError('Cliente não encontrado.', 404);
  if (!String(cliente.document || '').replace(/\D/g, '')) {
    throw new FunctionError(`${cliente.name} ainda não tem CPF ou CNPJ no cadastro. A Asaas exige esse dado para gerar a cobrança.`, 400);
  }
  const valor = r2(b.value);
  if (!(valor > 0)) throw new FunctionError('Informe um valor maior que zero.', 400);
  const origem = b.source_type || 'avulso';
  const origemId = b.source_id || null;

  if (origemId && origem !== 'avulso') {
    const viva = db.rows('tenant_charges').find((c) => c.source_type === origem && String(c.source_id) === String(origemId) && !MORTAS.includes(String(c.status).toUpperCase()));
    if (viva) return { charge: saida(viva) };
  }

  const codigo = codigoNovo(db);
  const id = uuid();
  const tipo = b.billing_type || 'UNDEFINED';
  const asaasId = 'pay_' + id.replace(/-/g, '').slice(0, 16);
  const cobranca = db.insert('tenant_charges', {
    id, company_id: companyId, customer_id: cliente.id, value: valor, description: b.description || '', billing_type: tipo, status: 'PENDING',
    due_date: b.due_date, asaas_payment_id: asaasId, public_short_code: codigo, invoice_url: `https://pagamentos.glacialcold.example/fatura/${codigo}`,
    boleto_url: tipo === 'PIX' ? null : `https://pagamentos.glacialcold.example/boleto/${codigo}`,
    pix_copy_paste: tipo === 'BOLETO' || tipo === 'CREDIT_CARD' ? null : `00020126360014br.gov.bcb.pix0114exemplo${codigo}5204000053039865802BR5920GLACIAL COLD BRASIL6008NITEROI6304EX01`,
    post_to_finance: b.post_to_finance ?? conta.auto_post_to_finance, source_type: origem, source_id: origemId, created_by: userId,
  });

  if (origem === 'contract_installment' && origemId) {
    db.update('financial_transactions', (t) => String(t.id) === String(origemId) && !t.parent_transaction_id, { tenant_charge_id: id });
  } else if (origem === 'receivable' && origemId) {
    db.update('financial_transactions', (t) => String(t.id) === String(origemId), { tenant_charge_id: id });
  } else if (cobranca.post_to_finance) {
    db.insert('financial_transactions', {
      company_id: companyId, transaction_type: 'entrada', amount: valor, description: b.description || '', customer_id: cliente.id, due_date: b.due_date,
      tenant_charge_id: id, service_order_id: origem === 'service_order' ? origemId : null, is_paid: false, transaction_date: dateBR(0, now()),
      account_id: conta.default_finance_account_id ?? null, category: (b.category && String(b.category).trim()) || conta.default_income_category || null,
      cost_center_id: b.cost_center_id ?? null, created_by: null,
    });
  }
  return { charge: saida(cobranca) };
}

function saida(c) {
  return {
    id: c.id, public_short_code: c.public_short_code, checkout_url: `/pagar/${c.public_short_code}`, invoice_url: c.invoice_url, pix_copy_paste: c.pix_copy_paste,
    boleto_url: c.boleto_url, value: c.value, due_date: c.due_date, status: c.status,
  };
}
