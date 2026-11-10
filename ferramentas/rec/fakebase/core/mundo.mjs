// Mundo fictício de uma série fora do núcleo do Supabase falso.
//   FAKE_MUNDO=/caminho/do/mundo node rec/fakebase/server.mjs
// A pasta do mundo tem (tudo opcional, menos schema.json):
//   mundo.json        identidade (empresa, usuário logado), endereços (env), navegador (localStorage, local do celular),
//                     defaults por tabela e textos de erro do smoke
//   defaults.json     DEFAULT de cada coluna, lido das migrations do app (o "defaults" do mundo.json vale por cima)
//   schema.json       gerado do types.ts do app (tools/gen-schema.mjs --out <mundo>/schema.json)
//   seeds/ seeds-extra/ handlers/{rpc,functions,ext,views}/ hooks/ storage/
// Sem FAKE_MUNDO vale o mundo que mora dentro de rec/fakebase (o da Dominex, como sempre foi): nada muda.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
export const FAKEBASE_DIR = path.resolve(here, '..');
export const MUNDO_DIR = process.env.FAKE_MUNDO ? path.resolve(process.env.FAKE_MUNDO) : null;
if (MUNDO_DIR && !fs.existsSync(path.join(MUNDO_DIR, 'schema.json'))) {
  throw new Error(`FAKE_MUNDO=${MUNDO_DIR} sem schema.json (gere com tools/gen-schema.mjs --out ${MUNDO_DIR}/schema.json)`);
}

/** Caminho de um item do mundo: dentro do FAKE_MUNDO quando ligado, senão dentro de rec/fakebase. */
export const doMundo = (rel) => path.join(MUNDO_DIR || FAKEBASE_DIR, rel);

function lerMundo() {
  if (!MUNDO_DIR) return {};
  const ler = (n) => (fs.existsSync(path.join(MUNDO_DIR, n)) ? JSON.parse(fs.readFileSync(path.join(MUNDO_DIR, n), 'utf8')) : {});
  const m = ler('mundo.json');
  // defaults por tabela: os das migrations (defaults.json) e, por cima, os escritos à mão no mundo.json
  const d = ler('defaults.json');
  delete d._doc;
  for (const [t, cols] of Object.entries(m.defaults || {})) d[t] = { ...(d[t] || {}), ...cols };
  m.defaults = d;
  return m;
}
/** Conteúdo do mundo.json ({} sem FAKE_MUNDO). */
export const mundo = lerMundo();
// relógio do mundo: "env.fakeClock": "anda" faz o FAKE_NOW correr (ver core/util.mjs now())
if (!process.env.FAKE_CLOCK && mundo.env?.fakeClock) process.env.FAKE_CLOCK = mundo.env.fakeClock;
