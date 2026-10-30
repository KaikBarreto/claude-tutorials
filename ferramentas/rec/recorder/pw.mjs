// Carrega o Playwright ja instalado na maquina (NAO rodar `playwright install`: o Chromium ja esta em
// PLAYWRIGHT_BROWSERS_PATH). ESM nao honra NODE_PATH, entao resolvemos via createRequire.
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);

const candidates = [
  process.env.PLAYWRIGHT_MODULE,
  'playwright',
  '/opt/npm-tools/node_modules/playwright',
  '/opt/node22/lib/node_modules/playwright',
  path.resolve(here, '../../app/node_modules/playwright'),
].filter(Boolean);

let pw = null;
const tried = [];
for (const c of candidates) {
  try {
    pw = require(c);
    break;
  } catch (e) {
    tried.push(c);
  }
}
if (!pw) throw new Error('Playwright nao encontrado. Tentei: ' + tried.join(', ') + '. Defina PLAYWRIGHT_MODULE=/caminho/para/playwright');

export const { chromium } = pw;
export default pw;
