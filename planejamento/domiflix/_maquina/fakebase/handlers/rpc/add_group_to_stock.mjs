// RPC add_group_to_stock(p_stock_id, p_group_id) → void · 20260814225028_stock_access_acl.sql
// "Adicionar grupo" na janela "Configurar <local>": grava NA HORA (sem esperar o Salvar) a presença de todos os materiais do grupo
// no local (cria o nível com saldo 0 ou só liga a presença; saldo existente fica como está).
import { RpcError } from '../../http/rest.mjs';
import { podeAcessarLocal } from '../../lib/estoque.mjs';
import { marcarPresenca } from '../../lib/estoque_locais.mjs';

export default async function addGroupToStock(a, { userId, db }) {
  const stock = db.first('stocks', { id: a.p_stock_id });
  if (!stock) throw new RpcError(`Estoque nao encontrado: ${a.p_stock_id}`, 'P0002', 404);
  if (!podeAcessarLocal(userId, stock.id)) throw new RpcError('sem acesso a este local de estoque', '42501', 403);
  const grupo = db.first('material_groups', { id: a.p_group_id });
  if (!grupo || grupo.company_id !== stock.company_id) throw new RpcError(`Grupo invalido/de outra empresa: ${a.p_group_id}`, '42501', 403);
  for (const i of db.rows('inventory').filter((x) => x.company_id === stock.company_id && x.group_id === grupo.id)) {
    marcarPresenca(stock.company_id, i.id, stock.id, true);
  }
}
