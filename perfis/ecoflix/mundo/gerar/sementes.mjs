#!/usr/bin/env node
// Gera as sementes do mundo base da EcoFlix (Recicla Vale Metais, Taubaté/SP) para o Supabase falso.
//   node gerar/sementes.mjs            -> seeds/*.json e seeds-extra/base/*.json (determinístico)
// Tudo fictício (planejamento/ecoflix/MUNDO_FICTICIO.md, seção "Decidido pelas aulas"): CPF/CNPJ com dígito válido,
// e-mails .example, telefones (12) 9 0000-xxxx, placas inventadas. Data do mundo: FAKE_NOW=2026-11-10T08:30:00-03:00.
// Histórico de 01/08 a 09/11/2026 montado por plano, não por sorteio solto: outubro bate no centavo com o T15 (compras
// R$ 256.860,00, vendas R$ 269.240,00, 40 t de ferro pesado paradas no pátio), o estoque de 10/11 08:30 é o do T21
// (R$ 52.112,25), os saldos de parceiro são os do T4, as contas do T13, os caixas do T6/T9 (#70 do Marcos em 21/10,
// #83 e #84 em 09/11) e o ferro pesado do T10. Os saldos gravados (estoque, cofre, bancos, parceiros, caixas) saem da
// soma do próprio histórico, como os triggers do banco fariam. O gerador confere tudo isso e para se algo não bater.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MUNDO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(MUNDO, 'seeds');

// ---------------------------------------------------------------- utilidades
const id = (k) => `@id:${k}`;
let seed = 20261110;
function rnd() { // mulberry32
  seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const between = (a, b) => a + rnd() * (b - a);
const r2 = (n) => Math.round(n * 100) / 100;
const r1 = (n) => Math.round(n * 10) / 10;
const pad = (n, w = 2) => String(n).padStart(w, '0');
const at = (d, hhmm) => new Date(`${d}T${hhmm}:00-03:00`).toISOString(); // AAAA-MM-DD + HH:MM de Brasília -> ISO UTC
const addDays = (d, n) => { const t = new Date(`${d}T12:00:00Z`); t.setUTCDate(t.getUTCDate() + n); return t.toISOString().slice(0, 10); };
const weekday = (d) => new Date(`${d}T12:00:00Z`).getUTCDay(); // 0 domingo
const hm = (min) => `${pad(Math.floor(min / 60))}:${pad(min % 60)}`;
const fmt = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
function confere(cond, msg) { if (!cond) throw new Error(`sementes: ${msg}`); }
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
const fone = (n) => `(12) 90000-${pad(n, 4)}`;

// ---------------------------------------------------------------- a empresa e as pessoas
const COMPANY = id('company.reciclavale');
const RAFAEL = id('user.rafael');
const MARCOS = id('user.marcos');
const JULIANA = id('user.juliana');
const CREATED = '2026-07-27T13:00:00.000Z'; // cliente da EcoSistema desde o fim de julho (o histórico começa em 01/08)
const HOJE = '2026-11-10';
const INICIO = '2026-08-01';
const CNPJ_MATRIZ = cnpj('47318506'); // T1 e T22 (a filial é 47.318.506/0002-98)
confere(CNPJ_MATRIZ === '47.318.506/0001-07' && cnpj('47318506', '0002') === '47.318.506/0002-98', 'CNPJ da matriz/filial');
confere(cpf('274913508') === '274.913.508-79', 'CPF do Rafael (T18)');

const empresa = {
  id: COMPANY, name: 'Recicla Vale Metais', cnpj: CNPJ_MATRIZ, email: 'contato@reciclavalemetais.example', phone: fone(1000),
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
  perfil(RAFAEL, 'rafael@reciclavalemetais.example', 'Rafael Nogueira', { role: 'company_admin', permission_preset: 'full_access', terms_accepted_at: '2026-07-27T13:01:00.000Z', cato_invite_seen_at: '2026-07-28T12:00:00.000Z', origin: 'cadastro', created_at: CREATED }),
  // T2: Marcos = "Operador Padrão" menos "Ver Projeção de Lucro" (31 permissões, selo "Personalizado"), tela inicial Caixa
  perfil(MARCOS, 'marcos.antunes@reciclavalemetais.example', 'Marcos Antunes', { initial_screen_path: '/caixa' }),
  perfil(JULIANA, 'juliana.prado@reciclavalemetais.example', 'Juliana Prado'),
];
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
// estoque em 10/11 08:30 (T21: 15 materiais, 20.363,5 kg, R$ 52.112,25 a custo, R$ 64.422,35 pela tabela de venda)
const ESTOQUE_HOJE = { ferro_pesado: 2180, ferro_misto: 6420, chaparia: 3150, cobre_mel: 212.5, cobre_misto: 148, fio_cobre: 96, al_latinha: 640, al_perfil: 185, al_bloco: 230, latao: 74, bronze: 38, inox: 260, bateria: 3960, papelao: 1850, pet: 920 };
confere(r2(KS.reduce((s, k) => s + ESTOQUE_HOJE[k] * MAT[k].pc, 0)) === 52112.25 && r2(KS.reduce((s, k) => s + ESTOQUE_HOJE[k] * MAT[k].pv, 0)) === 64422.35, 'estoque do T21');

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
  // T17: a Serra Fina fica em Itamonte, MG (a carga atravessa o RJ: MDF-e); código IBGE fica para a busca de CEP do app
  { k: 'serrafina', name: 'Serra Fina Alumínio Reciclagem', razao: 'Serra Fina Alumínio Reciclagem Ltda', doc: cnpj('92837465'), phone: '(35) 90000-1807', contact: 'Diego Prado', ...END('Rodovia BR-354', '4100', 'Distrito Industrial', '37466-000', 'Itamonte', 'MG'), code: '3', industria: true },
  { k: 'siqueira', ...SIQUEIRA, code: '4', industria: false },
];
const VEICULOS = [
  { k: 'truck', plate: 'FKD2E41', description: 'Caminhão truck', motorista: 'Edson Moura', cap: 14000, tara: 9200, carroceria: 'aberta', rodado: 'truck', categoria: 'caminhao' },
  { k: '34', plate: 'GHT7B19', description: 'Caminhão 3/4', motorista: 'Jair Lopes', cap: 4000, tara: 3500, carroceria: 'aberta', rodado: 'toco', categoria: 'caminhao' },
  { k: 'picape', plate: 'EZR4C63', description: 'Picape', motorista: 'Tiago Freitas', cap: 800, tara: 1300, carroceria: 'aberta', rodado: 'outros', categoria: 'utilitario' },
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
// níveis do módulo Notas Fiscais (catálogo da migration 20260615190000_nfe_module_tiers); a empresa está no 1
[[1, 'Nível 1', 1000, 150], [2, 'Nível 2', 3000, 300], [3, 'Nível 3', 5000, 400]].forEach(([level, name, doc_limit, price]) => add('nfe_module_tiers', { id: id(`nfe_tier.${level}`), level, name, doc_limit, price, is_active: true }));
for (const code of DA_TRILHA) add('company_modules', { id: id(`company_module.${code}`), company_id: COMPANY, module_code: code, added_at: '2026-07-27T13:00:00.000Z', removed_at: null, effective_until: null, price_override: null });

add('app_config', { id: id('app_config.app_version'), key: 'app_version', value: '1.59.154', description: 'Versão publicada do app', updated_at: '2026-11-07T19:05:00.000Z' });
add('app_config', { id: id('app_config.ecotray_version'), key: 'ecotray_version', value: '1.7.22', description: 'Versão publicada do EcoTray', updated_at: '2026-10-28T12:00:00.000Z' });
add('app_config', { id: id('app_config.reconciliation_enabled'), key: 'reconciliation_enabled', value: 'true', description: 'Conciliação bancária ligada', updated_at: '2026-09-08T12:00:00.000Z' });
add('currencies', { code: 'BRL', name: 'Real Brasileiro', symbol: 'R$', decimals: 2, locale: 'pt-BR' });
add('currencies', { code: 'USD', name: 'Dólar Americano', symbol: 'US$', decimals: 2, locale: 'en-US' });
add('currencies', { code: 'PYG', name: 'Guarani Paraguaio', symbol: '₲', decimals: 0, locale: 'es-PY' });

for (const [k, name, color] of GRUPOS) add('material_groups', { id: id(`grupo.${k}`), company_id: COMPANY, name, color, icon: 'circle', created_at: '2026-07-28T12:00:00.000Z', updated_at: '2026-07-28T12:00:00.000Z' });
for (const m of Object.values(MAT)) {
  add('materials', {
    id: m.id, company_id: COMPANY, code: m.code, name: m.nome, fiscal_name: null, group_id: id(`grupo.${m.g}`), unit: 'Kg', ncm: m.ncm,
    purchase_price: m.pc, sale_price: m.pv, purchase_price_currency: 'BRL', sale_price_currency: 'BRL', current_stock: 0,
    is_archived: false, created_by: RAFAEL, created_at: '2026-07-28T12:10:00.000Z', updated_at: '2026-10-20T12:00:00.000Z',
  });
}
// tabela padrão "Principal" (T4) e a "Tabela Depósitos" (+4 %, criada no T3, ligada ao Depósito Irmãos Siqueira)
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
for (const f of FORNECEDORES) add('suppliers', { id: id(`fornecedor.${f.k}`), ...parceiroBase(f), linked_customer_id: f.k === 'siqueira' ? id('cliente.siqueira') : null, is_industry: false, default_price_table_id: f.k === 'siqueira' ? id('tabela.depositos') : null });
for (const c of CLIENTES) {
  add('customers', {
    id: id(`cliente.${c.k}`), ...parceiroBase(c), linked_supplier_id: c.k === 'siqueira' ? id('fornecedor.siqueira') : null,
    is_industry: c.industria, is_intermediary: !c.industria, default_price_table_id: c.k === 'siqueira' ? id('tabela.depositos') : null,
    regime_tributario: c.industria ? 'lucro_real' : 'simples_nacional',
  });
}
for (const v of VEICULOS) {
  add('vehicles', { id: id(`veiculo.${v.k}`), company_id: COMPANY, plate: v.plate, description: v.description, capacidade_kg: v.cap, tara_kg: v.tara, tipo_carroceria: v.carroceria, tipo_rodado: v.rodado, categoria: v.categoria, uf_licenciamento: 'SP', created_by: RAFAEL, created_at: '2026-07-29T14:00:00.000Z' });
  add('drivers', { id: id(`motorista.${v.k}`), company_id: COMPANY, name: v.motorista, phone: fone(1900 + VEICULOS.indexOf(v)), cnh_categoria: v.k === 'picape' ? 'B' : 'D', created_by: RAFAEL, created_at: '2026-07-29T14:00:00.000Z' });
}

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
  ['tarifas_bancarias', 'Tarifas bancárias', 'expense', '#64748B', 'opex', 'despesas_operacionais', false],
  ['tarifas', 'Tarifas', 'expense', '#000000', 'opex', 'despesas_operacionais', true],
  ['juros', 'Juros e Multas', 'expense', '#000000', 'nao_operacionais', 'outras_receitas_despesas', true],
  ['outras_despesas', 'Outras Despesas', 'expense', '#000000', 'opex', 'despesas_operacionais', true],
];
CATEGORIAS.forEach(([k, name, type, color, dre, nat, sys], i) => add('financial_categories', { id: id(`categoria.${k}`), company_id: COMPANY, name, type, color, icon: null, parent_id: null, dre_group: dre, dre_group_id: id(`dre.${nat}`), cash_flow_group: 'operacional', is_system: sys, sort_order: i, created_at: CREATED, updated_at: CREATED }));
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
// caixas: o Marcos abre um por dia útil; o Rafael abre o dele às segundas e em quatro dias de carga (T6: #83 do Marcos e
// #84 do Rafael em 09/11; T9: #70 do Marcos em 21/10)
const RAFAEL_ABRE = new Set([...DIAS.filter((d) => weekday(d) === 1), '2026-08-14', '2026-09-15', '2026-09-30', '2026-10-15']);

