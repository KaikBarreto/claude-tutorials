#!/usr/bin/env node
// Autoteste do Supabase falso, usando o MESMO supabase-js que o app usa (app/node_modules).
// Sobe o servidor numa porta propria com seeds minimos, roda as verificacoes e encerra o filho pelo PID.
//   node rec/fakebase/tools/selftest.mjs
import { spawn } from 'node:child_process';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const REC = path.resolve(here, '../..');
const APP = path.resolve(REC, '../app');
const require = createRequire(path.join(APP, 'package.json'));
const { createClient } = require('@supabase/supabase-js');

const PORT = 54399;
const URL_ = `http://127.0.0.1:${PORT}`;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'fakebase-selftest-'));
const seeds = path.join(tmp, 'seeds');
fs.mkdirSync(seeds);
fs.writeFileSync(
  path.join(seeds, 'mini.json'),
  JSON.stringify({
    companies: [{ id: '@id:co', name: 'Ártica Climatização' }],
    profiles: [{ id: '@id:p1', user_id: '@id:user.camila', company_id: '@id:co', full_name: 'Camila Duarte', email: 'camila.duarte@exemplo.com.br' }],
    customers: [
      { id: '@id:c1', company_id: '@id:co', name: 'Padaria Bom Grão', customer_type: 'pj', city: 'Niterói', created_at: '@now-5d' },
      { id: '@id:c2', company_id: '@id:co', name: 'Hotel Mirante do Mar', customer_type: 'pj', city: 'Niterói', created_at: '@now-3d' },
      { id: '@id:c3', company_id: '@id:co', name: 'Mariana Lopes', customer_type: 'pf', city: 'Niterói', notes: null },
      { id: '@id:c4', company_id: '@id:co', name: 'Roberto Nunes', customer_type: 'pf', city: 'Rio de Janeiro', is_deleted: true },
    ],
    equipment: [
      { id: '@id:e1', company_id: '@id:co', customer_id: '@id:c1', name: 'Split Hi-Wall 12.000 BTU' },
      { id: '@id:e2', company_id: '@id:co', customer_id: '@id:c1', name: 'Split Hi-Wall 18.000 BTU' },
      { id: '@id:e3', company_id: '@id:co', customer_id: '@id:c2', name: 'Cassete 36.000 BTU' },
    ],
  }),
);

const child = spawn(process.execPath, [path.join(REC, 'fakebase/server.mjs')], {
  env: { ...process.env, FAKE_PORT: String(PORT), FAKE_SEEDS_DIR: seeds, FAKE_UNKNOWN_LOG: path.join(tmp, 'desconhecidos.log'), FAKE_VERBOSE: '0' },
  stdio: ['ignore', 'pipe', 'inherit'],
});
let ready;
const up = new Promise((r) => (ready = r));
child.stdout.on('data', (b) => {
  if (String(b).includes('fakebase pronto')) ready();
});
await Promise.race([up, new Promise((_, rej) => setTimeout(() => rej(new Error('servidor nao subiu')), 8000))]);

let passed = 0;
const results = [];
async function t(name, fn) {
  try {
    await fn();
    passed++;
    results.push(`ok   ${name}`);
  } catch (e) {
    results.push(`FAIL ${name}\n     ${e.message.split('\n').join('\n     ')}`);
    process.exitCode = 1;
  }
}

const sb = createClient(URL_, 'chave-falsa', { auth: { persistSession: false, autoRefreshToken: false } });

await t('select * com todas as colunas do schema', async () => {
  const { data, error } = await sb.from('customers').select('*').eq('is_deleted', false).order('name');
  assert.equal(error, null);
  assert.deepEqual(data.map((c) => c.name), ['Hotel Mirante do Mar', 'Mariana Lopes', 'Padaria Bom Grão']);
  assert.ok('whatsapp_notifications_enabled' in data[0] && 'public_short_code' in data[0]);
  assert.equal(data[0].is_service_customer, true); // default do banco
});

await t('filtros eq/neq/in/ilike/is/not/or/gt', async () => {
  const q = (b) => b.then(({ data, error }) => (assert.equal(error, null), data.map((c) => c.name).sort()));
  assert.deepEqual(await q(sb.from('customers').select('name').eq('customer_type', 'pj')), ['Hotel Mirante do Mar', 'Padaria Bom Grão']);
  assert.deepEqual(await q(sb.from('customers').select('name').neq('customer_type', 'pj').eq('is_deleted', false)), ['Mariana Lopes']);
  assert.deepEqual(await q(sb.from('customers').select('name').in('name', ['Mariana Lopes', 'Padaria Bom Grão'])), ['Mariana Lopes', 'Padaria Bom Grão']);
  assert.deepEqual(await q(sb.from('customers').select('name').ilike('name', '%padaria%')), ['Padaria Bom Grão']);
  assert.deepEqual(await q(sb.from('customers').select('name').is('notes', null).eq('is_deleted', false)), ['Hotel Mirante do Mar', 'Mariana Lopes', 'Padaria Bom Grão']);
  assert.deepEqual(await q(sb.from('customers').select('name').not('city', 'eq', 'Niterói')), ['Roberto Nunes']);
  assert.deepEqual(await q(sb.from('customers').select('name').or('name.ilike.%mar%,city.eq.Rio de Janeiro')), ['Hotel Mirante do Mar', 'Mariana Lopes', 'Roberto Nunes']);
  assert.deepEqual(await q(sb.from('customers').select('name').eq('customer_type', 'pj').gt('created_at', new Date(Date.now() - 4 * 86400000).toISOString()).not('created_at', 'is', null)), ['Hotel Mirante do Mar']);
});

