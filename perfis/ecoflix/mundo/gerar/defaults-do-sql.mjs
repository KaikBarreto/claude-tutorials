#!/usr/bin/env node
// Lê os DEFAULTs das colunas nas migrations SQL do app (CREATE TABLE / ALTER TABLE ... ADD COLUMN / SET DEFAULT) e grava
// <mundo>/defaults.json: o Supabase falso preenche uma linha nova como o Postgres faria (o types.ts só diz QUE a coluna
// tem default, não o valor). Só literais (texto, número, booleano, json, array vazio, now(), current_date, uuid).
//   node gerar/defaults-do-sql.mjs <app>/supabase/migrations [--out <mundo>/defaults.json]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MUNDO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
const oi = argv.indexOf('--out');
const out = oi >= 0 ? argv.splice(oi, 2)[1] : path.join(MUNDO, 'defaults.json');
const dir = argv[0];
if (!dir || !fs.existsSync(dir)) {
  console.error('uso: node gerar/defaults-do-sql.mjs <app>/supabase/migrations [--out defaults.json]');
  process.exit(2);
}
const schema = JSON.parse(fs.readFileSync(path.join(MUNDO, 'schema.json'), 'utf8'));

// tira comentários e corpos $$...$$ (funções) para não confundir com DDL
function limpa(sql) {
  sql = sql.replace(/\$([a-zA-Z_]*)\$[\s\S]*?\$\1\$/g, "''");
  sql = sql.replace(/--[^\n]*/g, '').replace(/\/\*[\s\S]*?\*\//g, '');
  return sql;
}
// divide no nível 0 (fora de parênteses e aspas)
function divide(s, sep = ',') {
  const parts = [];
  let d = 0, q = false, cur = '';
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (q) { cur += c; if (c === "'") { if (s[i + 1] === "'") { cur += s[++i]; } else q = false; } continue; }
    if (c === "'") { q = true; cur += c; continue; }
    if (c === '(') d++;
    if (c === ')') d--;
    if (c === sep && d === 0) { parts.push(cur); cur = ''; continue; }
    cur += c;
  }
  if (cur.trim()) parts.push(cur);
  return parts;
}
const PARA = /\s+(not\s+null|null|check|references|constraint|primary\s+key|unique|generated|collate)\b/i;
function exprDefault(def) {
  const m = def.match(/\bdefault\s+([\s\S]*)$/i);
  if (!m) return undefined;
  let e = m[1];
  // corta no próximo termo da definição (fora de aspas/parênteses)
  let d = 0, q = false, end = e.length;
  for (let i = 0; i < e.length; i++) {
    const c = e[i];
    if (q) { if (c === "'") { if (e[i + 1] === "'") i++; else q = false; } continue; }
    if (c === "'") { q = true; continue; }
    if (c === '(') d++;
    if (c === ')') d--;
    if (d === 0 && PARA.test(' ' + e.slice(i)) && /\s/.test(e[i - 1] || ' ') && PARA.exec(' ' + e.slice(i))?.index === 0) { end = i; break; }
  }
  return e.slice(0, end).trim();
}
function valor(expr, tipo) {
  if (expr === undefined) return undefined;
  let e = expr.trim().replace(/^\((.*)\)$/s, '$1').trim();
  const cast = e.match(/^([\s\S]*?)::\s*([\w\s\[\]."]+)$/);
  let alvo = tipo || '';
  if (cast) { e = cast[1].trim(); alvo = cast[2].trim().toLowerCase(); }
  e = e.replace(/^\((.*)\)$/s, '$1').trim();
  if (/^(now\(\)|current_timestamp|timezone\('utc'\s*,\s*now\(\)\)|\(now\(\)\s+at\s+time\s+zone\s+'utc'\)|statement_timestamp\(\)|clock_timestamp\(\))$/i.test(e)) return '@now';
  if (/^current_date$/i.test(e) || /^\(?now\(\)\)?::date$/i.test(e)) return '@today';
  if (/^(gen_random_uuid|uuid_generate_v4)\(\)$/i.test(e)) return '@uuid';
  if (/^(true|false)$/i.test(e)) return e.toLowerCase() === 'true';
  if (/^-?\d+(\.\d+)?$/.test(e)) return Number(e);
  if (/^array\[\s*\]$/i.test(e)) return [];
  const arr = e.match(/^array\[([\s\S]*)\]$/i);
  if (arr) return divide(arr[1]).map((x) => valor(x.trim())).filter((x) => x !== undefined);
  const s = e.match(/^'((?:[^']|'')*)'$/);
  if (s) {
    const txt = s[1].replace(/''/g, "'");
    if (/json/.test(alvo)) { try { return JSON.parse(txt); } catch { return undefined; } }
    if (/\[\]$/.test(alvo) || /^\{.*\}$/.test(txt) && /\[\]|array/.test(alvo)) {
      const inner = txt.replace(/^\{|\}$/g, '');
      return inner ? inner.split(',').map((x) => x.replace(/^"|"$/g, '')) : [];
    }
    if (/^(int|bigint|smallint|numeric|real|double|decimal)/.test(alvo) && /^-?\d+(\.\d+)?$/.test(txt)) return Number(txt);
    return txt;
  }
  return undefined; // expressão (função, nextval...): fica com o padrão do núcleo
}

const defs = {}; // tabela -> coluna -> valor
const set = (t, c, v) => { (defs[t] ||= {})[c] = v; };
const drop = (t, c) => { if (defs[t]) delete defs[t][c]; };
const nome = (s) => s.replace(/"/g, '').replace(/^public\./i, '').trim();

const files = fs.readdirSync(dir).filter((f) => f.endsWith('.sql')).sort();
for (const f of files) {
  const sql = limpa(fs.readFileSync(path.join(dir, f), 'utf8'));
  // CREATE TABLE
  const reCreate = /create\s+(?:unlogged\s+)?table\s+(?:if\s+not\s+exists\s+)?((?:public\.)?"?\w+"?)\s*\(/gi;
  let m;
  while ((m = reCreate.exec(sql))) {
    const t = nome(m[1]);
    let d = 1, i = reCreate.lastIndex, q = false;
    for (; i < sql.length && d > 0; i++) {
      const c = sql[i];
      if (q) { if (c === "'") q = false; continue; }
      if (c === "'") q = true; else if (c === '(') d++; else if (c === ')') d--;
    }
    const body = sql.slice(reCreate.lastIndex, i - 1);
    for (const part of divide(body)) {
      const p = part.trim();
      if (!p || /^(constraint|primary|unique|check|foreign|exclude|like)\b/i.test(p)) continue;
      const cm = p.match(/^"?(\w+)"?\s+([\w\s\[\]."()]+?)(\s|$)/);
      if (!cm) continue;
      const v = valor(exprDefault(p), cm[2].toLowerCase());
      if (v !== undefined) set(t, cm[1], v);
    }
  }
  // ALTER TABLE
  const reAlter = /alter\s+table\s+(?:if\s+exists\s+)?(?:only\s+)?((?:public\.)?"?\w+"?)\s+([\s\S]*?);/gi;
  while ((m = reAlter.exec(sql))) {
    const t = nome(m[1]);
    for (const a of divide(m[2])) {
      const s = a.trim();
      let x;
      if ((x = s.match(/^add\s+(?:column\s+)?(?:if\s+not\s+exists\s+)?"?(\w+)"?\s+([\w\s\[\]."()]+?)(\s|$)/i)) && !/^add\s+(constraint|primary|unique|check|foreign)/i.test(s)) {
        const v = valor(exprDefault(s), x[2].toLowerCase());
        if (v !== undefined) set(t, x[1], v);
      } else if ((x = s.match(/^alter\s+(?:column\s+)?"?(\w+)"?\s+set\s+default\s+([\s\S]+)$/i))) {
        const v = valor(x[2]);
        if (v !== undefined) set(t, x[1], v); else drop(t, x[1]);
      } else if ((x = s.match(/^alter\s+(?:column\s+)?"?(\w+)"?\s+drop\s+default/i))) {
        drop(t, x[1]);
      }
    }
  }
}

// só colunas que existem no schema do app e que ele diz ter default; id/created_at/updated_at ficam com o núcleo
const final = {};
let n = 0;
for (const [t, cols] of Object.entries(defs).sort()) {
  const sc = schema.tables[t]?.columns;
  if (!sc) continue;
  for (const [c, v] of Object.entries(cols).sort()) {
    if (!sc[c] || sc[c].o !== 1 || ['id', 'created_at', 'updated_at'].includes(c)) continue;
    (final[t] ||= {})[c] = v;
    n++;
  }
}
const lines = ['{', `"_doc": ${JSON.stringify('Gerado por gerar/defaults-do-sql.mjs a partir das migrations do app: DEFAULT de cada coluna (só literais). Não editar à mão: rode de novo.')},`];
const ents = Object.entries(final);
ents.forEach(([t, cols], i) => lines.push(`${JSON.stringify(t)}: ${JSON.stringify(cols)}${i < ents.length - 1 ? ',' : ''}`));
lines.push('}');
fs.writeFileSync(out, lines.join('\n') + '\n');
console.log(`defaults.json: ${n} colunas em ${ents.length} tabelas (${files.length} migrations) -> ${out}`);
