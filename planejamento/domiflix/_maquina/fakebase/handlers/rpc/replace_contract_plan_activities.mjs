// RPC replace_contract_plan_activities(p_contract_id, p_activities jsonb) → integer · T11 (1.38.19).
// Troca o plano de atividades do contrato (apaga as linhas atuais e grava as enviadas, na ordem recebida) e devolve a contagem.
// No PMOC novo (checklists de norma por máquina) o app nem chama; o comum com plano e o PMOC legado chamam.
import { RpcError } from '../../http/rest.mjs';

export default async function replaceContractPlanActivities({ p_contract_id, p_activities }, { db }) {
  const contrato = db.first('contracts', { id: p_contract_id });
  if (!contrato) throw new RpcError('Contrato não encontrado', 'P0002', 404);
  db.remove('contract_plan_activities', (a) => a.contract_id === p_contract_id);
  const lista = Array.isArray(p_activities) ? p_activities : [];
  lista.forEach((a, i) => {
    db.insert('contract_plan_activities', {
      contract_id: p_contract_id, company_id: contrato.company_id, catalog_activity_id: a.catalog_activity_id ?? null,
      contract_item_id: a.contract_item_id ?? null, section: a.section ?? null, component: a.component ?? null, description: a.description,
      guidance: a.guidance ?? null, freq_code: a.freq_code ?? null, freq_months: a.freq_months ?? null, is_measurement: a.is_measurement ?? false,
      unit: a.unit ?? null, expected_min: a.expected_min ?? null, expected_max: a.expected_max ?? null,
      applies_per_equipment: a.applies_per_equipment ?? true, is_active: a.is_active ?? true, sort_order: a.sort_order ?? i,
    }, { companyId: contrato.company_id });
  });
  return lista.length;
}
