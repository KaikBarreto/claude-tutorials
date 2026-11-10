#!/usr/bin/env node
// Gera as sementes do mundo base da EcoFlix (Recicla Vale Metais, Taubaté/SP) para o Supabase falso.
//   node gerar/sementes.mjs            -> seeds/*.json (determinístico: mesma saída a cada execução)
// Tudo fictício (planejamento/ecoflix/MUNDO_FICTICIO.md): CPF/CNPJ com dígito válido gerados aqui, e-mails .example,
// telefones (12) 9 0000-xxxx, placas inventadas. Data do mundo: FAKE_NOW=2026-11-10T08:30:00-03:00 (terça).
// Histórico fechado de 01/08 a 09/11/2026: compras quase todo dia, vendas semanais, um caixa por dia (Rafael), despesas
// fixas, transferências banco -> cofre, contas a pagar e a receber, um fiado parcelado, adiantamento do Valdir, ticket
// de pesagem aguardando valorização. Os saldos gravados (estoque, cofre, bancos, saldos de parceiro, caixas) saem da
// soma do próprio histórico, como o banco de verdade faria com os triggers.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const MUNDO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(MUNDO, 'seeds');

// ---------------------------------------------------------------- utilidades
const id = (k) => `@id:${k}`;
function stableId(key) { // igual ao core/util.mjs (para gerar FKs já resolvidas quando preciso)
  const h = crypto.createHash('sha1').update('domiflix-fake:' + key).digest();
  h[6] = (h[6] & 0x0f) | 0x50; h[8] = (h[8] & 0x3f) | 0x80;
  const x = h.subarray(0, 16).toString('hex');
  return `${x.slice(0, 8)}-${x.slice(8, 12)}-${x.slice(12, 16)}-${x.slice(16, 20)}-${x.slice(20, 32)}`;
}
let seed = 20261110;
function rnd() { // mulberry32
  seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const pick = (arr) => arr[Math.floor(rnd() * arr.length)];
const between = (a, b) => a + rnd() * (b - a);
const r2 = (n) => Math.round(n * 100) / 100;
const r1 = (n) => Math.round(n * 10) / 10;
const pad = (n, w = 2) => String(n).padStart(w, '0');
/** instante ISO (UTC) de uma data AAAA-MM-DD e hora HH:MM em Brasília (-03:00) */
const at = (d, hhmm) => new Date(`${d}T${hhmm}:00-03:00`).toISOString();
const addDays = (d, n) => { const t = new Date(`${d}T12:00:00Z`); t.setUTCDate(t.getUTCDate() + n); return t.toISOString().slice(0, 10); };
const weekday = (d) => new Date(`${d}T12:00:00Z`).getUTCDay(); // 0 domingo
const hm = (min) => `${pad(Math.floor(min / 60))}:${pad(min % 60)}`;

// documentos com dígito verificador válido (mesmo algoritmo de rec/fakebase/tools/docs.mjs)
function cpfDigit(nums) { let s = 0; for (let i = 0; i < nums.length; i++) s += nums[i] * (nums.length + 1 - i); const d = 11 - (s % 11); return d > 9 ? 0 : d; }
function cpf(base9) {
  const n = String(base9).padStart(9, '0').split('').map(Number); const d1 = cpfDigit(n); const d2 = cpfDigit([...n, d1]);
  return `${n.slice(0, 3).join('')}.${n.slice(3, 6).join('')}.${n.slice(6, 9).join('')}-${d1}${d2}`;
}
function cnpjDigit(nums, w) { const s = nums.reduce((a, n, i) => a + n * w[i], 0); const m = s % 11; return m < 2 ? 0 : 11 - m; }
function cnpj(base8, branch = '0001') { // base iniciada em 9: faixa que a Receita ainda não emitiu
  const n = (String(base8).padStart(8, '0') + branch).split('').map(Number);
  const d1 = cnpjDigit(n, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]); const d2 = cnpjDigit([...n, d1], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
  const s = n.join('') + d1 + d2;
  return `${s.slice(0, 2)}.${s.slice(2, 5)}.${s.slice(5, 8)}/${s.slice(8, 12)}-${s.slice(12)}`;
}
const fone = (n) => `(12) 90000-${pad(n, 4)}`;

// ---------------------------------------------------------------- o mundo
const COMPANY = id('company.reciclavale');
const RAFAEL = id('user.rafael');
const CREATED = '2026-07-27T13:00:00.000Z'; // cliente da EcoSistema desde o fim de julho (o histórico começa em 01/08)
const HOJE = '2026-11-10';
const INICIO = '2026-08-01';

const empresa = {
  id: COMPANY,
  name: 'Recicla Vale Metais',
  cnpj: cnpj('93418276'),
  email: 'contato@reciclavalemetais.example',
  phone: fone(1000),
  address: 'Avenida dos Metalúrgicos, 1850 - Distrito Industrial, Taubaté - SP, 12072-010',
  contact_name: 'Rafael Nogueira',
  timezone: 'America/Sao_Paulo',
  base_currency: 'BRL',
  subscription_status: 'active',
  subscription_plan: 'personalizado',
  subscription_value: 1025,
  base_subscription_value: 1025,
  subscription_expires_at: '2026-12-02T23:59:59.000Z',
  billing_cycle: 'monthly',
  payment_method: 'pix',
  ltv: 3075,
  max_users: 10,
  extra_users: 0,
  plan_locked: false,
  is_test_account: false,
  cash_account_enabled: true,
  cash_account_opt_out: false,
  cash_account_seeded_at: '2026-08-01T10:30:00.000Z',
  multi_cash_enabled: false,
  onboarding_completed_at: '2026-07-31T18:00:00.000Z',
  onboarding_state: {},
  cato_enabled: true,
  ai_consent_at: '2026-07-27T13:05:00.000Z',
  ai_consent_version: '1',
  white_label_enabled: false,
  show_name_in_documents: true,
  show_cnpj_in_documents: true,
  show_address_in_documents: true,
  show_phone_in_documents: true,
  show_email_in_documents: false,
  show_receipt_phrase: true,
  receipt_phrase: 'Obrigado pela preferência! Recicla Vale Metais',
  lat: -23.0262,
  lng: -45.5559,
  geocode_status: 'ok',
  origin: 'site',
  created_at: CREATED,
  updated_at: '2026-11-01T12:00:00.000Z',
};

const perfilRafael = {
  id: RAFAEL,
  email: 'rafael@reciclavalemetais.example',
  full_name: 'Rafael Nogueira',
  company_id: COMPANY,
  role: 'company_admin',
  permission_preset: 'full_access',
  is_active: true,
  must_change_password: false,
  terms_accepted_at: '2026-07-27T13:01:00.000Z',
  cato_invite_seen_at: '2026-07-28T12:00:00.000Z',
  preferred_language: 'pt-BR',
  preferred_currency: 'BRL',
  default_payment_method: 'cash',
  balanca_ativada: false,
  direct_print_enabled: false,
  auto_print_receipts: false,
  show_profit_on_receipt: false,
  origin: 'cadastro',
  created_at: CREATED,
  updated_at: '2026-11-01T12:00:00.000Z',
};

// módulos do catálogo (subscription_modules, como nas migrations) e o plano Personalizado com todos os da trilha
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

// materiais (R$/kg compra e venda, NCM sugerido) — MUNDO_FICTICIO.md
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
const MAT = Object.fromEntries(MATERIAIS.map(([k, g, nome, pc, pv, ncm], i) => [k, { k, g, nome, pc, pv, ncm, code: pad(i + 1, 3), id: id(`material.${k}`) }]));
// estoque de partida em 01/08 (kg), antes do histórico
const ESTOQUE_INICIAL = { ferro_pesado: 3400, ferro_misto: 2600, chaparia: 1500, cobre_mel: 85, cobre_misto: 70, fio_cobre: 30, al_latinha: 310, al_perfil: 120, al_bloco: 110, latao: 45, bronze: 30, inox: 210, bateria: 380, papelao: 1150, pet: 480 };

// parceiros (cliente = para quem a empresa vende; fornecedor = de quem compra)
const END = (logradouro, numero, bairro, cep, cidade = 'Taubaté') => ({ logradouro, numero, bairro, cep, cidade, uf: 'SP', address: `${logradouro}, ${numero} - ${bairro}, ${cidade} - SP`, codigo_ibge: cidade === 'Taubaté' ? '3554102' : cidade === 'Pindamonhangaba' ? '3538006' : cidade === 'Tremembé' ? '3554805' : cidade === 'Caçapava' ? '3508504' : '3549904' });
const FORNECEDORES = [
  { k: 'valdir', name: 'Valdir Pereira', doc: '111.444.777-35', pf: true, phone: null, phone_unavailable: true, ...END('Rua Sete de Setembro', '412', 'Vila São José', '12070-410'), code: '1', pix: null },
  { k: 'cida', name: 'Aparecida Ramos', nome_fantasia: 'Dona Cida', doc: '529.982.247-25', pf: true, phone: fone(1201), ...END('Rua das Acácias', '88', 'Jardim Gurilândia', '12071-150'), code: '2', pix: fone(1201) },
  { k: 'siqueira', name: 'Depósito Irmãos Siqueira', razao: 'Depósito de Sucatas Irmãos Siqueira Ltda', doc: cnpj('95127438'), pf: false, phone: fone(1302), contact: 'Joel Siqueira', ...END('Estrada do Pinheirinho', '2730', 'Pinheirinho', '12091-500', 'Tremembé'), code: '3', pix: cnpj('95127438') },
  { k: 'valeforte', name: 'Auto Peças Vale Forte', razao: 'Auto Peças Vale Forte Ltda', doc: cnpj('96384120'), pf: false, phone: fone(1403), contact: 'Sandra Lemes', ...END('Avenida Brasil', '1290', 'Centro', '12080-010'), code: '4', pix: null },
  { k: 'recomeco', name: 'Cooperativa Recomeço', razao: 'Cooperativa de Catadores Recomeço', doc: cnpj('97250936'), pf: false, phone: fone(1504), contact: 'Marta Oliveira', ...END('Rua do Trabalho', '57', 'Vila Nossa Senhora das Graças', '12060-640'), code: '5', pix: cnpj('97250936') },
];
const CLIENTES = [
  { k: 'quiririm', name: 'Aços Quiririm Ltda', razao: 'Aços Quiririm Indústria e Comércio Ltda', doc: cnpj('98463027'), phone: fone(1605), contact: 'Paulo Henrique', ...END('Rodovia Vereador Abel Fabrício Dias', '3400', 'Quiririm', '12043-300'), code: '1', industria: true },
  { k: 'bandeira', name: 'Fundição Bandeira do Vale', razao: 'Fundição Bandeira do Vale Ltda', doc: cnpj('94716352'), phone: fone(1706), contact: 'Cristina Moura', ...END('Rua Anhanguera', '980', 'Distrito Industrial', '12412-010', 'Pindamonhangaba'), code: '2', industria: true },
  { k: 'serrafina', name: 'Serra Fina Alumínio Reciclagem', razao: 'Serra Fina Alumínio Reciclagem Ltda', doc: cnpj('92837465'), phone: fone(1807), contact: 'Diego Prado', ...END('Avenida Itália', '1520', 'Jardim das Nações', '12030-212'), code: '3', industria: true },
  { k: 'siqueira', name: 'Depósito Irmãos Siqueira', razao: 'Depósito de Sucatas Irmãos Siqueira Ltda', doc: cnpj('95127438'), phone: fone(1302), contact: 'Joel Siqueira', ...END('Estrada do Pinheirinho', '2730', 'Pinheirinho', '12091-500', 'Tremembé'), code: '4', industria: false },
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
add('profiles', perfilRafael);
add('user_roles', { id: id('role.rafael'), user_id: RAFAEL, role: 'company_admin', created_at: CREATED });
add('user_shortcuts', { id: id('atalhos.rafael'), user_id: RAFAEL, shortcuts_enabled: true, custom_shortcuts: null, created_at: CREATED, updated_at: CREATED });
// pesquisa NPS principal da plataforma (consultada com .single()): existe, mas inativa, sem resposta da empresa
add('nps_surveys', { id: id('nps.principal'), title: 'NPS EcoSistema', description: 'Pesquisa de satisfação', is_active: false, is_main_nps: true, target_audience: 'all', trigger_type: 'manual', created_at: '2026-01-15T12:00:00.000Z', updated_at: '2026-01-15T12:00:00.000Z' });
for (const [code, name, description, price, screens, base, active] of MODULOS) {
  add('subscription_modules', { id: id(`modulo.${code}`), code, name, description, price, screens, is_base_module: base, is_active: active, created_at: '2025-12-05T14:47:07.000Z' });
}
add('subscription_plans', { id: id('plano.start'), code: 'start', name: 'Plano Start', description: 'Kit Básico com 2 usuários', price: 125, max_users: 2, modules: ['kit_basico'], is_active: true });
add('subscription_plans', { id: id('plano.avancado'), code: 'avancado', name: 'Plano Avançado', description: 'Kit Básico + Funcionários com 3 usuários', price: 225, max_users: 3, modules: ['kit_basico', 'funcionarios'], is_active: true });
add('subscription_plans', { id: id('plano.master'), code: 'master', name: 'Plano Master', description: 'Todos os módulos com 4 usuários', price: 415, max_users: 4, modules: ['kit_basico', 'funcionarios', 'notas_fiscais'], is_active: true });
add('subscription_plans', { id: id('plano.personalizado'), code: 'personalizado', name: 'Personalizado', description: 'Monte seu plano escolhendo módulos', price: 0, max_users: 2, modules: ['kit_basico'], is_active: true });
for (const code of DA_TRILHA) add('company_modules', { id: id(`company_module.${code}`), company_id: COMPANY, module_code: code, added_at: '2026-07-27T13:00:00.000Z', removed_at: null, effective_until: null, price_override: null });

add('app_config', { id: id('app_config.app_version'), key: 'app_version', value: '1.59.154', description: 'Versão publicada do app', updated_at: '2026-11-07T19:05:00.000Z' });
add('app_config', { id: id('app_config.ecotray_version'), key: 'ecotray_version', value: '1.7.24', description: 'Versão publicada do EcoTray', updated_at: '2026-11-03T12:00:00.000Z' });
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

// tabela de preço padrão (a do cadastro) + a tabela própria da Aços Quiririm
add('price_tables', { id: id('tabela.padrao'), company_id: COMPANY, name: 'Tabela Padrão', is_default: true, is_linked: false, created_at: '2026-07-28T12:20:00.000Z', updated_at: '2026-10-20T12:00:00.000Z' });
add('price_tables', { id: id('tabela.quiririm'), company_id: COMPANY, name: 'Aços Quiririm', is_default: false, is_linked: false, created_at: '2026-07-30T12:00:00.000Z', updated_at: '2026-10-20T12:00:00.000Z' });
for (const m of Object.values(MAT)) add('price_table_items', { id: id(`pti.padrao.${m.k}`), price_table_id: id('tabela.padrao'), material_id: m.id, purchase_price: m.pc, sale_price: m.pv, is_override: false, created_at: '2026-07-28T12:20:00.000Z', updated_at: '2026-10-20T12:00:00.000Z' });
const QUIRIRIM_VENDA = { ferro_pesado: 1.32, ferro_misto: 1.10, chaparia: 1.03 };
for (const [k, pv] of Object.entries(QUIRIRIM_VENDA)) add('price_table_items', { id: id(`pti.quiririm.${k}`), price_table_id: id('tabela.quiririm'), material_id: MAT[k].id, purchase_price: MAT[k].pc, sale_price: pv, is_override: true, created_at: '2026-07-30T12:00:00.000Z', updated_at: '2026-10-20T12:00:00.000Z' });

const parceiroBase = (p) => ({
  company_id: COMPANY, name: p.name, nome_fantasia: p.nome_fantasia || null, razao_social: p.razao || (p.pf ? p.name : null), cpf_cnpj: p.doc,
  phone: p.phone || null, phone_unavailable: !!p.phone_unavailable, email: p.pf ? null : `contato@${p.k}.example`, contact_name: p.contact || null,
  address: p.address, logradouro: p.logradouro, numero: p.numero, bairro: p.bairro, cep: p.cep, cidade: p.cidade, uf: p.uf, codigo_ibge: p.codigo_ibge,
  pix_key: p.pix || null, code: p.code, is_mei: false, created_by: RAFAEL, created_at: '2026-07-29T12:00:00.000Z', updated_at: '2026-10-15T12:00:00.000Z',
  indicador_ie: p.pf ? 9 : 1, inscricao_estadual: p.pf ? null : `68${pad(Number(p.code) * 731 % 1000, 3)}${pad(Number(p.code) * 4127 % 100000, 5)}`,
});
for (const f of FORNECEDORES) {
  add('suppliers', { id: id(`fornecedor.${f.k}`), ...parceiroBase(f), linked_customer_id: f.k === 'siqueira' ? id('cliente.siqueira') : null, is_industry: false });
}
for (const c of CLIENTES) {
  add('customers', {
    id: id(`cliente.${c.k}`), ...parceiroBase(c), linked_supplier_id: c.k === 'siqueira' ? id('fornecedor.siqueira') : null,
    is_industry: c.industria, is_intermediary: !c.industria, default_price_table_id: c.k === 'quiririm' ? id('tabela.quiririm') : null,
    regime_tributario: c.industria ? 'lucro_real' : 'simples_nacional',
  });
}
for (const v of VEICULOS) {
  add('vehicles', { id: id(`veiculo.${v.k}`), company_id: COMPANY, plate: v.plate, description: v.description, capacidade_kg: v.cap, tara_kg: v.tara, tipo_carroceria: v.carroceria, tipo_rodado: v.rodado, categoria: v.categoria, uf_licenciamento: 'SP', created_by: RAFAEL, created_at: '2026-07-29T14:00:00.000Z' });
  add('drivers', { id: id(`motorista.${v.k}`), company_id: COMPANY, name: v.motorista, phone: fone(1900 + VEICULOS.indexOf(v)), cnh_categoria: v.k === 'picape' ? 'B' : 'D', created_by: RAFAEL, created_at: '2026-07-29T14:00:00.000Z' });
}

// financeiro: contas, categorias, centros de custo, condições de pagamento
add('bank_accounts', { id: id('banco.principal'), company_id: COMPANY, name: 'Conta Principal', kind: 'bank', is_default: true, is_protected: false, is_archived: false, institution_name: 'Banco Vale Real', color: '#2563EB', currency: 'BRL', balance: 0, created_at: CREATED, updated_at: CREATED });
add('bank_accounts', { id: id('banco.reserva'), company_id: COMPANY, name: 'Conta Reserva', kind: 'bank', is_default: false, is_protected: false, is_archived: false, institution_name: 'Cooperativa de Crédito Paraíba', color: '#7C3AED', currency: 'BRL', balance: 0, created_at: '2026-07-28T15:00:00.000Z', updated_at: '2026-07-28T15:00:00.000Z' });
add('bank_accounts', { id: id('banco.cofre'), company_id: COMPANY, name: 'DINHEIRO (COFRE)', kind: 'cash', is_default: false, is_protected: true, is_archived: false, institution_name: 'Conta DINHEIRO (COFRE)', color: '#22C55E', currency: 'BRL', balance: 0, created_at: '2026-08-01T10:30:00.000Z', updated_at: '2026-08-01T10:30:00.000Z' });

const CATEGORIAS = [ // [chave, nome, tipo, cor, dre_group, sistema]
  ['outras_receitas', 'Outras Receitas', 'income', '#000000', 'receita', true],
  ['outras_despesas', 'Outras Despesas', 'expense', '#000000', 'opex', true],
  ['folha', 'Folha Salarial', 'expense', '#EC4899', 'opex', false],
  ['energia', 'Energia elétrica', 'expense', '#F59E0B', 'opex', false],
  ['aluguel', 'Aluguel do pátio', 'expense', '#8B5CF6', 'opex', false],
  ['combustivel', 'Combustível', 'expense', '#EF4444', 'opex', false],
  ['tarifa', 'Tarifas bancárias', 'expense', '#64748B', 'opex', false],
  ['manutencao', 'Manutenção de equipamentos', 'expense', '#0EA5E9', 'opex', false],
  ['alimentacao', 'Alimentação', 'expense', '#F97316', 'opex', false],
  ['servicos', 'Serviços prestados', 'income', '#16A34A', 'receita', false],
];
for (const [k, name, type, color, dre, sys] of CATEGORIAS) add('financial_categories', { id: id(`categoria.${k}`), company_id: COMPANY, name, type, color, dre_group: dre, cash_flow_group: 'operacional', is_system: sys, sort_order: 0, created_at: CREATED, updated_at: CREATED });
add('cost_centers', { id: id('cc.patio'), company_id: COMPANY, name: 'Pátio', color: '#16A34A', is_active: true, created_at: CREATED, updated_at: CREATED });
add('cost_centers', { id: id('cc.escritorio'), company_id: COMPANY, name: 'Escritório', color: '#2563EB', is_active: true, created_at: CREATED, updated_at: CREATED });
add('payment_conditions', { id: id('condicao.30_60_90'), company_id: COMPANY, name: '30/60/90 dias', installments: [{ days: 30, percent: 33.34 }, { days: 60, percent: 33.33 }, { days: 90, percent: 33.33 }], active: true, is_default: false, created_at: '2026-07-30T12:00:00.000Z', updated_at: '2026-07-30T12:00:00.000Z' });

// ---------------------------------------------------------------- histórico
const estoque = { ...ESTOQUE_INICIAL };
for (const [k, q] of Object.entries(ESTOQUE_INICIAL)) {
  add('stock_movements', { id: id(`sm.inicial.${k}`), company_id: COMPANY, material_id: MAT[k].id, type: 'AJUSTE', quantity: q, stock_before: 0, stock_after: q, description: 'Saldo inicial de estoque', created_by: RAFAEL, transaction_at: at(INICIO, '07:00'), transaction_date: INICIO, created_at: at(INICIO, '07:00') });
}
let ordem = 1240; // numeração compartilhada compra/venda (template #{NUM})
let caixaNum = 0;
const saldoBanco = { principal: 0, reserva: 0, cofre: 0 }; // perna banco
let gavetaCofre = 0; // perna gaveta do cofre (cash_transactions com sinal, sem opening/closing/transfer)
const saldoParceiro = {}; // "tipo:id" -> saldo

function bankTx(conta, d, hhmm, type, amount, description, extra = {}) {
  const row = add('bank_transactions', {
    id: id(`bt.${T.bank_transactions?.length || 0}`), company_id: COMPANY, bank_account_id: id(`banco.${conta}`), type, amount: r2(amount), description,
    transaction_at: at(d, hhmm), transaction_date: d, created_at: at(d, hhmm), created_by: RAFAEL, source: 'manual', excluded_from_dre: false, ...extra,
  });
  saldoBanco[conta] = r2(saldoBanco[conta] + row.amount);
  row.balance_after = saldoBanco[conta];
  return row;
}
const SINAL = { sale: 1, purchase: -1, deposit: 1, withdrawal: -1, expense: -1, adjustment: 1 };
function cashTx(caixa, d, hhmm, type, amount, description, extra = {}) {
  const row = add('cash_transactions', {
    id: id(`ct.${T.cash_transactions?.length || 0}`), company_id: COMPANY, cash_register_id: caixa ? caixa.id : null, type, amount: r2(amount), description,
    transaction_at: at(d, hhmm), transaction_date: d, created_at: at(d, hhmm), created_by: RAFAEL, excluded_from_dre: false, ...extra,
  });
  if (!['opening', 'closing', 'transfer'].includes(type)) gavetaCofre = r2(gavetaCofre + (SINAL[type] || 0) * row.amount);
  if (caixa && type !== 'opening' && type !== 'closing') {
    caixa.saldo = r2(caixa.saldo + (SINAL[type] || 0) * row.amount);
    caixa.minimo = Math.min(caixa.minimo ?? caixa.saldo, caixa.saldo);
  }
  return row;
}
function saldo(tipo, entityId, valor, d, hhmm, desc, extra = {}) {
  // update_balance: parceiro duplo (Siqueira) vai para a linha 'party' do lado do cliente, com o sinal invertido no fornecedor
  let et = tipo, eid = entityId, v = valor;
  if (entityId === id('fornecedor.siqueira')) { et = 'party'; eid = id('cliente.siqueira'); v = -valor; }
  else if (entityId === id('cliente.siqueira')) { et = 'party'; }
  const key = `${et}:${eid}`;
  saldoParceiro[key] = r2((saldoParceiro[key] || 0) + v);
  add('balance_movements', {
    id: id(`bm.${T.balance_movements?.length || 0}`), company_id: COMPANY, balance_id: id(`saldo.${key}`), entity_type: tipo, entity_id: entityId,
    movement_type: extra.movement_type || 'order', amount: r2(valor), description: desc, transaction_at: at(d, hhmm), transaction_date: d,
    created_at: at(d, hhmm), created_by: RAFAEL, is_settled: false, ...extra,
  });
}
function mov(material, d, hhmm, qtd, type, order, desc) {
  const before = r1(estoque[material]);
  const after = r1(before + qtd);
  estoque[material] = after;
  add('stock_movements', {
    id: id(`sm.${T.stock_movements.length}`), company_id: COMPANY, material_id: MAT[material].id, type, quantity: r1(qtd), stock_before: before, stock_after: after,
    order_id: order?.id || null, order_type: order?.tipo || null, description: desc, created_by: RAFAEL, transaction_at: at(d, hhmm), transaction_date: d, created_at: at(d, hhmm),
  });
}

/** Pedido de compra ou venda completo (cabeçalho, itens, estoque, pagamento) como create_*_atomic faria. */
function pedido(tipo, d, hhmm, parceiroK, itens, pagamento, caixa, extra = {}) {
  const num = ++ordem;
  const isCompra = tipo === 'purchase';
  const pid = id(`${isCompra ? 'compra' : 'venda'}.${num}`);
  const total = r2(itens.reduce((s, it) => s + it.total, 0));
  const pagoCom = pagamento.forma; // cash | transfer | balance
  const head = {
    id: pid, company_id: COMPANY, order_number: num, order_seq: num, order_period: null, order_ref: `#${num}`, status: 'completed',
    total_amount: total, paid_amount: total, payment_method: pagoCom, created_by: RAFAEL, transaction_at: at(d, hhmm), transaction_date: d,
    created_at: at(d, hhmm), currency: 'BRL', hide_financial_details: false, notes: extra.notes || null,
    driver_name: extra.motorista || null, vehicle_plate: extra.placa || null, driver_id: extra.driverId || null, vehicle_id: extra.vehicleId || null,
  };
  if (isCompra) head.supplier_id = parceiroK ? id(`fornecedor.${parceiroK}`) : null;
  else head.customer_id = id(`cliente.${parceiroK}`);
  add(isCompra ? 'purchases' : 'sales', head);
  itens.forEach((it, i) => {
    add(isCompra ? 'purchase_items' : 'sale_items', {
      id: id(`${isCompra ? 'pi' : 'si'}.${num}.${i}`), [isCompra ? 'purchase_id' : 'sale_id']: pid, material_id: MAT[it.m].id, material_name: MAT[it.m].nome,
      quantity: it.q, unit_price: it.p, total_price: it.total, impurity: it.imp || 0, impurity_kg: it.imp || null, impurity_pct: null, item_discount: 0,
      tare_weight: null, first_weight: null, second_weight: null, weighing_mode: null, weight_source: 'manual',
    });
    const liquido = r1(it.q - (it.imp || 0));
    mov(it.m, d, hhmm, isCompra ? liquido : -liquido, isCompra ? 'COMPRA' : 'VENDA', { id: pid, tipo }, `${isCompra ? 'Compra' : 'Venda'} #${num}${it.imp ? ` (${it.imp}kg impureza)` : ''}`);
  });
  const rotulo = isCompra ? 'Compra' : 'Venda';
  if (pagoCom === 'cash') cashTx(caixa, d, hhmm, tipo, total, `${rotulo} #${num}`, { order_id: pid });
  else if (pagoCom === 'transfer') {
    bankTx(pagamento.conta || 'principal', d, hhmm, isCompra ? 'withdrawal' : 'deposit', isCompra ? -total : total, `${rotulo} #${num}`, { order_id: pid, payment_method: 'transfer' });
    if (caixa) cashTx(caixa, d, hhmm, tipo, 0, `${rotulo} #${num} (PIX/Transferência)`, { order_id: pid });
  } else if (pagoCom === 'balance') {
    saldo(isCompra ? 'supplier' : 'customer', isCompra ? id(`fornecedor.${parceiroK}`) : id(`cliente.${parceiroK}`), total, d, hhmm, `${rotulo} #${num}`, { order_id: pid, payment_method: 'balance' });
    if (caixa) cashTx(caixa, d, hhmm, tipo, 0, `${rotulo} #${num} (Saldo)`, { order_id: pid });
  }
  return { ...head, num, total };
}
const item = (m, q, p, imp = 0) => ({ m, q: r1(q), p, imp, total: r2((r1(q) - imp) * p) });
const precoCompra = (m, delta = 0) => r2(MAT[m].pc + delta);
const precoVenda = (m, delta = 0) => r2(MAT[m].pv + delta);
// quanto fica no pátio depois de uma venda (sobra natural, nunca número redondo)
const sobra = (m, a, b) => r1(estoque[m] - between(a, b));
// volume do pátio: ~120 mil reais de compra por mês (o que paga folha, aluguel e energia com a margem de 15 a 30%)
const ESC = 2.2;

// semana a semana: transferências do banco para o cofre seguram o dinheiro do pátio
const dias = [];
for (let d = INICIO; d < HOJE; d = addDays(d, 1)) if (weekday(d) !== 0) dias.push(d);

// saldo inicial do cofre (ativação em 01/08) e do banco
cashTx(null, INICIO, '07:15', 'adjustment', 12000, 'Saldo inicial do dinheiro (ativação do cofre)', { excluded_from_dre: true });
bankTx('principal', INICIO, '07:00', 'deposit', 116250, 'Saldo inicial', { source: 'manual', excluded_from_dre: true });
bankTx('reserva', INICIO, '07:00', 'deposit', 40000, 'Saldo inicial', { source: 'manual', excluded_from_dre: true });

let adiantamentoValdir = false;
for (const d of dias) {
  const wd = weekday(d); // 1 seg ... 6 sáb
  const sab = wd === 6;
  const abre = sab ? '07:30' : '07:30';
  const fecha = sab ? '12:40' : '17:40';
  // segunda: reforço do cofre a partir do banco (saque)
  if (wd === 1 && gavetaCofre + saldoBanco.cofre < 26000) {
    const valor = Math.ceil((30000 - (gavetaCofre + saldoBanco.cofre)) / 500) * 500;
    const g = id(`grupo_transf.${d}`);
    bankTx('principal', d, '07:10', 'transfer', -valor, 'Transferência para DINHEIRO (COFRE)', { group_id: g });
    bankTx('cofre', d, '07:10', 'transfer', valor, 'Transferência de Conta Principal', { group_id: g });
  }
  caixaNum++;
  const caixa = add('cash_register', {
    id: id(`caixa.${d}`), company_id: COMPANY, register_number: caixaNum, status: 'closed', opened_at: at(d, abre), opened_by: RAFAEL,
    initial_opening_balance: 1500, opening_balance: 1500, closing_balance: null, closed_at: at(d, fecha), currency: 'BRL', created_at: at(d, abre),
  });
  caixa.saldo = 1500;
  cashTx(caixa, d, abre, 'opening', 1500, `Abertura do Caixa #${caixaNum}`);
  // reforço do caixa durante o dia quando a gaveta vai faltar (saída do cofre para a gaveta)
  let minuto = 7 * 60 + 50;
  const proximo = (min = 12, max = 45) => { minuto += Math.round(between(min, max)); return hm(Math.min(minuto, sab ? 12 * 60 + 30 : 17 * 60 + 25)); };
  const compras = [];
  // Dona Cida: latinha e papelão quase todo dia
  if (rnd() < 0.85) compras.push(['cida', [item('al_latinha', ESC * between(18, 46), precoCompra('al_latinha')), item('papelao', ESC * between(60, 160), precoCompra('papelao'))], 'cash']);
  // Valdir: carroceiro, 2 a 3 vezes por semana
  if ([1, 3, 5].includes(wd) && rnd() < 0.8) compras.push(['valdir', [item('ferro_misto', ESC * between(180, 420), precoCompra('ferro_misto')), ...(rnd() < 0.5 ? [item('chaparia', ESC * between(80, 200), precoCompra('chaparia'))] : []), ...(rnd() < 0.35 ? [item('fio_cobre', ESC * between(4, 12), precoCompra('fio_cobre'))] : [])], 'cash']);
  // Cooperativa Recomeço: quarta, latinha e PET em volume, por PIX
  if (wd === 3) compras.push(['recomeco', [item('al_latinha', ESC * between(160, 300), precoCompra('al_latinha', -0.10)), item('pet', ESC * between(220, 420), precoCompra('pet'))], 'transfer']);
  // Depósito Irmãos Siqueira: quinta, carga mista, por PIX
  if (wd === 4) compras.push(['siqueira', [item('ferro_pesado', ESC * between(2400, 4200), precoCompra('ferro_pesado', 0.05)), item('cobre_misto', ESC * between(25, 60), precoCompra('cobre_misto', 0.5)), item('al_perfil', ESC * between(40, 110), precoCompra('al_perfil')), ...(rnd() < 0.6 ? [item('latao', ESC * between(15, 40), precoCompra('latao'))] : [])], 'transfer']);
  // Auto Peças Vale Forte: a cada ~10 dias, bateria, radiador e sucata de oficina
  if (d.endsWith('-05') || d.endsWith('-15') || d.endsWith('-25')) compras.push(['valeforte', [item('bateria', ESC * between(180, 360), precoCompra('bateria')), item('cobre_misto', ESC * between(12, 30), precoCompra('cobre_misto')), item('al_bloco', ESC * between(40, 90), precoCompra('al_bloco')), item('ferro_pesado', ESC * between(300, 700), precoCompra('ferro_pesado'))], 'transfer']);
  // balcão (sem cadastro): 1 a 4 por dia
  const balcao = sab ? 1 + Math.floor(rnd() * 2) : 1 + Math.floor(rnd() * 4);
  for (let i = 0; i < balcao; i++) {
    const op = rnd();
    const its = op < 0.35 ? [item('ferro_misto', ESC * between(25, 140), precoCompra('ferro_misto'))]
      : op < 0.6 ? [item('al_latinha', ESC * between(3, 15), precoCompra('al_latinha'))]
      : op < 0.75 ? [item('cobre_mel', ESC * between(1.5, 7), precoCompra('cobre_mel'))]
      : op < 0.85 ? [item('latao', ESC * between(2, 9), precoCompra('latao'))]
      : op < 0.92 ? [item('bronze', ESC * between(1.5, 6), precoCompra('bronze'))]
      : [item('inox', ESC * between(10, 45), precoCompra('inox'))];
    compras.push([null, its, 'cash']);
  }
  // embaralha a ordem do dia
  compras.sort(() => rnd() - 0.5);
  for (const [k, its, forma0] of compras) {
    const h = proximo();
    // Siqueira é fornecedor e cliente: quando ele deve muito (vendas no saldo), a compra dele abate do saldo unificado
    const forma = k === 'siqueira' && (saldoParceiro[`party:${id('cliente.siqueira')}`] || 0) > 6000 ? 'balance'
      : k === 'valeforte' && d === '2026-11-05' ? 'balance' // compra a prazo: a empresa fica devendo à Vale Forte
      : forma0;
    // Valdir: o adiantamento de 28/10 abate na compra seguinte? fica em aberto (adiantamento a favor da empresa)
    pedido('purchase', d, h, k, its, { forma }, caixa);
  }
  // vendas
  // outubro: a Aços Quiririm parou o forno para manutenção (só comprou em 05/10) e a Serra Fina pulou duas sextas:
  // o pátio comprou muito e vendeu pouco no mês (o exemplo do T15, caixa x competência); o estoque sai em novembro
  const pausaQuiririm = d >= '2026-10-12' && d <= '2026-10-31'; // forno da Aços Quiririm parado de 12 a 31/10
  if (wd === 1 && !pausaQuiririm) { // Aços Quiririm: ferro e chaparia, por PIX, com motorista do cliente
    const teto = d >= '2026-11-01' ? 1.9 : d >= '2026-10-01' ? 0.75 : 1; // outubro: forno parado, cargas menores; novembro leva o acumulado
    const its = [item('ferro_pesado', Math.min(sobra('ferro_pesado', 1200, 1900), ESC * between(5200, 8200) * teto), QUIRIRIM_VENDA.ferro_pesado), item('ferro_misto', Math.min(sobra('ferro_misto', 700, 1200), ESC * between(2200, 4200) * teto), QUIRIRIM_VENDA.ferro_misto), item('chaparia', Math.min(sobra('chaparia', 400, 800), ESC * between(1100, 2400) * teto), QUIRIRIM_VENDA.chaparia)].filter((x) => x.q > 50);
    if (its.length) pedido('sale', d, proximo(), 'quiririm', its, { forma: 'transfer' }, caixa, { motorista: 'Paulo Henrique', placa: 'FTQ3H52' });
  }
  if (wd === 5 && d !== '2026-10-16' && d !== '2026-10-23') { // Serra Fina: alumínio, por PIX
    const its = [item('al_latinha', sobra('al_latinha', 150, 260), precoVenda('al_latinha')), item('al_perfil', sobra('al_perfil', 80, 140), precoVenda('al_perfil')), item('al_bloco', sobra('al_bloco', 60, 110), precoVenda('al_bloco'))].filter((x) => x.q > 20);
    if (its.length) pedido('sale', d, proximo(), 'serrafina', its, { forma: 'transfer' }, caixa);
  }
  const semana = Math.floor((new Date(`${d}T12:00:00Z`) - new Date('2026-08-03T12:00:00Z')) / (7 * 86400000));
  if (wd === 2 && ((semana % 2 === 1 && d !== '2026-10-06') || d === '2026-10-20')) { // Fundição Bandeira do Vale: cobre, latão e bronze, a cada 2 semanas (20/10 é a do fiado)
    const its = [item('cobre_mel', sobra('cobre_mel', 40, 80), precoVenda('cobre_mel')), item('cobre_misto', sobra('cobre_misto', 25, 55), precoVenda('cobre_misto')), item('fio_cobre', sobra('fio_cobre', 10, 25), precoVenda('fio_cobre')), item('latao', sobra('latao', 15, 35), precoVenda('latao')), item('bronze', sobra('bronze', 10, 30), precoVenda('bronze'))].filter((x) => x.q > 10);
    // o fiado parcelado: a venda de 20/10 vai para o saldo do cliente, em 3 parcelas (30/60/90)
    const fiado = d === '2026-10-20';
    if (its.length) {
      const v = pedido('sale', d, proximo(), 'bandeira', its, { forma: fiado ? 'balance' : 'transfer' }, caixa);
      if (fiado) {
        const parc = [r2(v.total / 3), r2(v.total / 3)];
        parc.push(r2(v.total - parc[0] - parc[1]));
        ['2026-11-19', '2026-12-19', '2027-01-18'].forEach((due, i) => add('financial_bills', {
          id: id(`titulo.fiado_bandeira.${i + 1}`), company_id: COMPANY, direction: 'receivable', description: `Venda #${v.num} - parcela ${i + 1}/3`, amount: parc[i], currency: 'BRL',
          due_date: due, status: 'pending', paid_amount: 0, order_id: v.id, order_type: 'sale', partner_id: id('cliente.bandeira'), partner_type: 'customer',
          installment_number: i + 1, installment_total: 3, payment_condition_id: id('condicao.30_60_90'), source_type: 'order', category_id: null, created_by: RAFAEL, created_at: at(d, '15:00'), updated_at: at(d, '15:00'),
        }));
      }
    }
  }
  if (wd === 6 && d.slice(8) <= '07') { // Siqueira compra inox e bateria no 1º sábado do mês (saldo unificado)
    const its = [item('inox', sobra('inox', 90, 160), precoVenda('inox', -0.2)), item('bateria', Math.min(sobra('bateria', 200, 380), 2000), precoVenda('bateria', -0.1)), item('papelao', sobra('papelao', 400, 900), precoVenda('papelao')), item('pet', sobra('pet', 250, 600), precoVenda('pet'))].filter((x) => x.q > 30);
    if (its.length) pedido('sale', d, proximo(), 'siqueira', its, { forma: 'balance' }, caixa);
  }
  if (wd === 6 && d.slice(8) >= '15' && d.slice(8) <= '21') { // 3º sábado: o Siqueira leva papelão e PET de novo
    const its = [item('papelao', sobra('papelao', 300, 800), precoVenda('papelao')), item('pet', sobra('pet', 200, 500), precoVenda('pet'))].filter((x) => x.q > 30);
    if (its.length) pedido('sale', d, proximo(), 'siqueira', its, { forma: 'balance' }, caixa);
  }
  // despesas do caixa: combustível na terça, almoço da equipe de vez em quando
  if (wd === 2) cashTx(caixa, d, proximo(), 'withdrawal', r2(between(220, 340)), 'Combustível da picape', { category_id: id('categoria.combustivel'), cost_center_id: id('cc.patio') });
  if (rnd() < 0.25 && !sab) cashTx(caixa, d, proximo(), 'withdrawal', r2(between(60, 140)), 'Almoço da equipe', { category_id: id('categoria.alimentacao'), cost_center_id: id('cc.patio') });
  // adiantamento ao Valdir (28/10): sai do caixa e fica como crédito da empresa no saldo dele
  if (d === '2026-10-28' && !adiantamentoValdir) {
    adiantamentoValdir = true;
    const h = proximo();
    // como pay_partner_balance: saída do caixa fora da DRE e baixa no saldo do fornecedor (fica negativo = ele deve material)
    cashTx(caixa, d, h, 'withdrawal', 300, 'Pagamento de saldo', { excluded_from_dre: true });
    saldo('supplier', id('fornecedor.valdir'), -300, d, h, 'Baixa de saldo (Pagamento)', { movement_type: 'payment', payment_method: 'cash' });
  }
  // o troco da abertura sai do cofre (opening/closing não mexem no cofre): abre com o bastante para o dia não faltar
  if ((caixa.minimo ?? 0) < 120) {
    const extra = Math.ceil((120 - caixa.minimo) / 500) * 500;
    caixa.initial_opening_balance += extra;
    caixa.saldo = r2(caixa.saldo + extra);
    const tx = T.cash_transactions.find((x) => x.cash_register_id === caixa.id && x.type === 'opening');
    tx.amount = r2(tx.amount + extra);
  }
  delete caixa.minimo;
  if (d === '2026-11-07') {
    // como pay_partner_balance (recebimento): entra no banco fora da DRE e o saldo do cliente fica negativo
    bankTx('principal', d, '09:15', 'deposit', 2000, 'Recebimento de saldo', { excluded_from_dre: true, payment_method: 'transfer' });
    saldo('customer', id('cliente.serrafina'), -2000, d, '09:15', 'Baixa de saldo (Recebimento)', { movement_type: 'payment', payment_method: 'transfer' });
  }
  // fechamento: devolve a gaveta ao cofre
  caixa.closing_balance = r2(caixa.saldo);
  caixa.opening_balance = r2(caixa.saldo);
  cashTx(caixa, d, fecha, 'closing', caixa.saldo, 'Fechamento de caixa');
  delete caixa.saldo;

  // banco: despesas fixas e recebimentos do mês
  const dia = Number(d.slice(8));
  if (dia === 5 || (dia === 6 && weekday(addDays(d, -1)) === 0)) bankTx('principal', d, '09:00', 'withdrawal', -4800, 'Aluguel do pátio', { category_id: id('categoria.aluguel'), cost_center_id: id('cc.patio') });
  if (dia === 10 || (dia === 11 && weekday(addDays(d, -1)) === 0)) bankTx('principal', d, '09:10', 'withdrawal', -r2(between(1650, 2150)), 'Conta de energia', { category_id: id('categoria.energia'), cost_center_id: id('cc.patio') });
  if (dia === 30 || (d.slice(5) === '08-31' && false)) bankTx('principal', d, '16:00', 'withdrawal', -14600, 'Folha salarial do mês', { category_id: id('categoria.folha') });
  if (dia === 1 || (dia === 2 && weekday(addDays(d, -1)) === 0)) bankTx('principal', d, '08:00', 'withdrawal', -89.9, 'Tarifa do pacote de serviços', { category_id: id('categoria.tarifa') });
  if (dia === 20) bankTx('principal', d, '10:00', 'withdrawal', -r2(between(380, 920)), 'Manutenção da prensa e da balança', { category_id: id('categoria.manutencao'), cost_center_id: id('cc.patio') });
}
// folha de 31/10 (sábado): paga na sexta 30/10 já entrou; agosto (30/08 domingo) -> 31/08
bankTx('principal', '2026-08-31', '16:00', 'withdrawal', -14600, 'Folha salarial do mês', { category_id: id('categoria.folha') });

// saldos gravados (o que os triggers do banco manteriam)
for (const m of Object.values(MAT)) T.materials.find((x) => x.id === m.id).current_stock = r1(estoque[m.k]);
const cofreTotal = r2(gavetaCofre + saldoBanco.cofre);
// o mundo pede R$ 18.500,00 no cofre em 10/11: o saldo inicial de 01/08 é o que fecha a conta
const ajusteIni = T.cash_transactions.find((x) => x.type === 'adjustment' && x.cash_register_id === null);
const delta = r2(18500 - cofreTotal);
ajusteIni.amount = r2(ajusteIni.amount + delta);
gavetaCofre = r2(gavetaCofre + delta);
T.bank_accounts.find((x) => x.id === id('banco.cofre')).balance = r2(gavetaCofre + saldoBanco.cofre);
T.bank_accounts.find((x) => x.id === id('banco.principal')).balance = saldoBanco.principal;
T.bank_accounts.find((x) => x.id === id('banco.reserva')).balance = saldoBanco.reserva;
for (const [key, v] of Object.entries(saldoParceiro)) {
  const [et, eid] = [key.slice(0, key.indexOf(':')), key.slice(key.indexOf(':') + 1)];
  add('balances', { id: id(`saldo.${key}`), company_id: COMPANY, entity_type: et, entity_id: eid, balance: v, currency: 'BRL', created_at: '2026-08-01T12:00:00.000Z', updated_at: '2026-11-09T18:00:00.000Z' });
}

// contas a pagar e a receber abertas em novembro (e as recorrências)
const recorrente = (k, desc, valor, dia, cat) => add('recurring_bill_templates', {
  id: id(`recorrencia.${k}`), company_id: COMPANY, direction: 'payable', description: desc, amount: valor, frequency: 'monthly', interval: 1, is_active: true,
  start_date: `2026-08-${pad(dia)}`, next_due_date: `2026-12-${pad(dia)}`, category_id: id(`categoria.${cat}`), expected_bank_account_id: id('banco.principal'), expected_payment_method: 'transfer', created_by: RAFAEL, created_at: '2026-07-31T12:00:00.000Z', updated_at: '2026-11-01T12:00:00.000Z',
});
recorrente('aluguel', 'Aluguel do pátio', 4800, 5, 'aluguel');
recorrente('energia', 'Conta de energia', 1900, 15, 'energia');
const titulo = (k, dir, desc, valor, due, extra = {}) => add('financial_bills', {
  id: id(`titulo.${k}`), company_id: COMPANY, direction: dir, description: desc, amount: valor, currency: 'BRL', due_date: due, status: 'pending', paid_amount: 0,
  created_by: RAFAEL, created_at: '2026-11-01T12:00:00.000Z', updated_at: '2026-11-01T12:00:00.000Z', expected_bank_account_id: id('banco.principal'), ...extra,
});
titulo('aluguel_nov', 'payable', 'Aluguel do pátio', 4800, '2026-11-05', { status: 'paid', paid_amount: 4800, paid_at: at('2026-11-05', '09:00'), recurring_template_id: id('recorrencia.aluguel'), category_id: id('categoria.aluguel'), source_type: 'recurring' });
titulo('energia_nov', 'payable', 'Conta de energia', 1987.4, '2026-11-16', { recurring_template_id: id('recorrencia.energia'), category_id: id('categoria.energia'), source_type: 'recurring' });
titulo('aluguel_dez', 'payable', 'Aluguel do pátio', 4800, '2026-12-05', { recurring_template_id: id('recorrencia.aluguel'), category_id: id('categoria.aluguel'), source_type: 'recurring', is_projection: true });
titulo('manutencao_prensa', 'payable', 'Revisão da prensa enfardadeira', 1350, '2026-11-12', { category_id: id('categoria.manutencao'), cost_center_id: id('cc.patio') });
titulo('epi', 'payable', 'Luvas e botas (EPI) da equipe', 640, '2026-11-18', { category_id: id('categoria.outras_despesas') });
titulo('frete_quiririm', 'receivable', 'Frete cobrado da Aços Quiririm', 450, '2026-11-06', { partner_id: id('cliente.quiririm'), partner_type: 'customer', category_id: id('categoria.servicos') });

// ticket de pesagem aguardando valorização (T8): caminhão do Siqueira pesado na entrada, saída ontem à tarde
add('weighing_tickets', {
  id: id('ticket.1'), company_id: COMPANY, ticket_number: 87, ticket_seq: 87, ticket_ref: '#87', status: 'pending', ticket_kind: 'standard', type: 'purchase',
  customer_supplier_id: id('fornecedor.siqueira'), customer_supplier_name: 'Depósito Irmãos Siqueira', customer_supplier_type: 'supplier',
  driver_name: 'Joel Siqueira', vehicle_plate: 'BRS5D27', vehicle_type: 'Caminhão toco', first_weight: 11840, first_weight_at: at('2026-11-09', '15:20'),
  second_weight: 7960, second_weight_at: at('2026-11-09', '15:52'), net_weight: 3880, material_id: MAT.ferro_pesado.id, material_name: MAT.ferro_pesado.nome,
  pricing_mode: 'weighing_only', items: [], attachments: [], created_by: RAFAEL, created_at: at('2026-11-09', '15:20'), updated_at: at('2026-11-09', '15:52'),
});

// agenda (dashboard e T25)
const tarefa = (k, title, date, time, extra = {}) => add('schedule_tasks', { id: id(`tarefa.${k}`), company_id: COMPANY, title, scheduled_date: date, scheduled_time: time, category: 'tarefa', status: 'pendente', priority: 'media', created_by: RAFAEL, assigned_to: RAFAEL, created_at: '2026-11-06T12:00:00.000Z', updated_at: '2026-11-06T12:00:00.000Z', notify_on_day: true, notify_minutes_before: 0, notify_push: false, ...extra });
tarefa('quiririm', 'Carregamento Aços Quiririm', '2026-11-10', '14:00', { customer_supplier_id: id('cliente.quiririm'), customer_supplier_name: 'Aços Quiririm Ltda', description: 'Separar ferro pesado e chaparia para a carga de terça.' });
tarefa('prensa', 'Revisão da prensa enfardadeira', '2026-11-12', '08:00', { priority: 'alta' });
tarefa('cooperativa', 'Buscar material na Cooperativa Recomeço', '2026-11-11', '09:30', { supplier_id: id('fornecedor.recomeco'), supplier_name: 'Cooperativa Recomeço' });

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
];

// ---------------------------------------------------------------- grava
fs.mkdirSync(OUT, { recursive: true });
const grava = (nome, tabelas) => {
  const obj = {};
  for (const t of tabelas) if (T[t]?.length) obj[t] = T[t];
  const lines = ['{'];
  const ents = Object.entries(obj);
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
const n1 = grava('01-empresa.json', ['companies', 'profiles', 'user_roles', 'user_shortcuts', 'nps_surveys', 'subscription_modules', 'subscription_plans', 'company_modules', 'app_config', 'currencies']);
const n2 = grava('02-cadastros.json', ['material_groups', 'materials', 'price_tables', 'price_table_items', 'suppliers', 'customers', 'vehicles', 'drivers', 'bank_accounts', 'financial_categories', 'cost_centers', 'payment_conditions']);
const n3 = grava('03-historico.json', ['cash_register', 'purchases', 'purchase_items', 'sales', 'sale_items', 'stock_movements', 'cash_transactions', 'bank_transactions', 'balances', 'balance_movements', 'financial_bills', 'recurring_bill_templates', 'weighing_tickets', 'schedule_tasks']);

// ---------------------------------------------------------------- sementes extras do mundo base
const EXTRA = path.join(MUNDO, 'seeds-extra', 'base');
fs.mkdirSync(EXTRA, { recursive: true });
{
  // caixa #87 de hoje, aberto às 07:30 com R$ 1.500,00; Dona Cida às 07:52 e uma compra de balcão às 08:14
  const antes = { ...estoque };
  const ini = { cash_transactions: T.cash_transactions.length, stock_movements: T.stock_movements.length, purchases: (T.purchases || []).length, purchase_items: (T.purchase_items || []).length };
  const caixa = { id: id(`caixa.${HOJE}`), company_id: COMPANY, register_number: caixaNum + 1, status: 'open', opened_at: at(HOJE, '07:30'), opened_by: RAFAEL, initial_opening_balance: 1500, opening_balance: 1500, closing_balance: null, closed_at: null, currency: 'BRL', created_at: at(HOJE, '07:30'), saldo: 1500 };
  cashTx(caixa, HOJE, '07:30', 'opening', 1500, `Abertura do Caixa #${caixa.register_number}`);
  pedido('purchase', HOJE, '07:52', 'cida', [item('al_latinha', 31.4, precoCompra('al_latinha')), item('papelao', 118.6, precoCompra('papelao'))], { forma: 'cash' }, caixa);
  pedido('purchase', HOJE, '08:14', null, [item('cobre_mel', 4.2, precoCompra('cobre_mel'))], { forma: 'cash' }, caixa);
  caixa.opening_balance = caixa.saldo;
  delete caixa.saldo;
  delete caixa.minimo;
  const novos = (t) => (T[t] || []).slice(ini[t]);
  const patch = Object.entries(estoque).filter(([k, v]) => v !== antes[k]).map(([k, v]) => ({ match: { id: MAT[k].id }, set: { current_stock: v } }));
  const obj = {
    _doc: `Caixa de hoje (#${caixa.register_number}) aberto pelo Rafael às 07:30 com R$ 1.500,00 de troco, com as duas compras da manhã (Dona Cida às 07:52 e uma de balcão às 08:14): estado de partida das aulas que compram e vendem (T7 em diante). Gerado por gerar/sementes.mjs. Aplicar com "seedExtra": ["base/caixa-aberto"].`,
    cash_register: [caixa], purchases: novos('purchases'), purchase_items: novos('purchase_items'), stock_movements: novos('stock_movements'), cash_transactions: novos('cash_transactions'),
    // saldo gravado do cofre (o trigger do banco recalcula a cada lançamento do caixa)
    _patch: { materials: patch, bank_accounts: [{ match: { id: id('banco.cofre') }, set: { balance: r2(gavetaCofre + saldoBanco.cofre) } }] },
  };
  fs.writeFileSync(path.join(EXTRA, 'caixa-aberto.json'), JSON.stringify(obj, null, 1) + '\n');
  // desfaz no estado do gerador (o mundo base fica sem o caixa de hoje)
  for (const t of Object.keys(ini)) T[t].length = ini[t];
  Object.assign(estoque, antes);
  ordem -= 2;
}
fs.writeFileSync(path.join(EXTRA, 'balanca-ativada.json'), JSON.stringify({
  _doc: 'Integração com a balança ligada no perfil do Rafael (Configurações > Integrações, aula do EcoTray): o app abre o WebSocket do EcoTray (8053/8054), que o robô simula. Impressão direta pelo EcoTray na térmica "Elgin i9 (USB)", bobina de 80 mm. Aplicar com "seedExtra": ["base/balanca-ativada"].',
  _patch: { profiles: [{ match: { id: RAFAEL }, set: { balanca_ativada: true, balanca_continua: true, balanca_decimais: 1, balanca_unidade: 'kg', balanca_url: 'ws://127.0.0.1:8053', direct_print_enabled: true, direct_print_printer_name: 'Elgin i9 (USB)', thermal_print_mode: 'pdf', receipt_paper_width_mm: 80 } }] },
}, null, 1) + '\n');

const fmt = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
console.log(`sementes: empresa ${n1} linhas, cadastros ${n2}, histórico ${n3} -> ${OUT}`);
console.log(`  ${T.purchases.length} compras, ${T.sales.length} vendas, ${T.cash_register.length} caixas, pedidos #1241 a #${ordem}`);
console.log(`  cofre R$ ${fmt(T.bank_accounts.find((x) => x.kind === 'cash').balance)} (saldo inicial ${fmt(ajusteIni.amount)}), Conta Principal R$ ${fmt(saldoBanco.principal)}, Conta Reserva R$ ${fmt(saldoBanco.reserva)}`);
console.log(`  estoque: ${Object.entries(estoque).map(([k, v]) => `${k} ${v}`).join(', ')}`);
console.log(`  saldos de parceiro: ${Object.entries(saldoParceiro).map(([k, v]) => `${k.split(':')[0]} ${fmt(v)}`).join(', ')}`);
