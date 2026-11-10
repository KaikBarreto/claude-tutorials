// RPC commit_os_material_consumption(p_service_order_id, p_lines) · 20261013150000_customer_paid_expenses_and_customer_stock.sql:1042-1375
// Baixa do estoque ao finalizar a OS. `p_lines` é o ESTADO FINAL completo do rascunho ({id, inventory_id, stock_id, quantity, notes}):
// linha do banco que não vier é estornada e apagada; para cada linha o movimento sai do delta contra `committed_quantity`
// (consumo se positivo, estorno se negativo) e o custo congela no 1º commit. Saldo negativo NÃO é erro: vira `warnings`.
// Sem esta RPC a tela diz "Materiais baixados do estoque" e nada baixa (o T8 não veria a saída no Kardex).
import { RpcError } from '../../http/rest.mjs';
import { registrarMovimento, ehGestor, podeAcessarLocal, arredonda } from '../../lib/estoque.mjs';

export default async function commitOsMaterialConsumption({ p_service_order_id, p_lines }, { db, userId, user }) {
  if (!user) throw new RpcError('Sessão expirada. Entre novamente para registrar o consumo de materiais.', '42501', 403);
  if (!Array.isArray(p_lines)) throw new RpcError('Lista de materiais inválida.', '22023');
  const os = db.first('service_orders', { id: p_service_order_id });
  if (!os) throw new RpcError('Ordem de serviço não encontrada.', 'P0002', 404);
  if (!(ehGestor(userId) || os.technician_id === userId || os.created_by === userId)) {
    throw new RpcError('Acesso negado: apenas o técnico responsável, quem criou a ordem de serviço ou um gestor pode registrar o consumo de materiais.', '42501', 403);
  }

  // PASSO A: valida o payload inteiro antes de mexer em qualquer coisa
  const mantidos = new Set();
  for (const l of p_lines) {
    const qtd = Number(l?.quantity);
    if (!l || typeof l !== 'object') throw new RpcError('Lista de materiais inválida.', '22023');
    if (!l.inventory_id || !l.stock_id) throw new RpcError('Informe o material e o local de estoque de cada item.', '22023');
    if (!(qtd > 0)) throw new RpcError('A quantidade de cada material precisa ser maior que zero.', '22023');
    if (l.id && mantidos.has(l.id)) throw new RpcError('O mesmo item de material foi enviado duas vezes.', '22023');
    const inv = db.first('inventory', { id: l.inventory_id });
    if (!inv || inv.company_id !== os.company_id || inv.archived_at) throw new RpcError('Material ativo não encontrado no estoque desta empresa.', '42501', 403);
    const loc = db.first('stocks', { id: l.stock_id });
    if (!loc || loc.company_id !== os.company_id) throw new RpcError('Local de estoque não encontrado nesta empresa.', '42501', 403);
    if ((inv.customer_id || null) !== (loc.customer_id || null)) throw new RpcError('Material e local de estoque devem pertencer ao mesmo cliente.', '42501', 403);
    if (inv.customer_id && inv.customer_id !== os.customer_id) throw new RpcError('Estoque de cliente só pode ser consumido em OS do mesmo cliente.', '42501', 403);
    if (!podeAcessarLocal(userId, loc.id)) throw new RpcError(`Acesso negado: você não tem permissão no local de estoque "${loc.name}".`, '42501', 403);
    if (l.id) {
      if (!db.first('service_order_materials', { id: l.id, service_order_id: p_service_order_id })) {
        throw new RpcError('Um dos itens não pertence a esta ordem de serviço.', '42501', 403);
      }
      mantidos.add(l.id);
    }
  }

  // PASSO B: sincroniza o rascunho e monta a fila (linha, material, local, quantidade ALVO)
  const ops = [];
  const existentes = db.find('service_order_materials', { service_order_id: p_service_order_id })
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)));
  for (const r of existentes) {
    if (!mantidos.has(r.id)) ops.push({ row_id: r.id, inventory_id: r.inventory_id, stock_id: r.stock_id, target: 0, notes: r.notes, delete_after: true });
  }
  for (const l of p_lines) {
    const notas = String(l.notes ?? '').trim() || null;
    let linha;
    if (!l.id) {
      linha = db.insert('service_order_materials', {
        company_id: os.company_id, service_order_id: p_service_order_id, inventory_id: l.inventory_id, stock_id: l.stock_id,
        quantity: Number(l.quantity), committed_quantity: 0, notes: notas, created_by: userId,
      });
    } else {
      linha = db.first('service_order_materials', { id: l.id });
      if (linha.inventory_id !== l.inventory_id || linha.stock_id !== l.stock_id) {
        const mudouMaterial = linha.inventory_id !== l.inventory_id;
        if (Number(linha.committed_quantity) !== 0) {
          ops.push({ row_id: linha.id, inventory_id: linha.inventory_id, stock_id: linha.stock_id, target: 0, notes: linha.notes, delete_after: false });
        }
        db.update('service_order_materials', { id: linha.id }, { inventory_id: l.inventory_id, stock_id: l.stock_id, ...(mudouMaterial ? { unit_cost: null } : {}) });
      }
      db.update('service_order_materials', { id: linha.id }, { quantity: Number(l.quantity), notes: notas });
    }
    ops.push({ row_id: linha.id, inventory_id: l.inventory_id, stock_id: l.stock_id, target: Number(l.quantity), notes: notas, delete_after: false });
  }

  // PASSO C: executa a fila (delta -> movimento -> atualiza a âncora)
  const committed = [];
  const warnings = [];
  for (const op of ops) {
    const row = db.first('service_order_materials', { id: op.row_id });
    if (!row) continue;
    const delta = arredonda(op.target - Number(row.committed_quantity || 0));
    if (delta !== 0) {
      let custo = row.unit_cost;
      if (custo === null || custo === undefined) {
        custo = db.first('inventory', { id: op.inventory_id })?.cost_price ?? null;
        db.update('service_order_materials', { id: op.row_id }, { unit_cost: custo });
      }
      const tipo = delta > 0 ? 'consumo' : 'estorno';
      const obs = (delta > 0 ? 'Consumo na OS #' : 'Estorno de consumo na OS #') + os.order_number + (String(op.notes ?? '').trim() ? ` — ${String(op.notes).trim()}` : '');
      const mov = registrarMovimento({
        inventory_id: op.inventory_id, movement_type: tipo, quantity: delta > 0 ? -delta : Math.abs(delta), unit_cost: custo,
        notes: obs, service_order_id: p_service_order_id, stock_id: op.stock_id,
      }, userId);
      committed.push({ line_id: op.row_id, inventory_id: op.inventory_id, stock_id: op.stock_id, movement_id: mov.id, movement_type: tipo, quantity: Math.abs(delta), stock_after: mov.stock_after });
      if (mov.stock_after < 0) {
        warnings.push({ line_id: op.row_id, inventory_id: op.inventory_id, stock_id: op.stock_id, resulting_quantity: mov.stock_after, reason: 'saldo_negativo' });
      }
    }
    db.update('service_order_materials', { id: op.row_id }, { committed_quantity: op.target });
    if (op.delete_after) db.remove('service_order_materials', { id: op.row_id });
  }
  return { committed, warnings };
}
