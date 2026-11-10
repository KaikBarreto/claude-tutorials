// T11 · gatilhos e DEFAULTs do banco real em `contracts` que o fakebase precisa imitar:
//  - ensure_pmoc_token (20260523144134): contrato PMOC nasce com `public_pmoc_token` (32 hex); is_pmoc=false limpa o token;
//  - trg_ensure_public_short_code (20260620200000): `public_short_code` de 12 caracteres (alfabeto base32 sem ambíguos);
//  - DEFAULTs: portal_is_public true (20260611110747), portal_documents_released false (20260607120000), portal_sections {}.
// As sementes (seeds-extra) entram sem hooks: as linhas semeadas trazem token e código prontos.
import crypto from 'node:crypto';
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

TABLE_DEFAULTS.contracts = {
  ...(TABLE_DEFAULTS.contracts || {}),
  portal_is_public: true,
  portal_documents_released: false,
  portal_sections: () => ({}),
};

const ALFABETO = 'abcdefghjkmnpqrstuvwxyz23456789';
const codigoCurto = () => Array.from(crypto.randomBytes(12), (b) => ALFABETO[b % ALFABETO.length]).join('');

export default {
  beforeInsert(row) {
    if (row.is_pmoc === true && !row.public_pmoc_token) row.public_pmoc_token = crypto.randomBytes(16).toString('hex');
    if (!row.public_short_code) row.public_short_code = codigoCurto();
  },
  beforeUpdate(row, patch) {
    if (!('is_pmoc' in patch) || patch.is_pmoc === row.is_pmoc) return;
    if (patch.is_pmoc === true && !row.public_pmoc_token) patch.public_pmoc_token = crypto.randomBytes(16).toString('hex');
    if (patch.is_pmoc === false) patch.public_pmoc_token = null;
  },
};
