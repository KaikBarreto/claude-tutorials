// /auth/v1 — GoTrue falso: login por senha (qualquer senha), sessao, refresh, user, logout.
import { config } from '../core/config.mjs';
import { store } from '../core/store.mjs';
import { unknown } from '../core/log.mjs';
import { readJson, sendJson, send, signJwt, decodeJwt, userFromRequest } from './common.mjs';

const TEN_YEARS = 10 * 365 * 86400;

/** Perfis que podem logar: a linha de `profiles` cujo e-mail bate (Camila e a padrao). */
function findUserByEmail(email) {
  const e = String(email || '').trim().toLowerCase();
  const prof = store.rows('profiles').find((p) => String(p.email || '').toLowerCase() === e);
  if (prof) return userFromProfile(prof);
  if (e === config.userEmail.toLowerCase()) return defaultUser();
  return null;
}

function findUserById(id) {
  const prof = store.rows('profiles').find((p) => p.user_id === id);
  if (prof) return userFromProfile(prof);
  if (id === config.userId) return defaultUser();
  return null;
}

function defaultUser() {
  return { id: config.userId, email: config.userEmail, name: config.userName };
}

function userFromProfile(p) {
  return { id: p.user_id, email: p.email || config.userEmail, name: p.full_name || config.userName };
}

export function toAuthUser(u) {
  const created = '2025-03-10T12:00:00.000Z';
  return {
    id: u.id,
    aud: 'authenticated',
    role: 'authenticated',
    email: u.email,
    email_confirmed_at: created,
    phone: '',
    confirmed_at: created,
    last_sign_in_at: new Date().toISOString(),
    app_metadata: { provider: 'email', providers: ['email'] },
    user_metadata: { full_name: u.name, email_verified: true },
    identities: [
      {
        identity_id: u.id,
        id: u.id,
        user_id: u.id,
        identity_data: { email: u.email, sub: u.id, email_verified: true },
        provider: 'email',
        last_sign_in_at: created,
        created_at: created,
        updated_at: created,
        email: u.email,
      },
    ],
    created_at: created,
    updated_at: new Date().toISOString(),
    is_anonymous: false,
  };
}

export function buildSession(u) {
  const nowSec = Math.floor(Date.now() / 1000);
  const exp = nowSec + TEN_YEARS;
  const user = toAuthUser(u);
  const access_token = signJwt({
    aud: 'authenticated',
    exp,
    iat: nowSec,
    iss: `http://${config.host}:${config.port}/auth/v1`,
    sub: u.id,
    email: u.email,
    phone: '',
    app_metadata: user.app_metadata,
    user_metadata: user.user_metadata,
    role: 'authenticated',
    aal: 'aal1',
    amr: [{ method: 'password', timestamp: nowSec }],
    session_id: u.id,
    is_anonymous: false,
  });
  return {
    access_token,
    token_type: 'bearer',
    expires_in: TEN_YEARS,
    expires_at: exp,
    refresh_token: `rt.${u.id}.${nowSec}`,
    user,
  };
}

/** Chave do localStorage onde o supabase-js guarda a sessao (sb-<primeiro rotulo do host>-auth-token). */
export function storageKey(supabaseUrl) {
  return `sb-${new URL(supabaseUrl).hostname.split('.')[0]}-auth-token`;
}

function authError(res, status, code, message) {
  return sendJson(res, status, { code: status, error_code: code, msg: message, error: code, error_description: message });
}

export async function handleAuth(req, res, url, ctx) {
  const route = url.pathname.replace(/^\/auth\/v1\/?/, '');
  const method = req.method;

  if (route === 'settings') {
    return sendJson(res, 200, {
      external: { email: true, phone: false, google: false },
      disable_signup: false,
      mailer_autoconfirm: true,
      phone_autoconfirm: false,
      sms_provider: '',
      saml_enabled: false,
    });
  }

  if (route === 'token' && method === 'POST') {
    const grant = url.searchParams.get('grant_type');
    const body = (await readJson(req)) || {};
    if (grant === 'password') {
      const u = findUserByEmail(body.email);
      if (!u) return authError(res, 400, 'invalid_credentials', 'Invalid login credentials');
      return sendJson(res, 200, buildSession(u));
    }
    if (grant === 'refresh_token') {
      const m = String(body.refresh_token || '').match(/^rt\.([^.]+)\./);
      const u = m ? findUserById(m[1]) : null;
      if (!u) return authError(res, 400, 'refresh_token_not_found', 'Invalid Refresh Token: Refresh Token Not Found');
      return sendJson(res, 200, buildSession(u));
    }
    return authError(res, 400, 'unsupported_grant_type', 'Unsupported grant type');
  }

  if (route === 'user') {
    const me = userFromRequest(req);
    if (!me) return authError(res, 401, 'bad_jwt', 'invalid claim: missing sub claim');
    const u = findUserById(me.id) || { id: me.id, email: me.email, name: me.email };
    if (method === 'PUT' || method === 'PATCH') {
      const body = (await readJson(req)) || {};
      const out = toAuthUser(u);
      if (body.data) out.user_metadata = { ...out.user_metadata, ...body.data };
      return sendJson(res, 200, out);
    }
    return sendJson(res, 200, toAuthUser(u));
  }

  if (route === 'logout') return send(res, 204, null);
  if (route === 'recover' || route === 'otp' || route === 'resend' || route === 'magiclink') return sendJson(res, 200, {});
  if (route === '.well-known/jwks.json' || route === 'jwks') return sendJson(res, 200, { keys: [] });

  if (route === 'factors' || route === 'mfa') return sendJson(res, 200, []);

  unknown('AUTH_SEM_HANDLER', `${method} /auth/v1/${route}`);
  return sendJson(res, 200, {});
}
