// Simulação do motor fiscal próprio da Dominex 1.38.24 (Padrão Nacional da NFS-e, Sefin Nacional) e da Receita (DF-e),
// comum aos handlers nfse-* e dfe-* do backend falso (T14). Esta pasta (`_fiscal/`) não vira edge function: o carregador
// só registra os .mjs do primeiro nível de handlers/functions/.
// Fonte do comportamento imitado: src-1.38.24/supabase/functions/_shared/{providers/sefin.ts,nfse-handlers/*.ts,dfe-*.ts}.
// Nada aqui fala com serviço real: certificado, chave, número e PDF são inventados.
import crypto from 'node:crypto';
import { now } from '../../../core/util.mjs';
import { FunctionError } from '../../../http/functions.mjs';

export const digitos = (v) => String(v ?? '').replace(/\D/g, '');
export const limpo = (v) => (v == null ? '' : String(v).trim());
export const pad = (v, n) => digitos(v).padStart(n, '0').slice(-n);

/** Erro no formato das edges fiscais: { error: <código>, message: <PT-BR> } com o HTTP dado. */
export function erro(status, codigo, message, extra = {}) {
  return new FunctionError(codigo, status, { message, ...extra });
}

export const empresaDe = (db, companyId) => db.first('companies', { id: companyId });
export const fiscalDe = (db, companyId) => db.first('company_fiscal_settings', { company_id: companyId });
export const ambienteValido = (v) => (v === 'homologacao' || v === 'producao' ? v : null);

/** CNPJ da empresa (só dígitos): `companies.cnpj`, com `company_settings.document` de reserva. */
export function cnpjEmpresa(db, companyId) {
  const c = digitos(empresaDe(db, companyId)?.cnpj);
  if (c.length === 14) return c;
  return digitos(db.first('company_settings', { company_id: companyId })?.document);
}

/** Bloco de custódia completo (é o que `carregarCertificado` do motor exige). */
export const custodiaCompleta = (f) =>
  !!(f && limpo(f.certificado_ref) && limpo(f.certificado_dek_envelopada) && limpo(f.certificado_senha_cifrada));

/** A1 próprio com validade conhecida e futura (mesmo critério de `isFiscalReadyToEmit`). */
export function certificadoValido(f, ms = now().getTime()) {
  if (!f || !limpo(f.certificado_ref) || !f.certificate_expires_at) return false;
  const t = Date.parse(f.certificate_expires_at);
  return Number.isFinite(t) && t > ms;
}

export const SEM_CERTIFICADO = 'Envie o certificado digital da empresa nas configurações fiscais antes de emitir notas.';

/** `carregarCertificado` do motor: sem a custódia, 422 certificado_ausente. */
export function exigirCertificado(f) {
  if (!custodiaCompleta(f)) throw erro(422, 'certificado_ausente', SEM_CERTIFICADO);
}

/**
 * Instante para uma linha nova de uma trilha append-only. O relógio do falso é congelado (FAKE_NOW), então duas
 * linhas seguidas sairiam com o mesmo `created_at` e a tela (ordenada do mais recente para o mais antigo) poderia
 * inverter a ordem: cada linha nova fica 1 s depois da última da empresa.
 */
export function instante(db, tabela, companyId, filtro = {}) {
  const base = now().getTime();
  const ult = db.find(tabela, { company_id: companyId, ...filtro }).reduce((m, r) => Math.max(m, Date.parse(r.created_at) || 0), 0);
  return new Date(Math.max(base, ult + 1000)).toISOString();
}

/** Trilha de uso do certificado (`auditar` de sefin.ts): toda decifra vira linha em fiscal_certificate_audit. */
export function auditar(db, companyId, operacao, contexto, origem = 'edge:nfse') {
  return db.insert('fiscal_certificate_audit', {
    company_id: companyId, operacao, contexto, origem, created_at: instante(db, 'fiscal_certificate_audit', companyId),
  });
}

