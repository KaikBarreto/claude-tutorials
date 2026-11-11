// Edge plugnotas-dfe-fetch-doc ("Buscar documento" das Notas Recebidas): baixa o XML e o DANFE de uma nota que chegou só com o resumo,
// sem confirmar nem recusar nada. O XML fica guardado na própria semente da nota (coluna de bastidor xml_pendente) até ser buscado.
import { agoraIso } from '../../lib/nfe.mjs';

export default (body, { db, FunctionError }) => {
  const nota = db.first('inbound_nfe', { chave: body?.chave });
  if (!nota) throw new FunctionError('Nota não encontrada', 404, { success: false, error: 'Nota não encontrada' });
  if (nota.xml_content) return { xmlSaved: true, pdfSaved: !!nota.pdf_url, queued: false };
  if (!nota.xml_pendente) return { xmlSaved: false, pdfSaved: false, queued: false, reason: 'documento_indisponivel' };
  db.update('inbound_nfe', { id: nota.id }, { xml_content: nota.xml_pendente, resumo: false, updated_at: agoraIso() });
  return { xmlSaved: true, pdfSaved: false, queued: false };
};
