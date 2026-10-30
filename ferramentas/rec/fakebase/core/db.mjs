// Ajudante simples para handlers de RPC / edge function / hooks mexerem nos dados (sem passar pelo HTTP).
//   db.rows('customers')                           todas as linhas
//   db.find('customers', { id })                   filtra por igualdade (ou por funcao)
//   db.first('customers', { id })                  primeira ou null
//   db.insert('customer_portals', {...} | [...])   insere com defaults do banco (id, created_at, token...)
//   db.update('customers', { id }, { name })       atualiza as que casam
//   db.upsert('customer_portals', ['customer_id'], {...})
//   db.remove('customers', { id })
import { store } from './store.mjs';
import { applyDefaults } from './defaults.mjs';
import { columnsOf } from './schema.mjs';
import { nowIso, uuid } from './util.mjs';
import { config } from './config.mjs';

const matcher = (m) => (typeof m === 'function' ? m : (r) => Object.entries(m || {}).every(([k, v]) => String(r[k]) === String(v)));

export const db = {
  rows: (table) => store.rows(table),
  find: (table, m) => store.rows(table).filter(matcher(m)),
  first: (table, m) => store.rows(table).find(matcher(m)) || null,
  insert(table, input, ctx = {}) {
    const list = Array.isArray(input) ? input : [input];
    const out = list.map((r) => {
      const row = applyDefaults(table, r, { companyId: ctx.companyId || config.companyId });
      if (row.id === undefined || row.id === null) row.id = uuid();
      return store.insertRaw(table, row);
    });
    return Array.isArray(input) ? out : out[0];
  },
  update(table, m, patch) {
    const hit = store.rows(table).filter(matcher(m));
    for (const r of hit) {
      Object.assign(r, patch);
      if (columnsOf(table).updated_at && patch.updated_at === undefined) r.updated_at = nowIso();
    }
    if (hit.length) store.table(table).touch();
    return hit;
  },
  upsert(table, keys, input, ctx = {}) {
    const existing = store.rows(table).find((r) => keys.every((k) => String(r[k]) === String(input[k])));
    if (existing) return db.update(table, (r) => r === existing, input)[0];
    return db.insert(table, input, ctx);
  },
  remove(table, m) {
    const t = store.table(table);
    const keep = [];
    const gone = [];
    const fn = matcher(m);
    for (const r of t.rows) (fn(r) ? gone : keep).push(r);
    if (gone.length) {
      t.rows = keep;
      t.touch();
    }
    return gone;
  },
};
