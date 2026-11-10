// Gatilho ensure_public_short_code + DEFAULTs de disc_assessments (20260724120000_disc_perfil_comportamental.sql; 20260620200000_public_short_codes_links_amigaveis.sql).
// No banco real o código de 12 caracteres é aleatório; no fakebase ele é DETERMINÍSTICO (nome do funcionário + ordem do link) para o robô
// saber o link /avaliacao/<nome>-<código> e quais das 56+20 perguntas o sorteio (semeado pelo código) vai mostrar, antes de o link existir.
import { shortCode } from '../core/util.mjs';
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

TABLE_DEFAULTS.disc_assessments = { ...(TABLE_DEFAULTS.disc_assessments || {}), status: 'pending' };

export default {
  beforeInsert(row, hc) {
    const emp = hc.store.rows('employees').find((e) => String(e.id) === String(row.employee_id));
    const n = hc.store.rows('disc_assessments').filter((a) => String(a.employee_id) === String(row.employee_id)).length;
    row.public_short_code = shortCode(`disc_assessments:${emp?.name ?? row.employee_id}:${n}`);
  },
};
