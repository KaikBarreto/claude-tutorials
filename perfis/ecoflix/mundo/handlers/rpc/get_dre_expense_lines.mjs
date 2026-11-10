// Linhas que compõem as despesas da DRE (o detalhe por lançamento do Relatório Financeiro), paginadas.
import { linhasDRE } from '../../lib/eco.mjs';
export default (a, ctx) => linhasDRE(a, ctx, 'expense');