const OUT_PLAN = { compras: [], vendas: [] }; // linhas do plano: { mes, quem, mat, kg, dias }
const comprar = (mes, quem, mat, kg, dias) => kg > 0 && OUT_PLAN.compras.push({ mes, quem, mat, kg, dias });
const vender = (mes, quem, mat, kg, dias) => kg > 0 && OUT_PLAN.vendas.push({ mes, quem, mat, kg, dias });
const sorteia = (lista, n) => { const c = [...lista]; const out = []; while (out.length < Math.min(n, c.length)) out.push(c.splice(Math.floor(rnd() * c.length), 1)[0]); return out.sort(); };

// outubro (T15, no centavo): quem vendeu o quê para a Recicla e para quem ela vendeu
const OUTM = '2026-10';
const OUTUBRO_COMPRAS = { // fornecedor -> material -> kg
  siqueira: { ferro_pesado: 42000, ferro_misto: 14000, chaparia: 5000, cobre_mel: 230, cobre_misto: 100, al_perfil: 600, latao: 250, inox: 600 },
  valdir: { ferro_pesado: 4000, ferro_misto: 16000, chaparia: 6000, cobre_mel: 240, fio_cobre: 350 },
  valeforte: { cobre_mel: 230, cobre_misto: 400, al_perfil: 300, al_bloco: 700, bateria: 2000 },
  cida: { al_latinha: 1500, papelao: 7000 },
  recomeco: { al_latinha: 2000, papelao: 3000, pet: 2000 },
  balcao: { ferro_pesado: 3820, ferro_misto: 10000, chaparia: 4000, cobre_mel: 300, cobre_misto: 200, fio_cobre: 250, al_latinha: 500, al_perfil: 600, al_bloco: 300, latao: 250, bronze: 200, inox: 600, bateria: 760 },
};
const CLIENTE_DE = { ferro_pesado: 'quiririm', ferro_misto: 'quiririm', chaparia: 'quiririm', inox: 'quiririm', cobre_mel: 'bandeira', cobre_misto: 'bandeira', fio_cobre: 'bandeira', latao: 'bandeira', bronze: 'bandeira', al_latinha: 'serrafina', al_perfil: 'serrafina', al_bloco: 'serrafina', bateria: 'siqueira', papelao: 'siqueira', pet: 'siqueira' };
const diasDe = (mes) => ({
  valdir: naSemana(mes, 1, 3, 5), cida: sorteia(diasDoMes(mes), diasDoMes(mes).length - 2), recomeco: naSemana(mes, 3),
  balcao: diasDoMes(mes), valeforte: { '2026-08': ['2026-08-05', '2026-08-14', '2026-08-25'], '2026-09': ['2026-09-04', '2026-09-15', '2026-09-25'], '2026-10': ['2026-10-05', '2026-10-15', '2026-10-29'] }[mes],
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
    for (const [mat, kg] of Object.entries(mats)) {
      let dias = D[quem];
      if (quem === 'valdir' && mat !== 'ferro_misto') dias = subconj(dias, mat === 'cobre_mel' ? 5 : mat === 'fio_cobre' ? 6 : 8);
      if (quem === 'balcao') dias = subconj(dias, { ferro_misto: 99, ferro_pesado: 10, chaparia: 10, cobre_mel: 12, cobre_misto: 6, fio_cobre: 8, al_latinha: 12, al_perfil: 6, al_bloco: 5, latao: 8, bronze: 8, inox: 6, bateria: 5 }[mat] || 6);
      comprar(mes, quem, mat, kg, dias);
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
planoCompras(OUTM, OUTUBRO_COMPRAS);
const totalPorMaterial = (tab) => { const o = Object.fromEntries(KS.map((k) => [k, 0])); for (const mats of Object.values(tab)) for (const [k, kg] of Object.entries(mats)) o[k] += kg; return o; };
// mais os dois pedidos fixos de outubro: a bateria do T9 (240 kg) e o ferro pesado da Vale Forte do T10 (180 kg)
const COMPRADO_OUT = totalPorMaterial(OUTUBRO_COMPRAS);
COMPRADO_OUT.bateria += 240; COMPRADO_OUT.ferro_pesado += 180;
confere(COMPRADO_OUT.ferro_pesado === 50000, 'outubro: 50 t de ferro pesado compradas');
planoVendas(OUTM, { ...COMPRADO_OUT, ferro_pesado: 10000 });

// setembro: compras abaixo de outubro, o pátio vende um pouco mais do que compra (resultado acima do de outubro);
// agosto: compras menores e o estoque crescendo
const escala = (tab, f, fp) => Object.fromEntries(Object.entries(tab).map(([q, mats]) => [q, Object.fromEntries(Object.entries(mats).map(([k, kg]) => [k, k === 'ferro_pesado' ? (fp[q] || 0) : Math.round(kg * f)]))]));
const SETEMBRO_COMPRAS = escala(OUTUBRO_COMPRAS, 0.93, { siqueira: 3000, valdir: 2500, balcao: 2000 });
const AGOSTO_COMPRAS = escala(OUTUBRO_COMPRAS, 0.85, { siqueira: 1500, valdir: 2000, balcao: 2500 });
const DESCARGA_SET = { ferro_pesado: 2000, ferro_misto: 3000, chaparia: 1500, cobre_mel: 60, cobre_misto: 40, fio_cobre: 30, al_latinha: 300, al_perfil: 100, al_bloco: 100, latao: 40, bronze: 20, inox: 150, bateria: 500, papelao: 2000, pet: 400 };

// novembro (01 a 09/11): os fatos das aulas (T4, T10, T13) e o movimento miúdo do pátio
const NOV = '2026-11';
const NOV_COMPRAS_MIUDAS = [ // [dia, fornecedor, [[material, kg], ...], forma]
  ['2026-11-03', 'cida', [['al_latinha', 38], ['papelao', 280]], 'cash'], ['2026-11-04', 'cida', [['al_latinha', 42], ['papelao', 320]], 'cash'],
  ['2026-11-05', 'cida', [['al_latinha', 35], ['papelao', 260]], 'cash'], ['2026-11-06', 'cida', [['al_latinha', 47], ['papelao', 340]], 'cash'],
  ['2026-11-09', 'cida', [['al_latinha', 40], ['papelao', 300]], 'cash'],
  ['2026-11-03', null, [['ferro_misto', 180]], 'cash'], ['2026-11-03', null, [['cobre_mel', 18]], 'cash'], ['2026-11-03', null, [['fio_cobre', 14], ['al_latinha', 12]], 'cash'],
  ['2026-11-04', null, [['ferro_misto', 240]], 'cash'], ['2026-11-04', null, [['chaparia', 120]], 'cash'], ['2026-11-04', null, [['latao', 16]], 'cash'],
  ['2026-11-05', null, [['ferro_misto', 150]], 'cash'], ['2026-11-05', null, [['cobre_mel', 12.5]], 'cash'], ['2026-11-05', null, [['bronze', 9], ['al_latinha', 8]], 'cash'],
  ['2026-11-05', 'valeforte', [['bateria', 640], ['cobre_misto', 32], ['al_bloco', 75], ['al_perfil', 40]], 'transfer'],
  ['2026-11-06', null, [['chaparia', 160]], 'cash'], ['2026-11-06', null, [['latao', 22]], 'cash'], ['2026-11-06', null, [['inox', 85]], 'cash'],
  ['2026-11-09', null, [['ferro_misto', 210]], 'cash'], ['2026-11-09', null, [['cobre_mel', 24]], 'cash'], ['2026-11-09', null, [['fio_cobre', 22], ['al_latinha', 15]], 'cash'],
];
const NOV_FATOS = [ // [dia, hora, tipo, quem, itens, forma, extra]
  ['2026-11-03', '09:40', 'purchase', 'siqueira', [['ferro_pesado', 640]], 'transfer'], // T10
  ['2026-11-03', '15:10', 'sale', 'bandeira', [['cobre_mel', 300]], 'parcelado'], // T13: 3x R$ 4.790,00
  ['2026-11-04', '14:30', 'sale', 'quiririm', [['ferro_pesado', 38592]], 'transfer'], // o ferro parado de outubro sai (junção T10 x T15)
  ['2026-11-05', '14:20', 'sale', 'quiririm', [['ferro_pesado', 2608], ['chaparia', 1000], ['ferro_misto', 600]], 'balance'], // T4: +4.870
  ['2026-11-05', '16:10', 'sale', 'siqueira', [['papelao', 1250], ['pet', 100]], 'balance'], // T4
  ['2026-11-06', '09:50', 'purchase', 'siqueira', [['ferro_pesado', 1200], ['ferro_misto', 320], ['cobre_misto', 20]], 'balance'], // T4
  ['2026-11-06', '10:45', 'purchase', 'recomeco', [['al_latinha', 370], ['pet', 740]], 'balance'], // T4: R$ 3.700,00 no saldo
  ['2026-11-06', '15:30', 'sale', 'quiririm', [['ferro_pesado', 1180]], 'transfer'], // T10
  ['2026-11-09', '15:20', 'purchase', 'siqueira', [['ferro_pesado', 860]], 'transfer', { fotos: 2 }], // T10
];
// o que entra e sai em novembro define o estoque de 31/10 (de trás para a frente a partir do T21)
const NOV_LIQ = Object.fromEntries(KS.map((k) => [k, 0]));
for (const [, , its] of NOV_COMPRAS_MIUDAS) for (const [k, kg] of its) NOV_LIQ[k] += kg;
for (const [, , tipo, , its] of NOV_FATOS) for (const [k, kg] of its) NOV_LIQ[k] += tipo === 'purchase' ? kg : -kg;
const AJUSTE_3110 = -14; // T10: "Contagem do pátio no fechamento do mês"
const EST_3110 = Object.fromEntries(KS.map((k) => [k, r1(ESTOQUE_HOJE[k] - NOV_LIQ[k])]));
confere(EST_3110.ferro_pesado === 41860, `ferro pesado em 31/10 (${EST_3110.ferro_pesado})`);
const EST_3009 = { ...EST_3110, ferro_pesado: EST_3110.ferro_pesado - AJUSTE_3110 - 40000 };
const EST_3108 = Object.fromEntries(KS.map((k) => [k, r1(EST_3009[k] + DESCARGA_SET[k])]));
const ACUMULA_AGO = Object.fromEntries(KS.map((k) => [k, Math.round(EST_3108[k] * 0.35)]));
const EST_0108 = Object.fromEntries(KS.map((k) => [k, r1(EST_3108[k] - ACUMULA_AGO[k])]));
planoCompras('2026-09', SETEMBRO_COMPRAS);
const COMPRADO_SET = totalPorMaterial(SETEMBRO_COMPRAS);
planoVendas('2026-09', Object.fromEntries(KS.map((k) => [k, COMPRADO_SET[k] + DESCARGA_SET[k]])));
planoCompras('2026-08', AGOSTO_COMPRAS);
const COMPRADO_AGO = totalPorMaterial(AGOSTO_COMPRAS);
planoVendas('2026-08', Object.fromEntries(KS.map((k) => [k, COMPRADO_AGO[k] - ACUMULA_AGO[k]])));
// valor planejado das vendas do mês (base do imposto sobre vendas)
const vendasPlanejadas = (mes) => r2(OUT_PLAN.vendas.filter((v) => v.mes === mes).reduce((s, v) => s + v.kg * MAT[v.mat].pv, 0));

// despesas e receitas fora dos pedidos, por mês: [dia, hora, categoria, centro, valor, descrição, conta|'caixa']
const DESPESAS = [];
const desp = (d, h, cat, cc, valor, desc) => DESPESAS.push({ d, h, cat, cc, valor: r2(valor), desc });
function despesasFixas(mes, c) {
  const dia = (n) => { let d = `${mes}-${pad(n)}`; while (!util(d)) d = addDays(d, 1); return d; };
  desp(dia(1), '08:00', 'tarifas_bancarias', null, 89.9, 'Tarifa do pacote de serviços');
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
  desp(ultimoDia(mes), '18:00', 'tarifas_bancarias', null, c.tarifasPix, 'Tarifas de Pix e TED do mês');
  c.cacamba.forEach(([d, v, desc]) => DESPESAS.push({ d, h: '10:15', cat: 'aluguel_cacamba', cc: 'coleta', valor: v, desc, receita: true }));
}
despesasFixas(OUTM, { // T15: os lançamentos de outubro (a energia uma vez só; a duplicata das 16:40 é semente do T15)
  aluguel: 6500, folha: [14300, 3100, 2400], energia: ['2026-10-13', '09:12', 3850], impostos: 3574.1, tarifasPix: 96.1,
  combustivel: [['2026-10-02', 1120, 'Diesel do caminhão truck'], ['2026-10-09', 1060, 'Diesel do caminhão 3/4'], ['2026-10-16', 1050, 'Diesel do caminhão truck'], ['2026-10-23', 1050, 'Diesel e gasolina da picape']],
  manutencao: ['2026-10-20', 1950, 'Revisão do caminhão 3/4'], frete: [['2026-10-14', 1200], ['2026-10-21', 1200]],
  cacamba: [['2026-10-09', 1400, 'Aluguel de caçamba - obra no Jardim das Nações'], ['2026-10-23', 1400, 'Aluguel de caçamba - reforma no Centro']],
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
// novembro: tarifa, aluguel do galpão (conta paga do T13), combustível e a folha no 5º dia útil (09/11)
desp('2026-11-03', '08:00', 'tarifas_bancarias', null, 89.9, 'Tarifa do pacote de serviços');
desp('2026-11-05', '09:00', 'aluguel', 'patio', 6800, 'Aluguel do galpão de novembro');
desp('2026-11-05', '11:20', 'combustivel', 'coleta', 1180, 'Diesel do caminhão truck');
desp('2026-11-09', '16:00', 'folha', 'patio', 14300, 'Salários do pátio');
desp('2026-11-09', '16:02', 'folha', 'coleta', 3100, 'Salários dos motoristas');
desp('2026-11-09', '16:04', 'folha', null, 2400, 'Salários do escritório');

// ---------------------------------------------------------------- execução: dia a dia, como o app gravaria
let ordem = 1240; // numeração compartilhada compra/venda (template #{NUM})
let caixaNum = 0;
const estoque = { ...EST_0108 };
let cofre = 0; // saldo do cofre pela regra do app (lançamentos do caixa com sinal + extrato da conta dinheiro)
const saldoParceiro = {}; // "tipo:id" -> saldo
const SINAL = { sale: 1, purchase: -1, deposit: 1, withdrawal: -1, expense: -1, adjustment: 1 };

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
  confere(after >= 0, `estoque negativo: ${material} em ${d} ${hhmm} (${before} ${qtd >= 0 ? '+' : ''}${qtd})`);
  estoque[material] = after;
  add('stock_movements', {
    id: id(`sm.${T.stock_movements?.length || 0}`), company_id: COMPANY, material_id: MAT[material].id, type, quantity: r1(qtd), stock_before: before, stock_after: after,
    order_id: order?.id || null, order_type: order?.tipo || null, description: desc, created_by: quem, transaction_at: at(d, hhmm), transaction_date: d, created_at: at(d, hhmm),
  });
}
const PEDIDOS = []; // resumo para as conferências
/** Pedido de compra ou venda completo (cabeçalho, itens, estoque, pagamento), como create_*_atomic faria. */
function pedido(tipo, d, hhmm, parceiroK, itens, forma, caixa, extra = {}) {
  const num = ++ordem;
  const isCompra = tipo === 'purchase';
  const pid = id(`${isCompra ? 'compra' : 'venda'}.${num}`);
  const its = itens.map(([m, kg]) => ({ m, q: r1(kg), p: isCompra ? MAT[m].pc : MAT[m].pv, total: r2(r1(kg) * (isCompra ? MAT[m].pc : MAT[m].pv)) }));
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
      quantity: it.q, unit_price: it.p, total_price: it.total, impurity: 0, impurity_kg: null, impurity_pct: null, item_discount: 0,
      tare_weight: null, first_weight: null, second_weight: null, weighing_mode: null, weight_source: 'manual',
    });
    mov(it.m, d, hhmm, isCompra ? it.q : -it.q, isCompra ? 'COMPRA' : 'VENDA', { id: pid, tipo }, `${isCompra ? 'Compra' : 'Venda'} #${num}`, quem);
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
  const p = { tipo, d, hhmm, num, id: pid, parceiroK, total, its, forma };
  PEDIDOS.push(p);
  return p;
}

// estoque de partida (01/08) e saldos iniciais (dinheiro e bancos fora da DRE)
for (const k of KS) add('stock_movements', { id: id(`sm.inicial.${k}`), company_id: COMPANY, material_id: MAT[k].id, type: 'SALDO_INICIAL', quantity: EST_0108[k], stock_before: 0, stock_after: EST_0108[k], description: 'Saldo inicial de estoque', created_by: RAFAEL, transaction_at: at(INICIO, '07:00'), transaction_date: INICIO, created_at: at(INICIO, '07:00') });
const ajusteIni = cashTx(null, INICIO, '07:15', 'adjustment', 20000, 'Saldo inicial do dinheiro (ativação do cofre)', { excluded_from_dre: true });
const iniPrincipal = bankTx('principal', INICIO, '07:00', 'deposit', 0, 'Saldo inicial', { excluded_from_dre: true });
bankTx('secundaria', INICIO, '07:00', 'deposit', 32000, 'Saldo inicial', { excluded_from_dre: true });

// as linhas do plano viram eventos por dia (compras de manhã e à tarde, vendas no fim da tarde)
const porDia = new Map(); // dia -> eventos
const evento = (d, e) => { if (!porDia.has(d)) porDia.set(d, []); porDia.get(d).push(e); };
for (const c of OUT_PLAN.compras) split(c.kg, c.dias.length).forEach((kg, i) => evento(c.dias[i], { kind: 'compra', quem: c.quem, mat: c.mat, kg }));
const carry = new Map(); // venda planejada que não coube no estoque do dia passa para a próxima data do mesmo cliente
for (const v of OUT_PLAN.vendas) {
  const partes = split(v.kg, v.dias.length, 0.3);
  partes.forEach((kg, i) => evento(v.dias[i], { kind: 'venda', quem: v.quem, mat: v.mat, kg, chave: `${v.mes}:${v.quem}:${v.mat}`, ultima: i === partes.length - 1 }));
}
for (const [d, quem, its, forma] of NOV_COMPRAS_MIUDAS) evento(d, { kind: 'compraFixa', quem, its, forma });
for (const [d, h, tipo, quem, its, forma, extra] of NOV_FATOS) evento(d, { kind: 'fixo', h, tipo, quem, its, forma, extra: extra || {} });
// T9: a bateria de 21/10 (240 kg, R$ 744,00, Pix) lançada no Depósito Irmãos Siqueira em vez da Auto Peças Vale Forte
evento('2026-10-21', { kind: 'fixo', h: '14:05', tipo: 'purchase', quem: 'siqueira', its: [['bateria', 240]], forma: 'transfer', extra: { notes: null } });
// T10: a compra de 180 kg de ferro pesado da Vale Forte em 22/10 lançada duas vezes; a repetida foi excluída no mesmo dia
evento('2026-10-22', { kind: 'fixo', h: '10:20', tipo: 'purchase', quem: 'valeforte', its: [['ferro_pesado', 180]], forma: 'transfer', extra: {} });
evento('2026-10-22', { kind: 'duplicada', h: '10:24', mat: 'ferro_pesado', kg: 180, excluida: '11:02' });
for (const e of DESPESAS) evento(e.d, { kind: 'despesa', ...e });
// T4: vale de R$ 300,00 em dinheiro ao Valdir (03/11), adiantamento da Serra Fina (06/11) e Pix parcial à cooperativa (09/11)
evento('2026-11-03', { kind: 'pagSaldo', h: '08:40', tipo: 'supplier', quem: 'valdir', valor: 300, via: 'cash' });
evento('2026-11-06', { kind: 'pagSaldo', h: '11:30', tipo: 'customer', quem: 'serrafina', valor: 1500, via: 'transfer' });
evento('2026-11-09', { kind: 'pagSaldo', h: '10:10', tipo: 'supplier', quem: 'recomeco', valor: 1150, via: 'transfer' });
// cofre: reforço do banco às segundas e quintas (o pátio paga carroceiro e balcão em dinheiro)
const saidaDinheiro = (d) => (porDia.get(d) || []).reduce((s, e) => {
  if (e.kind === 'compra' && ['valdir', 'cida', 'balcao'].includes(e.quem)) return s + e.kg * MAT[e.mat].pc;
  if (e.kind === 'compraFixa' && e.forma === 'cash') return s + e.its.reduce((a, [k, kg]) => a + kg * MAT[k].pc, 0);
  if (e.kind === 'pagSaldo' && e.via === 'cash') return s + e.valor;
  return s;
}, 0);
const diaDeReforco = (d, i) => i === 0 || weekday(d) === 1 || weekday(d) === 4 || FERIADOS.has(addDays(d, -1)) && weekday(d) === 2;

const CAIXAS = [];
DIAS.forEach((d, iDia) => {
  const evs = porDia.get(d) || [];
  // reforço do cofre: cobre o dinheiro até o próximo reforço com folga; em 09/11 fecha o cofre em R$ 18.500,00 (MUNDO)
  if (diaDeReforco(d, iDia)) {
    let ate = iDia + 1; while (ate < DIAS.length && !diaDeReforco(DIAS[ate], ate)) ate++;
    const precisa = DIAS.slice(iDia, ate).reduce((s, x) => s + saidaDinheiro(x), 0);
    let valor = d === '2026-11-09' ? r2(18500 + precisa - cofre) : Math.ceil((precisa + 6000 - cofre) / 1000) * 1000;
    if (valor !== 0) {
      const g = id(`grupo_transf.${d}`);
      if (valor > 0) { bankTx('principal', d, '07:10', 'transfer', -valor, 'Transferência para DINHEIRO (COFRE)', { group_id: g }); bankTx('cofre', d, '07:10', 'transfer', valor, 'Transferência de Conta Principal', { group_id: g }); }
      else { valor = -valor; bankTx('cofre', d, '07:10', 'transfer', -valor, 'Transferência para Conta Principal', { group_id: g }); bankTx('principal', d, '07:10', 'transfer', valor, 'Transferência de DINHEIRO (COFRE)', { group_id: g }); }
    }
  }
  // caixas do dia: o do Marcos (07:04) e, nos dias dele, o do Rafael (07:58)
  const abre = (uid, hh, fecha) => {
    caixaNum++;
    const cx = add('cash_register', { id: id(`caixa.${caixaNum}`), company_id: COMPANY, register_number: caixaNum, status: 'closed', opened_at: at(d, hh), opened_by: uid, initial_opening_balance: 0, opening_balance: 0, closing_balance: null, closed_at: at(d, fecha), currency: 'BRL', created_at: at(d, hh) });
    cx.saldo = 0; cx._fecha = fecha; cx._abertura = cashTx(cx, d, hh, 'opening', 0, `Abertura do Caixa #${caixaNum}`);
    CAIXAS.push({ d, num: caixaNum, uid, cx });
    return cx;
  };
  const cxM = abre(MARCOS, hm(7 * 60 + 2 + Math.floor(rnd() * 5)), hm(17 * 60 + 33 + Math.floor(rnd() * 6)));
  const cxR = RAFAEL_ABRE.has(d) ? abre(RAFAEL, '07:58', '17:44') : null;
  // agrupa as compras do plano em pedidos: fornecedor cadastrado = um pedido por dia; balcão = um por material
  const compras = new Map();
  for (const e of evs.filter((x) => x.kind === 'compra')) {
    const k = e.quem === 'balcao' ? `balcao:${e.mat}` : e.quem;
    if (!compras.has(k)) compras.set(k, { quem: e.quem === 'balcao' ? null : e.quem, its: [] });
    compras.get(k).its.push([e.mat, e.kg]);
  }
  const fila = [];
  const formaDe = (q) => (['siqueira', 'valeforte', 'recomeco'].includes(q) ? 'transfer' : 'cash');
  for (const c of compras.values()) fila.push({ h: null, run: (h) => pedido('purchase', d, h, c.quem, c.its, formaDe(c.quem), formaDe(c.quem) === 'transfer' && cxR ? cxR : cxM) });
  for (const e of evs.filter((x) => x.kind === 'compraFixa')) fila.push({ h: null, run: (h) => pedido('purchase', d, h, e.quem, e.its, e.forma, e.forma === 'cash' || !cxR ? cxM : cxR) });
  // horários das compras soltas: de 07:20 a 16:30, em ordem aleatória
  fila.sort(() => rnd() - 0.5);
  const passo = Math.max(6, Math.floor((16 * 60 + 30 - (7 * 60 + 20)) / Math.max(1, fila.length)));
  fila.forEach((f, i) => { f.h = hm(7 * 60 + 20 + i * passo + Math.floor(rnd() * Math.max(1, passo - 4))); });
  for (const e of evs.filter((x) => ['fixo', 'despesa', 'pagSaldo', 'duplicada'].includes(x.kind))) fila.push({ h: e.h, e });
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
      if (its.length) pedido('sale', d, f.h, f.venda.quem, its, 'transfer', cxR || cxM, f.venda.quem === 'quiririm' ? { motorista: 'Paulo Henrique', placa: 'FTQ3H52' } : {});
      continue;
    }
    const e = f.e;
    if (e.kind === 'fixo') {
      const p = pedido(e.tipo, d, e.h, e.quem, e.its, e.forma, e.forma === 'cash' || !cxR ? cxM : cxR, e.extra);
      if (e.forma === 'parcelado') { // T13: 3 parcelas a receber com o pedido; o saldo do cliente fica todo itemizado
        const parc = r2(p.total / 3);
        ['2026-11-17', '2026-12-17', '2027-01-18'].forEach((due, i) => add('financial_bills', {
          id: id(`titulo.fiado_bandeira.${i + 1}`), company_id: COMPANY, direction: 'receivable', description: `Fatura venda #${p.num} (parcela ${i + 1}/3)`, amount: i < 2 ? parc : r2(p.total - 2 * parc), currency: 'BRL',
          due_date: due, status: 'pending', paid_amount: 0, order_id: p.id, order_type: 'sale', partner_id: id('cliente.bandeira'), partner_type: 'customer',
          installment_number: i + 1, installment_total: 3, payment_condition_id: id('condicao.30_60_90'), source_type: 'order', category_id: id('categoria.venda_sucata'), cost_center_id: null,
          created_by: RAFAEL, created_at: at(d, e.h), updated_at: at(d, e.h),
        }));
      }
    } else if (e.kind === 'duplicada') {
      const num = ++ordem; const pid = id(`compra.${num}`);
      mov(e.mat, d, e.h, e.kg, 'COMPRA', { id: pid, tipo: 'purchase' }, `Compra #${num}`, MARCOS);
      mov(e.mat, d, e.excluida, -e.kg, 'EXCLUSAO', { id: pid, tipo: 'purchase' }, `Exclusão do pedido #${num} (lançado em duplicidade)`, RAFAEL);
    } else if (e.kind === 'despesa') {
      const extra = { category_id: id(`categoria.${e.cat}`), cost_center_id: e.cc ? id(`cc.${e.cc}`) : null, payment_method: 'transfer' };
      if (e.receita) bankTx('principal', d, e.h, 'deposit', e.valor, e.desc, extra);
      else bankTx('principal', d, e.h, 'withdrawal', -e.valor, e.desc, extra);
    } else if (e.kind === 'pagSaldo') {
      const ent = id(`${e.tipo === 'supplier' ? 'fornecedor' : 'cliente'}.${e.quem}`);
      const pagando = e.tipo === 'supplier'; // a Recicla paga (fornecedor) ou recebe (cliente)
      if (e.via === 'cash') cashTx(cxM, d, e.h, 'withdrawal', e.valor, 'Pagamento de saldo', { excluded_from_dre: true, partner_id: ent, partner_type: e.tipo });
      else bankTx('principal', d, e.h, pagando ? 'withdrawal' : 'deposit', pagando ? -e.valor : e.valor, pagando ? 'Pagamento de saldo' : 'Recebimento de saldo', { excluded_from_dre: true, payment_method: 'transfer', partner_id: ent, partner_type: e.tipo });
      saldo(e.tipo, ent, -e.valor, d, e.h, pagando ? 'Baixa de saldo (Pagamento)' : 'Baixa de saldo (Recebimento)', { movement_type: 'payment', payment_method: e.via, created_by: e.via === 'cash' ? MARCOS : RAFAEL });
    }
  }
  // abertura: o troco que o caixa precisa para pagar o dia sem faltar (sai do cofre; abertura e fechamento não mexem nele)
  for (const cx of [cxM, cxR].filter(Boolean)) {
    const rows = T.cash_transactions.filter((x) => x.cash_register_id === cx.id && x.type !== 'opening');
    let s = 0, min = 0;
    for (const x of rows.sort((a, b) => a.transaction_at.localeCompare(b.transaction_at))) { s = r2(s + (SINAL[x.type] || 0) * x.amount); min = Math.min(min, s); }
    // T6: em 09/11 o #83 (Marcos) fecha com R$ 640,00 e o #84 (Rafael) com R$ 1.250,00 (a dica da abertura de hoje)
    const sobra = d === '2026-11-09' ? (cx === cxM ? 640 : 1250) : cx === cxR ? 1000 : 300 + Math.floor(rnd() * 12) * 100;
    const abertura = d === '2026-11-09' ? r2(sobra - s) : Math.max(cx === cxR ? 1000 : 1500, Math.ceil((sobra - min) / 100) * 100);
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
  }
});
for (const d of porDia.keys()) confere(DIAS.includes(d), `evento fora de dia útil: ${d}`);
for (const [k, v] of carry) confere(Math.abs(v) < 1e-9, `venda planejada que sobrou: ${k} (${v})`);

