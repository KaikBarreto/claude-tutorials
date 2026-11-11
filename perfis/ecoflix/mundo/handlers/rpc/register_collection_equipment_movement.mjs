// Lançamento avulso de equipamento ("Movimentar": de onde saiu pra onde foi), 20261008140000: uma linha do razão por equipamento
// (unidade identificável ou quantidade); a posição sai da view collection_equipment_positions.
import { inserirMovimento } from '../../lib/coletas.mjs';

const KINDS = ['base', 'partner', 'externo'];
export default (a, { store, db, userId, companyId, RpcError }) => {
  const co = a.p_company_id || companyId;
  if (!KINDS.includes(a.p_origem_kind) || !KINDS.includes(a.p_destino_kind)) throw new RpcError('Origem e destino precisam ser base, parceiro ou externo.');
  if (a.p_origem_kind === a.p_destino_kind && (a.p_origem_partner_id || null) === (a.p_destino_partner_id || null)) {
    throw new RpcError('A origem e o destino são o mesmo lugar.');
  }
  const linhas = Array.isArray(a.p_lines) ? a.p_lines : [];
  if (!linhas.length) throw new RpcError('Informe ao menos um equipamento.');
  const ids = linhas.map((l) => inserirMovimento(db, store, {
    company_id: co, equipment_type_id: l.equipment_type_id, container_id: l.container_id || null, quantidade: l.quantidade ?? 1,
    origem_kind: a.p_origem_kind, origem_partner_type: a.p_origem_partner_type, origem_partner_id: a.p_origem_partner_id,
    destino_kind: a.p_destino_kind, destino_partner_type: a.p_destino_partner_type, destino_partner_id: a.p_destino_partner_id,
    moved_at: a.p_moved_at, collection_order_id: a.p_collection_order_id, observacao: a.p_observacao, created_by: userId,
  }).id);
  return { movement_ids: ids, inseridas: ids.length, avisos: [] };
};
