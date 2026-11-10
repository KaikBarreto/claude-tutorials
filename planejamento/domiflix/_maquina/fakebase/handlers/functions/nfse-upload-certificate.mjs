// Edge function `nfse-upload-certificate` falsa (T14, 1.38.24). Mesmo contrato da real
// (src-1.38.24/supabase/functions/_shared/nfse-handlers/upload-certificate.ts + providers/sefin.ts `enviarCertificado`):
//   multipart { file (.pfx/.p12), password, nome } -> 200 { status: 'ativo', certificate_expires_at, message }
//   - sem linha em company_fiscal_settings -> 422 fiscal_not_configured ("Salve os dados fiscais...");
//   - empresa sem CNPJ -> 422 company_cnpj_missing; arquivo de outro tipo -> 422 invalid_file_type; sem senha -> 422 missing_password.
// Grava a custódia (certificado_ref + DEK/senha/nonce/algoritmo, valores fictícios), a validade e a linha "upload" na trilha
// do certificado. O arquivo do mundo fictício não é certificado (bytes aleatórios): a validade e o CNPJ do titular são os
// do mundo (A1 de um ano, emitido em 10/11/2026 para o CNPJ da Glacial), então a identidade sempre confere.
// O desvio de rede do gravador (FAKE_URL diferente da URL do build) pode chegar sem o corpo multipart (limitação do
// Playwright com arquivo no corpo; ver rec/t7/gerar.py, FAKE_DIRETO): sem corpo, o envio é aceito como se o arquivo tivesse
// chegado, porque a tela só envia quando há arquivo, senha e autorização.
import { erro, fiscalDe, cnpjEmpresa, auditar } from './_fiscal/comum.mjs';
import { now } from '../../core/util.mjs';

export const VALIDADE_A1 = '2027-11-10T15:00:00.000Z'; // 10/11/2027 12:00 em Brasília

/** Campos de um corpo multipart/form-data (texto; o arquivo só pelo nome). */
function lerMultipart(raw, contentType) {
  const m = /boundary=(?:"([^"]+)"|([^;]+))/i.exec(contentType || '');
  if (!raw?.length || !m) return null;
  const sep = '--' + (m[1] || m[2]).trim();
  const texto = raw.toString('latin1');
  const campos = {};
  for (const parte of texto.split(sep)) {
    const i = parte.indexOf('\r\n\r\n');
    if (i < 0) continue;
    const cab = parte.slice(0, i);
    const nome = /name="([^"]*)"/i.exec(cab)?.[1];
    if (!nome) continue;
    const arquivo = /filename="([^"]*)"/i.exec(cab)?.[1];
    const valor = parte.slice(i + 4).replace(/\r\n$/, '');
    campos[nome] = arquivo !== undefined ? { arquivo: Buffer.from(arquivo, 'latin1').toString('utf8'), tamanho: valor.length } : Buffer.from(valor, 'latin1').toString('utf8');
  }
  return campos;
}

export default async function nfseUploadCertificate(body, { db, companyId, req }) {
  const fiscal = fiscalDe(db, companyId);
  if (!fiscal) throw erro(422, 'fiscal_not_configured', 'Salve os dados fiscais da empresa antes de enviar o certificado digital.');
  const cnpj = cnpjEmpresa(db, companyId);
  if (cnpj.length !== 14) throw erro(422, 'company_cnpj_missing', 'Cadastre um CNPJ válido para a empresa antes de enviar o certificado digital.');

  const campos = lerMultipart(body?.__raw, req?.headers?.['content-type']);
  if (campos) {
    const f = campos.file;
    if (f && typeof f === 'object') {
      // pelo desvio do gravador a parte do arquivo chega com 0 byte (o Playwright não repassa o conteúdo do File):
      // vale o nome do arquivo, que a tela já exige ser .pfx/.p12
      if (!f.arquivo) throw erro(422, 'missing_file', 'Anexe o arquivo do certificado digital (.pfx ou .p12).');
      if (!/\.(pfx|p12)$/i.test(f.arquivo)) throw erro(422, 'invalid_file_type', 'O certificado deve ser um arquivo .pfx ou .p12.');
    }
    if ('password' in campos && !String(campos.password || '').trim()) throw erro(422, 'missing_password', 'Informe a senha do certificado digital.');
  }

  const ref = `${companyId}/cert-${now().getTime()}.b64`;
  db.update('company_fiscal_settings', { company_id: companyId }, {
    certificate_expires_at: VALIDADE_A1,
    certificado_ref: ref,
    certificado_dek_envelopada: 'ZGVrLWZpY3RpY2lh',       // "dek-ficticia" (base64): o falso não guarda chave nenhuma
    certificado_senha_cifrada: 'c2VuaGEtZmljdGljaWE=',   // "senha-ficticia"
    certificado_nonce: 'bm9uY2U=',
    certificado_algoritmo: 'AES-256-GCM',
  });
  auditar(db, companyId, 'upload', 'upload_certificado', 'edge:nfse-upload-certificate');
  return { status: 'ativo', certificate_expires_at: VALIDADE_A1, message: 'Certificado digital enviado e guardado com segurança.' };
}
