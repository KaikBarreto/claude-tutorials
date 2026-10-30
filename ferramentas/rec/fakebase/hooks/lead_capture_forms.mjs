// Gatilho ensure_lead_form_short_code: o app nunca manda short_code, o banco gera. No fakebase o codigo e DETERMINISTICO
// a partir do titulo (o roteiro do robo precisa saber o link /cadastro/<slug>-<codigo> antes de o formulario existir).
import { shortCode } from '../core/util.mjs';

export default {
  beforeInsert(row) {
    row.short_code = shortCode(`lead_capture_forms:${row.title || ''}`);
    if (row.submission_count === undefined || row.submission_count === null) row.submission_count = 0;
  },
};
