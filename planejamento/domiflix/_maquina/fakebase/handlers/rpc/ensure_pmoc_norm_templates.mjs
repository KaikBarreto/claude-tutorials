// RPC ensure_pmoc_norm_templates(p_company_id) · 20260628160000_pmoc_norm_form_templates.sql (T11, 1.38.19).
// Materializa, por empresa, os 4 checklists de NORMA (família expansao_direta | sistemas_centrais x camada essencial | complementar) a partir do
// catálogo global `pmoc_activity_catalog`; idempotente (casa por (empresa, família, camada) e, nas perguntas, por pmoc_catalog_activity_id).
// Família pela seção (expansao_direta = condicionadores, medicoes, testes); camada pelo essential_tier (essencial = NOT NULL).
import { RpcError } from '../../http/rest.mjs';

const FAMILIAS = [['expansao_direta', 'Expansão Direta'], ['sistemas_centrais', 'Sistemas Centrais']];
const CAMADAS = [['essencial', 'Essencial'], ['complementar', 'Norma completa']];
const SECOES_AC = ['condicionadores', 'medicoes', 'testes'];
const FREQ = { M: 1, T: 3, S: 6, A: 12 };

export default async function ensurePmocNormTemplates({ p_company_id }, { db }) {
  if (!p_company_id) throw new RpcError('p_company_id obrigatório', '22004', 400);
  const catalogo = db.rows('pmoc_activity_catalog').filter((c) => c.is_active !== false);
  for (const [fam, famRotulo] of FAMILIAS) {
    for (const [camada, camadaRotulo] of CAMADAS) {
      const nome = `PMOC — ${famRotulo} (${camadaRotulo})`;
      const descricao = `Checklist da norma PMOC (Lei 13.589/2018) — ${famRotulo}, camada ${camadaRotulo.toLowerCase()}. Gerado automaticamente a partir do catálogo da norma; editável.`;
      let tpl = db.rows('form_templates').find((t) => t.company_id === p_company_id && t.pmoc_family === fam && t.pmoc_tier === camada);
      if (tpl) {
        db.update('form_templates', (t) => t === tpl, { name: nome, description: descricao, is_active: true, is_pmoc_default: true });
      } else {
        tpl = db.insert('form_templates', { company_id: p_company_id, name: nome, description: descricao, is_active: true, is_pmoc_default: true, pmoc_family: fam, pmoc_tier: camada }, { companyId: p_company_id });
      }
      const ja = new Set(db.rows('form_questions').filter((q) => q.template_id === tpl.id && q.pmoc_catalog_activity_id).map((q) => q.pmoc_catalog_activity_id));
      for (const c of catalogo) {
        const daFamilia = fam === 'expansao_direta' ? SECOES_AC.includes(c.section) : !SECOES_AC.includes(c.section);
        const daCamada = camada === 'essencial' ? c.essential_tier != null : c.essential_tier == null;
        if (!daFamilia || !daCamada || ja.has(c.id)) continue;
        const temFreq = c.default_freq_code in FREQ;
        db.insert('form_questions', {
          template_id: tpl.id, question: c.description, question_type: c.is_measurement ? 'number' : 'conformidade', description: c.guidance,
          position: c.sort_order, is_required: false, freq_kind: temFreq ? 'time' : null, freq_months: temFreq ? FREQ[c.default_freq_code] : null,
          freq_days: null, freq_visits: null, start_kind: temFreq ? 'contract_start' : null, start_visit: null,
          unit: c.is_measurement ? c.unit : null, expected_min: c.is_measurement ? c.expected_min : null, expected_max: c.is_measurement ? c.expected_max : null,
          pmoc_catalog_activity_id: c.id, pmoc_section: c.section, pmoc_group: c.activity_group, pmoc_essential_tier: c.essential_tier,
        }, { companyId: p_company_id });
      }
    }
  }
  return null;
}
