// RPC get_public_os_technician_location(p_os_id) · 20261019060000_zerar_sistema_solta_compra_do_financeiro_e_grant_de_avaliacao.sql:359-393
// Corte barato da última posição do técnico para o polling do mapa público (a cada 20 s): { lat, lng, event_type, created_at }
// ou null (OS inexistente, tarefa interna ou sem ponto).
import { osPublicaExiste, ultimaPosicaoTecnico } from '../../lib/publicOs.mjs';

export default async function getPublicOsTechnicianLocation({ p_os_id }) {
  return osPublicaExiste(p_os_id) ? ultimaPosicaoTecnico(p_os_id) : null;
}
