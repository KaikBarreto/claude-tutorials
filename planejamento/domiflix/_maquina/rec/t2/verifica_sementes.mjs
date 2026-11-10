#!/usr/bin/env node
// Confere as sementes do T2 sem subir servidor: carrega a base e os extras na memória e imprime o resumo de usuários, papéis,
// permissões e cargos (um por linha, em ordem estável). Duas formas de uso; as saídas têm de ser IGUAIS:
//   FAKE_SEEDS_DIR=<seeds-extra/t2/_base> node rec/t2/verifica_sementes.mjs t1/apos-cap13 t2/inicio t2/apos-cap09
//   node rec/t2/verifica_sementes.mjs t1/apos-cap13 t2/apos-cap10            (base padrão + delta do T2)
// (a diferença esperada: nenhuma; o T2 termina com 2 cargos e 8 usuários ativos).
import { store } from '../fakebase/core/store.mjs';

store.loadSeeds();
store.applyExtra(process.argv.slice(2));

const rows = (t) => store.rows(t);
const presets = new Map(rows('permission_presets').map((p) => [p.id, p]));
const roles = new Map();
for (const r of rows('user_roles')) roles.set(r.user_id, [...(roles.get(r.user_id) || []), r.role]);
const perms = new Map(rows('user_permissions').map((p) => [p.user_id, p]));

const linhas = [];
for (const p of rows('profiles')) {
  const perm = perms.get(p.user_id);
  const set = perm ? [...perm.permissions].sort().join(',') : '(sem linha em user_permissions)';
  linhas.push(`${p.full_name} | ${p.email} | ${p.phone} | ativo=${p.is_active} | papel=${(roles.get(p.user_id) || ['-']).join('+')} | cargo=${perm?.preset_id ? presets.get(perm.preset_id)?.name : '-'} | ${perm ? perm.permissions.length : 0} perms | ${set}`);
}
linhas.sort();
console.log(`perfis: ${rows('profiles').length}, ativos: ${rows('profiles').filter((p) => p.is_active).length}`);
console.log(linhas.join('\n'));
console.log('cargos:');
console.log([...presets.values()].map((p) => `${p.name} | ${p.description} | ${p.permissions.length} perms | ${[...p.permissions].sort().join(',')}`).sort().join('\n'));
const c = rows('companies')[0];
console.log(`empresa: ${c.name} | plano ${c.subscription_plan} | max_users ${c.max_users} | planos: ${rows('subscription_plans').map((p) => `${p.code}=${p.max_users}`).join(' ')}`);