/** `corpoBase` do motor: lê a custódia e registra a decifra com o contexto da operação. */
export function decifrar(db, companyId, fiscal, contexto, origem = 'edge:nfse') {
  exigirCertificado(fiscal);
  auditar(db, companyId, 'decifra', contexto, origem);
}

/** Dígito verificador módulo 11 (pesos 2..9 da direita para a esquerda), como nas chaves fiscais. */
function dvMod11(base) {
  let soma = 0;
  let peso = 2;
  for (let i = base.length - 1; i >= 0; i--) {
    soma += Number(base[i]) * peso;
    peso = peso === 9 ? 2 : peso + 1;
  }
  const r = soma % 11;
  return r < 2 ? 0 : 11 - r;
}

const numeroDe = (semente, n) => {
  const h = crypto.createHash('sha1').update('t14-fiscal:' + semente).digest();
  let s = '';
  for (let i = 0; s.length < n; i++) s += String(h[i % h.length] % 10);
  return s.slice(0, n);
};

/**
 * Chave de acesso da NFS-e (50 dígitos, layout do Padrão Nacional): município emissor (7) + ambiente gerador (1) +
 * tipo de inscrição (1, CNPJ) + CNPJ (14) + número da NFS-e (13) + AAMM (4) + código numérico (9) + DV (1). Fictícia.
 */
export function chaveNfse({ ibge, cnpj, numero, emitidaEm, semente }) {
  const d = new Date(emitidaEm);
  const aamm = String(d.getUTCFullYear()).slice(2) + String(d.getUTCMonth() + 1).padStart(2, '0');
  const base = pad(ibge, 7) + '2' + '2' + pad(cnpj, 14) + pad(numero, 13) + aamm + numeroDe(semente, 9);
  return base + String(dvMod11(base));
}

/** Chave da NF-e (44 dígitos): UF + AAMM + CNPJ + modelo 55 + série + número + tipo de emissão + código + DV. Fictícia. */
export function chaveNfe({ uf = '33', cnpj, serie = 1, numero, emitidaEm, semente }) {
  const d = new Date(emitidaEm);
  const aamm = String(d.getUTCFullYear()).slice(2) + String(d.getUTCMonth() + 1).padStart(2, '0');
  const base = pad(uf, 2) + aamm + pad(cnpj, 14) + '55' + pad(serie, 3) + pad(numero, 9) + '1' + numeroDe(semente, 8);
  return base + String(dvMod11(base));
}

/** Mês corrente em Brasília (UTC-3 fixo), no formato YYYY-MM. */
export function mesBR(iso) {
  const t = new Date(new Date(iso).getTime() - 3 * 3600 * 1000);
  return `${t.getUTCFullYear()}-${String(t.getUTCMonth() + 1).padStart(2, '0')}`;
}

// ------------------------------------------------------------------------------------------------ PDF fictício
// Um PDF de uma página, escrito à mão (fontes padrão Helvetica, WinAnsi), com layout próprio: sem brasão nem marca de
// órgão público. Em homologação leva a marca d'água "SEM VALOR FISCAL" (decisão do PRODUCAO.md).
const esc = (s) => String(s ?? '').replace(/[\\()]/g, (c) => '\\' + c).replace(/[\r\n]+/g, ' ');

