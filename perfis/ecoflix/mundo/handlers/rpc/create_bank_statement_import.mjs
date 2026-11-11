// create_bank_statement_import (T14 cap06): grava o extrato e as linhas (o parse é no navegador); linha com dedup_key já importada na
// conta fica de fora; saldo de abertura = saldo final do arquivo − Σ das linhas inseridas.
import { r2, num } from '../../lib/eco.mjs';
import { agoraIso } from '../../lib/conciliacao.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const conta = store.rows('bank_accounts').find((b) => b.id === a.p_bank_account_id);
  if (!conta) throw new RpcError('Conta bancária não encontrada.');
  if (!Array.isArray(a.p_entries)) throw new RpcError('p_entries deve ser um array JSON.');
  const vivos = new Set(store.rows('bank_statement_imports').filter((i) => i.bank_account_id === conta.id && i.status !== 'cancelled').map((i) => i.id));
  if (a.p_file_hash && store.rows('bank_statement_imports').some((i) => vivos.has(i.id) && i.file_hash === a.p_file_hash)) throw new RpcError('ja_importado: file_hash');
  const ja = new Set(store.rows('bank_statement_entries').filter((e) => vivos.has(e.import_id)).map((e) => e.dedup_key));
  const cid = conta.company_id;
  const imp = ctx.db.insert('bank_statement_imports', {
    company_id: cid, bank_account_id: conta.id, file_name: a.p_file_name ?? null, file_hash: a.p_file_hash ?? null, bank_id: a.p_bank_id ?? null, acct_id: a.p_acct_id ?? null,
    period_start: a.p_period_start ?? null, period_end: a.p_period_end ?? null, ledger_balance: a.p_ledger_balance ?? null, ledger_balance_date: a.p_ledger_balance_date ?? null,
    opening_balance: 0, entry_count: 0, status: 'open', created_by: ctx.userId, created_at: agoraIso(),
  }, { companyId: cid });
  let soma = 0, n = 0;
  for (const e of a.p_entries) {
    if (ja.has(e.dedup_key)) continue;
    ja.add(e.dedup_key);
    ctx.db.insert('bank_statement_entries', {
      company_id: cid, bank_account_id: conta.id, import_id: imp.id, dedup_key: e.dedup_key, original_dedup_key: e.dedup_key, fitid: e.fitid || null,
      posted_at: e.posted_at, amount: r2(num(e.amount)), trn_type: e.trn_type ?? null, memo: e.memo ?? null, name: e.name ?? null, status: 'pending', created_at: agoraIso(),
    }, { companyId: cid });
    soma += num(e.amount); n++;
  }
  const abertura = r2(num(a.p_ledger_balance) - soma);
  imp.entry_count = n; imp.opening_balance = abertura;
  store.table('bank_statement_imports').touch();
  return { import_id: imp.id, inserted_count: n, total_entries: a.p_entries.length, skipped_count: a.p_entries.length - n, skipped_dup_count: 0, skipped_samples: [],
    opening_balance: abertura, acct_warning: false };
};
