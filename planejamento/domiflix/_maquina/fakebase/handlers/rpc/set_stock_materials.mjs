// RPC set_stock_materials(p_stock_id, p_inventory_ids) → void · 20260930100000_estoque_presenca_materializa_ausencia.sql
// "Configurar <local>" › Itens › Salvar: os materiais marcados ficam presentes no local; os demais materiais da empresa têm a
// ausência GRAVADA (saldo 0 e is_present = false). Trava: não desmarca material com saldo no local ("presence_has_balance: <materiais>").
import { RpcError } from '../../http/rest.mjs';
import { podeAcessarLocal } from '../../lib/estoque.mjs';
import { marcarPresenca, porNome } from '../../lib/estoque_locais.mjs';

export default async function setStockMaterials(a, { userId, db }) {
  const stock = db.first('stocks', { id: a.p_stock_id });
  if (!stock) throw new RpcError(`Estoque nao encontrado: ${a.p_stock_id}`, 'P0002', 404);
  if (!podeAcessarLocal(userId, stock.id)) throw new RpcError('sem acesso a este local de estoque', '42501', 403);
  const empresa = stock.company_id;
  const pedidos = new Set(a.p_inventory_ids || []);
  const materiais = db.rows('inventory').filter((i) => i.company_id === empresa);
  const validos = materiais.filter((i) => pedidos.has(i.id)).map((i) => i.id);

  const bloqueados = db.rows('inventory_stock_levels')
    .filter((l) => l.stock_id === stock.id && l.company_id === empresa && l.is_present && Number(l.quantity) > 0 && !validos.includes(l.inventory_id))
    .map((l) => materiais.find((i) => i.id === l.inventory_id)?.name)
    .filter(Boolean)
    .sort(porNome);
  if (bloqueados.length) throw new RpcError(`presence_has_balance: ${bloqueados.join(', ')}`, '23514');

  for (const id of validos) marcarPresenca(empresa, id, stock.id, true);
  for (const i of materiais) if (!validos.includes(i.id)) marcarPresenca(empresa, i.id, stock.id, false);
}
