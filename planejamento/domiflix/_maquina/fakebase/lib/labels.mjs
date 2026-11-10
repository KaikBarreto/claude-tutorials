// Etiquetas (Dominex 1.38.9): grava os vinculos de um cadastro com as etiquetas, como as tres RPC SECURITY DEFINER do
// banco real (supabase/migrations/20261031193000_party_multi_labels.sql:154-256): set_customer_labels, set_supplier_labels
// e set_equipment_labels. O app chama a RPC em TODO salvamento de cliente, fornecedor e equipamento, inclusive sem etiqueta.
//   - confere que o cadastro existe e que cada etiqueta e da mesma empresa e do escopo certo (party|all ou equipment|all);
//   - apaga os vinculos que sairam da lista, grava os da lista com position = indice (a ordem em que foram marcadas);
//   - cliente e fornecedor: espelha a primeira etiqueta na coluna legada `label_id` (equipamento nao tem essa coluna).
import { RpcError } from '../http/rest.mjs';
import { store } from '../core/store.mjs';
import { db } from '../core/db.mjs';
import { applyDefaults } from '../core/defaults.mjs';
import { config } from '../core/config.mjs';

const ENTIDADES = {
  customer: { tabela: 'customers', vinculos: 'customer_label_assignments', fk: 'customer_id', escopos: ['party', 'all'], nome: 'Cliente', espelha: true },
  supplier: { tabela: 'suppliers', vinculos: 'supplier_label_assignments', fk: 'supplier_id', escopos: ['party', 'all'], nome: 'Fornecedor', espelha: true },
  equipment: { tabela: 'equipment', vinculos: 'equipment_label_assignments', fk: 'equipment_id', escopos: ['equipment', 'all'], nome: 'Equipamento', espelha: false },
};

export function definirEtiquetas(tipo, entidadeId, labelIds) {
  const e = ENTIDADES[tipo];
  const cadastro = db.first(e.tabela, { id: entidadeId });
  if (!cadastro || cadastro.is_deleted === true) throw new RpcError(`${e.nome} indisponivel para esta empresa.`, '42501', 403);
  const empresa = cadastro.company_id;
  const ids = [...new Set((labelIds ?? []).map(String))]; // sem repetidos, na ordem em que vieram
  for (const id of ids) {
    const etiqueta = db.first('party_labels', { id });
    if (!etiqueta || etiqueta.company_id !== empresa || !e.escopos.includes(etiqueta.scope)) {
      throw new RpcError('Uma ou mais etiquetas nao estao disponiveis para esta empresa.', '42501', 403);
    }
  }
  const dele = (r) => r.company_id === empresa && String(r[e.fk]) === String(entidadeId);
  db.remove(e.vinculos, (r) => dele(r) && !ids.includes(String(r.label_id)));
  ids.forEach((labelId, posicao) => {
    const existente = db.first(e.vinculos, (r) => dele(r) && String(r.label_id) === labelId);
    if (existente) {
      existente.position = posicao;
      store.table(e.vinculos).touch();
    } else {
      // a tabela de vinculos nao tem coluna `id` (a chave e empresa+cadastro+etiqueta): insere direto, sem inventar um
      store.insertRaw(e.vinculos, applyDefaults(e.vinculos, { company_id: empresa, [e.fk]: entidadeId, label_id: labelId, position: posicao, created_by: config.userId }));
    }
  });
  if (e.espelha) {
    cadastro.label_id = ids[0] ?? null;
    store.table(e.tabela).touch();
  }
}
