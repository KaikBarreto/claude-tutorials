// RPC set_customer_labels(p_customer_id, p_label_ids): grava as etiquetas do cadastro (ver lib/labels.mjs). Devolve void.
import { definirEtiquetas } from '../../lib/labels.mjs';

export default async function set_customer_labels(args) {
  definirEtiquetas('customer', args.p_customer_id, args.p_label_ids);
}
