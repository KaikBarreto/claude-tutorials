// Edge function `generate-pmoc-planilha-pdf` falsa (T11): grava a versão em pmoc_documents; ver lib/pmocDocs.mjs.
import { criaGerador } from '../../lib/pmocDocs.mjs';

export default criaGerador('generate-pmoc-planilha-pdf');
