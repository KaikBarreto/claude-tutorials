// Edge function `nfse-tax-codes` falsa (T4, aba Fiscal do tipo de servico). Mesmo contrato da real
// (app/supabase/functions/_shared/nfse-handlers/tax-codes.ts, busca no catalogo LOCAL):
//   { type: 'servico', q? } -> { items: [{ codigo, descricao, itemLc116 }], total }   (ordem de codigo, ate 400)
//   { type: 'nbs', q }      -> { items: [{ codigo, descricao }], total }              (q com >= 2 caracteres)
// Os dados NAO sao inventados: saem da propria migration do app que cria o catalogo
// (supabase/migrations/20260903182000_nfse_catalogos_tributacao_e_nbs.sql, linhas do INSERT: texto literal da LC 116).
// A posicao da migration e relativa a este arquivo ($TUT_HOME/app); se o arquivo nao existir, cai numa lista curta
// com as mesmas linhas reais (14.01 a 14.06), o bastante para a aula.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const MIGRATION = path.resolve(HERE, '../../../../app/supabase/migrations/20260903182000_nfse_catalogos_tributacao_e_nbs.sql');

const FALLBACK = [
  ['140101', '14.01', 'Lubrificação, limpeza, lustração, revisão, carga e recarga, conserto, restauração, blindagem, manutenção e conservação de máquinas, veículos, aparelhos, equipamentos, motores, elevadores ou de qualquer objeto (exceto peças e partes empregadas, que ficam sujeitas ao ICMS).'],
  ['140201', '14.02', 'Assistência técnica.'],
  ['140301', '14.03', 'Recondicionamento de motores (exceto peças e partes empregadas, que ficam sujeitas ao ICMS).'],
  ['140601', '14.06', 'Instalação e montagem de aparelhos, máquinas e equipamentos, inclusive montagem industrial, prestados ao usuário final, exclusivamente com material por ele fornecido.'],
];

let cache = null;

const unq = (s) => s.replace(/''/g, "'");
const norm = (v) => String(v ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

function load() {
  if (cache) return cache;
  let servico = [];
  let nbs = [];
  try {
    const sql = fs.readFileSync(MIGRATION, 'utf8');
    const iNbs = sql.indexOf('INSERT INTO public.nfse_codigos_nbs');
    const blocoServico = iNbs > 0 ? sql.slice(0, iNbs) : sql;
    const blocoNbs = iNbs > 0 ? sql.slice(iNbs) : '';
    for (const m of blocoServico.matchAll(/\(\s*'(\d{6})'\s*,\s*'([\d.]+)'\s*,\s*'((?:[^']|'')*)'\s*,\s*(?:true|false)\s*\)/g)) {
      servico.push({ codigo: m[1], itemLc116: m[2], descricao: unq(m[3]) });
    }
    for (const m of blocoNbs.matchAll(/\(\s*'([\d.]+)'\s*,\s*'((?:[^']|'')*)'\s*,\s*'(?:[^']|'')*'\s*,\s*(?:true|false)\s*\)/g)) {
      nbs.push({ codigo: m[1], descricao: unq(m[2]) });
    }
  } catch {
    /* sem a migration: usa a lista curta */
  }
  if (!servico.length) servico = FALLBACK.map(([codigo, itemLc116, descricao]) => ({ codigo, itemLc116, descricao }));
  servico.sort((a, b) => a.codigo.localeCompare(b.codigo));
  nbs.sort((a, b) => a.codigo.localeCompare(b.codigo));
  cache = { servico, nbs };
  return cache;
}

export default async function nfseTaxCodes(body) {
  const type = body?.type === 'nbs' ? 'nbs' : 'servico';
  const q = String(body?.q ?? '').trim();
  const limit = Math.min(Number(body?.limit) > 0 ? Math.floor(Number(body.limit)) : type === 'nbs' ? 50 : 400, type === 'nbs' ? 200 : 400);
  const { servico, nbs } = load();
  if (type === 'servico') {
    const items = (q
      ? servico.filter((r) => r.codigo.startsWith(q) || norm(r.descricao).includes(norm(q)))
      : servico
    ).slice(0, limit);
    return { items, total: items.length };
  }
  if (q.length < 2) return { items: [], total: 0 };
  const porCodigo = nbs.filter((r) => r.codigo.startsWith(q));
  const porDescricao = nbs.filter((r) => !r.codigo.startsWith(q) && norm(r.descricao).includes(norm(q)));
  const items = [...porCodigo, ...porDescricao].slice(0, limit);
  return { items, total: items.length };
}
