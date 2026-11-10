// T5 · gatilhos e DEFAULTs do banco real em `service_orders` que o fakebase precisa imitar (inventário T05, 4.1 e 4.7):
//  - DEFAULTs: `status` nasce 'pendente' (a OS manual nasce Pendente; só o "+" de uma coluna do Kanban manda outro status),
//    `entry_type` 'os', `origin` 'manual' e `order_number` pela sequência (a base semeia 1 a 15, a próxima nasce 16;
//    tarefa também gasta número, como no banco real: `DEFAULT nextval('service_orders_order_number_seq')`).
//  - `scheduled_time` volta como "HH:MM:SS" (coluna `time` do Postgres), mesmo que o app mande "HH:MM".
//  - service_orders_track_pause_resume (BEFORE UPDATE, 20260505000002_...sql): na TROCA de status carimba
//    paused_at/resumed_at/started_at/completed_at. Arrastar o cartão no Kanban é um UPDATE, então é isso que alimenta
//    a "Linha do tempo" da Agenda, o "Tempo médio" e a "Saúde do agendamento". INSERT direto numa coluna não passa por aqui.
// As sementes (seeds-extra) entram sem hooks: as linhas semeadas trazem os carimbos prontos.
import { TABLE_DEFAULTS } from '../core/defaults.mjs';
import { nowIso } from '../core/util.mjs';

TABLE_DEFAULTS.service_orders = {
  ...(TABLE_DEFAULTS.service_orders || {}),
  status: 'pendente',
  entry_type: 'os',
  origin: 'manual',
};

const withSeconds = (t) => (typeof t === 'string' && /^\d{2}:\d{2}$/.test(t) ? `${t}:00` : t);

export default {
  beforeInsert(row, hc) {
    if (!row.order_number) row.order_number = hc.nextSeq('service_orders', 'order_number', hc.store.rows('service_orders'));
    row.scheduled_time = withSeconds(row.scheduled_time);
  },

  beforeUpdate(row, patch) {
    if ('scheduled_time' in patch) patch.scheduled_time = withSeconds(patch.scheduled_time);
    if (!('status' in patch) || patch.status === row.status) return;
    const now = nowIso();
    const to = patch.status;
    const from = row.status;
    if (to === 'pausada') {
      patch.paused_at = now;
      patch.resumed_at = null;
    }
    if (from === 'pausada' && to !== 'pausada') patch.resumed_at = now;
    if (to === 'em_andamento' && !row.started_at && !patch.started_at) patch.started_at = now;
    if (to === 'concluida') patch.completed_at = now;
  },
};
