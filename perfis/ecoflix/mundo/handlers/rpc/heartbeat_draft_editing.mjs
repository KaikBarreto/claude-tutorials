// Sinal de vida do editor de um rascunho ("ainda estou aqui"): renova o bastão da sessão dona.
import { bastao } from '../../lib/eco.mjs';
export default (a, ctx) => bastao(ctx, a, 'heartbeat');
