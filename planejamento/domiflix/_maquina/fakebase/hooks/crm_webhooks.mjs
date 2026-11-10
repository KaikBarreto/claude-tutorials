// T10 · crm_webhooks.token: 64 caracteres hexadecimais por padrao no banco (gen_random_bytes(32)). No fakebase o token e DETERMINISTICO
// (sha256 do nome do webhook), para a gravacao ser repetivel; o app nunca manda o token. is_active nasce ligado.
import crypto from 'node:crypto';

export default {
  beforeInsert(row) {
    if (!row.token) row.token = crypto.createHash('sha256').update(`dominex-fake-crm-webhook-${row.company_id}-${row.name || ''}`).digest('hex');
    if (row.is_active === null || row.is_active === undefined) row.is_active = true;
  },
};
