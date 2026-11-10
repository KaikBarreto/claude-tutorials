// RPC set_supplier_labels(p_supplier_id, p_label_ids): grava as etiquetas do cadastro (ver lib/labels.mjs). Devolve void.
import { definirEtiquetas } from '../../lib/labels.mjs';

export default async function set_supplier_labels(args) {
  definirEtiquetas('supplier', args.p_supplier_id, args.p_label_ids);
}
