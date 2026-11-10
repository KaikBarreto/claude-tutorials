// RPC submit_public_os_rating(p_os_id, p_nps, p_comment, p_name, p_criteria) · 20260616140000_nps_onda2_criterios_dinamicos.sql:204-294
// Avaliação do cliente pelo link público: exige OS concluída, nota 0 a 10 e uma única resposta por OS; grava a nota em
// `service_ratings` e cada estrela (1 a 5) em `service_rating_criteria`, só para critérios da empresa da OS.
// Sem este handler a tela diz "Avaliação enviada" e nada é gravado (o NPS do T5 não mudaria).
import crypto from 'node:crypto';
import { RpcError } from '../../http/rest.mjs';
import { nowIso } from '../../core/util.mjs';

// colunas legadas de estrela que o banco ainda mantém junto dos critérios (as sementes do T5 também as preenchem)
const LEGADO = { Qualidade: 'quality_rating', Pontualidade: 'punctuality_rating', Profissionalismo: 'professionalism_rating' };

export default async function submitPublicOsRating({ p_os_id, p_nps, p_comment = null, p_name = null, p_criteria = [] }, { db }) {
  const os = db.first('service_orders', { id: p_os_id });
  if (!os) throw new RpcError('OS não encontrada.', 'P0002', 404);
  if (os.status !== 'concluida') throw new RpcError('A avaliação só fica disponível após a conclusão do serviço.', '23514');
  if (p_nps === null || p_nps === undefined || !Number.isInteger(Number(p_nps)) || p_nps < 0 || p_nps > 10) {
    throw new RpcError('A nota de recomendação deve estar entre 0 e 10.', '23514');
  }
  let nota = db.first('service_ratings', { service_order_id: p_os_id });
  if (!nota) nota = db.insert('service_ratings', { service_order_id: p_os_id, token: crypto.randomBytes(32).toString('hex') });
  if (nota.rated_at) throw new RpcError('Esta avaliação já foi enviada. Obrigado!', '23505', 409);

  // valida antes de gravar (o banco faz tudo numa transação)
  const itens = Array.isArray(p_criteria) ? p_criteria : [];
  const gravar = itens.map((it) => {
    const valor = Number(it?.value);
    if (!Number.isInteger(valor) || valor < 1 || valor > 5) throw new RpcError('As notas por critério devem estar entre 1 e 5.', '23514');
    const crit = db.first('nps_criteria', (c) => c.id === it.criterion_id && c.company_id === os.company_id);
    if (!crit) throw new RpcError('Critério de avaliação inválido para esta empresa.', '23514');
    return { criterion_id: crit.id, label_snapshot: crit.label, value: valor };
  });

  const legado = {};
  for (const g of gravar) if (LEGADO[g.label_snapshot]) legado[LEGADO[g.label_snapshot]] = g.value;
  db.update('service_ratings', (r) => r === nota, {
    nps_score: Number(p_nps), comment: String(p_comment ?? '').trim() || null, rated_by_name: String(p_name ?? '').trim() || null,
    rated_at: nowIso(), ...legado,
  });
  for (const g of gravar) db.insert('service_rating_criteria', { rating_id: nota.id, ...g });
  return { success: true };
}
