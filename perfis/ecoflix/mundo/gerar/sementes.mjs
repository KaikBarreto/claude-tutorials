#!/usr/bin/env node
// Gera as sementes do mundo base da EcoFlix (Recicla Vale Metais, Taubaté/SP) para o Supabase falso.
//   node gerar/sementes.mjs                 -> seeds/*.json e seeds-extra/base/*.json (determinístico). Grava tudo numa pasta
//                                              temporária ao lado e troca arquivo a arquivo por renomeação: quem der
//                                              /__dev/reset no meio nunca lê arquivo pela metade.
//   node gerar/sementes.mjs --saida <pasta> -> grava em <pasta>/seeds e <pasta>/seeds-extra/base (para conferir antes)
// Tudo fictício (planejamento/ecoflix/MUNDO_FICTICIO.md): CPF/CNPJ com dígito válido, e-mails .example, telefones
// (12) 9 0000-xxxx, placas inventadas. Data do mundo: FAKE_NOW=2026-11-10T08:30:00-03:00.
// O mundo é o da junção de 10/11 (planejamento/ecoflix/MUNDO_LINHA_DO_TEMPO.md, seção 16 aplicada sobre a semente de
// 51224e1): histórico de 01/08 a 09/11/2026 montado por plano, não por sorteio solto. Outubro no centavo do T15 por
// fornecedor e por cliente (seção 5), setembro e agosto pela regra da seção 6, novembro com os fatos da seção 7, bancos e
// cofre da seção 8, caixas da seção 9, saldos da seção 10, notas fiscais da seção 11 e o estoque de 10/11 08:30 da seção 4
// (com o lote de Minas e a chaparia da T18 parados desde o saldo inicial de 01/08). Os saldos gravados (estoque, cofre,
// bancos, parceiros, caixas) saem da soma do próprio histórico, como os triggers do banco fariam. O gerador confere os
// números da seção 16 (item 15 e os totais de cada item) e para se algum não bater.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MUNDO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const iSaida = process.argv.indexOf('--saida');
const SAIDA = iSaida >= 0 ? path.resolve(process.argv[iSaida + 1]) : null;

