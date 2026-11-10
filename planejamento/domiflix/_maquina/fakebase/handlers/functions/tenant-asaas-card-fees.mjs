// Edge function `tenant-asaas-card-fees` falsa (T1 · subaba "Cobranças (Asaas)"; o T19 reaproveita).
// Mesmo contrato da real (app/supabase/functions/tenant-asaas-card-fees + hooks/useTenantCardFees.ts):
//   POST { refresh? } -> { fees, card, source, feePayerDefault, syncedAt, pix, bankSlip, anticipation, settlementDays, extrasSource }
// A real le a tabela de taxas da conta Asaas do tenant (myAccount/fees). Aqui devolve a tabela PUBLICADA da Asaas
// (os mesmos numeros que o proprio codigo do app documenta como base factual, _shared/asaas-card-fees.ts) como se
// tivesse vindo da conta: source 'asaas', sem tela de "Taxas de referencia". Sao taxas da Asaas, nao preco de plano da Dominex.
// Regra da real: sem conta Asaas ativa devolve a tabela de referencia (fallback, extras nulos): idem aqui.
import { nowIso } from '../../core/util.mjs';

const CARD = { operationValue: 0.49, oneInstallment: 2.99, upToSix: 3.49, upToTwelve: 3.99, upToTwentyOne: 4.29 };
const FALLBACK_CARD = { operationValue: 0.49, oneInstallment: 2.99, upToSix: 2.99, upToTwelve: 2.99, upToTwentyOne: 4.29 };

export default async function tenantAsaasCardFees(_body, { db }) {
  const conta = db.find('tenant_payment_accounts', { status: 'active' })[0] || null;
  const feePayerDefault = conta?.card_fee_payer === 'customer' ? 'customer' : 'company';

  if (!conta) {
    return {
      fees: { ...FALLBACK_CARD },
      card: { ...FALLBACK_CARD },
      source: 'fallback',
      feePayerDefault,
      syncedAt: null,
      pix: null,
      bankSlip: null,
      anticipation: null,
      settlementDays: { pix: null, bankSlip: null, card: null },
      extrasSource: 'fallback',
    };
  }

  return {
    fees: { ...CARD },
    card: { ...CARD },
    source: 'asaas',
    feePayerDefault,
    syncedAt: nowIso(),
    // T19: a conta ativada ao vivo (`tenant-asaas-provision`) grava `card_fee_override.pixFreeCount: 0` (sem franquia de Pix); sem o campo, 100 como no T1
    pix: { fixed: 1.99, percent: 0, freeCount: conta.card_fee_override?.pixFreeCount ?? 100, freeUsed: 0, minFee: null, maxFee: null },
    bankSlip: { fixed: 1.99 },
    anticipation: {
      monthlyPercent: 5.79,
      bankSlipMonthlyPercent: 5.79,
      pixMonthlyPercent: 5.79,
      cardDetachedMonthlyPercent: 1.15,
      cardInstallmentMonthlyPercent: 1.6,
    },
    settlementDays: { pix: null, bankSlip: 1, card: 32 },
    extrasSource: 'asaas',
  };
}
