// RPC set_equipment_labels(p_equipment_id, p_label_ids): grava as etiquetas do cadastro (ver lib/labels.mjs). Devolve void.
import { definirEtiquetas } from '../../lib/labels.mjs';

export default async function set_equipment_labels(args) {
  definirEtiquetas('equipment', args.p_equipment_id, args.p_label_ids);
}