await t('count exact, limit/offset/range e head', async () => {
  const r1 = await sb.from('customers').select('*', { count: 'exact' }).eq('is_deleted', false).order('name').range(0, 1);
  assert.equal(r1.error, null);
  assert.equal(r1.count, 3);
  assert.equal(r1.data.length, 2);
  const r2 = await sb.from('customers').select('*', { count: 'exact', head: true }).eq('customer_type', 'pj');
  assert.equal(r2.error, null);
  assert.equal(r2.count, 2);
  assert.equal(r2.data, null);
  const r3 = await sb.from('customers').select('name').order('name', { ascending: false }).limit(1);
  assert.equal(r3.data[0].name, 'Roberto Nunes');
});

await t('single / maybeSingle', async () => {
  const a = await sb.from('customers').select('name').eq('name', 'Mariana Lopes').single();
  assert.equal(a.error, null);
  assert.equal(a.data.name, 'Mariana Lopes');
  const b = await sb.from('customers').select('name').eq('name', 'Nao existe').single();
  assert.equal(b.error?.code, 'PGRST116');
  const c = await sb.from('customers').select('name').eq('name', 'Nao existe').maybeSingle();
  assert.equal(c.error, null);
  assert.equal(c.data, null);
  const d = await sb.from('customers').select('name').eq('customer_type', 'pj').maybeSingle();
  assert.equal(d.error?.code, 'PGRST116');
});

await t('embeds: muitos-para-um, um-para-muitos, alias, !inner, count', async () => {
  const a = await sb.from('equipment').select('name, cliente:customers(name)').eq('name', 'Cassete 36.000 BTU').single();
  assert.equal(a.error, null);
  assert.deepEqual(a.data, { name: 'Cassete 36.000 BTU', cliente: { name: 'Hotel Mirante do Mar' } });
  const b = await sb.from('customers').select('name, equipment(name)').eq('name', 'Padaria Bom Grão').single();
  assert.equal(b.data.equipment.length, 2);
  const c = await sb.from('customers').select('name, equipment!inner(name)').order('name');
  assert.deepEqual(c.data.map((x) => x.name), ['Hotel Mirante do Mar', 'Padaria Bom Grão']);
  const d = await sb.from('customers').select('name, equipment(count)').eq('name', 'Padaria Bom Grão').single();
  assert.deepEqual(d.data.equipment, [{ count: 2 }]);
  const e = await sb.from('customers').select('name, equipment!inner(name)').eq('equipment.name', 'Cassete 36.000 BTU');
  assert.deepEqual(e.data.map((x) => x.name), ['Hotel Mirante do Mar']);
  const f = await sb.from('customers').select('name, equipment(name)').eq('name', 'Padaria Bom Grão').order('name', { referencedTable: 'equipment', ascending: false }).single();
  assert.deepEqual(f.data.equipment.map((x) => x.name), ['Split Hi-Wall 18.000 BTU', 'Split Hi-Wall 12.000 BTU']);
});

await t('insert + select().single(), defaults e company_id', async () => {
  const { data, error } = await sb
    .from('customers')
    .insert({ name: 'Cliente Novo Ltda', customer_type: 'pj', company_id: '00000000-0000-0000-0000-000000000001' })
    .select()
    .single();
  assert.equal(error, null);
  assert.ok(data.id && data.created_at && data.public_short_code);
  assert.equal(data.is_deleted, false);
  const again = await sb.from('customers').select('name').eq('id', data.id).single();
  assert.equal(again.data.name, 'Cliente Novo Ltda');
});

