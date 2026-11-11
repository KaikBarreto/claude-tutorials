// Contas do portal do parceiro (T20): senha do portal, sessão e os links públicos. Espelho de supabase/functions/_shared/portal-session.ts
// (hash e sessão; aqui sha256 e uma assinatura de mentira: o falso não tem o segredo do servidor) e de portal-order-receipt/public-link-slug.ts
// (shortenId e buildOrderPhotosPath).
import crypto from 'node:crypto';
import { agoraMs } from './eco.mjs';

/** hash da senha, salgado com o id da linha (como o portal-set-credentials: o mesmo hash não vale em outra linha) */
export const hashSenha = (id, senha) => crypto.createHash('sha256').update(`${id}:${senha ?? ''}`).digest('hex');

const b64 = (s) => Buffer.from(s).toString('base64url');
const assina = (payload) => crypto.createHash('sha256').update(`falso:${payload}`).digest('hex');

/** sessão de 30 dias, `payload.assinatura` como a do portal-login */
export function novaSessao(entityId, entityType) {
  const payload = b64(JSON.stringify({ entityId, entityType, exp: agoraMs() + 30 * 24 * 3600 * 1000 }));
  return `${payload}.${assina(payload)}`;
}

/** verifySessionForParty: assinatura, validade e um dos ids do par */
export function sessaoValida(sessao, ids) {
  if (!sessao || !String(sessao).includes('.')) return false;
  const [payload, sig] = String(sessao).split('.');
  if (sig !== assina(payload)) return false;
  try {
    const d = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8'));
    return d.exp > agoraMs() && ids.includes(d.entityId);
  } catch {
    return false;
  }
}

const BASE62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
function b62(n) {
  let r = '';
  let v = n;
  while (v > 0n) {
    r = BASE62[Number(v % 62n)] + r;
    v /= 62n;
  }
  return r.padStart(11, '0');
}
/** uuid -> 22 letras (shortenId) */
export function encurta(uuid) {
  const c = String(uuid).replace(/-/g, '');
  return b62(BigInt('0x' + c.slice(0, 16))) + b62(BigInt('0x' + c.slice(16, 32)));
}
const slug = (t) => String(t ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
function rotulo(...partes) {
  const s = partes.map((p) => (p === null || p === undefined ? '' : slug(p))).filter(Boolean).join('-');
  if (s.length <= 48) return s;
  const cut = s.slice(0, 48);
  const i = cut.lastIndexOf('-');
  return (i > 0 ? cut.slice(0, i) : cut).replace(/-+$/, '');
}
/** /fotos/<empresa>-<compra|venda>-<nº>-<22 letras> (buildOrderPhotosPath) */
export function caminhoFotos(token, { empresa, tipo, ref }) {
  const segredo = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(String(token)) ? encurta(token) : token;
  const r = rotulo(empresa, tipo === 'sale' ? 'venda' : tipo === 'purchase' ? 'compra' : null, ref);
  return `/fotos/${r ? `${r}-${segredo}` : segredo}`;
}

/** fotos de um pedido com a URL "assinada" do storage falso (o arquivo mora em rec/mundo/storage/order-attachments/...) */
export function anexos(store, orderId, tipo) {
  const base = `http://${process.env.FAKE_HOST || '127.0.0.1'}:${process.env.FAKE_PORT || 54321}/storage/v1/object/sign/order-attachments`;
  return store.rows('order_attachments').filter((a) => a.order_id === orderId && a.order_kind === tipo)
    .sort((x, y) => String(x.created_at).localeCompare(String(y.created_at)))
    .map((a) => ({ id: a.id, fileName: a.file_name, url: `${base}/${a.storage_path}?token=falso` }));
}
