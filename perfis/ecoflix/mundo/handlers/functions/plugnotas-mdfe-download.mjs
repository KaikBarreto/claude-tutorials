// DAMDFE (PDF) e XML do MDF-e (T17: menu "Ações" e a Exportação Contábil; supabase/functions/plugnotas-mdfe-download): arquivos
// fictícios montados aqui, com os dados do manifesto (o PDF é uma página simples; não é o leiaute oficial).
export function pdfSimples(linhas) {
  const txt = linhas.map((l, i) => `BT /F1 ${i ? 11 : 16} Tf 56 ${790 - i * 22} Td (${String(l).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[()\\]/g, ' ')}) Tj ET`).join('\n');
  const objs = ['<</Type/Catalog/Pages 2 0 R>>', '<</Type/Pages/Kids[3 0 R]/Count 1>>',
    '<</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>',
    `<</Length ${txt.length}>>\nstream\n${txt}\nendstream`, '<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>'];
  let out = '%PDF-1.4\n';
  const offs = [];
  objs.forEach((o, i) => { offs.push(out.length); out += `${i + 1} 0 obj\n${o}\nendobj\n`; });
  const x = out.length;
  out += `xref\n0 ${objs.length + 1}\n0000000000 65535 f \n${offs.map((o) => `${String(o).padStart(10, '0')} 00000 n \n`).join('')}`;
  out += `trailer\n<</Size ${objs.length + 1}/Root 1 0 R>>\nstartxref\n${x}\n%%EOF\n`;
  return Buffer.from(out, 'latin1').toString('base64');
}

export default (body, { db, FunctionError }) => {
  const m = db.first('mdfe_manifests', { id: body?.mdfeId });
  if (!m) throw new FunctionError('MDF-e não encontrado', 404, { success: false });
  if (!m.mdfe_key) return { success: false, error: 'MDF-e ainda não autorizado' };
  if (body?.type === 'xml') {
    return { success: true, content: `<?xml version="1.0" encoding="UTF-8"?><mdfeProc versao="3.00"><MDFe><infMDFe Id="MDFe${m.mdfe_key}"><ide><serie>${m.serie}</serie><nMDF>${m.mdfe_number}</nMDF><UFIni>${m.uf_carregamento}</UFIni><UFFim>${m.uf_descarregamento}</UFFim></ide><infModal><rodo><veicTracao><placa>${m.placa_veiculo}</placa><condutor><xNome>${m.condutor_nome}</xNome></condutor></veicTracao></rodo></infModal><tot><vCarga>${m.valor_total_carga}</vCarga><qCarga>${m.peso_bruto_total}</qCarga></tot></infMDFe></MDFe><protMDFe><infProt><chMDFe>${m.mdfe_key}</chMDFe><nProt>${m.mdfe_protocol}</nProt></infProt></protMDFe></mdfeProc>` };
  }
  return { success: true, content: pdfSimples([`DAMDFE - MDF-e ${m.mdfe_number} serie ${m.serie}`, `Chave ${m.mdfe_key}`, `Protocolo ${m.mdfe_protocol}`,
    `Veiculo ${m.placa_veiculo} - Condutor ${m.condutor_nome}`, `${m.cidade_carregamento}/${m.uf_carregamento} -> ${m.cidade_descarregamento}/${m.uf_descarregamento}`,
    `Peso bruto ${m.peso_bruto_total} kg - Valor da carga R$ ${m.valor_total_carga}`, 'Documento ficticio (ambiente de demonstracao)']) };
};
