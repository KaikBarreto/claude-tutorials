// get_company_dre_configuration(p_company_id): configuração das "Outras visões" do DRE (Organizar categorias > Outras visões, T15 cap07).
// O mundo não tem visão personalizada: modo "legacy" (DRE padrão do sistema, "Em uso"), sem perfis. As tabelas dre_layout_* ficam vazias.
export default (a, ctx) => ({
  settings: { company_id: a.p_company_id || ctx.companyId, mode: 'legacy', default_profile_id: null },
  profiles: [],
});
