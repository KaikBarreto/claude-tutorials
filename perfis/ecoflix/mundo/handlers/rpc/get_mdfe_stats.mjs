// Cartões de Transporte (MDF-e) (T17 caps. 1, 4 e 5: "MDF-e Autorizados", "Pendentes", "Rejeitados", "Encerrados"), como a RPC do
// banco (migration 20261028193000_mdfe_contingency.sql): contagem por status de todos os manifestos da empresa.
const PENDENTES = ['pendente', 'aguardando_sefaz', 'encerramento_pendente', 'encerramento_rejeitado', 'cancelamento_pendente',
  'cancelamento_rejeitado', 'preparando_contingencia', 'contingencia', 'contingencia_erro', 'contingencia_rejeitada'];

export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const ms = store.rows('mdfe_manifests').filter((m) => m.company_id === cid);
  const conta = (f) => ms.filter(f).length;
  return {
    total_autorizados: conta((m) => m.status === 'autorizado'),
    total_pendentes: conta((m) => PENDENTES.includes(m.status)),
    total_rejeitados: conta((m) => m.status === 'rejeitado'),
    total_encerrados: conta((m) => m.status === 'encerrado'),
  };
};
