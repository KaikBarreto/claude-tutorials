// Linhas que compõem as outras receitas da DRE (lançamentos de entrada categorizados), paginadas.
import { linhasDRE } from '../../lib/eco.mjs';
export default (a, ctx) => linhasDRE(a, ctx, 'income');
