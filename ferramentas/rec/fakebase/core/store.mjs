// Estado em memoria: tabelas, indices, carga dos seeds JSON.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { stableId, resolveTokens, resetSeq, reiniciaRelogio } from './util.mjs';
import { applyDefaults, resetSeqs } from './defaults.mjs';
import { isKnown, columnsOf } from './schema.mjs';
import { doMundo } from './mundo.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
export const SEEDS_DIR = process.env.FAKE_SEEDS_DIR || doMundo('seeds'); // FAKE_MUNDO/seeds ou rec/fakebase/seeds
// Seeds EXTRAS (nao entram no carregamento normal): estados prontos de um tutorial, aplicados sob demanda por
// POST /__dev/seed { files: ["t3/apos-cap02", ...] } (ou pelo campo `seedExtra` do roteiro do robo). Ver rec/README.md.
export const EXTRA_DIR = process.env.FAKE_SEEDS_EXTRA_DIR || doMundo('seeds-extra');

class Table {
  constructor(name) {
    this.name = name;
    this.rows = [];
    this.version = 0;
    this.seeded = false; // recebeu linhas de seed
    this.idx = new Map(); // col -> { version, map }
  }
  touch() {
    this.version++;
  }
}

export const store = {
  tables: new Map(),
  seedFiles: [],

  /** Tabela existente ou null (nao cria). */
  peek(name) {
    return this.tables.get(name) || null;
  },
  /** Tabela, criando vazia se preciso (escritas em tabelas desconhecidas viram tabelas dinamicas). */
  table(name) {
    let t = this.tables.get(name);
    if (!t) {
      t = new Table(name);
      this.tables.set(name, t);
    }
    return t;
  },
  rows(name) {
    return this.tables.get(name)?.rows || [];
  },
  /** Indice coluna -> linhas, invalidado por versao. */
  lookup(name, col, value) {
    const t = this.tables.get(name);
    if (!t) return [];
    let ix = t.idx.get(col);
    if (!ix || ix.version !== t.version) {
      const map = new Map();
      for (const r of t.rows) {
        const k = r[col];
        if (k === null || k === undefined) continue;
        const key = String(k);
        const arr = map.get(key);
        if (arr) arr.push(r);
        else map.set(key, [r]);
      }
      ix = { version: t.version, map };
      t.idx.set(col, ix);
    }
    return ix.map.get(String(value)) || [];
  },
  insertRaw(name, row) {
    const t = this.table(name);
    t.rows.push(row);
    t.touch();
    return row;
  },
  clear() {
    this.tables.clear();
    this.seedFiles = [];
    reiniciaRelogio();
    resetSeq();
    resetSeqs();
  },

  /**
   * Aplica seeds extras (EXTRA_DIR/<nome>.json) por cima do estado atual, sem apagar nada, na ordem dada. Mesmo formato
   * dos seeds normais ({ tabela: [linhas] }, tokens @id:/@now.../@storage:), mais:
   *   { "_patch": { "tabela": [ { "match": { coluna: valor }, "set": { coluna: novoValor } } ] } }
   * que altera linhas que ja existem (ex.: o contador de identificadores do equipamento).
   */
  applyExtra(names, dir = EXTRA_DIR) {
    const done = [];
    for (const name of names) {
      const rel = String(name).replace(/\.json$/, '');
      const file = path.resolve(dir, `${rel}.json`);
      if (!file.startsWith(path.resolve(dir) + path.sep) || !fs.existsSync(file)) throw new Error(`seed extra nao encontrado: ${name}`);
      const data = JSON.parse(fs.readFileSync(file, 'utf8'));
      const groups = Array.isArray(data) ? { [path.basename(rel)]: data } : data;
      for (const [table, rows] of Object.entries(groups)) {
        if (table === '_patch' && rows && typeof rows === 'object') {
          for (const [pt, items] of Object.entries(rows)) {
            const t = this.table(pt);
            for (const it of items) {
              const match = resolveTokens(it.match || {});
              const set = resolveTokens(it.set || {});
              for (const r of t.rows) if (Object.entries(match).every(([k, v]) => String(r[k]) === String(v))) Object.assign(r, set);
            }
            t.touch();
          }
          continue;
        }
        if (table.startsWith('_') || !Array.isArray(rows)) continue;
        const t = this.table(table);
        rows.forEach((raw, i) => {
          const resolved = resolveTokens(raw);
          if (resolved.id === undefined && (columnsOf(table).id || !isKnown(table))) resolved.id = stableId(`${table}:extra:${rel}:${i}`);
          t.rows.push(applyDefaults(table, resolved));
        });
        t.seeded = true;
        t.touch();
      }
      done.push(rel);
    }
    return done;
  },

  /**
   * Carrega todos os seeds de SEEDS_DIR (recursivo, ordem alfabetica; linhas da mesma tabela se acumulam).
   * Formatos de arquivo .json:
   *   { "customers": [ {...}, {...} ], "suppliers": [ ... ] }   varias tabelas num arquivo
   *   [ {...}, {...} ]                                          o nome do arquivo e a tabela (customers.json)
   *   { "_vazias": ["admin_notices", ...] }                      tabelas que o app consulta e que ficam vazias
   *                                                              de proposito (nao entram no desconhecidos.log)
   * Valores string podem usar tokens (@id:chave, @today+3d, @now-2h ...) — ver core/util.mjs.
   */
  loadSeeds(dir = SEEDS_DIR) {
    this.clear();
    if (!fs.existsSync(dir)) return;
    const files = [];
    const walk = (d) => {
      for (const ent of fs.readdirSync(d, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
        const full = path.join(d, ent.name);
        if (ent.isDirectory()) walk(full);
        else if (ent.name.endsWith('.json')) files.push(full);
      }
    };
    walk(dir);
    for (const file of files) {
      const f = path.relative(dir, file);
      let data;
      try {
        data = JSON.parse(fs.readFileSync(file, 'utf8'));
      } catch (e) {
        console.error(`[seed] ${f}: JSON invalido: ${e.message}`);
        continue;
      }
      const base = path.basename(f).replace(/\.json$/, '');
      const groups = Array.isArray(data) ? { [base]: data } : data;
      for (const [table, rows] of Object.entries(groups)) {
        if (table === '_vazias' && Array.isArray(rows)) {
          for (const name of rows) this.table(name).seeded = true;
          continue;
        }
        if (table.startsWith('_') || !Array.isArray(rows)) continue;
        const t = this.table(table);
        rows.forEach((raw, i) => {
          const resolved = resolveTokens(raw);
          if (resolved.id === undefined && (columnsOf(table).id || !isKnown(table))) resolved.id = stableId(`${table}:${f}:${i}`);
          t.rows.push(applyDefaults(table, resolved));
        });
        t.seeded = true;
        t.touch();
      }
      this.seedFiles.push(f);
    }
  },
};
