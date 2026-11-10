// DEFAULTs de processes (20261001130000_processes.sql): `status` nasce 'draft' e `version` 1 (o fakebase chutaria null e 0).
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

TABLE_DEFAULTS.processes = { ...(TABLE_DEFAULTS.processes || {}), status: 'draft', version: 1, meta: () => ({}) };

export default {};
