// Fila cato_jobs do Cato (T21, hooks/useCato.tsx:308-394): a tela lê o job a cada 1 s; aqui ele anda sozinho a cada leitura, de
// "processing" para "completed" quando passa a espera da resposta (lib/cato.mjs, `espera` de cada R1 a R9). O response_payload já veio
// gravado pela edge cato-background; a tela só o mostra no "completed".
import { agoraMs } from '../../lib/eco.mjs';
import { esperaDoJob } from '../../lib/cato.mjs';

export default function catoJobs(store) {
  const t = store.table('cato_jobs');
  const agora = agoraMs();
  for (const j of t.rows) {
    if (j.status !== 'processing') continue;
    if (agora - Date.parse(j.created_at) < esperaDoJob(j.id)) continue;
    j.status = 'completed';
    j.finished_at = new Date(agora).toISOString();
    t.touch();
  }
  return t.rows;
}