await t('insert em lote, upsert (on_conflict) e update/delete com representation', async () => {
  const ins = await sb.from('equipment').insert([{ name: 'Piso-teto 48.000 BTU', customer_id: null }, { name: 'Split 9.000 BTU' }]).select('name');
  assert.equal(ins.data.length, 2);
  const row = ins.data[0];
  const e1 = (await sb.from('equipment').select('id').eq('name', 'Piso-teto 48.000 BTU').single()).data;
  const up = await sb.from('equipment').upsert({ id: e1.id, name: 'Piso-teto 60.000 BTU' }, { onConflict: 'id' }).select('name');
  assert.equal(up.data[0].name, 'Piso-teto 60.000 BTU');
  assert.equal((await sb.from('equipment').select('id', { count: 'exact', head: true })).count, 5);
  const upd = await sb.from('equipment').update({ name: 'Split 9.000 BTU Inverter' }).eq('name', 'Split 9.000 BTU').select();
  assert.equal(upd.data.length, 1);
  assert.ok(upd.data[0].updated_at);
  const del = await sb.from('equipment').delete().in('name', ['Piso-teto 60.000 BTU', 'Split 9.000 BTU Inverter']).select('name');
  assert.equal(del.data.length, 2);
  assert.equal((await sb.from('equipment').select('id', { count: 'exact', head: true })).count, 3);
  void row;
});

await t('tabela desconhecida: vazio e registro no log', async () => {
  const { data, error } = await sb.from('tabela_que_nao_existe').select('*');
  assert.equal(error, null);
  assert.deepEqual(data, []);
  const log = fs.readFileSync(path.join(tmp, 'desconhecidos.log'), 'utf8');
  assert.match(log, /TABELA_DESCONHECIDA\ttabela_que_nao_existe/);
});

await t('rpc sem handler: vazio do tipo certo + log', async () => {
  const a = await sb.rpc('get_user_company_id');
  assert.equal(a.error, null);
  const log = fs.readFileSync(path.join(tmp, 'desconhecidos.log'), 'utf8');
  assert.match(log, /RPC_SEM_HANDLER\tget_user_company_id/);
});

await t('auth: login, user, refresh, logout', async () => {
  const { data, error } = await sb.auth.signInWithPassword({ email: 'camila.duarte@exemplo.com.br', password: 'qualquer' });
  assert.equal(error, null);
  assert.equal(data.user.email, 'camila.duarte@exemplo.com.br');
  const u = await sb.auth.getUser();
  assert.equal(u.error, null);
  assert.equal(u.data.user.id, data.user.id);
  const r = await sb.auth.refreshSession();
  assert.equal(r.error, null);
  assert.ok(r.data.session.access_token);
  const bad = await sb.auth.signInWithPassword({ email: 'ninguem@exemplo.com.br', password: 'x' });
  assert.ok(bad.error);
  assert.equal((await sb.auth.signOut({ scope: 'local' })).error, null);
});

await t('storage: upload, url publica, url assinada, list, remove, placeholder', async () => {
  const body = new Blob([Buffer.from('conteudo-de-teste')], { type: 'text/plain' });
  const up = await sb.storage.from('company-logos').upload('empresa/teste.txt', body, { upsert: true, contentType: 'text/plain' });
  assert.equal(up.error, null, JSON.stringify(up.error));
  const pub = sb.storage.from('company-logos').getPublicUrl('empresa/teste.txt').data.publicUrl;
  assert.equal(await (await fetch(pub)).text(), 'conteudo-de-teste');
  const signed = await sb.storage.from('company-logos').createSignedUrl('empresa/teste.txt', 60);
  assert.equal(signed.error, null);
  assert.equal(await (await fetch(signed.data.signedUrl)).text(), 'conteudo-de-teste');
  const ls = await sb.storage.from('company-logos').list('empresa');
  assert.ok(ls.data.some((f) => f.name === 'teste.txt'));
  const img = await fetch(sb.storage.from('customer-photos').getPublicUrl('x/nao-existe.png').data.publicUrl);
  assert.equal(img.status, 200);
  assert.match(img.headers.get('content-type'), /svg/);
  const rm = await sb.storage.from('company-logos').remove(['empresa/teste.txt']);
  assert.equal(rm.error, null);
});

await t('functions.invoke desconhecida: {} e log', async () => {
  const { data, error } = await sb.functions.invoke('funcao-que-nao-existe', { body: { a: 1 } });
  assert.equal(error, null);
  assert.deepEqual(data, {});
});

await t('realtime: canal chega em SUBSCRIBED sem erro', async () => {
  const status = await new Promise((resolve) => {
    const ch = sb
      .channel('teste')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'customers' }, () => {})
      .subscribe((s, err) => {
        if (s === 'SUBSCRIBED' || s === 'CHANNEL_ERROR' || s === 'TIMED_OUT') resolve(err ? `${s}: ${err.message}` : s);
      });
    setTimeout(() => resolve('timeout do teste'), 6000);
    void ch;
  });
  assert.equal(status, 'SUBSCRIBED');
  await sb.removeAllChannels();
});

child.kill('SIGTERM');
await new Promise((r) => child.once('exit', r));
fs.rmSync(tmp, { recursive: true, force: true });
console.log(results.join('\n'));
console.log(`\n${passed}/${results.length} verificacoes passaram`);
process.exit(process.exitCode || 0);
