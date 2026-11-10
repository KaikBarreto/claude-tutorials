// Ajuste de saldo de um material por DELTA, como a função SQL (20260908213200_matriz_ajusta_filial_e_saldo_por_unidade.sql): idempotência
// pelo client_request_id, saldo novo = saldo + delta e UM stock_movements (type EXCLUSAO se p_reason = EXCLUSAO, senão EDICAO_MANUAL; a
// descrição é a observação do usuário ou o texto automático "Ajuste manual de estoque (<motivo>): <delta> kg"). Movimentar estoque (T03
// cap08: saída de 2 kg, p_reason SAIDA), edição do saldo no Editar Material (EDICAO_MANUAL) e Zerar Estoque.
import { inserir, agoraMs, r3, num } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  if (!a.p_material_id) throw new RpcError('p_material_id é obrigatório', 'P0001');
  if (a.p_delta === undefined || a.p_delta === null) throw new RpcError('p_delta é obrigatório', 'P0001');
  const m = store.rows('materials').find((x) => x.id === a.p_material_id);
  if (!m) throw new RpcError('Material não encontrado', 'P0001');
  const antes = num(m.current_stock);
  const cri = a.p_client_request_id && String(a.p_client_request_id).trim() ? String(a.p_client_request_id) : null;
  if (cri && store.rows('stock_movements').some((s) => s.company_id === m.company_id && s.material_id === m.id && s.client_request_id === cri)) {
    return { material_id: m.id, new_stock: antes, stock_before: antes, stock_after: antes, delta: 0, idempotent_skip: true };
  }
  const delta = num(a.p_delta);
  const depois = r3(antes + delta);
  const agora = new Date(agoraMs()).toISOString();
  m.current_stock = depois;
  m.updated_at = agora;
  store.table('materials').touch();
  let mov = null;
  if (delta !== 0) {
    const motivo = a.p_reason && String(a.p_reason).trim() ? String(a.p_reason) : '';
    const desc = a.p_description && String(a.p_description).trim()
      ? String(a.p_description)
      : `Ajuste manual de estoque${motivo ? ` (${motivo})` : ''}: ${delta > 0 ? '+' : ''}${delta.toFixed(3)} kg`;
    mov = inserir(ctx, 'stock_movements', {
      company_id: m.company_id, material_id: m.id, type: motivo.toUpperCase() === 'EXCLUSAO' ? 'EXCLUSAO' : 'EDICAO_MANUAL',
      quantity: delta, stock_before: antes, stock_after: depois, description: desc, created_by: ctx.userId || null,
      client_request_id: cri, transaction_at: agora, invoice_id: a.p_invoice_id || null,
    });
  }
  return { material_id: m.id, material_name: m.name, new_stock: depois, stock_before: antes, stock_after: depois, delta,
    movement_id: mov ? mov.id : null, via_group: false, idempotent_skip: false };
};
