#!/usr/bin/env node
// Servidor estatico minimo para o build de producao do app (app/dist), com fallback de SPA para index.html.
//   node rec/recorder/serve-dist.mjs <pasta-dist> <porta>
// Por que nao o vite dev: no dev cada rota carrega centenas de modulos soltos (segundos de tela vazia com a
// captura ocupando a CPU). O build de producao se comporta como o sistema real: 1 a 3 arquivos por rota.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(process.argv[2] || 'dist');
const port = Number(process.argv[3] || 8080);
const host = process.env.HOST || '127.0.0.1';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif',
  '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.otf': 'font/otf',
  '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml', '.pdf': 'application/pdf', '.mp4': 'video/mp4',
  '.webmanifest': 'application/manifest+json', '.map': 'application/json', '.wasm': 'application/wasm',
};

function safe(p) {
  const full = path.join(root, decodeURIComponent(p));
  return full.startsWith(root) ? full : null;
}

const server = http.createServer((req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    let file = safe(url.pathname);
    if (file && fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    let spa = false;
    if (!file || !fs.existsSync(file)) {
      // arquivo com extensao que nao existe = 404 de verdade; rota do app = shell da SPA
      if (path.extname(url.pathname) && !url.pathname.endsWith('.html')) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        return res.end('not found');
      }
      file = path.join(root, 'index.html');
      spa = true;
    }
    const ext = path.extname(file).toLowerCase();
    const body = fs.readFileSync(file);
    const hashed = /\/assets\//.test(url.pathname) && !spa;
    res.writeHead(200, {
      'Content-Type': MIME[ext] || 'application/octet-stream',
      'Content-Length': body.length,
      'Cache-Control': hashed ? 'public, max-age=31536000, immutable' : 'no-cache',
    });
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch (e) {
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end(String(e?.message || e));
  }
});

server.listen(port, host, () => console.log(`app (build) em http://${host}:${port}  <- ${root}`));
const stop = () => server.close(() => process.exit(0));
process.on('SIGTERM', stop);
process.on('SIGINT', stop);
