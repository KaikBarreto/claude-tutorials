// Edge plugnotas-dfe-sync ("Sincronizar agora" e o sync inicial das Notas Recebidas): consulta a distribuição de documentos do
// emitente. As notas do mundo já estão na tabela (semente da aula); a busca só carimba a última consulta e conta o que há.
import { configFiscal, agoraIso } from '../../lib/nfe.mjs';

export default (body, { store, db, companyId }) => {
  const cid = body?.companyId || companyId;
  const cfg = configFiscal(store, cid, body?.fiscalConfigId);
  if (!cfg?.dfe_ativo) return { success: false, error: 'Ative as Notas Recebidas antes de sincronizar' };
  db.update('company_fiscal_config', { id: cfg.id }, { dfe_last_sync_at: agoraIso() });
  return { success: true, synced: 0, total: store.rows('inbound_nfe').filter((n) => n.company_id === cid).length };
};
