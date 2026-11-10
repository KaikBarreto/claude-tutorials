// RPC get_accessible_inventory_ids() · 20260816120000_get_accessible_inventory_ids.sql
// Ids dos materiais que o usuário pode ver: presentes (is_present) em ao menos um local que ele acessa, OU sem nenhuma linha
// de presença (legado/global). Sem este handler o seletor "Material" do Consumo na OS (e a lista do Estoque) aparece vazio.
import { podeAcessarLocal } from '../../lib/estoque.mjs';

export default async function getAccessibleInventoryIds(_args, { userId, db }) {
  const empresa = db.first('profiles', { user_id: userId })?.company_id;
  const niveis = db.rows('inventory_stock_levels');
  return db.rows('inventory')
    .filter((i) => !empresa || i.company_id === empresa)
    .filter((i) => {
      const meus = niveis.filter((l) => l.inventory_id === i.id);
      return meus.length === 0 || meus.some((l) => l.is_present && podeAcessarLocal(userId, l.stock_id));
    })
    .map((i) => i.id);
}
