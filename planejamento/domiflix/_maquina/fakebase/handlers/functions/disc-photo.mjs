// Edge function disc-photo?code=<código> (pública): a foto do funcionário no cabeçalho do teste DISC. O mundo fictício não tem foto:
// responde 404 e a tela cai nas iniciais (SVG), como acontece com funcionário sem foto no sistema real.
import { FunctionError } from '../../http/functions.mjs';

export default async function discPhoto() {
  throw new FunctionError('Foto não encontrada', 404);
}
