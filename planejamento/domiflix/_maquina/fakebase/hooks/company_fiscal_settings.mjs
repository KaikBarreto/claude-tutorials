// T14 · gatilho do banco real em `company_fiscal_settings` (1.38.24, supabase/migrations/20261105013000_nfse_ambiente_canonico.sql,
// trg_invalidate_nfse_coverage_on_city_change): a cobertura pertence ao par (município, ambiente); trocar qualquer um dos
// dois numa gravação da tela derruba `pode_emitir` na mesma hora (falha fechado). Gravações iguais (salvar de novo) não mexem.
// As edges falsas (nfse-check-coverage) gravam direto pelo `db` e não passam por aqui, como o service_role no banco real.
export default {
  beforeUpdate(row, patch) {
    const muda = (k) => k in patch && String(patch[k] ?? '') !== String(row[k] ?? '');
    if (muda('municipio_ibge') || muda('fiscal_ambiente')) patch.pode_emitir = false;
  },
};
