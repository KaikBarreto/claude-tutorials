// Trigger de financial_categories (T15): o app não manda `dre_group_id` ao criar uma categoria; o banco preenche com o grupo do
// sistema pela natureza (validate_financial_category_dre_group, migration 20261020220000): receita -> outras_receitas_despesas,
// nome com "imposto" -> deducoes, o resto -> despesas_operacionais. A lista e o DRE hierárquico leem esse vínculo.
export default {
  beforeInsert(row, { store }) {
    if (row.dre_group_id || !row.company_id) return;
    const natureza = row.type === 'income' ? 'outras_receitas_despesas' : /imposto/i.test(String(row.name || '')) ? 'deducoes' : 'despesas_operacionais';
    const g = store.rows('dre_groups').filter((d) => d.company_id === row.company_id && d.is_system && d.nature === natureza)
      .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0) || String(a.name).localeCompare(String(b.name)))[0];
    if (g) row.dre_group_id = g.id;
  },
};