export function pdfDaNota(campos) {
  const ops = [];
  const txt = (x, y, tam, s, negrito = false) => ops.push(`BT /${negrito ? 'F2' : 'F1'} ${tam} Tf ${x} ${y} Td (${esc(s)}) Tj ET`);
  const linha = (x1, y1, x2, y2) => ops.push(`${x1} ${y1} m ${x2} ${y2} l S`);
  const caixa = (x, y, w, h) => ops.push(`${x} ${y} ${w} ${h} re S`);
  if (campos.marcaDagua) {   // primeiro: a marca fica ATRÁS do texto
    ops.push('q 0.86 g');
    ops.push(`BT /F2 58 Tf 0.7071 0.7071 -0.7071 0.7071 120 230 Tm (${esc(campos.marcaDagua)}) Tj ET`);
    ops.push('Q');
  }
  ops.push('0.4 w 0.2 G 0 g');
  caixa(36, 36, 523, 770);
  txt(48, 780, 15, campos.titulo || 'Nota Fiscal de Serviço Eletrônica (NFS-e)', true);
  txt(48, 762, 9, campos.subtitulo || '');
  txt(400, 780, 10, `Número ${campos.numero || '-'}`, true);
  txt(400, 766, 9, `Emitida em ${campos.emitidaEm || '-'}`);
  txt(400, 752, 9, `Competência ${campos.competencia || '-'}`);
  linha(36, 740, 559, 740);
  txt(48, 726, 8, 'Chave de acesso', true);
  txt(48, 714, 9, campos.chave || '-');
  let y = 690;
  for (const bloco of campos.blocos || []) {
    linha(36, y + 10, 559, y + 10);
    txt(48, y - 4, 10, bloco.titulo, true);
    y -= 20;
    for (const l of bloco.linhas || []) {
      txt(48, y, 9, l);
      y -= 14;
    }
    y -= 8;
  }
  txt(48, 50, 7, campos.rodape || '');
  const conteudo = Buffer.from(ops.join('\n'), 'latin1');
  const objs = [
    '<< /Type /Catalog /Pages 2 0 R >>',
    '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>',
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>',
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>',
  ];
  const partes = [Buffer.from('%PDF-1.4\n%\xe2\xe3\xcf\xd3\n', 'latin1')];
  const offsets = [];
  let tam = partes[0].length;
  const add = (b) => { partes.push(b); tam += b.length; };
  objs.forEach((o, i) => { offsets.push(tam); add(Buffer.from(`${i + 1} 0 obj\n${o}\nendobj\n`, 'latin1')); });
  offsets.push(tam);
  add(Buffer.concat([Buffer.from(`6 0 obj\n<< /Length ${conteudo.length} >>\nstream\n`, 'latin1'), conteudo, Buffer.from('\nendstream\nendobj\n', 'latin1')]));
  const xref = tam;
  let x = `xref\n0 7\n0000000000 65535 f \n`;
  for (const o of offsets) x += `${String(o).padStart(10, '0')} 00000 n \n`;
  x += `trailer\n<< /Size 7 /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`;
  add(Buffer.from(x, 'latin1'));
  return Buffer.concat(partes);
}

/** Formatação pt-BR para o PDF (sem depender do Intl do processo). */
export const brl = (v) => {
  const n = Number(v || 0);
  const [i, d] = n.toFixed(2).split('.');
  return 'R$ ' + i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ',' + d;
};
export const dataBR = (iso, comHora = false) => {
  if (!iso) return '-';
  const t = new Date(new Date(iso).getTime() - 3 * 3600 * 1000);
  const dd = String(t.getUTCDate()).padStart(2, '0');
  const mm = String(t.getUTCMonth() + 1).padStart(2, '0');
  const s = `${dd}/${mm}/${t.getUTCFullYear()}`;
  return comHora ? `${s} ${String(t.getUTCHours()).padStart(2, '0')}:${String(t.getUTCMinutes()).padStart(2, '0')}` : s;
};
/** 140101 -> 14.01.01 (código de tributação nacional, como no catálogo da LC 116). */
export const codigoServicoMascara = (v) => (/^\d{6}$/.test(limpo(v)) ? `${v.slice(0, 2)}.${v.slice(2, 4)}.${v.slice(4)}` : limpo(v) || '-');
export const cnpjMascara = (v) => {
  const d = digitos(v);
  return d.length === 14 ? `${d.slice(0, 2)}.${d.slice(2, 5)}.${d.slice(5, 8)}/${d.slice(8, 12)}-${d.slice(12)}` : limpo(v);
};
