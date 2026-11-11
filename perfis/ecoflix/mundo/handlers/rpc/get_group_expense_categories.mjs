// RPC get_group_expense_categories (20261011202500): despesas da DRE do grupo por categoria (nome), com o tipo 'tax' para as de imposto.
import { exigeDono, empresasDoGrupo, categoriasDoGrupo } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  exigeDono(ctx, a._group_id);
  const c = categoriasDoGrupo(ctx.store, empresasDoGrupo(ctx.store, a._group_id), String(a._start_date).slice(0, 10), String(a._end_date).slice(0, 10));
  const linha = (e, tipo) => ({ category_name: e.name, category_color: e.color, category_type: tipo, total_value: e.value, currency: 'BRL', moedas: ['BRL'],
    moedas_misturadas: false, total_value_by_currency: [{ currency: 'BRL', total: e.value }] });
  return [...c.taxExpenses.map((e) => linha(e, 'tax')), ...c.operatingExpenses.map((e) => linha(e, 'expense'))];
};
