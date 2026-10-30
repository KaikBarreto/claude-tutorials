// Gatilhos do banco real em `customers` (t3/inventario.md, 13.1) que o fakebase precisa imitar:
//  - trg_create_customer_portal_on_insert: todo cliente novo ganha a linha de customer_portals (token aleatorio, ativo)
//  - track_customer_whatsapp_preference: carimba whatsapp_opt_in_at / whatsapp_opt_out_at quando o interruptor muda
import crypto from 'node:crypto';
import { db } from '../core/db.mjs';
import { nowIso } from '../core/util.mjs';

export default {
  beforeInsert(row) {
    if (row.whatsapp_notifications_enabled === true) {
      row.whatsapp_opt_in_at = nowIso();
      row.whatsapp_opt_out_at = null;
    }
  },
  afterInsert(row, hc) {
    if (db.first('customer_portals', { customer_id: row.id })) return;
    db.insert(
      'customer_portals',
      {
        customer_id: row.id,
        token: crypto.randomBytes(16).toString('hex'),
        is_active: true,
        is_public: true,
        password_enabled: false,
        permissions: {},
        public_sections: {},
      },
      { companyId: hc.companyId },
    );
  },
  beforeUpdate(row, patch) {
    if (!('whatsapp_notifications_enabled' in patch) || patch.whatsapp_notifications_enabled === row.whatsapp_notifications_enabled) return;
    if (patch.whatsapp_notifications_enabled) {
      patch.whatsapp_opt_in_at = nowIso();
      patch.whatsapp_opt_out_at = null;
    } else {
      patch.whatsapp_opt_out_at = nowIso();
    }
  },
};
