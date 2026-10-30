// Gatilho trg_set_equipment_identifier (next_equipment_identifier): identificador sequencial por empresa, 4 digitos
// ("0001", "0002"...), vindo do contador equipment_number_counters. O contador NAO volta quando um equipamento e apagado.
import { db } from '../core/db.mjs';

export default {
  beforeInsert(row, hc) {
    if (row.identifier !== null && row.identifier !== undefined && String(row.identifier).trim() !== '') return;
    const companyId = row.company_id || hc.companyId;
    let counter = db.first('equipment_number_counters', { company_id: companyId });
    if (!counter) counter = db.insert('equipment_number_counters', { company_id: companyId, next_value: 1 }, { companyId });
    row.identifier = String(counter.next_value).padStart(4, '0');
    db.update('equipment_number_counters', { company_id: companyId }, { next_value: counter.next_value + 1 });
  },
};
