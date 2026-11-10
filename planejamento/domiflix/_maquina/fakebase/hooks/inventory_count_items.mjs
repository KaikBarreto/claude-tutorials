// T8 · `inventory_count_items.diff` é coluna GERADA no banco: contado − esperado (nulo enquanto não contado). A tela grava só
// `counted_qty` (ao sair do campo) e lê `diff` de volta; sem este gatilho a "Diferença" e as Divergências ficariam vazias.
const calc = (counted, expected) => (counted === null || counted === undefined ? null : Math.round((Number(counted) - Number(expected || 0)) * 1e6) / 1e6);

export default {
  beforeInsert(row) {
    row.diff = calc(row.counted_qty, row.expected_qty);
  },
  beforeUpdate(row, patch) {
    if ('counted_qty' in patch || 'expected_qty' in patch) {
      patch.diff = calc('counted_qty' in patch ? patch.counted_qty : row.counted_qty, 'expected_qty' in patch ? patch.expected_qty : row.expected_qty);
    }
  },
};
