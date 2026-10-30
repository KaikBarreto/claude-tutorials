#!/usr/bin/env node
// Gera rec/fakebase/schema.json a partir de app/src/integrations/supabase/types.ts.
//
// O schema alimenta o Supabase falso com o que o PostgREST real sabe do banco:
//   - colunas de cada tabela/view (para `select=*` devolver todas, com null onde vazio);
//   - Relationships (FKs) -> é com elas que os embeds `cliente:customers(name)` são resolvidos;
//   - assinatura das RPCs (para devolver o "vazio" certo quando a RPC ainda não tem handler);
//   - enums.
//
// Uso:  node rec/fakebase/tools/gen-schema.mjs [caminho/do/types.ts]
// Rode de novo quando copiar uma versão nova do app para app/.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const REC = path.resolve(here, '../..');
const APP = path.resolve(REC, '../app');
const typesPath = process.argv[2] || path.join(APP, 'src/integrations/supabase/types.ts');
const outPath = path.join(here, '../schema.json');

const require = createRequire(import.meta.url);
const ts = require(path.join(APP, 'node_modules/typescript'));

const text = fs.readFileSync(typesPath, 'utf8');
const sf = ts.createSourceFile('types.ts', text, ts.ScriptTarget.Latest, true);

const nameOf = (n) => (n.name.kind === ts.SyntaxKind.Identifier ? n.name.text : n.name.text ?? n.name.getText(sf).replace(/^["']|["']$/g, ''));
const members = (typeNode) => (typeNode && ts.isTypeLiteralNode(typeNode) ? typeNode.members.filter(ts.isPropertySignature) : []);
const member = (typeNode, name) => members(typeNode).find((m) => nameOf(m) === name);
const T = (node) => (node ? node.getText(sf) : '');

const db = sf.statements.find((s) => ts.isTypeAliasDeclaration(s) && s.name.text === 'Database');
if (!db) throw new Error('type Database nao encontrado em ' + typesPath);
const pub = member(db.type, 'public')?.type;
if (!pub) throw new Error('Database.public nao encontrado');

/** Classifica o tipo TS de uma coluna. */
function classify(typeText) {
  let t = typeText.replace(/\|\s*null/g, '').replace(/null\s*\|/g, '').trim();
  if (/^Json$/.test(t)) return 'json';
  if (/\[\]$/.test(t)) return 'array';
  if (/^Database\["public"\]\["Enums"\]\["(\w+)"\]$/.test(t)) return 'enum:' + t.match(/\["(\w+)"\]$/)[1];
  if (t === 'string') return 'string';
  if (t === 'number') return 'number';
  if (t === 'boolean') return 'boolean';
  if (/^"/.test(t)) return 'string';
  return 'unknown';
}

function literalValue(node) {
  if (!node) return undefined;
  if (ts.isLiteralTypeNode(node)) {
    const l = node.literal;
    if (l.kind === ts.SyntaxKind.TrueKeyword) return true;
    if (l.kind === ts.SyntaxKind.FalseKeyword) return false;
    if (l.kind === ts.SyntaxKind.NullKeyword) return null;
    if (ts.isStringLiteral(l)) return l.text;
    if (ts.isNumericLiteral(l)) return Number(l.text);
  }
  if (ts.isTupleTypeNode(node)) return node.elements.map(literalValue);
  if (ts.isArrayTypeNode(node)) return [];
  if (node.kind === ts.SyntaxKind.BooleanKeyword) return 'boolean';
  return T(node);
}

function readRelationships(relNode) {
  const out = [];
  if (!relNode || !ts.isTupleTypeNode(relNode)) return out;
  for (const el of relNode.elements) {
    const lit = ts.isTypeLiteralNode(el) ? el : null;
    if (!lit) continue;
    const g = (k) => literalValue(member(lit, k)?.type);
    out.push({
      fk: g('foreignKeyName'),
      cols: g('columns'),
      to: g('referencedRelation'),
      toCols: g('referencedColumns'),
      one: g('isOneToOne') === true,
    });
  }
  return out;
}

function readRelation(entryNode) {
  const rowNode = member(entryNode, 'Row')?.type;
  const insNode = member(entryNode, 'Insert')?.type;
  const columns = {};
  for (const m of members(rowNode)) {
    const col = nameOf(m);
    const tt = T(m.type);
    columns[col] = { t: classify(tt), n: /\|\s*null|null\s*\|/.test(tt) };
  }
  const insertMembers = members(insNode);
  for (const m of insertMembers) {
    const col = nameOf(m);
    if (columns[col]) columns[col].o = !!m.questionToken && !/\bnull\b/.test(T(m.type)) ? 1 : 0; // opcional no insert e nao-nula = tem DEFAULT no banco
  }
  const relationships = readRelationships(member(entryNode, 'Relationships')?.type);
  return { columns, relationships };
}

const tables = {};
for (const m of members(member(pub, 'Tables')?.type)) tables[nameOf(m)] = readRelation(m.type);

const views = {};
for (const m of members(member(pub, 'Views')?.type)) views[nameOf(m)] = readRelation(m.type);

function classifyReturns(typeText) {
  const t = typeText.trim();
  if (/\[\]$/.test(t)) return 'array';
  if (/^Json$/.test(t)) return 'json';
  if (/^(undefined|void)$/.test(t)) return 'void';
  if (t === 'boolean') return 'boolean';
  if (t === 'number') return 'number';
  if (t === 'string') return 'string';
  if (/^\{/.test(t)) return 'object';
  if (/^Database\["public"\]\["Tables"\]/.test(t)) return t.endsWith('[]') ? 'array' : 'object';
  return 'unknown';
}

const functions = {};
for (const m of members(member(pub, 'Functions')?.type)) {
  const name = nameOf(m);
  const variants = ts.isUnionTypeNode(m.type) ? m.type.types : [m.type];
  const args = new Set();
  let returns = 'unknown';
  let returnsText = '';
  for (const v of variants) {
    for (const a of members(member(v, 'Args')?.type)) args.add(nameOf(a));
    const r = member(v, 'Returns')?.type;
    if (r) {
      returnsText = T(r).replace(/\s+/g, ' ').slice(0, 160);
      returns = classifyReturns(T(r).replace(/\s+/g, ' '));
    }
  }
  functions[name] = { args: [...args], returns, returnsText };
}

const enums = {};
for (const m of members(member(pub, 'Enums')?.type)) {
  const node = m.type;
  if (ts.isUnionTypeNode(node)) enums[nameOf(m)] = node.types.map(literalValue);
  else enums[nameOf(m)] = [literalValue(node)];
}

const out = {
  _geradoDe: 'app/src/integrations/supabase/types.ts (rec/fakebase/tools/gen-schema.mjs)',
  tables,
  views,
  functions,
  enums,
};

// Uma linha por tabela: diff legivel e arquivo compacto.
const lines = ['{'];
lines.push(`"_geradoDe": ${JSON.stringify(out._geradoDe)},`);
for (const key of ['tables', 'views', 'functions', 'enums']) {
  const entries = Object.entries(out[key]);
  lines.push(`"${key}": {`);
  entries.forEach(([k, v], i) => lines.push(`${JSON.stringify(k)}: ${JSON.stringify(v)}${i < entries.length - 1 ? ',' : ''}`));
  lines.push(`}${key === 'enums' ? '' : ','}`);
}
lines.push('}');
fs.writeFileSync(outPath, lines.join('\n') + '\n');

console.log(
  `schema.json: ${Object.keys(tables).length} tabelas, ${Object.keys(views).length} views, ` +
    `${Object.keys(functions).length} rpcs, ${Object.keys(enums).length} enums -> ${path.relative(process.cwd(), outPath)}`,
);