// ---------------------------------------------------------------- saldos gravados (o que os triggers do banco manteriam)
for (const m of Object.values(MAT)) T.materials.find((x) => x.id === m.id).current_stock = r1(estoque[m.k]);
// Conta Principal: o saldo inicial de 01/08 é o que mantém o banco com pelo menos R$ 20 mil no histórico
const extratos = {};
for (const b of T.bank_transactions) (extratos[b.bank_account_id] ||= []).push(b);
const ordena = (l) => l.sort((a, b) => a.transaction_at.localeCompare(b.transaction_at) || a.id.localeCompare(b.id, 'en', { numeric: true }));
{
  let s = 0, min = 0;
  for (const b of ordena(extratos[id('banco.principal')])) { s = r2(s + b.amount); min = Math.min(min, s); }
  iniPrincipal.amount = Math.ceil((20000 - min) / 1000) * 1000;
}
const saldoConta = {};
for (const [conta, lst] of Object.entries(extratos)) {
  let s = 0;
  for (const b of ordena(lst)) { s = r2(s + b.amount); b.balance_after = s; }
  saldoConta[conta] = s;
}
const cofreFinal = r2(T.cash_transactions.filter((x) => !['opening', 'closing', 'transfer'].includes(x.type)).reduce((s, x) => s + (SINAL[x.type] || 0) * x.amount, 0) + (saldoConta[id('banco.cofre')] || 0));
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
titulo('aluguel_nov', 'payable', 'Aluguel do galpão de novembro', 6800, '2026-11-05', { status: 'paid', paid_amount: 6800, paid_at: pgAluguel.transaction_at, recurring_template_id: id('recorrencia.aluguel'), source_type: 'recurring', category_id: id('categoria.aluguel'), cost_center_id: id('cc.patio'), expected_bank_account_id: id('banco.principal') });
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

