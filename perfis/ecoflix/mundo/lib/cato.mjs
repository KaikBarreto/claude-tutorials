// Cato simulado (T21, "Cato, o assistente"): nada de IA de verdade na gravação. A pergunta escolhe, pelo texto exato (sem acento,
// caixa e pontuação), uma das respostas R1 a R9 do planejamento/ecoflix/T21/plano.md, copiadas para lib/cato_respostas.json por
// rec/t21/t21_respostas.py (o plano é a fonte). O formato é o `response_payload` do app (hooks/useCato.tsx:32-46).
// Fluxo real imitado (useCato.tsx:308-394): a edge cato-background devolve { jobId }; a tela lê cato_jobs a cada 1 s; o job nasce
// "processing" e vira "completed" `espera` segundos depois (handlers/views/cato_jobs.mjs); depois a tela pede as sugestões à edge
// cato-assist com mode "followups".
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { agoraMs, diaBR } from './eco.mjs';

const ARQ = path.join(path.dirname(fileURLToPath(import.meta.url)), 'cato_respostas.json');
let cache = null;
function respostas() {
  if (!cache) cache = JSON.parse(fs.readFileSync(ARQ, 'utf8')).respostas;
  return cache;
}

export const normaliza = (t) => String(t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

/** A resposta simulada da pergunta (ou null). */
export function acharResposta(texto) {
  const n = normaliza(texto);
  return respostas().find((r) => normaliza(r.pergunta) === n) || null;
}

/** `response_payload` da resposta: interactionId novo, sem cache e "Atualizado às" na hora fixa da resposta (HH:MM do dia do relógio
 * falso), para a conversa contínua dos caps. 3 a 8 sair igual quando um capítulo restaura as respostas dos anteriores. */
export function payloadDe(r, agora = agoraMs()) {
  const p = JSON.parse(JSON.stringify(r.payload));
  if (p.context) p.context.updatedAt = r.hora ? new Date(`${diaBR(agora)}T${r.hora}:00-03:00`).toISOString() : new Date(agora).toISOString();
  p.interactionId = crypto.randomUUID();
  p.cacheHit = false;
  return p;
}

/** Pergunta fora do roteiro: resposta que salta aos olhos no ensaio (o observador de avisos do robô procura este texto). */
export function semResposta(texto) {
  return { answer: `SEM RESPOSTA SIMULADA para "${String(texto || '').slice(0, 80)}"`, toolsUsed: [], context: null, interactionId: crypto.randomUUID(), cacheHit: false };
}

// espera (ms) de cada job até virar "completed"; o view handlers/views/cato_jobs.mjs consulta
const ESPERA = new Map();
export const registraEspera = (jobId, ms) => ESPERA.set(jobId, ms);
export const esperaDoJob = (jobId) => ESPERA.get(jobId) ?? 3000;
