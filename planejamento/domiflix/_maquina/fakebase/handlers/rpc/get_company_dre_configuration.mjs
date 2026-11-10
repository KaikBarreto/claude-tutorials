// RPC get_company_dre_configuration(p_company_id) → jsonb · 20261030120000_dre_layouts_versionados.sql:1402-1432
// Configuração das "Outras visões do DRE" (1.38.4). Empresa que nunca criou visão: `settings` em modo "legacy" e nenhum perfil
// (o seletor "Visão do DRE" fica escondido e o bloco "Outras visões" da janela Configurar DRE abre vazio). Criado no T20;
// as tabelas dre_layout_* não estão no schema do fakebase, então nenhuma visão é criada (a aula só cita o botão).
export default async function getCompanyDreConfiguration({ p_company_id }) {
  return { settings: { company_id: p_company_id, mode: 'legacy', default_profile_id: null }, profiles: [] };
}
