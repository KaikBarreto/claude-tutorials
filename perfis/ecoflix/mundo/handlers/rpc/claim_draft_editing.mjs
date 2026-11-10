// "Bastão" de edição de um rascunho de pedido/ticket (quem está editando ao vivo): no mundo falso há um operador por
// sessão, então quem pede fica com o bastão (ou continua com ele). Devolve o dono vigente, como a função SQL.
import { bastao } from '../../lib/eco.mjs';
export default (a, ctx) => bastao(ctx, a, 'claim');