// ---------------------------------------------------------------- conferências (o que as aulas falam)
const doMes = (mes, tipo) => PEDIDOS.filter((p) => p.tipo === tipo && mesDe(p.d) === mes);
const soma = (l) => r2(l.reduce((s, p) => s + p.total, 0));
const kgDe = (l, m) => r1(l.reduce((s, p) => s + p.its.filter((it) => !m || it.m === m).reduce((a, it) => a + it.q, 0), 0));
const oc = doMes(OUTM, 'purchase'), ov = doMes(OUTM, 'sale');
confere(soma(oc) === 256860 && soma(ov) === 269240, `outubro: compras ${soma(oc)} / vendas ${soma(ov)}`);
confere(kgDe(oc, 'ferro_pesado') === 50000 && kgDe(ov, 'ferro_pesado') === 10000, 'outubro: ferro pesado 50 t / 10 t');
for (const [cli, v, kg] of [['bandeira', 112800, 3000], ['quiririm', 77840, 66200], ['serrafina', 53700, 6500], ['siqueira', 24900, 15000]]) {
  const l = ov.filter((p) => p.parceiroK === cli);
  confere(soma(l) === v && kgDe(l) === kg, `outubro: vendas para ${cli} ${soma(l)} / ${kgDe(l)} kg`);
}
const porForn = {};
for (const p of oc) porForn[p.parceiroK || 'Não informado'] = r2((porForn[p.parceiroK || 'Não informado'] || 0) + p.total);
confere(Object.entries(porForn).every(([k, v]) => k === 'siqueira' || v < porForn.siqueira), 'outubro: o depósito é o maior fornecedor');
for (const k of KS) confere(estoque[k] === ESTOQUE_HOJE[k], `estoque de 10/11: ${k} ${estoque[k]} (T21 ${ESTOQUE_HOJE[k]})`);
const esperado = { [`customer:${id('cliente.quiririm')}`]: 4870, [`customer:${id('cliente.serrafina')}`]: -1500, [`supplier:${id('fornecedor.recomeco')}`]: 2550, [`supplier:${id('fornecedor.valdir')}`]: -300, [`party:${id('cliente.siqueira')}`]: -840, [`customer:${id('cliente.bandeira')}`]: 14370 };
for (const [k, v] of Object.entries(esperado)) confere(saldoParceiro[k] === v, `saldo ${k}: ${saldoParceiro[k]} (esperado ${v})`);
confere(cofreFinal === 18500, `cofre em 10/11: ${cofreFinal}`);
const cx = (n) => CAIXAS.find((c) => c.num === n);
confere(cx(70).uid === MARCOS && cx(70).d === '2026-10-21' && cx(83).uid === MARCOS && cx(84).uid === RAFAEL && cx(84).d === '2026-11-09' && caixaNum === 84, 'caixas #70, #83 e #84');
confere(cx(83).cx.closing_balance === 640 && cx(84).cx.closing_balance === 1250, 'fechamentos de 09/11');
confere(T.purchases.filter((p) => p.supplier_id === id('fornecedor.recomeco')).length === 14, 'T4: 14 compras da cooperativa');
// DRE do mês nos dois regimes (mesma régua do lib/eco.mjs: custo médio = preço de compra da tabela)
function dre(mes) {
  const c = doMes(mes, 'purchase'), v = doMes(mes, 'sale');
  const cmv = r2(v.reduce((s, p) => s + p.its.reduce((a, it) => a + it.q * MAT[it.m].pc, 0), 0));
  const l = DESPESAS.filter((e) => mesDe(e.d) === mes);
  const tot = (f) => r2(l.filter(f).reduce((s, e) => s + e.valor, 0));
  const imp = tot((e) => e.cat === 'impostos_vendas'), frete = tot((e) => e.cat === 'frete'), rec = tot((e) => e.receita), opex = tot((e) => !e.receita && e.cat !== 'impostos_vendas' && e.cat !== 'frete');
  return { compras: soma(c), vendas: soma(v), cmv, opex, competencia: r2(soma(v) - imp - cmv - frete - opex + rec), caixa: r2(soma(v) - imp - soma(c) - frete - opex + rec) };
}
const D = Object.fromEntries(['2026-08', '2026-09', OUTM, NOV].map((m) => [m, dre(m)]));
confere(D[OUTM].competencia === 10350 && D[OUTM].caixa === -27650 && D[OUTM].opex === 36855.9, `DRE de outubro ${D[OUTM].competencia} / ${D[OUTM].caixa}`);
confere(D['2026-09'].compras < D[OUTM].compras && D['2026-09'].competencia > D[OUTM].competencia && D['2026-09'].caixa > 0, `setembro acima de outubro (${D['2026-09'].competencia} / ${D['2026-09'].caixa})`);

