// Conhecimento do schema (gerado de types.ts): colunas, relacionamentos (FKs), RPCs, enums.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { doMundo } from './mundo.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const raw = JSON.parse(fs.readFileSync(doMundo('schema.json'), 'utf8')); // FAKE_MUNDO/schema.json ou rec/fakebase/schema.json

export const schema = raw;
export const tables = raw.tables;
export const views = raw.views;
export const functions = raw.functions;
export const enums = raw.enums;

export const isView = (name) => Object.prototype.hasOwnProperty.call(views, name);
export const isKnown = (name) => Object.prototype.hasOwnProperty.call(tables, name) || isView(name);
export const relation = (name) => tables[name] || views[name] || null;
export const columnsOf = (name) => relation(name)?.columns || {};

/** FKs que saem de `name` (a tabela guarda a coluna FK). */
export function relsFrom(name) {
  return (relation(name)?.relationships || []).map((r) => ({ ...r, from: name }));
}

let reverseCache = null;
function reverseIndex() {
  if (reverseCache) return reverseCache;
  reverseCache = {};
  for (const group of [tables, views]) {
    for (const [tname, def] of Object.entries(group)) {
      for (const r of def.relationships || []) {
        (reverseCache[r.to] ||= []).push({ ...r, from: tname });
      }
    }
  }
  return reverseCache;
}
/** FKs de OUTRAS tabelas que apontam para `name`. */
export const relsTo = (name) => reverseIndex()[name] || [];

/**
 * Resolve um embed `target` a partir de `source`, como o PostgREST faz.
 * `hints` pode trazer nome da FK, nome da coluna FK, ou 'inner'/'left' (ignorados aqui).
 * Retorna { cardinality: 'one'|'many', rel, via: 'forward'|'reverse' } ou { m2m: {...} } ou null.
 */
export function findEmbed(source, target, hints = []) {
  const hs = hints.filter((h) => h !== 'inner' && h !== 'left');
  const matchesHint = (r, side) => {
    if (!hs.length) return true;
    return hs.some((h) => r.fk === h || (side === 'forward' ? r.cols.includes(h) : r.cols.includes(h)));
  };
  const forward = relsFrom(source).filter((r) => r.to === target && matchesHint(r, 'forward'));
  const reverse = relsTo(source).filter((r) => r.from === target && matchesHint(r, 'reverse'));
  // Preferencia: forward (muitos-para-um) quando ha uma unica opcao
  if (forward.length && !reverse.length) return { cardinality: 'one', rel: forward[0], via: 'forward' };
  if (reverse.length && !forward.length) {
    const r = reverse[0];
    return { cardinality: r.one ? 'one' : 'many', rel: r, via: 'reverse' };
  }
  if (forward.length && reverse.length) {
    // Auto-referencia (ex.: parent_id) ou dupla via: sem hint, PostgREST reclama; aqui escolhemos forward.
    return { cardinality: 'one', rel: forward[0], via: 'forward' };
  }
  // muitos-para-muitos via tabela de juncao
  for (const [jname, jdef] of Object.entries(tables)) {
    const toSource = (jdef.relationships || []).find((r) => r.to === source);
    const toTarget = (jdef.relationships || []).find((r) => r.to === target);
    if (toSource && toTarget && jname !== source && jname !== target) {
      return { cardinality: 'many', via: 'm2m', junction: jname, toSource, toTarget };
    }
  }
  return null;
}

export function rpcInfo(name) {
  return functions[name] || null;
}

/** "Vazio" apropriado para uma RPC sem handler, conforme o tipo declarado em types.ts. */
export function emptyRpcResult(name) {
  const info = functions[name];
  if (!info) return null;
  switch (info.returns) {
    case 'array':
      return [];
    case 'boolean':
      return false;
    case 'number':
      return 0;
    case 'object':
      return {};
    default:
      return null;
  }
}
