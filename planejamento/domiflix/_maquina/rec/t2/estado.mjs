#!/usr/bin/env node
// Imprime o que o robô deixou no Supabase falso do T2 (FAKE_URL): usuários, papéis, permissões e cargos, em nomes legíveis.
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54324';
const get = async (t) => (await fetch(`${FAKE}/__dev/state?table=${encodeURIComponent(t)}`)).json().catch(() => []);
const [profiles, roles, perms, presets, employees] = await Promise.all(['profiles', 'user_roles', 'user_permissions', 'permission_presets', 'employees'].map(get));
const P = new Map((presets || []).map((p) => [p.id, p]));
const R = new Map();
for (const r of roles || []) R.set(r.user_id, [...(R.get(r.user_id) || []), r.role]);
const U = new Map((perms || []).map((p) => [p.user_id, p]));
console.log(`cargos (${(presets || []).length}):`, (presets || []).map((p) => `${p.name} [${p.permissions.length}] "${p.description}"`).join(' | ') || '(nenhum)');
console.log(`usuários (${(profiles || []).length}, ativos ${(profiles || []).filter((p) => p.is_active).length}):`);
for (const p of profiles || []) {
  const u = U.get(p.user_id);
  console.log(`  ${p.full_name} | ${p.email} | ${p.phone} | ativo=${p.is_active} | papel=${(R.get(p.user_id) || ['-']).join('+')} | cargo=${u?.preset_id ? P.get(u.preset_id)?.name : '-'} | ${u ? (u.permissions.includes('*') ? '*' : u.permissions.length + ' perms') : 'sem permissões'} | termos=${p.terms_accepted_at ? 'sim' : 'não'}`);
}
console.log(`funcionários: ${(employees || []).length}`);