// ---------------------------------------------------------------- tabelas consultadas que ficam vazias de propósito
const VAZIAS = [
  'user_permissions', 'active_sessions', 'admin_banners', 'banner_views', 'user_notifications', 'force_update_signals', 'data_fix_notices',
  'terms_update_notifications', 'nps_surveys', 'nps_responses', 'nps_questions', 'order_drafts', 'order_attachments', 'push_subscriptions',
  'notification_preferences', 'user_header_shortcuts', 'contabil_export_jobs', 'blog_posts', 'company_group_members', 'company_groups', 'employees',
  'entity_custom_prices', 'entity_labels', 'entity_custom_field_definitions', 'customer_label_assignments', 'supplier_label_assignments',
  'invoices', 'invoice_items', 'invoice_orders', 'inbound_nfe', 'inbound_nfse', 'nfse_invoices', 'mtr_manifests', 'mtr_cdf',
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
];

// ---------------------------------------------------------------- grava
fs.mkdirSync(OUT, { recursive: true });
const grava = (nome, tabelas) => {
  const ents = tabelas.filter((t) => T[t]?.length).map((t) => [t, T[t]]);
  const lines = ['{'];
  ents.forEach(([t, rows], i) => {
    lines.push(`${JSON.stringify(t)}: [`);
    rows.forEach((r, j) => lines.push(`  ${JSON.stringify(r)}${j < rows.length - 1 ? ',' : ''}`));
    lines.push(`]${i < ents.length - 1 ? ',' : ''}`);
  });
  lines.push('}');
  fs.writeFileSync(path.join(OUT, nome), lines.join('\n') + '\n');
  return ents.reduce((s, [, r]) => s + r.length, 0);
};
fs.writeFileSync(path.join(OUT, '00-vazias.json'), JSON.stringify({ _vazias: VAZIAS.filter((t) => !T[t]?.length) }, null, 1) + '\n');
const n1 = grava('01-empresa.json', ['companies', 'profiles', 'user_roles', 'user_permissions', 'user_shortcuts', 'nps_surveys', 'subscription_modules', 'subscription_plans', 'nfe_module_tiers', 'company_modules', 'app_config', 'currencies']);
const n2 = grava('02-cadastros.json', ['material_groups', 'materials', 'price_tables', 'price_table_items', 'suppliers', 'customers', 'vehicles', 'drivers', 'bank_accounts', 'dre_groups', 'financial_categories', 'cost_centers', 'payment_conditions']);
const n3 = grava('03-historico.json', ['cash_register', 'purchases', 'purchase_items', 'sales', 'sale_items', 'stock_movements', 'cash_transactions', 'bank_transactions', 'balances', 'balance_movements', 'financial_bills', 'recurring_bill_templates', 'weighing_tickets', 'schedule_tasks']);

