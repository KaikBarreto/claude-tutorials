// T5 · DEFAULTs do banco real em `teams` (migration 20260308064313_...sql:3-12): `is_active boolean DEFAULT true` e
// `color text DEFAULT '#3b82f6'`. O app NÃO manda `is_active` ao criar a equipe (TeamFormDialog.tsx:115-123 -> useTeams.ts
// createTeam), então sem este default a equipe nova nasceria nula e apareceria como "Inativa" (e sumiria de quem filtra por ativas).
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

TABLE_DEFAULTS.teams = {
  ...(TABLE_DEFAULTS.teams || {}),
  is_active: true,
  color: '#3b82f6',
};

export default {};
