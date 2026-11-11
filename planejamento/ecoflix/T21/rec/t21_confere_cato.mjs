#!/usr/bin/env node
// T21 · confere os números das respostas simuladas do Cato (rec/mundo/lib/cato_respostas.json, R1 a R9) com o Supabase falso no
// estado de partida da aula (o fim da T15 + t21/inicio), pelos mesmos filtros das ferramentas do Cato (tools.ts da 1.59.154):
// resumo_financeiro = get_financial_dre_summary (regime de caixa), saldos_parceiros = balances, estoque_atual = Posição de Estoque,
// resumo_bancario = bank_accounts.balance + lançamentos com type ≠ transfer, caixa = cash_register, compras_vendas_mensais e
// top_parceiros = as RPCs. Só leitura, mas RESETA a instância (como uma gravação): não rode junto de uma gravação da T21.
// Uso: FAKE_URL=http://127.0.0.1:54321 TUT_SENHA=... node rec/t21/t21_confere_cato.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const U = process.env.FAKE_URL || 'http://127.0.0.1:54321';
const ANON = JSON.parse(fs.readFileSync(path.join(HERE, '../mundo/mundo.json'), 'utf8')).env.anonKey;
const R = Object.fromEntries(JSON.parse(fs.readFileSync(path.join(HERE, '../mundo/lib/cato_respostas.json'), 'utf8')).respostas.map((r) => [r.chave, r]));
const T14 = ['t14/inicio', ...[2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14].map((n) => `t14/apos-cap${String(n).padStart(2, '0')}`)];
const SEM = [...T14, 't15/inicio', 't15/apos-cap01', 't15/apos-cap02', 't15/apos-cap10', 't21/inicio'];
const brl = (v) => `R$ ${Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const r2 = (v) => Math.round(v * 100) / 100;
let falhas = 0;
const tem = (k, valor) => {
  const ok = JSON.stringify(R[k].payload).includes(valor);
  if (!ok) falhas++;
  console.log(`${ok ? 'OK       ' : 'DIFERENTE'} ${k}: ${valor}`);
};
const j = (r) => r.json();
await fetch(`${U}/__dev/reset`, { method: 'POST' });
const s = await fetch(`${U}/__dev/seed`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ files: SEM }) }).then(j);
if (!s.ok) throw new Error('semente: ' + JSON.stringify(s));
const tk = (await fetch(`${U}/auth/v1/token?grant_type=password`, { method: 'POST', headers: { apikey: ANON, 'content-type': 'application/json' }, body: JSON.stringify({ email: 'rafael@reciclavalemetais.example', password: process.env.TUT_SENHA || 'x' }) }).then(j)).access_token;
const H = { apikey: ANON, authorization: `Bearer ${tk}`, 'content-type': 'application/json' };
const rpc = (n, a) => fetch(`${U}/rest/v1/rpc/${n}`, { method: 'POST', headers: H, body: JSON.stringify(a) }).then(j);
const tab = (t) => fetch(`${U}/__dev/state?table=${t}`).then(j);

// R1
const d = await rpc('get_financial_dre_summary', { p_start_date: '2026-11-01T00:00:00-03:00', p_end_date: '2026-11-10T23:59:59.999-03:00' });
const desp = r2([...d.operatingExpenses, ...d.taxExpenses].reduce((a, c) => a + c.value, 0));
tem('R1', brl(d.totalSales)); tem('R1', brl(d.totalPurchases)); tem('R1', brl(desp)); tem('R1', brl(r2(d.totalSales - d.totalPurchases - desp + d.otherRevenues)));
tem('R1', brl(d.topClients[0].value)); tem('R1', d.topClients[0].name);
// R2
const nomes = new Map([...(await tab('customers')), ...(await tab('suppliers'))].map((p) => [p.id, p.name]));
const rec = (await tab('balances')).filter((b) => Math.abs(b.balance) >= 0.005 && ((b.entity_type !== 'supplier' && b.balance > 0) || (b.entity_type === 'supplier' && b.balance < 0)))
  .map((b) => [nomes.get(b.entity_id), Math.abs(b.balance)]).sort((a, b) => b[1] - a[1]);
tem('R2', `**${rec.length} parceiros**`); tem('R2', brl(r2(rec.reduce((a, x) => a + x[1], 0))));
for (const [n, v] of rec) tem('R2', `${n}:** ${brl(v)}`);
tem('R2', `${Math.round((rec[0][1] / rec.reduce((a, x) => a + x[1], 0)) * 100)}%`);
// R3 e R8
const est = await rpc('get_stock_balance_at_date', { p_at: '2026-11-10T23:59:59.999-03:00' });
const kg = est.reduce((a, m) => a + m.saldo, 0), val = r2(est.reduce((a, m) => a + m.saldo * m.avg_cost, 0)), proj = r2(est.reduce((a, m) => a + m.saldo * Number(m.sale_price), 0));
for (const k of ['R3', 'R8']) { tem(k, `${kg.toLocaleString('pt-BR')} kg`); tem(k, brl(val)); }
tem('R3', brl(proj));
const linhas = est.map((m) => [m.name, m.saldo, r2(m.saldo * m.avg_cost)]).sort((a, b) => b[2] - a[2]);
tem('R8', JSON.stringify(linhas));
for (const [n, q, v] of linhas.slice(0, 3)) tem('R3', `${n}:** ${q.toLocaleString('pt-BR')} kg, ${brl(v)}`);
// R4
const contas = (await tab('bank_accounts')).filter((a) => a.kind === 'bank' && !a.is_archived);
tem('R4', brl(r2(contas.reduce((a, c) => a + c.balance, 0))));
for (const c of contas) tem('R4', `${c.name}:** ${brl(c.balance)}`);
const ids = new Set(contas.map((c) => c.id));
const mov = (await tab('bank_transactions')).filter((t) => ids.has(t.bank_account_id) && t.type !== 'transfer' && t.transaction_date >= '2026-11-01' && t.transaction_date <= '2026-11-10');
tem('R4', brl(r2(mov.filter((t) => t.amount >= 0).reduce((a, t) => a + t.amount, 0))));
tem('R4', brl(r2(-mov.filter((t) => t.amount < 0).reduce((a, t) => a + t.amount, 0))));
// R5
const cx = await tab('cash_register');
const abertos = cx.filter((c) => c.status === 'open' || String(c.opened_at).slice(0, 10) === '2026-11-10');
console.log(`${abertos.length ? 'DIFERENTE' : 'OK       '} R5: nenhum caixa aberto ou de hoje (${abertos.length})`); if (abertos.length) falhas++;
for (const n of [83, 84]) tem('R5', brl(cx.find((c) => c.register_number === n).closing_balance));
// R6 e R7
for (const m of await rpc('get_monthly_purchases_sales', { p_reference_date: '2026-11-10', p_months: 3 })) { tem('R6', brl(m.purchases)); tem('R6', brl(m.sales)); }
const top = await rpc('get_top_partners', { p_kind: 'venda', p_start_date: '2026-10-01T00:00:00-03:00', p_end_date: '2026-10-31T23:59:59.999-03:00', p_limit: 5 });
for (const p of top.resultados.slice(0, 3)) tem('R7', `${p.parceiro}:** ${brl(p.valor)}`);
tem('R7', `${Math.round(top.resultados[0].percentual)}%`);
await fetch(`${U}/__dev/reset`, { method: 'POST' });
console.log(falhas ? `${falhas} número(s) DIFERENTE(S)` : 'todos os números das respostas batem com o Supabase falso');
process.exit(falhas ? 1 : 0);