// ---------------------------------------------------------------- sementes extras do mundo base
const EXTRA = path.join(MUNDO, 'seeds-extra', 'base');
fs.mkdirSync(EXTRA, { recursive: true });
fs.writeFileSync(path.join(EXTRA, 'caixa-aberto.json'), JSON.stringify({
  _doc: 'Caixa #85 de hoje aberto pelo Rafael às 08:05 com R$ 1.500,00 de troco e nenhum lançamento: para as rotas que pedem caixa aberto (/compra, /venda). Não mexe no estoque nem no cofre. Gerado por gerar/sementes.mjs. Aplicar com "seedExtra": ["base/caixa-aberto"].',
  cash_register: [{ id: id('caixa.85'), company_id: COMPANY, register_number: 85, status: 'open', opened_at: at(HOJE, '08:05'), opened_by: RAFAEL, initial_opening_balance: 1500, opening_balance: 1500, closing_balance: null, closed_at: null, currency: 'BRL', created_at: at(HOJE, '08:05') }],
  cash_transactions: [{ id: id('ct.hoje.abertura'), company_id: COMPANY, cash_register_id: id('caixa.85'), type: 'opening', amount: 1500, description: 'Abertura do Caixa #85', transaction_at: at(HOJE, '08:05'), transaction_date: HOJE, created_at: at(HOJE, '08:05'), created_by: RAFAEL, excluded_from_dre: false }],
}, null, 1) + '\n');
fs.writeFileSync(path.join(EXTRA, 'balanca-ativada.json'), JSON.stringify({
  _doc: 'Integração com a balança ligada no perfil do Rafael (T5): o app abre o WebSocket do EcoTray (8053/8054), que o robô simula ("Balança do pátio" na COM3). Impressão direta pelo EcoTray na térmica POS-58, bobina de 58 mm. Aplicar com "seedExtra": ["base/balanca-ativada"].',
  _patch: { profiles: [{ match: { id: RAFAEL }, set: { balanca_ativada: true, balanca_continua: true, balanca_decimais: 1, balanca_unidade: 'kg', balanca_url: 'ws://127.0.0.1:8053', direct_print_enabled: true, direct_print_printer_name: 'POS-58', thermal_print_mode: 'pdf', receipt_paper_width_mm: 58 } }] },
}, null, 1) + '\n');

console.log(`sementes: empresa ${n1} linhas, cadastros ${n2}, histórico ${n3} -> ${OUT}`);
console.log(`  ${T.purchases.length} compras, ${T.sales.length} vendas, ${T.cash_register.length} caixas (#70 Marcos 21/10, #84 Rafael 09/11), pedidos #1241 a #${ordem}`);
console.log(`  cofre R$ ${fmt(cofreFinal)} (saldo inicial ${fmt(ajusteIni.amount)}), Conta Principal R$ ${fmt(saldoConta[id('banco.principal')])} (inicial ${fmt(iniPrincipal.amount)}), Secundária R$ ${fmt(saldoConta[id('banco.secundaria')])}`);
for (const [m, x] of Object.entries(D)) console.log(`  ${m}: compras ${fmt(x.compras)}, vendas ${fmt(x.vendas)}, CMV ${fmt(x.cmv)}, despesas op. ${fmt(x.opex)}, resultado competência ${fmt(x.competencia)} / caixa ${fmt(x.caixa)}`);
console.log(`  estoque em 01/08: ${KS.map((k) => `${k} ${EST_0108[k]}`).join(', ')}`);
