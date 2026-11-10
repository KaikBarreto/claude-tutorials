// Edge function `nfse-delete-draft` falsa (T14, 1.38.24). Contrato da real (_shared/nfse-handlers/delete-draft.ts):
//   { id } -> 200 { deleted: true } · só rascunho da própria empresa (a aula não exclui: só mostra o item do menu).
import { erro, limpo } from './_fiscal/comum.mjs';

export default async function nfseDeleteDraft(body, { db, companyId }) {
  const id = limpo(body?.id);
  if (!id) throw erro(400, 'missing_id', 'Informe o rascunho.');
  const gone = db.remove('nfse_emissions', (r) => r.id === id && r.company_id === companyId && r.status === 'rascunho');
  if (!gone.length) throw erro(404, 'draft_not_found', 'Rascunho não encontrado.');
  return { deleted: true };
}
