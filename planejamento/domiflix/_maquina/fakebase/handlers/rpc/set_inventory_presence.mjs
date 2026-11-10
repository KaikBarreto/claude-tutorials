// RPC set_inventory_presence(p_inventory_id, p_stock_ids) → void · 20260930100000_estoque_presenca_materializa_ausencia.sql
// Marca em quais locais o material está presente (cadastro do material). Trava: não deixa tirar o material de um local que
// ainda tem saldo ("presence_has_balance: <locais>"). A AUSÊNCIA é gravada (nível com saldo 0 e is_present = false) em todos os
// demais locais da empresa; a presença cria o nível com saldo 0 se faltar.
import { RpcError } from '../../http/rest.mjs';
import { podeAcessarLocal } from '../../lib/estoque.mjs';
import { marcarPresenca, porNome } from '../../lib/estoque_locais.mjs';

export default async function setInventoryPresence(a, { userId, db }) {
  const inv = db.first('inventory', { id: a.p_inventory_id });
  if (!inv) throw new RpcError(`Item de estoque nao encontrado: ${a.p_inventory_id}`, 'P0002', 404);
  const empresa = inv.company_id;
  const pedidos = new Set(a.p_stock_ids || []);
  const locais = db.rows('stocks').filter((s) => s.company_id === empresa);
  const validos = locais.filter((s) => pedidos.has(s.id)).map((s) => s.id);
  for (const sid of validos) if (!podeAcessarLocal(userId, sid)) throw new RpcError('sem acesso a este local de estoque', '42501', 403);

  const bloqueados = db.rows('inventory_stock_levels')
    .filter((l) => l.inventory_id === inv.id && l.company_id === empresa && l.is_present && Number(l.quantity) > 0 && !validos.includes(l.stock_id))
    .map((l) => locais.find((s) => s.id === l.stock_id)?.name)
    .filter(Boolean)
    .sort(porNome);
  if (bloqueados.length) throw new RpcError(`presence_has_balance: ${bloqueados.join(', ')}`, '23514');

  for (const sid of validos) marcarPresenca(empresa, inv.id, sid, true);
  for (const s of locais) if (!validos.includes(s.id)) marcarPresenca(empresa, inv.id, s.id, false);
}