// ---------------------------------------------------------------- utilidades
const id = (k) => `@id:${k}`;
let seed = 20261110;
function rnd() { // mulberry32
  seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const r2 = (n) => Math.round(n * 100) / 100;
const r1 = (n) => Math.round(n * 10) / 10;
/** arredonda o meio para o par (1162,5 -> 1162), como as contas da junção (Python) fizeram a regra de setembro e agosto */
const roundPar = (x) => { const f = Math.floor(x); return Math.abs(x - f - 0.5) < 1e-9 ? (f % 2 === 0 ? f : f + 1) : Math.round(x); };
const pad = (n, w = 2) => String(n).padStart(w, '0');
const at = (d, hhmm) => new Date(`${d}T${hhmm}:00-03:00`).toISOString(); // AAAA-MM-DD + HH:MM de Brasília -> ISO UTC
const addDays = (d, n) => { const t = new Date(`${d}T12:00:00Z`); t.setUTCDate(t.getUTCDate() + n); return t.toISOString().slice(0, 10); };
const weekday = (d) => new Date(`${d}T12:00:00Z`).getUTCDay(); // 0 domingo
const hm = (min) => `${pad(Math.floor(min / 60))}:${pad(min % 60)}`;
const maisMin = (hhmm, n) => hm(Number(hhmm.slice(0, 2)) * 60 + Number(hhmm.slice(3)) + n);
const fmt = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const CONFERIDO = [];
function confere(cond, msg) { if (!cond) throw new Error(`sementes: ${msg}`); CONFERIDO.push(msg); }
/** n partes inteiras (>= 1) que somam total exatamente, com variação de ±jit em torno da média */
function split(total, n, jit = 0.45) {
  n = Math.min(n, Math.max(1, Math.floor(total)));
  if (n <= 1) return [total];
  const w = Array.from({ length: n }, () => 1 + (rnd() * 2 - 1) * jit);
  const sw = w.reduce((a, b) => a + b, 0);
  const parts = w.map((x) => Math.max(1, Math.floor((x / sw) * total)));
  let diff = total - parts.reduce((a, b) => a + b, 0);
  for (let i = 0; diff !== 0; i++) { const k = i % n; if (diff > 0) { parts[k]++; diff--; } else if (parts[k] > 1) { parts[k]--; diff++; } }
  return parts;
}
/** n partes inteiras quase iguais (as primeiras levam o resto) */
const splitIgual = (total, n) => Array.from({ length: n }, (_, i) => Math.floor(total / n) + (i < total % n ? 1 : 0));

// documentos com dígito verificador válido
function cpfDigit(nums) { let s = 0; for (let i = 0; i < nums.length; i++) s += nums[i] * (nums.length + 1 - i); const d = 11 - (s % 11); return d > 9 ? 0 : d; }
function cpf(base9) {
  const n = String(base9).padStart(9, '0').split('').map(Number); const d1 = cpfDigit(n); const d2 = cpfDigit([...n, d1]);
  return `${n.slice(0, 3).join('')}.${n.slice(3, 6).join('')}.${n.slice(6, 9).join('')}-${d1}${d2}`;
}
function cnpjDigit(nums, w) { const s = nums.reduce((a, n, i) => a + n * w[i], 0); const m = s % 11; return m < 2 ? 0 : 11 - m; }
function cnpj(base8, branch = '0001') {
  const n = (String(base8).padStart(8, '0') + branch).split('').map(Number);
  const d1 = cnpjDigit(n, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]); const d2 = cnpjDigit([...n, d1], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
  const s = n.join('') + d1 + d2;
  return `${s.slice(0, 2)}.${s.slice(2, 5)}.${s.slice(5, 8)}/${s.slice(8, 12)}-${s.slice(12)}`;
}
/** inscrição estadual de SP (12 dígitos, dígitos verificadores na 9ª e na 12ª posição) */
function ieSP(base8, meio2) {
  const a = String(base8).split('').map(Number);
  const d9 = (a.reduce((s, n, i) => s + n * [1, 3, 4, 5, 6, 7, 8, 10][i], 0) % 11) % 10;
  const b = [...a, d9, ...String(meio2).split('').map(Number)];
  const d12 = (b.reduce((s, n, i) => s + n * [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2][i], 0) % 11) % 10;
  const s = [...b, d12].join('');
  return `${s.slice(0, 3)}.${s.slice(3, 6)}.${s.slice(6, 9)}.${s.slice(9)}`;
}
const fone = (n) => `(12) 90000-${pad(n, 4)}`;

// ---------------------------------------------------------------- a empresa e as pessoas
const COMPANY = id('company.reciclavale');
const RAFAEL = id('user.rafael');
const MARCOS = id('user.marcos');
const JULIANA = id('user.juliana');
const CREATED = '2026-07-27T13:00:00.000Z'; // cliente da EcoSistema desde o fim de julho (o histórico começa em 01/08)
const HOJE = '2026-11-10';
const INICIO = '2026-08-01';
const DOMINIO = '@reciclavalemetais.example';
const CNPJ_MATRIZ = cnpj('47318506'); // T1 e T22 (a filial é 47.318.506/0002-98)
confere(CNPJ_MATRIZ === '47.318.506/0001-07' && cnpj('47318506', '0002') === '47.318.506/0002-98', 'CNPJ da matriz/filial');
confere(cpf('274913508') === '274.913.508-79', 'CPF do Rafael (T18)');

const empresa = {
  id: COMPANY, name: 'Recicla Vale Metais', cnpj: CNPJ_MATRIZ, email: `contato${DOMINIO}`, phone: fone(1000),
  address: 'Rua das Oficinas, 1250 - Parque Industrial, Taubaté - SP, 12086-410', contact_name: 'Rafael Nogueira',
  timezone: 'America/Sao_Paulo', base_currency: 'BRL', subscription_status: 'active', subscription_plan: 'personalizado',
  subscription_value: 1025, base_subscription_value: 1025, subscription_expires_at: '2026-12-05T23:59:59.000Z', billing_cycle: 'monthly',
  payment_method: 'pix', ltv: 4100, max_users: 3, nfe_tier: 1, extra_users: 0, plan_locked: false, is_test_account: false,
  cash_account_enabled: true, cash_account_opt_out: false, cash_account_seeded_at: '2026-08-01T10:30:00.000Z', multi_cash_enabled: true,
  onboarding_completed_at: '2026-07-31T18:00:00.000Z', onboarding_state: {}, cato_enabled: true, ai_consent_at: '2026-07-27T13:05:00.000Z',
  ai_consent_version: '1', white_label_enabled: false, show_name_in_documents: true, show_cnpj_in_documents: true,
  show_address_in_documents: true, show_phone_in_documents: true, show_email_in_documents: false, show_receipt_phrase: true,
  receipt_phrase: 'Obrigado pela preferência! Recicla Vale Metais', lat: -23.0262, lng: -45.5559, geocode_status: 'ok', origin: 'site',
  created_at: CREATED, updated_at: '2026-11-01T12:00:00.000Z',
};
const perfil = (uid, email, nome, extra = {}) => ({
  id: uid, email, full_name: nome, company_id: COMPANY, role: 'operator', permission_preset: null, is_active: true, must_change_password: false,
  terms_accepted_at: '2026-07-31T12:05:00.000Z', preferred_language: 'pt-BR', preferred_currency: 'BRL', default_payment_method: 'cash',
  balanca_ativada: false, direct_print_enabled: false, auto_print_receipts: false, show_profit_on_receipt: false, multiple_price_tables_enabled: true,
  origin: 'convite', created_at: '2026-07-31T12:00:00.000Z', updated_at: '2026-11-01T12:00:00.000Z', ...extra,
});
const PERFIS = [
  perfil(RAFAEL, `rafael${DOMINIO}`, 'Rafael Nogueira', { role: 'company_admin', permission_preset: 'full_access', terms_accepted_at: '2026-07-27T13:01:00.000Z', cato_invite_seen_at: '2026-07-28T12:00:00.000Z', origin: 'cadastro', created_at: CREATED }),
  // T2: Marcos = "Operador Padrão" menos "Ver Projeção de Lucro" (31 permissões, selo "Personalizado"), tela inicial Caixa
  perfil(MARCOS, `marcos.antunes${DOMINIO}`, 'Marcos Antunes', { initial_screen_path: '/caixa' }),
  perfil(JULIANA, `juliana.prado${DOMINIO}`, 'Juliana Prado'),
];
// T19/T22/T0/T2 (seção 16, item 13): todos os e-mails da empresa no domínio dela; o do Rafael é rafael@
confere([empresa.email, ...PERFIS.map((p) => p.email)].every((e) => e.endsWith(DOMINIO)) && PERFIS[0].email === `rafael${DOMINIO}`, 'item 13: e-mails da empresa em @reciclavalemetais.example (Rafael rafael@)');
const OPERADOR_PADRAO = ['screen_caixa', 'screen_historico_caixa', 'screen_pedidos', 'screen_estoque', 'screen_historico_materiais', 'screen_weighing_ticket', 'screen_producao', 'screen_coletas', 'screen_clientes_fornecedores', 'screen_funcionarios', 'screen_agenda', 'screen_contas_pagar_receber', 'action_register_purchase', 'action_register_sale', 'action_ticket_pesagem_compra', 'action_ticket_pesagem_venda', 'action_ticket_pesagem_ver_valorizados', 'action_register_expense', 'action_register_income', 'action_open_cash', 'action_close_cash', 'action_view_total_cash', 'action_use_bank_accounts', 'action_view_financial_values', 'action_view_profit_projection', 'action_view_production_costs', 'action_view_partner_balance', 'action_adjust_partner_balance', 'action_create_bill', 'action_pay_bill', 'action_manage_recurring', 'action_delete_bill'];
const PERMISSOES = {
  marcos: OPERADOR_PADRAO.filter((p) => p !== 'action_view_profit_projection'),
  juliana: ['screen_dashboard', 'screen_movimentacoes_bancarias', 'screen_relatorio_financeiro', 'screen_contas_pagar_receber', 'screen_pedidos', 'screen_notas_fiscais', 'screen_clientes_fornecedores', 'action_view_financial_values', 'action_manage_bank_accounts', 'action_reconcile_bank', 'action_create_bill', 'action_pay_bill', 'action_emit_nfe', 'action_emit_nfse', 'action_view_partner_balance'],
};
confere(PERMISSOES.marcos.length === 31 && PERMISSOES.juliana.length === 15, 'permissões do T2');

// módulos do catálogo (subscription_modules, como nas migrations) e o plano Personalizado com os 10 da trilha (T0)
const MODULOS = [
  ['kit_basico', 'Kit Básico', 'Caixa, Estoque, Clientes, Pedidos e mais', 125, ['screen_dashboard', 'screen_caixa', 'screen_historico_caixa', 'screen_movimentacoes_bancarias', 'screen_estoque', 'screen_historico_materiais', 'screen_relatorio_estoque', 'screen_relatorio_financeiro', 'screen_pedidos', 'screen_categorias', 'screen_clientes_fornecedores', 'screen_configuracoes', 'screen_tutoriais', 'screen_assinatura', 'screen_weighing_ticket'], true, true],
  ['funcionarios', 'Funcionários (RH)', 'Gestão completa de funcionários com vales, pagamentos e extratos', 100, ['screen_funcionarios'], false, true],
  ['ticket_pesagem', 'Ticket de Pesagem', 'Controle de pesagem rodoviária com tickets impressos', 50, ['screen_weighing_ticket'], false, false],
  ['notas_fiscais', 'Notas Fiscais', 'Emissão de NF-e integrada', 150, ['screen_notas_fiscais'], false, true],
  ['white_label', 'White Label', 'Personalize o sistema com seu próprio logo, removendo a marca EcoSistema', 100, [], false, true],
  ['balanca_integration', 'Integração com Balança', 'Leitura de peso da balança no sistema e no EcoTray (multi-balança)', 100, null, false, true],
  ['portal_cliente', 'Portal do Cliente', 'Portal para seus clientes acompanharem pedidos, saldos e fotos online', 150, ['screen_portal_cliente'], false, true],
  ['producao', 'Produção', 'Produção e beneficiamento: fichas técnicas, ordens de produção, consumo teórico x real, perdas e custo por peça.', 150, ['screen_producao'], false, true],
  ['coletas', 'Coletas (Logística)', 'Gestão de coletas e logística: ordens de coleta, agenda, cadastro de veículos, motoristas e caçambas, e relatórios.', 150, ['screen_coletas'], false, true],
  ['crm_kanban', 'CRM/Kanban', 'Organize oportunidades comerciais em múltiplos funis e acompanhe cada negociação pelo Kanban.', 100, ['screen_crm_kanban'], false, true],
  ['modulo_gerencial', 'Módulo Gerencial', 'Matriz e filiais: visão consolidada de estoque, financeiro e assinaturas do grupo.', 200, ['screen_gerencial_dashboard', 'screen_gerencial_financeiro', 'screen_gerencial_estoque'], false, true],
];
const DA_TRILHA = ['kit_basico', 'funcionarios', 'notas_fiscais', 'white_label', 'balanca_integration', 'portal_cliente', 'producao', 'coletas', 'crm_kanban', 'modulo_gerencial'];

// materiais (R$/kg compra e venda, NCM sugerido), códigos 1 a 15 na ordem do MUNDO_FICTICIO.md (T3)
const GRUPOS = [
  ['ferrosos', 'Ferrosos', '#64748B'], ['cobre', 'Cobre', '#C2410C'], ['aluminio', 'Alumínio', '#0EA5E9'],
  ['metais', 'Metais', '#CA8A04'], ['outros', 'Outros', '#16A34A'],
];
const MATERIAIS = [
  ['ferro_pesado', 'ferrosos', 'Ferro pesado', 0.95, 1.25, '7204.49.00'],
  ['ferro_misto', 'ferrosos', 'Ferro misto', 0.75, 1.05, '7204.49.00'],
  ['chaparia', 'ferrosos', 'Chaparia', 0.70, 0.98, '7204.49.00'],
  ['cobre_mel', 'cobre', 'Cobre mel', 42.50, 47.90, '7404.00.00'],
  ['cobre_misto', 'cobre', 'Cobre misto', 36.00, 41.50, '7404.00.00'],
  ['fio_cobre', 'cobre', 'Fio de cobre encapado', 18.00, 22.00, '7404.00.00'],
  ['al_latinha', 'aluminio', 'Alumínio latinha', 6.20, 7.40, '7602.00.00'],
  ['al_perfil', 'aluminio', 'Alumínio perfil', 8.90, 10.40, '7602.00.00'],
  ['al_bloco', 'aluminio', 'Alumínio bloco', 7.10, 8.50, '7602.00.00'],
  ['latao', 'metais', 'Metal amarelo (latão)', 27.50, 31.90, '7404.00.00'],
  ['bronze', 'metais', 'Bronze', 29.00, 33.50, '7404.00.00'],
  ['inox', 'metais', 'Inox', 5.80, 7.20, '7204.21.00'],
  ['bateria', 'outros', 'Bateria automotiva', 3.10, 3.90, '8549.11.00'],
  ['papelao', 'outros', 'Papelão', 0.55, 0.80, '4707.10.00'],
  ['pet', 'outros', 'Plástico PET', 1.90, 2.60, '3915.90.00'],
];
const MAT = Object.fromEntries(MATERIAIS.map(([k, g, nome, pc, pv, ncm], i) => [k, { k, g, nome, pc, pv, ncm, code: String(i + 1), id: id(`material.${k}`) }]));
const KS = Object.keys(MAT);
const somaKS = (o, f = () => 1) => r2(KS.reduce((s, k) => s + (o[k] || 0) * f(MAT[k]), 0));
// seção 4 / item 1: estoque em 10/11 08:30 (T7, T10, T21 e as cargas da T17 e da T18), o mesmo na Posição de Estoque e no Cato
const ESTOQUE_HOJE = { ferro_pesado: 2180, ferro_misto: 6420, chaparia: 3750, cobre_mel: 42, cobre_misto: 148, fio_cobre: 96, al_latinha: 640, al_perfil: 3385, al_bloco: 2830, latao: 214, bronze: 38, inox: 260, bateria: 3960, papelao: 1850, pet: 920 };
// o lote de Minas (T17) e a chaparia a mais (T18): no pátio desde o saldo inicial de 01/08, parados (fora do ACUMULA_AGO)
const LOTE_PARADO = { al_perfil: 3200, al_bloco: 2600, chaparia: 600 };
confere(somaKS(ESTOQUE_HOJE) === 26733 && somaKS(ESTOQUE_HOJE, (m) => m.pc) === 96076 && somaKS(ESTOQUE_HOJE, (m) => m.pv) === 116689.4, 'item 1: estoque de 10/11 com 26.733 kg, R$ 96.076,00 a custo e projeção R$ 116.689,40 (T21)');
confere(ESTOQUE_HOJE.latao === 214 && ESTOQUE_HOJE.cobre_mel === 42, 'item 1: latão 214 kg e cobre mel 42 kg (T7)');

// parceiros (cliente = para quem a empresa vende; fornecedor = de quem compra)
const IBGE = { 'Taubaté': '3554102', 'Pindamonhangaba': '3538006', 'Tremembé': '3554805', 'Itamonte': null };
const END = (logradouro, numero, bairro, cep, cidade = 'Taubaté', uf = 'SP') => ({ logradouro, numero, bairro, cep, cidade, uf, address: `${logradouro}, ${numero} - ${bairro}, ${cidade} - ${uf}`, codigo_ibge: IBGE[cidade] ?? null });
const SEM_END = { logradouro: null, numero: null, bairro: null, cep: null, cidade: null, uf: null, address: null, codigo_ibge: null };
const SIQUEIRA = { name: 'Depósito Irmãos Siqueira', razao: 'Depósito de Sucatas Irmãos Siqueira Ltda', doc: cnpj('95127438'), pf: false, phone: fone(1302), contact: 'Joel Siqueira', ...END('Estrada do Pinheirinho', '2730', 'Pinheirinho', '12091-500', 'Tremembé') };
const FORNECEDORES = [
  // T7: Valdir sem CPF nem endereço; "Não possui telefone"
  { k: 'valdir', name: 'Valdir Pereira', doc: null, pf: true, phone: null, phone_unavailable: true, ...SEM_END, code: '1', pix: null },
  { k: 'cida', name: 'Aparecida Ramos', nome_fantasia: 'Dona Cida', doc: cpf('903582716'), pf: true, phone: fone(1201), ...END('Rua das Acácias', '88', 'Jardim Gurilândia', '12071-150'), code: '2', pix: fone(1201) },
  { k: 'siqueira', ...SIQUEIRA, code: '3', pix: SIQUEIRA.doc },
  { k: 'valeforte', name: 'Auto Peças Vale Forte', razao: 'Auto Peças Vale Forte Ltda', doc: cnpj('96384120'), pf: false, phone: fone(1403), contact: 'Sandra Lemes', ...END('Avenida Brasil', '1290', 'Centro', '12080-010'), code: '4', pix: null },
  { k: 'recomeco', name: 'Cooperativa Recomeço', razao: 'Cooperativa de Catadores Recomeço', doc: cnpj('97250936'), pf: false, phone: fone(1504), contact: 'Marta Oliveira', ...END('Rua do Trabalho', '57', 'Vila Nossa Senhora das Graças', '12060-640'), code: '5', pix: cnpj('97250936') },
];
const CLIENTES = [
  { k: 'quiririm', name: 'Aços Quiririm Ltda', razao: 'Aços Quiririm Indústria e Comércio Ltda', doc: cnpj('98463027'), phone: fone(1605), contact: 'Paulo Henrique', ...END('Rodovia Vereador Abel Fabrício Dias', '3400', 'Quiririm', '12043-300'), code: '1', industria: true },
  { k: 'bandeira', name: 'Fundição Bandeira do Vale', razao: 'Fundição Bandeira do Vale Ltda', doc: cnpj('94716352'), phone: fone(1706), contact: 'Cristina Moura', ...END('Rua Anhanguera', '980', 'Distrito Industrial', '12412-010', 'Pindamonhangaba'), code: '2', industria: true },
  // T17: a Serra Fina fica em Itamonte, MG (a carga atravessa o RJ: MDF-e; CFOP 6102); código IBGE fica para a busca de CEP do app
  { k: 'serrafina', name: 'Serra Fina Alumínio Reciclagem', razao: 'Serra Fina Alumínio Reciclagem Ltda', doc: cnpj('92837465'), phone: '(35) 90000-1807', contact: 'Diego Prado', ...END('Rodovia BR-354', '4100', 'Distrito Industrial', '37466-000', 'Itamonte', 'MG'), code: '3', industria: true },
  { k: 'siqueira', ...SIQUEIRA, code: '4', industria: false },
];
// seção 3 / item 10: taras e capacidades da junção (a do FKD2E41 é a 2ª pesagem do T8); sem UF de licenciamento, tipo
// (categoria), rodado e carroceria (a T17 completa o FKD2E41 na tela); motoristas só com nome e telefone (sem CPF e CNH)
const VEICULOS = [
  { k: 'truck', plate: 'FKD2E41', description: 'Caminhão truck', motorista: 'Edson Moura', cap: 14000, tara: 6380 },
  { k: '34', plate: 'GHT7B19', description: 'Caminhão 3/4', motorista: 'Jair Lopes', cap: 4000, tara: 3900 },
  { k: 'picape', plate: 'EZR4C63', description: 'Picape', motorista: 'Tiago Freitas', cap: 1000, tara: 1750 },
];

// ---------------------------------------------------------------- tabelas
const T = {}; // tabela -> linhas
const add = (t, row) => ((T[t] ||= []).push(row), row);

add('companies', empresa);
for (const p of PERFIS) add('profiles', p);
for (const [k, uid, role] of [['rafael', RAFAEL, 'company_admin'], ['marcos', MARCOS, 'operator'], ['juliana', JULIANA, 'operator']]) {
  add('user_roles', { id: id(`role.${k}`), user_id: uid, role, created_at: k === 'rafael' ? CREATED : '2026-07-31T12:00:00.000Z' });
  add('user_shortcuts', { id: id(`atalhos.${k}`), user_id: uid, shortcuts_enabled: true, custom_shortcuts: null, created_at: CREATED, updated_at: CREATED });
}
for (const [k, uid] of [['marcos', MARCOS], ['juliana', JULIANA]]) PERMISSOES[k].forEach((p, i) => add('user_permissions', { id: id(`perm.${k}.${i}`), user_id: uid, permission: p, created_at: '2026-07-31T12:00:00.000Z' }));
// pesquisa NPS principal da plataforma (consultada com .single()): existe, mas inativa, sem resposta da empresa
add('nps_surveys', { id: id('nps.principal'), title: 'NPS EcoSistema', description: 'Pesquisa de satisfação', is_active: false, is_main_nps: true, target_audience: 'all', trigger_type: 'manual', created_at: '2026-01-15T12:00:00.000Z', updated_at: '2026-01-15T12:00:00.000Z' });
for (const [code, name, description, price, screens, base, active] of MODULOS) {
  add('subscription_modules', { id: id(`modulo.${code}`), code, name, description, price, screens, is_base_module: base, is_active: active, created_at: '2025-12-05T14:47:07.000Z' });
}
add('subscription_plans', { id: id('plano.start'), code: 'start', name: 'Plano Start', description: 'Kit Básico com 2 usuários', price: 125, max_users: 2, modules: ['kit_basico'], is_active: true });
add('subscription_plans', { id: id('plano.avancado'), code: 'avancado', name: 'Plano Avançado', description: 'Kit Básico + Funcionários com 3 usuários', price: 225, max_users: 3, modules: ['kit_basico', 'funcionarios'], is_active: true });
add('subscription_plans', { id: id('plano.master'), code: 'master', name: 'Plano Master', description: 'Todos os módulos com 4 usuários', price: 415, max_users: 4, modules: ['kit_basico', 'funcionarios', 'notas_fiscais'], is_active: true });
add('subscription_plans', { id: id('plano.personalizado'), code: 'personalizado', name: 'Personalizado', description: 'Monte seu plano escolhendo módulos', price: 0, max_users: 2, modules: ['kit_basico'], is_active: true });
// níveis do módulo Notas Fiscais (catálogo da migration 20260615190000_nfe_module_tiers); a empresa está no 1 (item 11)
[[1, 'Nível 1', 1000, 150], [2, 'Nível 2', 3000, 300], [3, 'Nível 3', 5000, 400]].forEach(([level, name, doc_limit, price]) => add('nfe_module_tiers', { id: id(`nfe_tier.${level}`), level, name, doc_limit, price, is_active: true }));
confere(empresa.nfe_tier === 1 && T.nfe_module_tiers.find((x) => x.level === 1).doc_limit === 1000, 'item 11: nfe_tier no Nível 1 do catálogo (1.000 documentos)');
for (const code of DA_TRILHA) add('company_modules', { id: id(`company_module.${code}`), company_id: COMPANY, module_code: code, added_at: '2026-07-27T13:00:00.000Z', removed_at: null, effective_until: null, price_override: null });

add('app_config', { id: id('app_config.app_version'), key: 'app_version', value: '1.59.154', description: 'Versão publicada do app', updated_at: '2026-11-07T19:05:00.000Z' });
add('app_config', { id: id('app_config.ecotray_version'), key: 'ecotray_version', value: '1.7.22', description: 'Versão publicada do EcoTray', updated_at: '2026-10-28T12:00:00.000Z' });
add('app_config', { id: id('app_config.reconciliation_enabled'), key: 'reconciliation_enabled', value: 'true', description: 'Conciliação bancária ligada', updated_at: '2026-09-08T12:00:00.000Z' });
add('currencies', { code: 'BRL', name: 'Real Brasileiro', symbol: 'R$', decimals: 2, locale: 'pt-BR' });
add('currencies', { code: 'USD', name: 'Dólar Americano', symbol: 'US$', decimals: 2, locale: 'en-US' });
add('currencies', { code: 'PYG', name: 'Guarani Paraguaio', symbol: '₲', decimals: 0, locale: 'es-PY' });
// catálogo MTR das migrations (20260623150000_mtr_sistemas e as seguintes): com a configuração fiscal de B (UF SP), o app resolve o
// sistema ambiental pela UF (useMtr: company_fiscal_config.uf -> mtr_uf_sistema -> mtr_sistemas); SP usa o SIGOR (T18)
const MTR_CRIADO = '2026-06-23T15:00:00.000Z';
for (const [sistema, nome, protocolo, auth_mode, base_url_prod, base_url_homolog, chave_header_nome] of [
  ['sigor_sp', 'SIGOR-MTR / CETESB-SP', 'sinir', 'senha', 'https://mtrr.cetesb.sp.gov.br/apiws/rest', 'https://mtrr-hom.cetesb.sp.gov.br/apiws/rest', null],
  ['sinir', 'SINIR Federal', 'sinir', 'token', 'https://admin.sinir.gov.br/api', 'https://homolog-admin.sinir.gov.br/api', null],
  ['feam_mg', 'FEAM-MG', 'feam', 'senha', 'https://mtr.meioambiente.mg.gov.br/api', 'https://homologa.mtr.meioambiente.mg.gov.br/api', 'chave_feam'],
  ['fepam_rs', 'FEPAM-RS', 'fepam', 'senha', 'https://mtr.fepam.rs.gov.br/mtrservice', 'https://mtr.fepam.rs.gov.br/mtrservice', null],
  ['iema_es', 'IEMA-ES', 'feam', 'senha', 'https://mtr.iema.es.gov.br/api', 'https://apps.iema.es.gov.br:8443/api', null],
]) add('mtr_sistemas', { sistema, nome, protocolo, auth_mode, base_url_prod, base_url_homolog, chave_header_nome, ativo: true, created_at: MTR_CRIADO, updated_at: '2026-08-12T16:00:00.000Z' });
const UF_MTR = { SP: 'sigor_sp', MG: 'feam_mg', RS: 'fepam_rs', ES: 'iema_es' };
for (const uf of ['SP', 'MG', 'RS', 'ES', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'GO', 'MA', 'MT', 'MS', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RO', 'RR', 'SC', 'SE', 'TO']) add('mtr_uf_sistema', { uf, sistema: UF_MTR[uf] || 'sinir', created_at: MTR_CRIADO, updated_at: MTR_CRIADO });

for (const [k, name, color] of GRUPOS) add('material_groups', { id: id(`grupo.${k}`), company_id: COMPANY, name, color, icon: 'circle', created_at: '2026-07-28T12:00:00.000Z', updated_at: '2026-07-28T12:00:00.000Z' });
for (const m of Object.values(MAT)) {
  add('materials', {
    id: m.id, company_id: COMPANY, code: m.code, name: m.nome, fiscal_name: null, group_id: id(`grupo.${m.g}`), unit: 'Kg', ncm: m.ncm,
    purchase_price: m.pc, sale_price: m.pv, purchase_price_currency: 'BRL', sale_price_currency: 'BRL', current_stock: 0,
    is_archived: false, created_by: RAFAEL, created_at: '2026-07-28T12:10:00.000Z', updated_at: '2026-10-20T12:00:00.000Z',
  });
}
// tabela padrão "Principal" (T4) e a "Tabela Depósitos" (+4 %, criada no T3). Seção 4: em B ela não está ligada ao Depósito Irmãos
// Siqueira (a T4 liga na tela); o depósito compra e vende pela tabela padrão
add('price_tables', { id: id('tabela.padrao'), company_id: COMPANY, name: 'Principal', is_default: true, is_linked: false, linked_to_table_id: null, created_at: '2026-07-28T12:20:00.000Z', updated_at: '2026-10-20T12:00:00.000Z' });
add('price_tables', { id: id('tabela.depositos'), company_id: COMPANY, name: 'Tabela Depósitos', is_default: false, is_linked: true, linked_to_table_id: id('tabela.padrao'), variation_type: 'percentage', variation_direction: 'positive', variation_amount: 4, created_at: '2026-11-09T17:50:00.000Z', updated_at: '2026-11-09T17:50:00.000Z' });
for (const m of Object.values(MAT)) {
  add('price_table_items', { id: id(`pti.padrao.${m.k}`), price_table_id: id('tabela.padrao'), material_id: m.id, purchase_price: m.pc, sale_price: m.pv, is_override: false, created_at: '2026-07-28T12:20:00.000Z', updated_at: '2026-10-20T12:00:00.000Z' });
  add('price_table_items', { id: id(`pti.depositos.${m.k}`), price_table_id: id('tabela.depositos'), material_id: m.id, purchase_price: Math.round(m.pc * 1040) / 1000, sale_price: Math.round(m.pv * 1040) / 1000, is_override: false, created_at: '2026-11-09T17:50:00.000Z', updated_at: '2026-11-09T17:50:00.000Z' });
}
const parceiroBase = (p) => ({
  company_id: COMPANY, name: p.name, nome_fantasia: p.nome_fantasia || null, razao_social: p.razao || (p.pf ? p.name : null), cpf_cnpj: p.doc,
  phone: p.phone || null, phone_unavailable: !!p.phone_unavailable, email: p.pf ? null : `contato@${p.k === 'siqueira' ? 'irmaossiqueira' : p.k}.example`, contact_name: p.contact || null,
  address: p.address, logradouro: p.logradouro, numero: p.numero, bairro: p.bairro, cep: p.cep, cidade: p.cidade, uf: p.uf, codigo_ibge: p.codigo_ibge,
  pix_key: p.pix || null, code: p.code, is_mei: false, created_by: RAFAEL, created_at: '2026-07-29T12:00:00.000Z', updated_at: '2026-10-15T12:00:00.000Z',
  indicador_ie: p.pf ? 9 : 1, inscricao_estadual: p.pf ? null : `68${pad(Number(p.code) * 731 % 1000, 3)}${pad(Number(p.code) * 4127 % 100000, 5)}`,
});
for (const f of FORNECEDORES) add('suppliers', { id: id(`fornecedor.${f.k}`), ...parceiroBase(f), linked_customer_id: f.k === 'siqueira' ? id('cliente.siqueira') : null, is_industry: false, default_price_table_id: null });
for (const c of CLIENTES) {
  add('customers', {
    id: id(`cliente.${c.k}`), ...parceiroBase(c), linked_supplier_id: c.k === 'siqueira' ? id('fornecedor.siqueira') : null,
    is_industry: c.industria, is_intermediary: !c.industria, default_price_table_id: null,
    regime_tributario: c.industria ? 'lucro_real' : 'simples_nacional',
  });
}
for (const v of VEICULOS) {
  add('vehicles', { id: id(`veiculo.${v.k}`), company_id: COMPANY, plate: v.plate, description: v.description, capacidade_kg: v.cap, tara_kg: v.tara, tipo_carroceria: null, tipo_rodado: null, categoria: null, uf_licenciamento: null, created_by: RAFAEL, created_at: '2026-07-29T14:00:00.000Z' });
  add('drivers', { id: id(`motorista.${v.k}`), company_id: COMPANY, name: v.motorista, phone: fone(1900 + VEICULOS.indexOf(v)), document: null, cnh: null, cnh_categoria: null, cnh_validade: null, created_by: RAFAEL, created_at: '2026-07-29T14:00:00.000Z' });
}
const tara = (p) => T.vehicles.find((v) => v.plate === p);
confere(tara('FKD2E41').tara_kg === 6380 && tara('FKD2E41').capacidade_kg === 14000 && tara('GHT7B19').tara_kg === 3900 && tara('GHT7B19').capacidade_kg === 4000 && tara('EZR4C63').tara_kg === 1750 && tara('EZR4C63').capacidade_kg === 1000
  && T.vehicles.every((v) => !v.uf_licenciamento && !v.categoria && !v.tipo_rodado && !v.tipo_carroceria) && T.drivers.every((m) => !m.document && !m.cnh && !m.cnh_categoria && m.phone),
  'item 10: frota com as taras e capacidades da seção 3, sem dados de transporte; motoristas só com nome e telefone');

// financeiro: contas (T13/T14: "Conta Principal", "Conta Secundária", sem código de banco; "Poupança antiga" zerada)
const conta = (k, name, extra) => add('bank_accounts', { id: id(`banco.${k}`), company_id: COMPANY, name, kind: 'bank', is_default: false, is_protected: false, is_archived: false, institution_name: null, institution_code: null, institution_ispb: null, color: '#2563EB', currency: 'BRL', balance: 0, created_at: CREATED, updated_at: CREATED, ...extra });
conta('principal', 'Conta Principal', { is_default: true });
conta('secundaria', 'Conta Secundária', { color: '#7C3AED', created_at: '2026-07-28T15:00:00.000Z', updated_at: '2026-07-28T15:00:00.000Z' });
conta('poupanca', 'Poupança antiga', { color: '#94A3B8', created_at: '2026-07-28T15:10:00.000Z', updated_at: '2026-07-28T15:10:00.000Z' });
conta('cofre', 'DINHEIRO (COFRE)', { kind: 'cash', is_protected: true, institution_name: 'Conta DINHEIRO (COFRE)', color: '#22C55E', created_at: '2026-08-01T10:30:00.000Z', updated_at: '2026-08-01T10:30:00.000Z' });

// grupos do DRE do sistema (um por natureza, nomes de lib/dreHierarchy.ts) e as categorias do T13/T15
const DRE = [['receita_bruta', 'Receita de vendas'], ['deducoes', 'Impostos e deduções'], ['custos', 'Custos dos materiais vendidos'], ['despesas_operacionais', 'Despesas operacionais'], ['outras_receitas_despesas', 'Outras receitas e despesas']];
DRE.forEach(([nature, name], i) => add('dre_groups', { id: id(`dre.${nature}`), company_id: COMPANY, name, nature, is_system: true, sort_order: i, created_at: CREATED, updated_at: CREATED }));
const CATEGORIAS = [ // [chave, nome, tipo, cor, dre_group, natureza do grupo, sistema]
  ['venda_sucata', 'Venda de sucata', 'income', '#16A34A', 'outros', 'receita_bruta', false],
  ['aluguel_cacamba', 'Aluguel de caçamba', 'income', '#0EA5E9', 'outros', 'outras_receitas_despesas', false],
  ['outras_receitas', 'Outras Receitas', 'income', '#000000', 'outros', 'outras_receitas_despesas', true],
  ['impostos_vendas', 'Impostos sobre vendas', 'expense', '#DC2626', 'impostos', 'deducoes', false],
  ['frete', 'Frete', 'expense', '#A16207', 'custos', 'custos', false],
  ['folha', 'Folha salarial', 'expense', '#EC4899', 'opex', 'despesas_operacionais', false],
  ['aluguel', 'Aluguel', 'expense', '#8B5CF6', 'opex', 'despesas_operacionais', false],
  ['energia', 'Energia elétrica', 'expense', '#F59E0B', 'opex', 'despesas_operacionais', false],
  ['agua', 'Água e esgoto', 'expense', '#0284C7', 'opex', 'despesas_operacionais', false],
  ['combustivel', 'Combustível', 'expense', '#EF4444', 'opex', 'despesas_operacionais', false],
  ['manut_veiculos', 'Manutenção de veículos', 'expense', '#0EA5E9', 'opex', 'despesas_operacionais', false],
  ['manut_maquinas', 'Manutenção de máquinas', 'expense', '#14B8A6', 'opex', 'despesas_operacionais', false],
  ['telefone', 'Telefone e internet', 'expense', '#6366F1', 'opex', 'despesas_operacionais', false],
  // item 6: só a categoria de sistema "Tarifas" (a ajuda do app confirma o nome); "Tarifas bancárias" saiu
  ['tarifas', 'Tarifas', 'expense', '#000000', 'opex', 'despesas_operacionais', true],
  ['juros', 'Juros e Multas', 'expense', '#000000', 'nao_operacionais', 'outras_receitas_despesas', true],
  ['outras_despesas', 'Outras Despesas', 'expense', '#000000', 'opex', 'despesas_operacionais', true],
];
CATEGORIAS.forEach(([k, name, type, color, dre, nat, sys], i) => add('financial_categories', { id: id(`categoria.${k}`), company_id: COMPANY, name, type, color, icon: null, parent_id: null, dre_group: dre, dre_group_id: id(`dre.${nat}`), cash_flow_group: 'operacional', is_system: sys, sort_order: i, created_at: CREATED, updated_at: CREATED }));
confere(!T.financial_categories.some((c) => /tarifas banc/i.test(c.name)) && T.financial_categories.filter((c) => c.name === 'Tarifas' && c.is_system).length === 1, 'item 6: só a categoria de sistema "Tarifas" (sem "Tarifas bancárias")');
const CENTROS = [ // T15 (Pátio, Coleta) e T13 (Escritório, Frota)
  ['patio', 'Pátio', '#F59E0B', 'Balança, separação e armazenagem'], ['coleta', 'Coleta', '#3B82F6', 'Caminhões, caçambas e motoristas'],
  ['escritorio', 'Escritório', '#64748B', 'Administrativo, financeiro e notas'], ['frota', 'Frota', '#10B981', 'Caminhões e picape próprios'],
];
for (const [k, name, color, description] of CENTROS) add('cost_centers', { id: id(`cc.${k}`), company_id: COMPANY, name, color, description, icon: null, is_active: true, created_at: '2026-07-31T12:30:00.000Z', updated_at: '2026-07-31T12:30:00.000Z' });
add('payment_conditions', { id: id('condicao.30_60_90'), company_id: COMPANY, name: '30/60/90 dias', installments: [{ days: 30, percent: 33.34 }, { days: 60, percent: 33.33 }, { days: 90, percent: 33.33 }], active: true, is_default: false, created_at: '2026-07-30T12:00:00.000Z', updated_at: '2026-07-30T12:00:00.000Z' });

// ---------------------------------------------------------------- o plano do histórico
const FERIADOS = new Set(['2026-09-07', '2026-10-12', '2026-11-02']);
const util = (d) => weekday(d) >= 1 && weekday(d) <= 5 && !FERIADOS.has(d);
const DIAS = [];
for (let d = '2026-08-03'; d < HOJE; d = addDays(d, 1)) if (util(d)) DIAS.push(d);
const mesDe = (d) => d.slice(0, 7);
const diasDoMes = (m) => DIAS.filter((d) => mesDe(d) === m);
const ultimoDia = (m) => diasDoMes(m).at(-1);
const naSemana = (m, ...wds) => diasDoMes(m).filter((d) => wds.includes(weekday(d)));
const proximoUtil = (d) => { let x = addDays(d, 1); while (!util(x)) x = addDays(x, 1); return x; };
// item 9 / seção 9: o Marcos abre um caixa por dia útil; o Rafael às segundas e nos dias de carga do Siqueira (20/08, 17/09 e os
// lotes de 14/10 e 21/10). Em dia de carga o Rafael chega antes do caminhão e abre o dele primeiro: assim o #70 é o do Marcos de
// 21/10 e, em 09/11, o #83 é o do Marcos e o #84 o do Rafael, o último antes da T6.
const CARGA = new Set(['2026-08-20', '2026-09-17', '2026-10-14', '2026-10-21']);
const RAFAEL_ABRE = new Set([...DIAS.filter((d) => weekday(d) === 1), ...CARGA]);

const OUT_PLAN = { compras: [], vendas: [] }; // linhas do plano: { mes, quem, mat, kg, dias, partes }
const comprar = (mes, quem, mat, kg, dias, partes = null) => kg > 0 && OUT_PLAN.compras.push({ mes, quem, mat, kg, dias, partes });
const vender = (mes, quem, mat, kg, dias) => kg > 0 && OUT_PLAN.vendas.push({ mes, quem, mat, kg, dias });
const sorteia = (lista, n) => { const c = [...lista]; const out = []; while (out.length < Math.min(n, c.length)) out.push(c.splice(Math.floor(rnd() * c.length), 1)[0]); return out.sort(); };
const totalPorMaterial = (tab) => { const o = Object.fromEntries(KS.map((k) => [k, 0])); for (const mats of Object.values(tab)) for (const [k, kg] of Object.entries(mats)) o[k] += kg; return o; };
const valorDe = (mats, preco = 'pc') => r2(Object.entries(mats).reduce((s, [k, kg]) => s + kg * MAT[k][preco], 0));

// outubro (seção 5 / item 2, T15 no centavo): quem vendeu o quê para a Recicla. A bateria de 240 kg do #70 (Siqueira, Pix,
// 21/10 10:12) e os 180 kg de ferro pesado do Valdir (22/10, lançados duas vezes) estão dentro da tabela.
const OUTM = '2026-10';
const OUTUBRO_COMPRAS = { // fornecedor -> material -> kg
  siqueira: { ferro_pesado: 42000, ferro_misto: 14000, chaparia: 5000, cobre_mel: 230, cobre_misto: 100, al_perfil: 600, latao: 250, inox: 600, bateria: 240 },
  valdir: { ferro_pesado: 4180, ferro_misto: 16000, chaparia: 6750, cobre_mel: 240, cobre_misto: 200, fio_cobre: 350 },
  valeforte: { chaparia: 850, cobre_mel: 230, cobre_misto: 400, al_perfil: 300, al_bloco: 700 },
  cida: { al_latinha: 1500, papelao: 7000 },
  recomeco: { papelao: 8400, pet: 2600, al_latinha: 1250, chaparia: 1100, ferro_misto: 900 },
  balcao: { ferro_pesado: 3820, ferro_misto: 10000, chaparia: 3150, cobre_mel: 280, fio_cobre: 250, al_latinha: 500, al_perfil: 1120, al_bloco: 300, latao: 250, bronze: 200, inox: 600, bateria: 1080 },
};
// item 3: para quem ela vendeu (a bateria não vende em outubro)
const OUTUBRO_VENDAS = {
  bandeira: { cobre_mel: 1000, cobre_misto: 700, fio_cobre: 600, latao: 500, bronze: 200 },
  quiririm: { ferro_pesado: 10000, ferro_misto: 38612, chaparia: 16100, inox: 1200 },
  serrafina: { al_latinha: 3250, al_perfil: 2673, al_bloco: 1000 },
  siqueira: { papelao: 15400, pet: 2427 },
};
const CLIENTE_DE = { ferro_pesado: 'quiririm', ferro_misto: 'quiririm', chaparia: 'quiririm', inox: 'quiririm', cobre_mel: 'bandeira', cobre_misto: 'bandeira', fio_cobre: 'bandeira', latao: 'bandeira', bronze: 'bandeira', al_latinha: 'serrafina', al_perfil: 'serrafina', al_bloco: 'serrafina', bateria: 'siqueira', papelao: 'siqueira', pet: 'siqueira' };
for (const [cli, mats] of Object.entries(OUTUBRO_VENDAS)) confere(Object.keys(mats).every((k) => CLIENTE_DE[k] === cli), `outubro: ${cli} só compra os materiais dele`);
// compras de outubro que viram pedido fixo (dia e hora certos) e saem do plano do mês
const OUT_FIXOS = [ // [dia, hora, fornecedor, itens, forma, extra]
  ['2026-10-08', '09:35', 'valeforte', [['chaparia', 850]], 'transfer', {}], // T9/T18: a 1ª das três compras da Vale Forte (R$ 595,00)
  ['2026-10-21', '09:15', 'cida', [['al_latinha', 18], ['papelao', 138]], 'cash', { cx: 'M' }], // T9: #70 (R$ 187,50)
  ['2026-10-21', '10:12', 'siqueira', [['bateria', 240]], 'transfer', { cx: 'M' }], // T9: #70, a bateria da Vale Forte lançada no depósito
  ['2026-10-22', '10:20', 'valdir', [['ferro_pesado', 180]], 'cash', {}], // T10: lançada duas vezes; a cópia (10:24) é excluída
];
// cooperativa (item 2, T4/T20): às sextas, no saldo, paga por Pix na segunda seguinte; agosto 4, setembro 4, outubro 5 (iguais)
const COOP_MES = {
  '2026-08': { papelao: 6700, pet: 2050, al_latinha: 1000, chaparia: 850, ferro_misto: 700 },
  '2026-09': { papelao: 6900, pet: 2150, al_latinha: 1050, chaparia: 900, ferro_misto: 750 },
  [OUTM]: OUTUBRO_COMPRAS.recomeco,
};
const diasDe = (mes) => ({
  valdir: naSemana(mes, 1, 3, 5), cida: sorteia(diasDoMes(mes).filter((d) => d !== '2026-10-21'), diasDoMes(mes).length - 2),
  balcao: diasDoMes(mes), valeforte: { '2026-08': ['2026-08-05', '2026-08-14', '2026-08-25'], '2026-09': ['2026-09-04', '2026-09-15', '2026-09-25'], '2026-10': ['2026-10-15', '2026-10-29'] }[mes],
  siqueira: { '2026-08': ['2026-08-20'], '2026-09': ['2026-09-17'], '2026-10': ['2026-10-14', '2026-10-21'] }[mes],
  // vendas: Aços Quiririm às segundas, Fundição a cada duas terças, Serra Fina às sextas, o depósito quando vem descarregar
  quiririm: [...new Set([...naSemana(mes, 1).filter((d) => d > `${mes}-03`), ultimoDia(mes)])],
  bandeira: [...new Set([...naSemana(mes, 2).filter((_, i) => i % 2 === 0), ultimoDia(mes)])],
  serrafina: [...new Set([...naSemana(mes, 5), ultimoDia(mes)])],
  siqueira_v: { '2026-08': ['2026-08-20', '2026-08-31'], '2026-09': ['2026-09-17', '2026-09-30'], '2026-10': ['2026-10-14', '2026-10-21', '2026-10-30'] }[mes],
});
const subconj = (dias, n) => (n >= dias.length ? dias : sorteia(dias, n));
function planoCompras(mes, tabela) {
  const D = diasDe(mes);
  for (const [quem, mats] of Object.entries(tabela)) {
    if (quem === 'recomeco') continue; // sextas, no saldo: pedidos fixos
    for (const [mat, kg] of Object.entries(mats)) {
      let dias = D[quem];
      if (quem === 'valdir' && mat !== 'ferro_misto') dias = subconj(dias, mat === 'cobre_mel' ? 5 : mat === 'fio_cobre' ? 6 : 8);
      if (quem === 'balcao') dias = subconj(dias, { ferro_misto: 99, ferro_pesado: 10, chaparia: 10, cobre_mel: 12, cobre_misto: 6, fio_cobre: 8, al_latinha: 12, al_perfil: 6, al_bloco: 5, latao: 8, bronze: 8, inox: 6, bateria: 5, papelao: 8, pet: 6 }[mat] || 6);
      // T10: os dois lotes do depósito em outubro, 21.000 kg cada
      comprar(mes, quem, mat, kg, dias, quem === 'siqueira' && mat === 'ferro_pesado' && mes === OUTM ? [21000, 21000] : null);
    }
  }
}
function planoVendas(mes, porMaterial) {
  const D = diasDe(mes);
  for (const [mat, kg] of Object.entries(porMaterial)) {
    const quem = CLIENTE_DE[mat];
    let dias = quem === 'siqueira' ? D.siqueira_v : D[quem];
    if (mat === 'ferro_pesado' && mes === OUTM) dias = ['2026-10-19', '2026-10-26']; // depois dos dois lotes do depósito
    if (mat === 'inox') dias = dias.slice(-2);
    vender(mes, quem, mat, kg, dias);
  }
}
const COMPRADO_OUT = totalPorMaterial(OUTUBRO_COMPRAS);
const VENDIDO_OUT = totalPorMaterial(OUTUBRO_VENDAS);
confere(COMPRADO_OUT.ferro_pesado === 50000 && VENDIDO_OUT.ferro_pesado === 10000, 'outubro: 50 t de ferro pesado compradas e 10 t vendidas (T15)');
confere(valorDe(COMPRADO_OUT) === 256860 && valorDe(VENDIDO_OUT, 'pv') === 269240 && valorDe(VENDIDO_OUT) === 218860, 'outubro: compras R$ 256.860,00, vendas R$ 269.240,00, CMV R$ 218.860,00 (T15)');
{ // o plano de outubro: a tabela menos os pedidos fixos e a cooperativa
  const plano = Object.fromEntries(Object.entries(OUTUBRO_COMPRAS).map(([q, m]) => [q, { ...m }]));
  for (const [, , quem, its] of OUT_FIXOS) for (const [k, kg] of its) plano[quem][k] -= kg;
  for (const mats of Object.values(plano)) for (const k of Object.keys(mats)) if (!mats[k]) delete mats[k];
  planoCompras(OUTM, plano);
}
planoVendas(OUTM, VENDIDO_OUT);

// setembro e agosto (seção 6 / item 4): 93 % e 85 % de cada compra de outubro (ferro pesado fixo por fornecedor); a cooperativa
// fica com o histórico do T4 (14 compras, R$ 52.937,50 com a de 06/11) e o que a regra dava a mais para ela vai para a Dona Cida
// (papelão, PET e latinha) e para o balcão (chaparia e ferro misto): os quilos e o valor do mês não mudam
const escala = (tab, f, fp) => Object.fromEntries(Object.entries(tab).map(([q, mats]) => [q, Object.fromEntries(Object.entries(mats).map(([k, kg]) => [k, k === 'ferro_pesado' ? (fp[q] || 0) : roundPar(kg * f)]))]));
function regraDoMes(mes, f, fp) {
  const t = escala(OUTUBRO_COMPRAS, f, fp);
  for (const [k, kg] of Object.entries(t.recomeco)) {
    const quem = ['papelao', 'pet', 'al_latinha'].includes(k) ? 'cida' : 'balcao';
    t[quem][k] = (t[quem][k] || 0) + kg - COOP_MES[mes][k];
  }
  t.recomeco = { ...COOP_MES[mes] };
  return t;
}
const SETEMBRO_COMPRAS = regraDoMes('2026-09', 0.93, { siqueira: 3000, valdir: 2500, balcao: 2000 });
const AGOSTO_COMPRAS = regraDoMes('2026-08', 0.85, { siqueira: 1500, valdir: 2000, balcao: 2500 });
const DESCARGA_SET = { ferro_pesado: 2000, ferro_misto: 3000, chaparia: 1500, cobre_mel: 60, cobre_misto: 40, fio_cobre: 30, al_latinha: 300, al_perfil: 100, al_bloco: 100, latao: 40, bronze: 20, inox: 150, bateria: 500, papelao: 2000, pet: 400 };
const COMPRADO_SET = totalPorMaterial(SETEMBRO_COMPRAS);
confere(valorDe(COMPRADO_SET) === 201784.25 && valorDe(Object.fromEntries(KS.map((k) => [k, COMPRADO_SET[k] + DESCARGA_SET[k]])), 'pv') === 273047.73, `item 4: setembro planejado com compras R$ 201.784,25 e vendas R$ 273.047,73 (${valorDe(COMPRADO_SET)})`);

// novembro até 10/11 08:30 (seção 7 / item 7): só os fatos da linha do tempo
const NOV = '2026-11';
const PAPELAO_NEGATIVO = { de: at('2026-11-05', '16:10'), ate: at('2026-11-06', '10:45') }; // ver a nota em mov()
const NOVEMBRO = [ // [dia, hora, tipo, quem, itens ([material, kg bruto, impureza kg]), forma, extra]
  ['2026-11-03', '07:35', 'purchase', null, [['ferro_misto', 180]], 'cash'],
  ['2026-11-03', '08:47', 'purchase', 'cida', [['al_latinha', 38], ['papelao', 280]], 'cash'], // T9: a original (a cópia é a das 08:48)
  ['2026-11-03', '09:20', 'purchase', 'siqueira', [['ferro_pesado', 640]], 'transfer', { conta: 'secundaria' }], // T10: 42.500 kg
  ['2026-11-03', '09:40', 'purchase', 'siqueira', [['ferro_misto', 3000]], 'transfer', { conta: 'principal' }], // T14
  ['2026-11-03', '11:05', 'purchase', null, [['cobre_mel', 18]], 'cash'],
  ['2026-11-03', '11:30', 'sale', 'bandeira', [['latao', 600]], 'transfer', { conta: 'secundaria', notes: 'Latão da NF-e 1248 (emitida em 30/10)' }], // T17
  ['2026-11-03', '14:20', 'purchase', null, [['fio_cobre', 14], ['al_latinha', 12]], 'cash'],
  ['2026-11-03', '15:10', 'sale', 'bandeira', [['cobre_mel', 300]], 'parcelado'], // T13: 3x R$ 4.790,00
  ['2026-11-03', '16:10', 'sale', 'serrafina', [['al_perfil', 463]], 'transfer', { conta: 'principal' }], // T14
  ['2026-11-04', '08:15', 'purchase', 'cida', [['al_latinha', 42], ['papelao', 320]], 'cash'],
  ['2026-11-04', '09:10', 'purchase', null, [['ferro_misto', 240]], 'cash'],
  ['2026-11-04', '10:30', 'purchase', null, [['chaparia', 120]], 'cash'],
  ['2026-11-04', '14:30', 'sale', 'quiririm', [['ferro_pesado', 38992]], 'transfer', { conta: 'secundaria', motorista: 'Paulo Henrique', placa: 'FTQ3H52' }], // T10/T15: o ferro de outubro sai
  ['2026-11-04', '15:45', 'purchase', null, [['latao', 16]], 'cash'],
  ['2026-11-05', '08:05', 'purchase', 'cida', [['al_latinha', 35], ['papelao', 260]], 'cash'],
  ['2026-11-05', '09:25', 'purchase', null, [['ferro_misto', 150]], 'cash'],
  ['2026-11-05', '10:50', 'purchase', null, [['cobre_mel', 12.5]], 'cash'],
  ['2026-11-05', '11:05', 'purchase', 'valeforte', [['bateria', 640]], 'transfer', { conta: 'secundaria' }], // T16: NF-e 2157 dela
  ['2026-11-05', '13:40', 'purchase', null, [['bronze', 9], ['al_latinha', 8]], 'cash'],
  ['2026-11-05', '14:20', 'sale', 'quiririm', [['ferro_pesado', 2608], ['chaparia', 1000], ['ferro_misto', 600]], 'balance', { motorista: 'Paulo Henrique', placa: 'FTQ3H52' }], // T4/T13: +4.870
  ['2026-11-05', '16:10', 'sale', 'siqueira', [['papelao', 1250], ['pet', 100]], 'balance'], // T4
  ['2026-11-06', '07:40', 'purchase', 'cida', [['al_latinha', 47], ['papelao', 340]], 'cash'],
  ['2026-11-06', '08:30', 'purchase', null, [['chaparia', 160]], 'cash'],
  ['2026-11-06', '09:40', 'purchase', 'cida', [['pet', 200]], 'transfer', { conta: 'principal' }], // T14 (era "Cooperativa")
  ['2026-11-06', '09:50', 'purchase', 'siqueira', [['ferro_pesado', 1200], ['ferro_misto', 320], ['cobre_misto', 20]], 'balance'], // T4/T16: NF-e 884 dele
  ['2026-11-06', '10:45', 'purchase', 'recomeco', [['papelao', 1700], ['pet', 520], ['al_latinha', 240], ['chaparia', 220], ['ferro_misto', 180]], 'balance'], // T4/T20 (as 3 fotos ficam com a T20)
  ['2026-11-06', '11:50', 'purchase', null, [['latao', 22]], 'cash'],
  ['2026-11-06', '14:05', 'purchase', 'valeforte', [['ferro_pesado', 400]], 'transfer', { conta: 'principal' }], // T14
  ['2026-11-06', '15:05', 'purchase', null, [['inox', 85]], 'cash'],
  ['2026-11-06', '15:30', 'sale', 'quiririm', [['ferro_pesado', 1180]], 'transfer', { conta: 'secundaria', motorista: 'Paulo Henrique', placa: 'FTQ3H52' }], // T10
  // 09/11: as três compras do #83 do Marcos (T16, R$ 803,30) e, no #84 do Rafael, a venda da T16 e a compra do T10 (Pix)
  ['2026-11-09', '08:12', 'purchase', 'cida', [['al_latinha', 38], ['papelao', 120]], 'cash'],
  ['2026-11-09', '10:40', 'sale', 'bandeira', [['cobre_mel', 506, 6]], 'transfer', { conta: 'secundaria' }], // T16: 500 kg líquidos, sem nota
  ['2026-11-09', '10:47', 'purchase', 'valdir', [['ferro_misto', 410]], 'cash'],
  ['2026-11-09', '15:20', 'purchase', 'siqueira', [['ferro_pesado', 860]], 'transfer', { conta: 'secundaria' }], // T10 (as 2 fotos ficam com o T10)
  ['2026-11-09', '15:26', 'purchase', 'cida', [['al_latinha', 26], ['papelao', 60]], 'cash'],
];
// o que entra e sai em novembro define o estoque de 31/10 (de trás para a frente a partir do de hoje)
const NOV_LIQ = Object.fromEntries(KS.map((k) => [k, 0]));
for (const [, , tipo, , its] of NOVEMBRO) for (const [k, kg, imp = 0] of its) NOV_LIQ[k] += (tipo === 'purchase' ? 1 : -1) * (kg - imp);
const AJUSTE_3110 = -14; // T10: "Contagem do pátio no fechamento do mês" (31/10, sábado, 12:40)
const EST_3110 = Object.fromEntries(KS.map((k) => [k, r1(ESTOQUE_HOJE[k] - NOV_LIQ[k])]));
const SECAO4_3110 = { ferro_pesado: 41860, ferro_misto: 2540, chaparia: 4250, cobre_mel: 811.5, cobre_misto: 128, fio_cobre: 82, al_latinha: 154, al_perfil: 3848, al_bloco: 2830, latao: 776, bronze: 29, inox: 175, bateria: 3320, papelao: 20, pet: 300 };
confere(KS.every((k) => EST_3110[k] === SECAO4_3110[k]), `seção 4: estoque em 31/10 23:59 (${KS.filter((k) => EST_3110[k] !== SECAO4_3110[k]).map((k) => `${k} ${EST_3110[k]}`).join(', ')})`);
const EST_3009 = Object.fromEntries(KS.map((k) => [k, r1(EST_3110[k] - (COMPRADO_OUT[k] - VENDIDO_OUT[k]) - (k === 'ferro_pesado' ? AJUSTE_3110 : 0))]));
confere(EST_3009.ferro_pesado === 1874 && EST_3009.ferro_misto === 252 && EST_3009.pet === 127 && KS.every((k) => EST_3009[k] >= 0), 'seção 4: em 30/09 nada fica negativo (ferro pesado 1.874, ferro misto 252, PET 127)');
const EST_3108 = Object.fromEntries(KS.map((k) => [k, r1(EST_3009[k] + DESCARGA_SET[k])]));
const ACUMULA_AGO = Object.fromEntries(KS.map((k) => [k, Math.round((EST_3108[k] - (LOTE_PARADO[k] || 0)) * 0.35)]));
const EST_0108 = Object.fromEntries(KS.map((k) => [k, r1(EST_3108[k] - ACUMULA_AGO[k])]));
planoCompras('2026-09', SETEMBRO_COMPRAS);
planoVendas('2026-09', Object.fromEntries(KS.map((k) => [k, COMPRADO_SET[k] + DESCARGA_SET[k]])));
planoCompras('2026-08', AGOSTO_COMPRAS);
const COMPRADO_AGO = totalPorMaterial(AGOSTO_COMPRAS);
confere(KS.every((k) => COMPRADO_AGO[k] - ACUMULA_AGO[k] >= 0), 'agosto: o pátio cresce sem vender menos que zero');
planoVendas('2026-08', Object.fromEntries(KS.map((k) => [k, COMPRADO_AGO[k] - ACUMULA_AGO[k]])));
// valor planejado das vendas do mês (base do imposto sobre vendas)
const vendasPlanejadas = (mes) => r2(OUT_PLAN.vendas.filter((v) => v.mes === mes).reduce((s, v) => s + v.kg * MAT[v.mat].pv, 0));

// despesas e receitas fora dos pedidos: { d, h, cat, cc, valor, desc, conta, receita }
const DESPESAS = [];
const desp = (d, h, cat, cc, valor, desc, conta = 'principal') => DESPESAS.push({ d, h, cat, cc, valor: r2(valor), desc, conta });
function despesasFixas(mes, c) {
  const dia = (n) => { let d = `${mes}-${pad(n)}`; while (!util(d)) d = addDays(d, 1); return d; };
  desp(dia(1), '08:00', 'tarifas', null, 89.9, 'Tarifa do pacote de serviços');
  desp(dia(5), '09:00', 'aluguel', 'patio', c.aluguel, 'Aluguel do galpão');
  const quinto = diasDoMes(mes)[4];
  desp(quinto, '16:00', 'folha', 'patio', c.folha[0], 'Salários do pátio');
  desp(quinto, '16:02', 'folha', 'coleta', c.folha[1], 'Salários dos motoristas');
  desp(quinto, '16:04', 'folha', null, c.folha[2], 'Salários do escritório');
  desp(c.energia[0], c.energia[1], 'energia', 'patio', c.energia[2], 'Conta de energia');
  c.combustivel.forEach(([d, v, desc]) => desp(d, '11:20', 'combustivel', 'coleta', v, desc));
  if (c.manutencao) desp(c.manutencao[0], '10:30', 'manut_veiculos', 'coleta', c.manutencao[1], c.manutencao[2]);
  desp(dia(15), '09:30', 'telefone', null, 289.9, 'Internet e telefone do escritório');
  desp(dia(20), '11:00', 'impostos_vendas', null, c.impostos, 'DARF PIS/COFINS sobre vendas');
  c.frete.forEach(([d, v]) => desp(d, '17:10', 'frete', null, v, 'Frete da carga do Depósito Irmãos Siqueira'));
  desp(ultimoDia(mes), '18:00', 'tarifas', null, c.tarifasPix, 'Tarifas de Pix e TED do mês');
  c.cacamba.forEach(([d, v, desc, cli]) => DESPESAS.push({ d, h: '10:15', cat: 'aluguel_cacamba', cc: 'coleta', valor: v, desc, conta: 'principal', receita: true, cli }));
}
despesasFixas(OUTM, { // T15: os lançamentos de outubro (a energia uma vez só; a duplicata das 16:40 é semente do T15)
  aluguel: 6500, folha: [14300, 3100, 2400], energia: ['2026-10-13', '09:12', 3850], impostos: 3574.1, tarifasPix: 96.1,
  combustivel: [['2026-10-02', 1120, 'Diesel do caminhão truck'], ['2026-10-09', 1060, 'Diesel do caminhão 3/4'], ['2026-10-16', 1050, 'Diesel do caminhão truck'], ['2026-10-23', 1050, 'Diesel e gasolina da picape']],
  manutencao: ['2026-10-20', 1950, 'Revisão do caminhão 3/4'], frete: [['2026-10-14', 1200], ['2026-10-21', 1200]],
  // item 5: as NFS-e 12 e 13 da T17 são as receitas de caçamba do T15
  cacamba: [['2026-10-13', 950, 'Aluguel de caçamba - Fundição Bandeira do Vale (NFS-e 12)', 'bandeira'], ['2026-10-29', 1850, 'Coleta com caçamba - Aços Quiririm (NFS-e 13)', 'quiririm']],
});
despesasFixas('2026-09', {
  aluguel: 6500, folha: [14300, 3100, 2400], energia: ['2026-09-14', '09:05', 3420], impostos: r2(vendasPlanejadas('2026-09') * 0.013275), tarifasPix: 82.5,
  combustivel: [['2026-09-04', 990, 'Diesel do caminhão truck'], ['2026-09-11', 990, 'Diesel do caminhão 3/4'], ['2026-09-18', 990, 'Diesel do caminhão truck'], ['2026-09-25', 990, 'Diesel e gasolina da picape']],
  manutencao: ['2026-09-22', 780, 'Troca de pneu da picape'], frete: [['2026-09-17', 1800]],
  cacamba: [['2026-09-10', 1400, 'Aluguel de caçamba - obra no Jardim das Nações'], ['2026-09-24', 700, 'Aluguel de caçamba - limpeza de terreno']],
});
despesasFixas('2026-08', {
  aluguel: 6500, folha: [13600, 3100, 2200], energia: ['2026-08-13', '09:10', 3180], impostos: r2(vendasPlanejadas('2026-08') * 0.013275), tarifasPix: 71.3,
  combustivel: [['2026-08-07', 910, 'Diesel do caminhão truck'], ['2026-08-14', 910, 'Diesel do caminhão 3/4'], ['2026-08-21', 910, 'Diesel do caminhão truck'], ['2026-08-28', 910, 'Diesel e gasolina da picape']],
  manutencao: ['2026-08-18', 1240, 'Revisão do caminhão truck'], frete: [['2026-08-20', 1200]],
  cacamba: [['2026-08-26', 1400, 'Aluguel de caçamba - obra no Jardim das Nações']],
});
// novembro (item 6 e 8): sem tarifa; aluguel do galpão às 10:05 na Principal (a conta paga do T13); diesel e a folha do 5º dia
// útil (09/11) na Secundária
desp('2026-11-05', '10:05', 'aluguel', 'patio', 6800, 'Aluguel do galpão de novembro');
desp('2026-11-05', '11:20', 'combustivel', 'coleta', 1180, 'Diesel do caminhão truck', 'secundaria');
desp('2026-11-09', '16:00', 'folha', null, 19800, 'Folha de outubro (pátio, motoristas e escritório)', 'secundaria');

// ---------------------------------------------------------------- execução: dia a dia, como o app gravaria
// numeração compartilhada compra/venda (template #{NUM}); começa onde a compra de 860 kg de 09/11 vira a #1757 e o último pedido
// antes de hoje a #1758, como na semente de 51224e1 (a semente do T10 aponta para a #1757; a do T9 e o T8 seguem da #1759)
let ordem = 1252;
let caixaNum = 0;
const estoque = { ...EST_0108 };
let cofre = 0; // saldo do cofre pela regra do app (lançamentos do caixa com sinal + extrato da conta dinheiro)
const saldoParceiro = {}; // "tipo:id" -> saldo
const SINAL = { sale: 1, purchase: -1, deposit: 1, withdrawal: -1, expense: -1, adjustment: 1 };
const NEGATIVOS = [];

function bankTx(contaK, d, hhmm, type, amount, description, extra = {}) {
  const row = add('bank_transactions', {
    id: id(`bt.${T.bank_transactions?.length || 0}`), company_id: COMPANY, bank_account_id: id(`banco.${contaK}`), type, amount: r2(amount), description,
    transaction_at: at(d, hhmm), transaction_date: d, created_at: at(d, hhmm), created_by: RAFAEL, source: 'manual', excluded_from_dre: false, ...extra,
  });
  if (contaK === 'cofre') cofre = r2(cofre + row.amount);
  return row;
}
function cashTx(caixa, d, hhmm, type, amount, description, extra = {}) {
  const row = add('cash_transactions', {
    id: id(`ct.${T.cash_transactions?.length || 0}`), company_id: COMPANY, cash_register_id: caixa ? caixa.id : null, type, amount: r2(amount), description,
    transaction_at: at(d, hhmm), transaction_date: d, created_at: at(d, hhmm), created_by: caixa?.opened_by || RAFAEL, excluded_from_dre: false, ...extra,
  });
  if (!['opening', 'closing', 'transfer'].includes(type)) cofre = r2(cofre + (SINAL[type] || 0) * row.amount);
  if (caixa && type !== 'opening' && type !== 'closing') caixa.saldo = r2(caixa.saldo + (SINAL[type] || 0) * row.amount);
  return row;
}
function saldo(tipo, entityId, valor, d, hhmm, desc, extra = {}) {
  // update_balance: o parceiro duplo (Siqueira) usa a linha 'party' do lado do cliente, com o sinal invertido no fornecedor
  let et = tipo, eid = entityId, v = valor;
  if (entityId === id('fornecedor.siqueira')) { et = 'party'; eid = id('cliente.siqueira'); v = -valor; }
  else if (entityId === id('cliente.siqueira')) et = 'party';
  const key = `${et}:${eid}`;
  saldoParceiro[key] = r2((saldoParceiro[key] || 0) + v);
  add('balance_movements', {
    id: id(`bm.${T.balance_movements?.length || 0}`), company_id: COMPANY, balance_id: id(`saldo.${key}`), entity_type: tipo, entity_id: entityId,
    movement_type: extra.movement_type || 'order', amount: r2(valor), description: desc, transaction_at: at(d, hhmm), transaction_date: d,
    created_at: at(d, hhmm), created_by: extra.created_by || RAFAEL, is_settled: false, ...extra,
  });
}
function mov(material, d, hhmm, qtd, type, order, desc, quem = RAFAEL) {
  const before = r1(estoque[material]);
  const after = r1(before + qtd);
  if (after < 0) {
    // seção 7: a venda de 1.250 kg de papelão ao depósito (05/11 16:10) é maior que o papelão que entrou em novembro antes dela
    // (o de 31/10 é 20 kg); só a cooperativa de 06/11 10:45 cobre. Única exceção aceita (anotada no relatório do gerador).
    const t = at(d, hhmm);
    confere(material === 'papelao' && t >= PAPELAO_NEGATIVO.de && t < PAPELAO_NEGATIVO.ate, `estoque negativo: ${material} em ${d} ${hhmm} (${before} ${qtd >= 0 ? '+' : ''}${qtd})`);
    NEGATIVOS.push(`${material} ${after} kg em ${d} ${hhmm}`);
  }
  estoque[material] = after;
  add('stock_movements', {
    id: id(`sm.${T.stock_movements?.length || 0}`), company_id: COMPANY, material_id: MAT[material].id, type, quantity: r1(qtd), stock_before: before, stock_after: after,
    order_id: order?.id || null, order_type: order?.tipo || null, description: desc, created_by: quem, transaction_at: at(d, hhmm), transaction_date: d, created_at: at(d, hhmm),
  });
}
const PEDIDOS = []; // resumo para as conferências
/** Pedido de compra ou venda completo (cabeçalho, itens, estoque, pagamento), como create_*_atomic faria. Item: [material, kg bruto, impureza kg]. */
function pedido(tipo, d, hhmm, parceiroK, itens, forma, caixa, extra = {}) {
  const num = ++ordem;
  const isCompra = tipo === 'purchase';
  const pid = id(`${isCompra ? 'compra' : 'venda'}.${num}`);
  const its = itens.map(([m, kg, imp = 0]) => { const q = r1(kg - imp); const p = isCompra ? MAT[m].pc : MAT[m].pv; return { m, bruto: r1(kg), imp, q, p, total: r2(q * p) }; });
  const total = r2(its.reduce((s, it) => s + it.total, 0));
  const quem = caixa?.opened_by || RAFAEL;
  const head = {
    id: pid, company_id: COMPANY, order_number: num, order_seq: num, order_period: null, order_ref: `#${num}`, status: 'completed',
    total_amount: total, paid_amount: total, payment_method: forma === 'parcelado' ? 'balance' : forma, created_by: quem, transaction_at: at(d, hhmm), transaction_date: d,
    created_at: at(d, hhmm), currency: 'BRL', hide_financial_details: false, notes: extra.notes || null,
    driver_name: extra.motorista || null, vehicle_plate: extra.placa || null, driver_id: null, vehicle_id: null,
  };
  if (isCompra) head.supplier_id = parceiroK ? id(`fornecedor.${parceiroK}`) : null;
  else head.customer_id = id(`cliente.${parceiroK}`);
  add(isCompra ? 'purchases' : 'sales', head);
  its.forEach((it, i) => {
    add(isCompra ? 'purchase_items' : 'sale_items', {
      id: id(`${isCompra ? 'pi' : 'si'}.${num}.${i}`), [isCompra ? 'purchase_id' : 'sale_id']: pid, material_id: MAT[it.m].id, material_name: MAT[it.m].nome,
      quantity: it.bruto, unit_price: it.p, total_price: it.total, impurity: it.imp, impurity_kg: it.imp || null, impurity_pct: it.imp ? r2((it.imp / it.bruto) * 100) : null, item_discount: 0,
      tare_weight: null, first_weight: null, second_weight: null, weighing_mode: null, weight_source: 'manual',
    });
    if (!extra.semEstoque) mov(it.m, d, hhmm, isCompra ? it.q : -it.q, isCompra ? 'COMPRA' : 'VENDA', { id: pid, tipo }, `${isCompra ? 'Compra' : 'Venda'} #${num}`, quem);
  });
  const rotulo = isCompra ? 'Compra' : 'Venda';
  if (forma === 'cash') cashTx(caixa, d, hhmm, tipo, total, `${rotulo} #${num}`, { order_id: pid });
  else if (forma === 'transfer') {
    bankTx(extra.conta || 'principal', d, hhmm, isCompra ? 'withdrawal' : 'deposit', isCompra ? -total : total, `${rotulo} #${num}`, { order_id: pid, payment_method: 'transfer', created_by: quem });
    if (caixa) cashTx(caixa, d, hhmm, tipo, 0, `${rotulo} #${num} (PIX/Transferência)`, { order_id: pid });
  } else {
    saldo(isCompra ? 'supplier' : 'customer', isCompra ? id(`fornecedor.${parceiroK}`) : id(`cliente.${parceiroK}`), total, d, hhmm, `${rotulo} #${num}`, { order_id: pid, payment_method: 'balance', created_by: quem });
    if (caixa) cashTx(caixa, d, hhmm, tipo, 0, `${rotulo} #${num} (Saldo)`, { order_id: pid });
  }
  const p = { tipo, d, hhmm, num, id: pid, parceiroK, total, its, forma, conta: forma === 'transfer' ? extra.conta || 'principal' : null, caixa: caixa?.id || null };
  PEDIDOS.push(p);
  return p;
}

// estoque de partida (01/08, com o lote parado) e saldos iniciais (dinheiro e bancos fora da DRE)
for (const k of KS) add('stock_movements', { id: id(`sm.inicial.${k}`), company_id: COMPANY, material_id: MAT[k].id, type: 'SALDO_INICIAL', quantity: EST_0108[k], stock_before: 0, stock_after: EST_0108[k], description: 'Saldo inicial de estoque', created_by: RAFAEL, transaction_at: at(INICIO, '07:00'), transaction_date: INICIO, created_at: at(INICIO, '07:00') });
const ajusteIni = cashTx(null, INICIO, '07:15', 'adjustment', 20000, 'Saldo inicial do dinheiro (ativação do cofre)', { excluded_from_dre: true });
const iniPrincipal = bankTx('principal', INICIO, '07:00', 'deposit', 0, 'Saldo inicial', { excluded_from_dre: true });
bankTx('secundaria', INICIO, '07:00', 'deposit', 25000, 'Saldo inicial', { excluded_from_dre: true }); // item 8: R$ 25.000,00 até 31/10

// as linhas do plano viram eventos por dia (compras de manhã e à tarde, vendas no fim da tarde)
const porDia = new Map(); // dia -> eventos
const evento = (d, e) => { if (!porDia.has(d)) porDia.set(d, []); porDia.get(d).push(e); };
for (const c of OUT_PLAN.compras) (c.partes || split(c.kg, c.dias.length)).forEach((kg, i) => evento(c.dias[i], { kind: 'compra', quem: c.quem, mat: c.mat, kg }));
const carry = new Map(); // venda planejada que não coube no estoque do dia passa para a próxima data do mesmo cliente
for (const v of OUT_PLAN.vendas) {
  const partes = split(v.kg, v.dias.length, 0.3);
  partes.forEach((kg, i) => evento(v.dias[i], { kind: 'venda', quem: v.quem, mat: v.mat, kg, chave: `${v.mes}:${v.quem}:${v.mat}`, ultima: i === partes.length - 1 }));
}
for (const [d, h, quem, its, forma, extra] of OUT_FIXOS) evento(d, { kind: 'fixo', h, tipo: 'purchase', quem, its, forma, extra });
evento('2026-10-22', { kind: 'duplicada', h: '10:24', quem: 'valdir', mat: 'ferro_pesado', kg: 180, excluida: '11:02' });
// a cooperativa: um pedido por sexta (no saldo) e o Pix na segunda seguinte (a de 30/10 só em 03/11, da Secundária)
for (const mes of ['2026-08', '2026-09', OUTM]) {
  const sextas = naSemana(mes, 5);
  const partes = Object.fromEntries(Object.entries(COOP_MES[mes]).map(([k, kg]) => [k, splitIgual(kg, sextas.length)]));
  sextas.forEach((d, i) => {
    const its = Object.keys(partes).map((k) => [k, partes[k][i]]);
    evento(d, { kind: 'fixo', h: '10:45', tipo: 'purchase', quem: 'recomeco', its, forma: 'balance', extra: {} });
    const paga = proximoUtil(d);
    evento(paga, { kind: 'pagSaldo', h: paga === '2026-11-03' ? '10:00' : '09:30', tipo: 'supplier', quem: 'recomeco', valor: valorDe(Object.fromEntries(its)), via: 'transfer', conta: paga === '2026-11-03' ? 'secundaria' : 'principal' });
  });
}
for (const [d, h, tipo, quem, its, forma, extra] of NOVEMBRO) evento(d, { kind: 'fixo', h, tipo, quem, its, forma, extra: extra || {} });
// T9: a compra de 03/11 da Aparecida lançada duas vezes; a cópia (08:48) é estornada em 05/11 com o caixa de 03/11 já fechado
evento('2026-11-03', { kind: 'copia', h: '08:48', quem: 'cida', its: [['al_latinha', 38], ['papelao', 280]] });
evento('2026-11-05', { kind: 'estorno', h: '08:20' });
for (const e of DESPESAS) evento(e.d, { kind: 'despesa', ...e });
// T4: vale de R$ 300,00 em dinheiro ao Valdir (03/11), adiantamento da Serra Fina (06/11) e Pix parcial à cooperativa (09/11)
evento('2026-11-03', { kind: 'pagSaldo', h: '08:40', tipo: 'supplier', quem: 'valdir', valor: 300, via: 'cash' });
evento('2026-11-06', { kind: 'pagSaldo', h: '11:30', tipo: 'customer', quem: 'serrafina', valor: 1500, via: 'transfer', conta: 'secundaria' });
evento('2026-11-09', { kind: 'pagSaldo', h: '10:10', tipo: 'supplier', quem: 'recomeco', valor: 1150, via: 'transfer', conta: 'secundaria' });
// cofre: reforço do banco às segundas e quintas até outubro (o pátio paga carroceiro e balcão em dinheiro); em novembro não há
// transferência entre banco e cofre (item 8): o reforço de 29/10 cobre o dinheiro até 09/11 e o cofre fecha em R$ 18.500,00
const valorFixo = (e) => r2(e.its.reduce((a, [k, kg, imp = 0]) => a + (kg - imp) * MAT[k][e.tipo === 'sale' ? 'pv' : 'pc'], 0));
const saidaDinheiro = (d) => (porDia.get(d) || []).reduce((s, e) => {
  if (e.kind === 'compra' && ['valdir', 'cida', 'balcao'].includes(e.quem)) return s + e.kg * MAT[e.mat].pc;
  if (e.kind === 'fixo' && e.forma === 'cash') return s + (e.tipo === 'sale' ? -1 : 1) * valorFixo(e);
  if (e.kind === 'copia') return s + valorFixo({ ...e, tipo: 'purchase' });
  if (e.kind === 'estorno') return s - valorFixo({ its: [['al_latinha', 38], ['papelao', 280]], tipo: 'purchase' });
  if (e.kind === 'pagSaldo' && e.via === 'cash') return s + e.valor;
  return s;
}, 0);
const diaDeReforco = (d, i) => d < '2026-11-01' && (i === 0 || weekday(d) === 1 || weekday(d) === 4 || FERIADOS.has(addDays(d, -1)) && weekday(d) === 2);
let ultimoReforco = null;
let COPIA = null;

const CAIXAS = [];
DIAS.forEach((d, iDia) => {
  const evs = porDia.get(d) || [];
  if (diaDeReforco(d, iDia)) {
    let ate = iDia + 1; while (ate < DIAS.length && !diaDeReforco(DIAS[ate], ate)) ate++;
    const precisa = DIAS.slice(iDia, ate).reduce((s, x) => s + saidaDinheiro(x), 0);
    let valor = Math.ceil((precisa + 6000 - cofre) / 1000) * 1000;
    if (ate >= DIAS.length) valor = r2(18500 + precisa - cofre); // o último: o cofre chega a 09/11 com R$ 18.500,00
    if (valor !== 0) {
      const g = id(`grupo_transf.${d}`);
      if (valor > 0) ultimoReforco = { d, banco: bankTx('principal', d, '07:10', 'transfer', -valor, 'Transferência para DINHEIRO (COFRE)', { group_id: g }), cofre: bankTx('cofre', d, '07:10', 'transfer', valor, 'Transferência de Conta Principal', { group_id: g }) };
      else { valor = -valor; bankTx('cofre', d, '07:10', 'transfer', -valor, 'Transferência para Conta Principal', { group_id: g }); bankTx('principal', d, '07:10', 'transfer', valor, 'Transferência de DINHEIRO (COFRE)', { group_id: g }); }
    }
  }
  // caixas do dia: o do Marcos (07:02 a 07:06) e, nos dias dele, o do Rafael (07:58; em dia de carga, 06:55, antes do Marcos)
  const abre = (uid, hh, fecha) => {
    caixaNum++;
    const cx = add('cash_register', { id: id(`caixa.${caixaNum}`), company_id: COMPANY, register_number: caixaNum, status: 'closed', opened_at: at(d, hh), opened_by: uid, initial_opening_balance: 0, opening_balance: 0, closing_balance: null, closed_at: at(d, fecha), currency: 'BRL', created_at: at(d, hh) });
    cx.saldo = 0; cx._fecha = fecha; cx._abertura = cashTx(cx, d, hh, 'opening', 0, `Abertura do Caixa #${caixaNum}`);
    CAIXAS.push({ d, num: caixaNum, uid, cx });
    return cx;
  };
  const carga = CARGA.has(d);
  const cxR0 = carga ? abre(RAFAEL, '06:55', '17:44') : null;
  let hM = hm(7 * 60 + 2 + Math.floor(rnd() * 5)), fM = hm(17 * 60 + 33 + Math.floor(rnd() * 6));
  if (d === '2026-10-21') { hM = '07:02'; fM = '17:31'; } // T9: #70, 07:02 -> 17:31
  if (d === '2026-11-09') { hM = '07:02'; fM = '17:36'; } // seção 9: #83, 07:02 -> 17:36
  const cxM = abre(MARCOS, hM, fM);
  const cxR = carga ? cxR0 : RAFAEL_ABRE.has(d) ? abre(RAFAEL, '07:58', '17:44') : null;
  // em 21/10 o #70 do Marcos só tem as duas compras da T9 (as com cx 'M'); o resto do dia vai para o caixa do Rafael
  const caixaPara = (forma, e = {}) => (e.cx === 'M' ? cxM : d === '2026-10-21' ? cxR : forma === 'cash' || !cxR ? cxM : cxR);
  // agrupa as compras do plano em pedidos: fornecedor cadastrado = um pedido por dia; balcão = um por material
  const compras = new Map();
  for (const e of evs.filter((x) => x.kind === 'compra')) {
    const k = e.quem === 'balcao' ? `balcao:${e.mat}` : e.quem;
    if (!compras.has(k)) compras.set(k, { quem: e.quem === 'balcao' ? null : e.quem, its: [] });
    compras.get(k).its.push([e.mat, e.kg]);
  }
  const fila = [];
  const formaDe = (q) => (['siqueira', 'valeforte'].includes(q) ? 'transfer' : 'cash');
  for (const c of compras.values()) fila.push({ h: null, run: (h) => pedido('purchase', d, h, c.quem, c.its, formaDe(c.quem), caixaPara(formaDe(c.quem))) });
  // horários das compras soltas: de 07:20 a 16:30, em ordem aleatória
  fila.sort(() => rnd() - 0.5);
  const passo = Math.max(6, Math.floor((16 * 60 + 30 - (7 * 60 + 20)) / Math.max(1, fila.length)));
  fila.forEach((f, i) => { f.h = hm(7 * 60 + 20 + i * passo + Math.floor(rnd() * Math.max(1, passo - 4))); });
  for (const e of evs.filter((x) => ['fixo', 'despesa', 'pagSaldo', 'duplicada', 'copia', 'estorno'].includes(x.kind))) fila.push({ h: e.h, e });
  // vendas do plano: no fim da tarde, um pedido por cliente
  const vendas = new Map();
  for (const e of evs.filter((x) => x.kind === 'venda')) { if (!vendas.has(e.quem)) vendas.set(e.quem, []); vendas.get(e.quem).push(e); }
  let hv = 16 * 60 + 35;
  for (const [quem, lst] of vendas) { const h = hm(hv); hv += 5; fila.push({ h, venda: { quem, lst } }); }
  fila.sort((a, b) => a.h.localeCompare(b.h));
  for (const f of fila) {
    if (f.run) { f.run(f.h); continue; }
    if (f.venda) {
      const its = [];
      for (const e of f.venda.lst) {
        const quer = e.kg + (carry.get(e.chave) || 0);
        const kg = e.ultima ? quer : Math.min(quer, Math.floor(estoque[e.mat]));
        carry.set(e.chave, quer - kg);
        if (kg > 0) its.push([e.mat, kg]);
      }
      if (its.length) pedido('sale', d, f.h, f.venda.quem, its, 'transfer', caixaPara('transfer'), f.venda.quem === 'quiririm' ? { motorista: 'Paulo Henrique', placa: 'FTQ3H52' } : {});
      continue;
    }
    const e = f.e;
    if (e.kind === 'fixo') {
      const p = pedido(e.tipo, d, e.h, e.quem, e.its, e.forma, caixaPara(e.forma, e.extra), e.extra);
      if (e.forma === 'parcelado') { // T13: 3 parcelas a receber com o pedido; o saldo do cliente fica todo itemizado
        const parc = r2(p.total / 3);
        ['2026-11-17', '2026-12-17', '2027-01-18'].forEach((due, i) => add('financial_bills', {
          id: id(`titulo.fiado_bandeira.${i + 1}`), company_id: COMPANY, direction: 'receivable', description: `Fatura venda #${p.num} (parcela ${i + 1}/3)`, amount: i < 2 ? parc : r2(p.total - 2 * parc), currency: 'BRL',
          due_date: due, status: 'pending', paid_amount: 0, order_id: p.id, order_type: 'sale', partner_id: id('cliente.bandeira'), partner_type: 'customer',
          installment_number: i + 1, installment_total: 3, payment_condition_id: id('condicao.30_60_90'), source_type: 'order', category_id: id('categoria.venda_sucata'), cost_center_id: null,
          created_by: RAFAEL, created_at: at(d, e.h), updated_at: at(d, e.h),
        }));
      }
    } else if (e.kind === 'copia') { // pedido normal no caixa do Marcos, sem estoque (o estorno apaga os movimentos dele)
      COPIA = { p: pedido('purchase', d, e.h, e.quem, e.its, 'cash', cxM, { semEstoque: true }), cx: cxM };
    } else if (e.kind === 'estorno') { // revert_consolidated_order_atomic, modo compensado: o caixa de 03/11 fica como estava
      const p = COPIA.p;
      cashTx(cxM, d, e.h, 'deposit', p.total, `Estorno do pedido #${p.num} (caixa 03/11/2026)`, { reversal_for_order_id: p.id, created_by: RAFAEL });
      Object.assign(T.purchases.find((x) => x.id === p.id), { reverted_at: at(d, e.h), reverted_compensation_register_id: cxM.id, original_order_number: p.num, order_number: null, order_seq: null, order_period: null });
      p.revertido = true;
    } else if (e.kind === 'duplicada') {
      const num = ++ordem; const pid = id(`compra.${num}`);
      mov(e.mat, d, e.h, e.kg, 'COMPRA', { id: pid, tipo: 'purchase' }, `Compra #${num}`, MARCOS);
      mov(e.mat, d, e.excluida, -e.kg, 'EXCLUSAO', { id: pid, tipo: 'purchase' }, `Exclusão do pedido #${num} (lançado em duplicidade)`, RAFAEL);
    } else if (e.kind === 'despesa') {
      const extra = { category_id: id(`categoria.${e.cat}`), cost_center_id: e.cc ? id(`cc.${e.cc}`) : null, payment_method: 'transfer' };
      if (e.receita) bankTx(e.conta, d, e.h, 'deposit', e.valor, e.desc, extra);
      else bankTx(e.conta, d, e.h, 'withdrawal', -e.valor, e.desc, extra);
    } else if (e.kind === 'pagSaldo') {
      const ent = id(`${e.tipo === 'supplier' ? 'fornecedor' : 'cliente'}.${e.quem}`);
      const pagando = e.tipo === 'supplier'; // a Recicla paga (fornecedor) ou recebe (cliente)
      if (e.via === 'cash') cashTx(cxM, d, e.h, 'withdrawal', e.valor, 'Pagamento de saldo', { excluded_from_dre: true, partner_id: ent, partner_type: e.tipo });
      else bankTx(e.conta || 'principal', d, e.h, pagando ? 'withdrawal' : 'deposit', pagando ? -e.valor : e.valor, pagando ? 'Pagamento de saldo' : 'Recebimento de saldo', { excluded_from_dre: true, payment_method: 'transfer', partner_id: ent, partner_type: e.tipo });
      saldo(e.tipo, ent, -e.valor, d, e.h, pagando ? 'Baixa de saldo (Pagamento)' : 'Baixa de saldo (Recebimento)', { movement_type: 'payment', payment_method: e.via, created_by: e.via === 'cash' ? MARCOS : RAFAEL });
    }
  }
  // abertura: o troco que o caixa precisa para pagar o dia sem faltar (sai do cofre; abertura e fechamento não mexem nele)
  for (const cx of [cxR0, cxM, carga ? null : cxR].filter(Boolean)) {
    const rows = T.cash_transactions.filter((x) => x.cash_register_id === cx.id && x.type !== 'opening');
    let s = 0, min = 0;
    for (const x of rows.sort((a, b) => a.transaction_at.localeCompare(b.transaction_at))) { s = r2(s + (SINAL[x.type] || 0) * x.amount); min = Math.min(min, s); }
    // seção 9: em 09/11 o #83 (Marcos) fecha com R$ 640,00 e o #84 (Rafael) com R$ 1.250,00; o #70 (21/10) abre com R$ 800,00
    const sobra = d === '2026-11-09' ? (cx === cxM ? 640 : 1250) : cx.opened_by === RAFAEL ? 1000 : 300 + Math.floor(rnd() * 12) * 100;
    let abertura = d === '2026-11-09' ? r2(sobra - s) : Math.max(cx.opened_by === RAFAEL ? 1000 : 1500, Math.ceil((sobra - min) / 100) * 100);
    if (d === '2026-10-21' && cx === cxM) abertura = 800;
    confere(abertura + min >= 0, `caixa #${cx.register_number} sem dinheiro para o dia`);
    cx._abertura.amount = abertura;
    cx.initial_opening_balance = abertura;
    cx.closing_balance = r2(abertura + s);
    cx.opening_balance = cx.closing_balance;
    cashTx(cx, d, cx._fecha, 'closing', cx.closing_balance, 'Fechamento de caixa');
    delete cx.saldo; delete cx._abertura; delete cx._fecha;
  }
  // 31/10 (sábado, sem caixa): contagem do pátio no fechamento do mês (T10), logo depois de sexta 30/10
  if (d === '2026-10-30') {
    mov('ferro_pesado', '2026-10-31', '12:40', AJUSTE_3110, 'EDICAO_MANUAL', null, 'Contagem do pátio no fechamento do mês', RAFAEL);
    confere(estoque.ferro_pesado === 41860, `ferro pesado em 31/10: ${estoque.ferro_pesado}`);
    confere(KS.every((k) => estoque[k] === SECAO4_3110[k]), `estoque em 31/10 23:59 da seção 4 (${KS.filter((k) => estoque[k] !== SECAO4_3110[k]).map((k) => `${k} ${estoque[k]}`).join(', ')})`);
  }
});
for (const d of porDia.keys()) confere(DIAS.includes(d), `evento fora de dia útil: ${d}`);
for (const [k, v] of carry) confere(Math.abs(v) < 1e-9, `venda planejada que sobrou: ${k} (${v})`);

// ---------------------------------------------------------------- saldos gravados (o que os triggers do banco manteriam)
for (const m of Object.values(MAT)) T.materials.find((x) => x.id === m.id).current_stock = r1(estoque[m.k]);
const somaCofre = () => r2(T.cash_transactions.filter((x) => !['opening', 'closing', 'transfer'].includes(x.type)).reduce((s, x) => s + (SINAL[x.type] || 0) * x.amount, 0)
  + T.bank_transactions.filter((b) => b.bank_account_id === id('banco.cofre')).reduce((s, b) => s + b.amount, 0));
{ // o último reforço (29/10) acerta o centavo do cofre de 10/11
  const delta = r2(18500 - somaCofre());
  ultimoReforco.cofre.amount = r2(ultimoReforco.cofre.amount + delta);
  ultimoReforco.banco.amount = r2(ultimoReforco.banco.amount - delta);
  confere(ultimoReforco.d === '2026-10-29' && ultimoReforco.cofre.amount > 0, `o último reforço do cofre é o de 29/10 (${ultimoReforco.d})`);
}
// A Conta Principal fecha 31/10 com R$ 46.382,57 (item 8) logo depois das vendas grandes do último dia do mês; sem uma saída
// depois de 29/10 ela ficaria negativa no fim de agosto, de setembro e de outubro (o saldo de um dia é o de 31/10 menos o que
// ainda vai entrar). A saída é a distribuição de lucros do trimestre aos sócios (fora da DRE), em 30/10, depois das vendas.
bankTx('principal', '2026-10-30', '17:50', 'withdrawal', -40000, 'Distribuição de lucros aos sócios (agosto a outubro)', { excluded_from_dre: true, payment_method: 'transfer' });
// item 8: a Conta Principal fecha 31/10 com R$ 46.382,57; o saldo inicial de 01/08 é o que dá isso
const extratos = {};
for (const b of T.bank_transactions) (extratos[b.bank_account_id] ||= []).push(b);
const ordena = (l) => l.sort((a, b) => a.transaction_at.localeCompare(b.transaction_at) || a.id.localeCompare(b.id, 'en', { numeric: true }));
iniPrincipal.amount = r2(46382.57 - extratos[id('banco.principal')].filter((b) => b !== iniPrincipal && b.transaction_date <= '2026-10-31').reduce((s, b) => s + b.amount, 0));
const saldoConta = {}, saldoEm = {}, minConta = {};
for (const [conta, lst] of Object.entries(extratos)) {
  let s = 0, min = Infinity;
  for (const b of ordena(lst)) { s = r2(s + b.amount); b.balance_after = s; min = Math.min(min, s); if (b.transaction_date <= '2026-10-31') saldoEm[conta] = s; }
  saldoConta[conta] = s; minConta[conta] = min;
}
const cofreFinal = somaCofre();
for (const b of T.bank_accounts) b.balance = b.kind === 'cash' ? cofreFinal : saldoConta[b.id] || 0;
for (const [key, v] of Object.entries(saldoParceiro)) {
  if (Math.abs(v) < 0.005) continue;
  const i = key.indexOf(':');
  add('balances', { id: id(`saldo.${key}`), company_id: COMPANY, entity_type: key.slice(0, i), entity_id: key.slice(i + 1), balance: v, currency: 'BRL', created_at: '2026-08-01T12:00:00.000Z', updated_at: '2026-11-09T18:00:00.000Z' });
}

// ---------------------------------------------------------------- contas a pagar e a receber (T13) e o resto do dia
const titulo = (k, dir, desc, valor, due, extra = {}) => add('financial_bills', {
  id: id(`titulo.${k}`), company_id: COMPANY, direction: dir, description: desc, amount: valor, currency: 'BRL', due_date: due, status: 'pending', paid_amount: 0,
  created_by: RAFAEL, created_at: '2026-11-01T12:00:00.000Z', updated_at: '2026-11-01T12:00:00.000Z', expected_bank_account_id: null, is_projection: false, ...extra,
});
add('recurring_bill_templates', {
  id: id('recorrencia.aluguel'), company_id: COMPANY, direction: 'payable', description: 'Aluguel do galpão', amount: 6800, frequency: 'monthly', interval: 1, is_active: true,
  start_date: '2026-11-05', next_due_date: '2026-12-05', category_id: id('categoria.aluguel'), cost_center_id: id('cc.patio'), expected_bank_account_id: id('banco.principal'), expected_payment_method: 'transfer', created_by: RAFAEL, created_at: '2026-10-28T12:00:00.000Z', updated_at: '2026-11-05T12:00:00.000Z',
});
const pgAluguel = T.bank_transactions.find((b) => b.description === 'Aluguel do galpão de novembro');
titulo('agua_out', 'payable', 'Água e esgoto de outubro', 238.4, '2026-11-05', { category_id: id('categoria.agua'), cost_center_id: id('cc.escritorio') });
titulo('aluguel_nov', 'payable', 'Aluguel do galpão de novembro', 6800, '2026-11-05', { status: 'paid', paid_amount: 6800, paid_at: pgAluguel.transaction_date /* a coluna é date */, recurring_template_id: id('recorrencia.aluguel'), source_type: 'recurring', category_id: id('categoria.aluguel'), cost_center_id: id('cc.patio'), expected_bank_account_id: id('banco.principal') });
titulo('energia_out', 'payable', 'Energia elétrica de outubro', 1874.3, '2026-11-10', { category_id: id('categoria.energia'), cost_center_id: id('cc.patio'), expected_bank_account_id: id('banco.principal'), expected_payment_method: 'transfer' });

// T8: próximo ticket 58; o #57 é o rascunho do Jair Lopes na coleta da Auto Peças Vale Forte (só a primeira pesagem)
add('weighing_tickets', {
  id: id('ticket.57'), company_id: COMPANY, ticket_number: 57, ticket_seq: 57, ticket_ref: '#57', status: 'pending', ticket_kind: 'standard', type: 'purchase',
  customer_supplier_id: id('fornecedor.valeforte'), customer_supplier_name: 'Auto Peças Vale Forte', customer_supplier_type: 'supplier',
  driver_name: 'Jair Lopes', vehicle_plate: 'GHT7B19', vehicle_type: 'Caminhão 3/4', first_weight: 6840, first_weight_at: at('2026-11-09', '16:12'),
  second_weight: null, second_weight_at: null, net_weight: null, material_id: MAT.bateria.id, material_name: MAT.bateria.nome,
  pricing_mode: 'weighing_only', items: [], attachments: [], created_by: MARCOS, created_at: at('2026-11-09', '16:12'), updated_at: at('2026-11-09', '16:12'),
});
// agenda (T25: duas tarefas no mês)
const tarefa = (k, title, date, time, extra = {}) => add('schedule_tasks', { id: id(`tarefa.${k}`), company_id: COMPANY, title, scheduled_date: date, scheduled_time: time, category: 'tarefa', status: 'pendente', priority: 'media', created_by: RAFAEL, assigned_to: RAFAEL, created_at: '2026-11-06T12:00:00.000Z', updated_at: '2026-11-06T12:00:00.000Z', notify_on_day: true, notify_minutes_before: 0, notify_push: false, ...extra });
tarefa('quiririm', 'Carregamento Aços Quiririm', '2026-11-10', '14:00', { customer_supplier_id: id('cliente.quiririm'), customer_supplier_name: 'Aços Quiririm Ltda', description: 'Separar chaparia e ferro misto para a carga da tarde.' });
tarefa('cooperativa', 'Buscar material na Cooperativa Recomeço', '2026-11-11', '09:30', { supplier_id: id('fornecedor.recomeco'), supplier_name: 'Cooperativa Recomeço' });

// ---------------------------------------------------------------- fiscal (seção 11 / item 11): série 1 no EcoSistema desde agosto
// Entrada e saída na mesma série; em outubro o "Última nota emitida" foi acertado errado (1247 em vez de 1245) e a 1248 (30/10,
// o latão de 600 kg da Fundição, pedido só em 03/11) saiu depois da 1245: 1246 e 1247 nunca viraram nota (a T16 inutiliza).
// As notas da Fundição espelham as vendas dela (pedido ligado); as outras são as do relatório do T17 (outubro: 12 de saída,
// R$ 168.940,00, e 9 de entrada, R$ 97.315,00), sem pedido ligado. As notas recebidas (2157 e 884) e o XML 3871 ficam na
// semente da T16. NFS-e: a 12 e a 13 de outubro são as receitas de caçamba do T15 (a T17 emite a 14).
const FISCAL = id('fiscal.matriz');
add('company_fiscal_config', {
  id: FISCAL, company_id: COMPANY, apelido: 'Matriz', ativo: true, is_default: true, cnpj: CNPJ_MATRIZ.replace(/\D/g, ''), razao_social: 'Recicla Vale Metais Ltda', nome_fantasia: 'Recicla Vale Metais',
  inscricao_estadual: ieSP('68812345', '11'), inscricao_municipal: '45.871', logradouro: 'Rua das Oficinas', numero: '1250', complemento: null, bairro: 'Parque Industrial', cep: '12086410',
  cidade: 'Taubaté', uf: 'SP', codigo_ibge: '3554102', codigo_municipio_ibge: '3554102', telefone: '(12) 90000-4410', email: `rafael${DOMINIO}`,
  regime_tributario: 'lucro_real', is_simples_nacional: false, is_icms_contributor: true, pis_cofins_regime: 'nao_cumulativo', pis_aliquota: 1.65, cofins_aliquota: 7.6, icms_aliquota_interna: 18,
  cfop_saida_interna: '5102', cfop_saida_interestadual: '6102', cfop_entrada_interna: '1102', cfop_entrada_interestadual: '2102',
  nfe_same_serie_both_types: true, nfe_default_serie_saida: 1, nfe_default_serie_entrada: 1, last_invoice_number: 1248, last_invoice_serie: '1', has_previous_invoices: true,
  last_mdfe_number: 0, nfse_ativo: true, nfse_serie: 1, nfse_nacional: true, nfse_dfe_ativo: false, dfe_ativo: false, iss_aliquota_padrao: 3,
  plugnotas_company_registered: true, plugnotas_company_registered_at: '2026-07-30T14:00:00.000Z', plugnotas_certificate_uploaded: true, plugnotas_environment: 'producao',
  created_at: '2026-07-30T14:00:00.000Z', updated_at: at('2026-10-30', '17:20'),
});
add('nfe_series', { id: id('nfe_serie.1'), company_id: COMPANY, fiscal_config_id: FISCAL, serie_number: 1, last_invoice_number: 1248, external_last_invoice_number: 1247, created_at: '2026-07-30T14:05:00.000Z', updated_at: at('2026-10-30', '17:20') });
const CNPJ_DIG = CNPJ_MATRIZ.replace(/\D/g, '');
function chaveNfe(d, num, cnf) {
  const base = `35${d.slice(2, 4)}${d.slice(5, 7)}${CNPJ_DIG}55001${pad(num, 9)}1${pad(cnf, 8)}`;
  let s = 0, w = 2;
  for (let i = base.length - 1; i >= 0; i--) { s += Number(base[i]) * w; w = w === 9 ? 2 : w + 1; }
  const r = s % 11;
  return base + (r < 2 ? 0 : 11 - r);
}
const AVULSOS = [ // vendedores de balcão (pessoa física, sem cadastro): a nota de entrada leva o nome e o CPF deles
  ['Benedito Carvalho', '418226703'], ['Rosângela Barbosa', '527901384'], ['Osvaldo Cardoso', '633018925'], ['Nilton Ribeiro', '702846159'],
  ['Geraldo Mendes', '815372640'], ['Luiz Fernando Teixeira', '926450318'], ['Antônio Carlos Vieira', '384715062'],
].map(([name, base]) => ({ name, razao_social: name, cpf_cnpj: cpf(base), indicador_ie: 9, cidade: 'Taubaté', uf: 'SP', codigo_ibge: '3554102' }));
// as notas de outubro sem pedido (as contas do T17); agosto e setembro levam os mesmos quilos a 85 % e 93 %
const SINTETICAS = {
  serrafina: [[['al_perfil', 580]], [['al_perfil', 620]], [['al_perfil', 590]], [['al_perfil', 610]]],
  quiririm: [[['chaparia', 1500], ['ferro_misto', 1440]], [['chaparia', 1510], ['ferro_misto', 1484]], [['chaparia', 1470], ['ferro_misto', 1428]], [['chaparia', 1540], ['ferro_misto', 1496]]],
  cida: [[['al_latinha', 180], ['papelao', 900]], [['al_latinha', 220], ['papelao', 1000]]],
  avulso: [[['ferro_misto', 8000]], [['cobre_mel', 300]], [['fio_cobre', 600]], [['al_perfil', 1500]], [['bronze', 400]], [['inox', 2000]], [['cobre_mel', 600], ['ferro_misto', 2920]]],
};
const NOTAS_PLANO = []; // { d, h, tipo, parceiro, its, order }
const ativos = () => PEDIDOS.filter((p) => !p.revertido);
for (const [mes, f] of [['2026-08', 0.85], ['2026-09', 0.93], [OUTM, 1]]) {
  const kg = (its) => its.map(([k, q]) => [k, f === 1 ? q : Math.round(q * f)]);
  const du = diasDoMes(mes);
  const vendasDe = (cli) => ativos().filter((p) => p.tipo === 'sale' && p.parceiroK === cli && mesDe(p.d) === mes);
  for (const p of vendasDe('bandeira')) NOTAS_PLANO.push({ d: p.d, h: maisMin(p.hhmm, 15), tipo: 'saida', parceiro: { k: 'bandeira' }, its: p.its.map((it) => [it.m, it.q]), order: p });
  const dSerra = [...new Set(vendasDe('serrafina').map((p) => p.d))].slice(0, 4);
  SINTETICAS.serrafina.forEach((its, i) => NOTAS_PLANO.push({ d: dSerra[i], h: '16:50', tipo: 'saida', parceiro: { k: 'serrafina' }, its: kg(its) }));
  const dQuir = [...new Set(vendasDe('quiririm').map((p) => p.d))].slice(0, 4);
  SINTETICAS.quiririm.forEach((its, i) => NOTAS_PLANO.push({ d: dQuir[i], h: '16:55', tipo: 'saida', parceiro: { k: 'quiririm' }, its: kg(its) }));
  SINTETICAS.cida.forEach((its, i) => NOTAS_PLANO.push({ d: du[[7, 17][i]], h: '17:05', tipo: 'entrada', parceiro: { k: 'cida', fornecedor: true }, its: kg(its) }));
  SINTETICAS.avulso.forEach((its, i) => NOTAS_PLANO.push({ d: du[1 + 3 * i], h: '17:10', tipo: 'entrada', parceiro: { avulso: AVULSOS[i] }, its: kg(its) }));
}
NOTAS_PLANO.sort((a, b) => (a.d + a.h).localeCompare(b.d + b.h));
NOTAS_PLANO.push({ d: '2026-10-30', h: '17:20', tipo: 'saida', parceiro: { k: 'bandeira' }, its: [['latao', 600]], numero: 1248 });
const NOTAS = [];
NOTAS_PLANO.forEach((n, i) => {
  const num = n.numero || 1185 + i;
  const iid = id(`nfe.${num}`);
  const cfop = n.tipo === 'entrada' ? '1102' : n.parceiro.k === 'serrafina' ? '6102' : '5102';
  const its = n.its.map(([m, q]) => { const p = n.tipo === 'saida' ? MAT[m].pv : MAT[m].pc; return { m, q, p, total: r2(q * p) }; });
  const total = r2(its.reduce((s, it) => s + it.total, 0));
  const emitida = at(n.d, n.h), autorizada = at(n.d, maisMin(n.h, 1));
  add('invoices', {
    id: iid, company_id: COMPANY, fiscal_config_id: FISCAL, invoice_number: num, serie: 1, modelo: 55, invoice_type: n.tipo, status: 'emitida', environment: 'producao', finalidade: 1,
    nature_operation: n.tipo === 'saida' ? 'Venda de mercadorias' : 'Compra de mercadorias', cfop_default: cfop, modalidade_frete: 9, is_consumer_final: false,
    customer_id: n.tipo === 'saida' ? id(`cliente.${n.parceiro.k}`) : null, supplier_id: n.parceiro.fornecedor ? id(`fornecedor.${n.parceiro.k}`) : null, destinatario_avulso: n.parceiro.avulso || null,
    order_id: n.order?.id || null, order_type: n.order ? 'sale' : null, issue_date: emitida, authorized_at: autorizada,
    nfe_key: chaveNfe(n.d, num, 30000000 + num * 7919 % 9999999), nfe_protocol: `135${n.d.slice(2, 4)}${pad(num * 104729 % 10000000000, 10)}`, plugnotas_id: `pn-${pad(num, 6)}`,
    total_products: total, total_amount: total, total_freight: 0, other_expenses: 0, valor_desconto_total: 0, computa_estoque_fiscal: true, baixa_estoque_ao_emitir: false,
    created_by: JULIANA, created_at: emitida, updated_at: autorizada,
  });
  its.forEach((it, j) => add('invoice_items', {
    id: id(`nfe_item.${num}.${j}`), invoice_id: iid, material_id: MAT[it.m].id, material_name: MAT[it.m].nome, ncm: MAT[it.m].ncm.replace(/\D/g, ''), cfop, unit: 'KG',
    quantity: it.q, unit_price: it.p, total_price: it.total, nfe_item_number: j + 1, origem: 0, impurity: 0, valor_desconto: 0, created_at: emitida,
  }));
  NOTAS.push({ num, d: n.d, tipo: n.tipo, total, its, parceiro: n.parceiro, order: n.order });
});
const nfse = (num, d, cli, valor, discriminacao) => {
  const nid = id(`nfse.${num}`);
  add('nfse_invoices', {
    id: nid, company_id: COMPANY, fiscal_config_id: FISCAL, nfse_number: num, nfse_numero_oficial: String(num), serie: 1, status: 'emitida', environment: 'producao',
    customer_id: id(`cliente.${cli}`), issue_date: at(d, '10:15'), authorized_at: at(d, '10:16'), data_competencia: d, total_servicos: valor, total_amount: valor,
    total_deducoes: 0, total_iss: r2(valor * 0.03), codigo_verificacao: `RV${pad(num * 7351 % 1000000, 6)}`, municipio_incidencia_ibge: '3554102', municipio_incidencia_nome: 'Taubaté',
    created_at: at(d, '10:15'), updated_at: at(d, '10:16'),
  });
  add('nfse_invoice_services', { id: id(`nfse_servico.${num}`), nfse_invoice_id: nid, codigo_servico: '7.09', discriminacao, valor_servico: valor, base_calculo: valor, deducoes: 0, iss_aliquota: 3, iss_valor: r2(valor * 0.03), iss_retido: false, created_at: at(d, '10:15') });
};
nfse(12, '2026-10-13', 'bandeira', 950, 'Locação de caçamba estacionária para a coleta de sucata metálica na Fundição Bandeira do Vale.');
nfse(13, '2026-10-29', 'quiririm', 1850, 'Coleta e remoção de resíduos metálicos com caçamba no pátio da Aços Quiririm.');

// ---------------------------------------------------------------- conferências (seção 16: item 15 e os totais de cada item)
const doMes = (mes, tipo) => ativos().filter((p) => p.tipo === tipo && mesDe(p.d) === mes);
const soma = (l) => r2(l.reduce((s, p) => s + p.total, 0));
const kgDe = (l, m) => r1(l.reduce((s, p) => s + p.its.filter((it) => !m || it.m === m).reduce((a, it) => a + it.q, 0), 0));
const oc = doMes(OUTM, 'purchase'), ov = doMes(OUTM, 'sale');
// item 1 e seção 4 (T21, T10)
confere(KS.every((k) => estoque[k] === ESTOQUE_HOJE[k]), `item 1: estoque de 10/11 (${KS.filter((k) => estoque[k] !== ESTOQUE_HOJE[k]).map((k) => `${k} ${estoque[k]}`).join(', ')})`);
const kardexFP = T.stock_movements.filter((s) => s.material_id === MAT.ferro_pesado.id && s.transaction_date >= '2026-10-31').sort((a, b) => a.transaction_at.localeCompare(b.transaction_at)).map((s) => s.stock_after);
confere(JSON.stringify(kardexFP) === JSON.stringify([41860, 42500, 3508, 900, 2100, 2500, 1320, 2180]), `seção 4: Kardex do ferro pesado de 31/10 a 09/11 (T10) ${kardexFP.join(' ')}`);
// item 2 (T15, T10, T9, T18)
const porForn = {};
for (const p of oc) porForn[p.parceiroK || 'balcao'] = r2((porForn[p.parceiroK || 'balcao'] || 0) + p.total);
const OUT_FORN = { siqueira: 83714, valdir: 44396, valeforte: 32410, cida: 13150, recomeco: 18755, balcao: 64435 };
confere(Object.entries(OUT_FORN).every(([k, v]) => porForn[k] === v) && soma(oc) === 256860, `item 2: compras de outubro por fornecedor (${JSON.stringify(porForn)})`);
const ocVF = oc.filter((p) => p.parceiroK === 'valeforte');
confere(ocVF.map((p) => p.d).join() === '2026-10-08,2026-10-15,2026-10-29' && ocVF[0].total === 595 && ocVF[0].forma === 'transfer' && !ocVF.some((p) => p.its.some((it) => it.m === 'bateria')), 'item 2: Vale Forte só em 08/10 (chaparia, Pix, R$ 595,00), 15/10 e 29/10, sem bateria');
const bateriaPix = oc.filter((p) => p.forma === 'transfer' && p.its.some((it) => it.m === 'bateria'));
confere(bateriaPix.length === 1 && bateriaPix[0].d === '2026-10-21' && bateriaPix[0].hhmm === '10:12' && bateriaPix[0].parceiroK === 'siqueira' && bateriaPix[0].total === 744, 'item 2: a única bateria paga em Pix em outubro é a de 21/10 10:12 no depósito (T9)');
const coop = ativos().filter((p) => p.tipo === 'purchase' && p.parceiroK === 'recomeco');
confere(coop.length === 14 && coop.every((p) => weekday(p.d) === 5 && p.forma === 'balance') && soma(coop) === 52937.5 && oc.filter((p) => p.parceiroK === 'recomeco').every((p) => p.total === 3751), 'item 2: cooperativa às sextas no saldo, 14 compras com R$ 52.937,50 (T4), as 5 de outubro com R$ 3.751,00');
confere(saldoParceiro[`supplier:${id('fornecedor.recomeco')}`] === 2550, 'item 2: as compras da cooperativa pagas na segunda seguinte (sobra a de 06/11)');
// item 3 (T15, T21)
for (const [cli, v, kgv] of [['bandeira', 112800, 3000], ['quiririm', 77460.6, 65912], ['serrafina', 60349.2, 6923], ['siqueira', 18630.2, 17827]]) {
  const l = ov.filter((p) => p.parceiroK === cli);
  confere(soma(l) === v && kgDe(l) === kgv, `item 3: vendas de outubro para ${cli} ${soma(l)} / ${kgDe(l)} kg`);
}
confere(soma(ov) === 269240 && kgDe(ov, 'bateria') === 0, 'item 3: vendas de outubro R$ 269.240,00, nenhuma bateria');
// T10 (item 15)
confere(kgDe(oc, 'ferro_pesado') === 50000 && kgDe(ov, 'ferro_pesado') === 10000, 'T10/T15: ferro pesado 50 t compradas e 10 t vendidas em outubro');
confere(kgDe(oc, 'cobre_mel') === 980 && kgDe(ov, 'cobre_mel') === 1000 && r2(kgDe(oc, 'cobre_mel') * MAT.cobre_mel.pc) === 41650 && kgDe(oc, 'bateria') === 1320 && kgDe(ov, 'bateria') === 0, 'T10 (item 15): cobre mel 980/1.000 kg e bateria 1.320/0 kg em outubro');
// item 4 (T21)
const sc = doMes('2026-09', 'purchase'), sv = doMes('2026-09', 'sale');
confere(soma(sc) === 201784.25 && soma(sv) === 273047.73, `item 4: setembro com compras R$ 201.784,25 e vendas R$ 273.047,73 (${soma(sc)} / ${soma(sv)})`);
// item 5 e 6 (T15, T17, T6, T14)
const despOut = DESPESAS.filter((e) => mesDe(e.d) === OUTM);
confere(despOut.filter((e) => e.receita).map((e) => `${e.d} ${e.valor}`).join() === '2026-10-13 950,2026-10-29 1850', 'item 5: caçamba de outubro 13/10 R$ 950,00 (Fundição) e 29/10 R$ 1.850,00 (Aços Quiririm)');
confere(r2(despOut.filter((e) => e.cat === 'tarifas').reduce((s, e) => s + e.valor, 0)) === 186 && !DESPESAS.some((e) => e.cat === 'tarifas' && mesDe(e.d) === NOV), 'item 6: Tarifas de outubro R$ 186,00 e nenhuma tarifa em novembro');
// DRE do mês nos dois regimes (mesma régua do lib/eco.mjs: custo médio = preço de compra da tabela)
function dre(mes) {
  const c = doMes(mes, 'purchase'), v = doMes(mes, 'sale');
  const cmv = r2(v.reduce((s, p) => s + p.its.reduce((a, it) => a + it.q * MAT[it.m].pc, 0), 0));
  const l = DESPESAS.filter((e) => mesDe(e.d) === mes);
  const tot = (f) => r2(l.filter(f).reduce((s, e) => s + e.valor, 0));
  const imp = tot((e) => e.cat === 'impostos_vendas'), frete = tot((e) => e.cat === 'frete'), rec = tot((e) => e.receita), opex = tot((e) => !e.receita && e.cat !== 'impostos_vendas' && e.cat !== 'frete');
  return { compras: soma(c), vendas: soma(v), cmv, opex, imp, frete, rec, competencia: r2(soma(v) - imp - cmv - frete - opex + rec), caixa: r2(soma(v) - imp - soma(c) - frete - opex + rec) };
}
const D = Object.fromEntries(['2026-08', '2026-09', OUTM, NOV].map((m) => [m, dre(m)]));
confere(D[OUTM].cmv === 218860 && D[OUTM].competencia === 10350 && D[OUTM].caixa === -27650 && D[OUTM].opex === 36855.9, `T15: DRE de outubro +R$ 10.350,00 / −R$ 27.650,00 (${D[OUTM].competencia} / ${D[OUTM].caixa})`);
confere(r2(D[OUTM].vendas + D[OUTM].rec) === 272040 && r2(D[OUTM].compras + D[OUTM].frete + D[OUTM].imp + D[OUTM].opex) === 299690, 'T22 (item 15): matriz em outubro com receita R$ 272.040,00 e despesa R$ 299.690,00');
confere(r2(D[OUTM].vendas - D[OUTM].compras) === 12380, 'T25: margem de outubro R$ 12.380,00');
// item 7 (T4, T10, T13, T14, T16, T17, T25)
const nc = doMes(NOV, 'purchase'), nv = doMes(NOV, 'sale');
const nvPor = (cli) => soma(nv.filter((p) => p.parceiroK === cli));
confere(soma(nv) === 118620.2 && nvPor('bandeira') === 57460 && nvPor('quiririm') === 55085 && nvPor('serrafina') === 4815.2 && nvPor('siqueira') === 1260, `item 7: vendas de novembro R$ 118.620,20 por cliente (${soma(nv)})`);
confere(soma(nc) === 18781.45 && r2(soma(nv) - soma(nc)) === 99838.75, `T25 (item 15): novembro com compras R$ 18.781,45 e margem R$ 99.838,75 (${soma(nc)})`);
const v0411 = nv.find((p) => p.d === '2026-11-04');
confere(v0411.its[0].q === 38992 && v0411.total === 48740 && v0411.conta === 'secundaria', 'item 7: a venda de 04/11 à Aços Quiririm com 38.992 kg (R$ 48.740,00, Pix Secundária)');
const v0911 = nv.find((p) => p.d === '2026-11-09');
const si0911 = T.sale_items.find((x) => x.sale_id === v0911.id);
confere(v0911.total === 23950 && si0911.quantity === 506 && si0911.impurity === 6 && v0911.caixa === id('caixa.84'), 'item 7: a venda da T16 de 09/11 (500 kg líquidos, bruto 506, R$ 23.950,00) no #84');
const cp = T.purchases.find((x) => x.id === COPIA.p.id);
confere(cp.reverted_at === at('2026-11-05', '08:20') && cp.reverted_compensation_register_id === CAIXAS.find((c) => c.d === '2026-11-05' && c.uid === MARCOS).cx.id && COPIA.p.total === 389.6 && cp.original_order_number === COPIA.p.num
  && !T.stock_movements.some((s) => s.order_id === cp.id) && T.cash_transactions.some((x) => x.reversal_for_order_id === cp.id && x.amount === 389.6 && x.type === 'deposit'), 'item 7: a cópia de 03/11 da Aparecida estornada em 05/11 com compensação no caixa do Marcos (T9)');
// item 8 (T6, T14, T21)
const bPri = id('banco.principal'), bSec = id('banco.secundaria'), bCof = id('banco.cofre');
const novDe = (b) => T.bank_transactions.filter((x) => x.bank_account_id === b && x.transaction_date >= '2026-11-01');
confere(saldoEm[bPri] === 46382.57 && saldoConta[bPri] === 41387.77 && novDe(bPri).length === 5, `item 8: Conta Principal R$ 46.382,57 em 31/10 e R$ 41.387,77 hoje, com 5 lançamentos em novembro (${saldoEm[bPri]} / ${saldoConta[bPri]})`);
confere(saldoEm[bSec] === 25000 && saldoConta[bSec] === 90515 && novDe(bSec).length === 12, `item 8: Conta Secundária R$ 25.000,00 em 31/10 e R$ 90.515,00 hoje, com 12 lançamentos em novembro (${saldoConta[bSec]})`);
confere(novDe(bCof).length === 0 && !novDe(bPri).some((x) => x.type === 'transfer') && cofreFinal === 18500, 'item 8: nenhuma transferência banco-cofre em novembro e cofre com R$ 18.500,00');
confere(pgAluguel.transaction_at === at('2026-11-05', '10:05') && pgAluguel.bank_account_id === bPri, 'item 8: aluguel de novembro às 10:05 na Principal');
confere(minConta[bPri] > 0, `Conta Principal nunca negativa (mínimo ${minConta[bPri]})`);
// item 9 (T6, T9, T16)
const cx = (n) => CAIXAS.find((c) => c.num === n);
confere(cx(70).uid === MARCOS && cx(70).d === '2026-10-21' && cx(83).uid === MARCOS && cx(83).d === '2026-11-09' && cx(84).uid === RAFAEL && cx(84).d === '2026-11-09' && caixaNum === 84, 'item 9: #70 do Marcos em 21/10, #83 e #84 em 09/11, o último antes da T6');
const pedidosDo = (n) => ativos().filter((p) => p.caixa === id(`caixa.${n}`));
confere(pedidosDo(70).map((p) => `${p.hhmm} ${p.parceiroK} ${p.total}`).join() === '09:15 cida 187.5,10:12 siqueira 744' && cx(70).cx.initial_opening_balance === 800 && cx(70).cx.closing_balance === 612.5
  && cx(70).cx.opened_at === at('2026-10-21', '07:02') && cx(70).cx.closed_at === at('2026-10-21', '17:31') && CAIXAS.some((c) => c.d === '2026-10-21' && c.uid === RAFAEL), 'item 9: #70 só com as duas compras da T9 (800,00 -> 612,50); o resto de 21/10 no caixa do Rafael');
confere(cx(83).cx.initial_opening_balance === 1443.3 && cx(83).cx.closing_balance === 640 && soma(pedidosDo(83)) === 803.3 && pedidosDo(83).length === 3 && cx(84).cx.initial_opening_balance === 1250 && cx(84).cx.closing_balance === 1250, 'item 9: #83 abre com R$ 1.443,30 e fecha com R$ 640,00 (803,30); #84 abre e fecha com R$ 1.250,00');
const c860 = ativos().find((p) => p.d === '2026-11-09' && p.hhmm === '15:20');
confere(c860.num === 1757 && ordem === 1758, `pedidos: a compra de 860 kg de 09/11 é a #1757 e o último pedido a #1758 (#${c860.num} / #${ordem})`);
confere(['2026-10-14', '2026-10-21'].every((d) => CAIXAS.some((c) => c.d === d && c.uid === RAFAEL)), 'item 9: o Rafael abre também em 14/10 e 21/10');
// item 11 (T16, T17)
const nOut = NOTAS.filter((n) => mesDe(n.d) === OUTM);
const tot = (l) => r2(l.reduce((s, n) => s + n.total, 0));
const saidaOut = nOut.filter((n) => n.tipo === 'saida'), entradaOut = nOut.filter((n) => n.tipo === 'entrada');
confere(nOut.length === 21 && saidaOut.length === 12 && entradaOut.length === 9 && tot(saidaOut) === 168940 && tot(entradaOut) === 97315 && r2(tot(saidaOut) - tot(entradaOut)) === 71625, `item 11: NF-e de outubro 21 (12 de saída R$ 168.940,00 e 9 de entrada R$ 97.315,00, saldo R$ 71.625,00) (${tot(saidaOut)} / ${tot(entradaOut)})`);
const n1248 = NOTAS.find((n) => n.num === 1248);
confere(n1248.d === '2026-10-30' && n1248.parceiro.k === 'bandeira' && n1248.its[0].m === 'latao' && n1248.its[0].q === 600 && n1248.total === 19140 && !NOTAS.some((n) => n.num === 1246 || n.num === 1247)
  && Math.max(...NOTAS.filter((n) => n.num !== 1248).map((n) => n.num)) === 1245 && NOTAS.every((n) => n.d >= '2026-08-01' && n.d <= '2026-10-31'), 'item 11: série 1 de agosto a outubro, 1246 e 1247 puladas, 1248 em 30/10 (latão da Fundição, 600 kg)');
confere(NOTAS.filter((n) => n.order).every((n) => n.total === n.order.total) && soma(ov.filter((p) => p.parceiroK === 'bandeira')) === tot(saidaOut.filter((n) => n.order)), 'item 11: as notas da Fundição são as vendas dela');
confere(T.nfse_invoices.map((n) => `${n.nfse_number} ${n.data_competencia} ${n.total_amount}`).join() === '12 2026-10-13 950,13 2026-10-29 1850', 'item 11: NFS-e 12 e 13 (as caçambas de outubro)');
// saldos dos parceiros (seção 10: T4, T13) e "A Receber" do T4
const esperado = { [`customer:${id('cliente.quiririm')}`]: 4870, [`customer:${id('cliente.serrafina')}`]: -1500, [`supplier:${id('fornecedor.recomeco')}`]: 2550, [`supplier:${id('fornecedor.valdir')}`]: -300, [`party:${id('cliente.siqueira')}`]: -840, [`customer:${id('cliente.bandeira')}`]: 14370 };
for (const [k, v] of Object.entries(esperado)) confere(saldoParceiro[k] === v, `seção 10: saldo ${k}: ${saldoParceiro[k]} (esperado ${v})`);
confere(Object.keys(saldoParceiro).filter((k) => Math.abs(saldoParceiro[k]) >= 0.005).length === 6, 'seção 10: só os seis parceiros com saldo');
confere(r2(14370 + saldoParceiro[`customer:${id('cliente.quiririm')}`] - saldoParceiro[`supplier:${id('fornecedor.valdir')}`]) === 19540, 'T4: "A Receber" R$ 19.540,00 (Fundição + Aços Quiririm + o vale do Valdir)');
confere(saldoParceiro[`customer:${id('cliente.quiririm')}`] === 4870, 'T13 (item 15): Aços Quiririm +R$ 4.870,00 (a T13 baixa 2.000,00 e sobra 2.870,00)');
// T20 (item 15): a cooperativa com o ticket #58 da T8 (3.018,4 kg de latinha a R$ 6,20)
const ticket58 = r2(3018.4 * MAT.al_latinha.pc);
confere(ticket58 === 18714.08 && r2(soma(coop) + ticket58) === 71651.58 && r2((soma(coop) + ticket58) / (coop.length + 1)) === 4776.77, 'T20 (item 15): R$ 71.651,58 em 15 pedidos, ticket médio R$ 4.776,77');
// T21 (item 15): as respostas do Cato com os números das seções 4, 7 e 8
confere(somaKS(estoque, (m) => m.pc) === 96076 && soma(nv) === 118620.2 && r2(saldoConta[bPri] + saldoConta[bSec]) === 131902.77, 'T21 (item 15): estoque R$ 96.076,00, vendas de novembro R$ 118.620,20 e bancos de hoje (seções 4, 7 e 8)');
confere(NEGATIVOS.every((n) => n.startsWith('papelao')), 'seção 7: o único estoque negativo aceito é o do papelão de 05/11 16:10 a 06/11 10:45');

// ---------------------------------------------------------------- tabelas consultadas que ficam vazias de propósito
const VAZIAS = [
  'user_permissions', 'active_sessions', 'admin_banners', 'banner_views', 'user_notifications', 'force_update_signals', 'data_fix_notices',
  'terms_update_notifications', 'nps_surveys', 'nps_responses', 'nps_questions', 'order_drafts', 'order_attachments', 'push_subscriptions',
  'notification_preferences', 'user_header_shortcuts', 'contabil_export_jobs', 'blog_posts', 'company_group_members', 'company_groups', 'employees',
  'entity_custom_prices', 'entity_labels', 'entity_custom_field_definitions', 'customer_label_assignments', 'supplier_label_assignments',
  'invoices', 'invoice_items', 'invoice_orders', 'inbound_nfe', 'inbound_nfse', 'nfse_invoices', 'mtr_manifests', 'mtr_cdf',
  'mtr_credentials', 'mtr_parceiros', 'mtr_manifest_items', 'mtr_ref_residuos', 'mtr_ref_classe', 'mtr_ref_estado_fisico', 'mtr_ref_acondicionamento',
  'mtr_ref_tratamento', 'mtr_ref_unidade', // o SIGOR do Rafael, os parceiros e as listas do órgão ficam com a semente da T18
  'production_orders', 'production_recipes', 'collection_orders', 'crm_opportunities', 'crm_pipelines', 'crm_stages',
  'bank_statement_imports', 'bank_statement_entries', 'reconciliation_matches', 'credit_card_bills', 'bill_payments', 'bill_payment_groups',
  'transaction_attachments', 'employee_movements', 'cato_events', 'cato_pending_actions', 'subscription_payments', 'subscription_history',
  'subscription_cancellation_requests', 'company_payments', 'referrals', 'schedule_task_reminders', 'material_import_batches',
  'stock_export_preferences', 'price_table_export_preferences', 'group_change_notifications', 'ecoflix_user_progress', 'ecoflix_watchlist',
  'ecoflix_user_preferences', 'consent_records', 'usage_events', 'financial_items', 'dre_groups', 'fiscal_scenarios', 'nfe_series',
  'company_fiscal_config', 'transportadoras', 'services', 'log_pesagens', 'cash_register_balance_audit',
  // não existe no banco: o app consulta por engano (useOfflinePrewarm) e o PostgREST responde 404; aqui fica vazia
  'cash_registers',
  // existe no banco mas não no types.ts da 1.59.154 (migration 20261021161000, bastão de edição do rascunho)
  'draft_editors',
  // existem no banco mas não no types.ts da 1.59.154: tentativas de envio do MTR e os resíduos salvos (T18)
  'mtr_manifest_attempts', 'mtr_residuo_presets',
];

// ---------------------------------------------------------------- grava (numa pasta ao lado; depois troca arquivo a arquivo)
const ARQUIVOS = {}; // caminho relativo -> conteúdo
const json = (tabelas) => {
  const ents = tabelas.filter((t) => T[t]?.length).map((t) => [t, T[t]]);
  const lines = ['{'];
  ents.forEach(([t, rows], i) => {
    lines.push(`${JSON.stringify(t)}: [`);
    rows.forEach((r, j) => lines.push(`  ${JSON.stringify(r)}${j < rows.length - 1 ? ',' : ''}`));
    lines.push(`]${i < ents.length - 1 ? ',' : ''}`);
  });
  lines.push('}');
  return { texto: lines.join('\n') + '\n', linhas: ents.reduce((s, [, r]) => s + r.length, 0) };
};
const TABS = {
  '01-empresa.json': ['companies', 'profiles', 'user_roles', 'user_permissions', 'user_shortcuts', 'nps_surveys', 'subscription_modules', 'subscription_plans', 'nfe_module_tiers', 'company_modules', 'app_config', 'currencies', 'mtr_sistemas', 'mtr_uf_sistema'],
  '02-cadastros.json': ['material_groups', 'materials', 'price_tables', 'price_table_items', 'suppliers', 'customers', 'vehicles', 'drivers', 'bank_accounts', 'dre_groups', 'financial_categories', 'cost_centers', 'payment_conditions', 'company_fiscal_config', 'nfe_series'],
  '03-historico.json': ['cash_register', 'purchases', 'purchase_items', 'sales', 'sale_items', 'stock_movements', 'cash_transactions', 'bank_transactions', 'balances', 'balance_movements', 'financial_bills', 'recurring_bill_templates', 'weighing_tickets', 'schedule_tasks', 'invoices', 'invoice_items', 'nfse_invoices', 'nfse_invoice_services'],
};
const todas = Object.values(TABS).flat();
confere(Object.keys(T).every((t) => todas.includes(t)), `toda tabela gerada vai para um arquivo (${Object.keys(T).filter((t) => !todas.includes(t))})`);
ARQUIVOS['seeds/00-vazias.json'] = JSON.stringify({ _vazias: VAZIAS.filter((t) => !T[t]?.length) }, null, 1) + '\n';
const LINHAS = {};
for (const [nome, tabs] of Object.entries(TABS)) { const j = json(tabs); ARQUIVOS[`seeds/${nome}`] = j.texto; LINHAS[nome] = j.linhas; }
// sementes extras do mundo base
ARQUIVOS['seeds-extra/base/caixa-aberto.json'] = JSON.stringify({
  _doc: 'Caixa #85 de hoje aberto pelo Rafael às 08:05 com R$ 1.500,00 de troco e nenhum lançamento: para as rotas que pedem caixa aberto (/compra, /venda). Não mexe no estoque nem no cofre. Gerado por gerar/sementes.mjs. Aplicar com "seedExtra": ["base/caixa-aberto"].',
  cash_register: [{ id: id('caixa.85'), company_id: COMPANY, register_number: 85, status: 'open', opened_at: at(HOJE, '08:05'), opened_by: RAFAEL, initial_opening_balance: 1500, opening_balance: 1500, closing_balance: null, closed_at: null, currency: 'BRL', created_at: at(HOJE, '08:05') }],
  cash_transactions: [{ id: id('ct.hoje.abertura'), company_id: COMPANY, cash_register_id: id('caixa.85'), type: 'opening', amount: 1500, description: 'Abertura do Caixa #85', transaction_at: at(HOJE, '08:05'), transaction_date: HOJE, created_at: at(HOJE, '08:05'), created_by: RAFAEL, excluded_from_dre: false }],
}, null, 1) + '\n';
ARQUIVOS['seeds-extra/base/balanca-ativada.json'] = JSON.stringify({
  _doc: 'Integração com a balança ligada no perfil do Rafael (T5): o app abre o WebSocket do EcoTray (8053/8054), que o robô simula ("Balança do pátio" na COM3). Impressão direta pelo EcoTray na térmica POS-58, bobina de 58 mm. Aplicar com "seedExtra": ["base/balanca-ativada"].',
  _patch: { profiles: [{ match: { id: RAFAEL }, set: { balanca_ativada: true, balanca_continua: true, balanca_decimais: 1, balanca_unidade: 'kg', balanca_url: 'ws://127.0.0.1:8053', direct_print_enabled: true, direct_print_printer_name: 'POS-58', thermal_print_mode: 'pdf', receipt_paper_width_mm: 58 } }] },
}, null, 1) + '\n';
if (SAIDA) {
  for (const [rel, texto] of Object.entries(ARQUIVOS)) { const f = path.join(SAIDA, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, texto); }
} else {
  // tudo numa pasta temporária no mesmo disco; só depois de gravar tudo, renomeia um arquivo por vez para o lugar
  const tmp = fs.mkdtempSync(path.join(MUNDO, '.sementes-novas-'));
  const mover = [];
  for (const [rel, texto] of Object.entries(ARQUIVOS)) { const f = path.join(tmp, rel.replace(/\//g, '__')); fs.writeFileSync(f, texto); mover.push([f, path.join(MUNDO, rel)]); }
  for (const [, destino] of mover) fs.mkdirSync(path.dirname(destino), { recursive: true });
  for (const [f, destino] of mover) fs.renameSync(f, destino);
  fs.rmdirSync(tmp);
}

console.log(`sementes: empresa ${LINHAS['01-empresa.json']} linhas, cadastros ${LINHAS['02-cadastros.json']}, histórico ${LINHAS['03-historico.json']} -> ${SAIDA || MUNDO}`);
console.log(`  ${T.purchases.length} compras (1 estornada), ${T.sales.length} vendas, ${T.cash_register.length} caixas (#70 Marcos 21/10, #84 Rafael 09/11), pedidos #1253 a #${ordem}; ${T.invoices.length} NF-e (série 1, #1185 a #1245 e a 1248), NFS-e 12 e 13`);
console.log(`  cofre R$ ${fmt(cofreFinal)} (saldo inicial ${fmt(ajusteIni.amount)}), Conta Principal R$ ${fmt(saldoConta[bPri])} (inicial ${fmt(iniPrincipal.amount)}, 31/10 ${fmt(saldoEm[bPri])}, mínimo ${fmt(minConta[bPri])}), Secundária R$ ${fmt(saldoConta[bSec])}`);
for (const [m, x] of Object.entries(D)) console.log(`  ${m}: compras ${fmt(x.compras)}, vendas ${fmt(x.vendas)}, CMV ${fmt(x.cmv)}, despesas op. ${fmt(x.opex)}, resultado competência ${fmt(x.competencia)} / caixa ${fmt(x.caixa)}`);
console.log(`  estoque em 01/08: ${KS.map((k) => `${k} ${EST_0108[k]}`).join(', ')}`);
console.log(`  aviso: estoque negativo aceito (seção 7 não fecha): ${NEGATIVOS.join('; ')}`);
console.log(`  ${CONFERIDO.length} conferências passaram`);
