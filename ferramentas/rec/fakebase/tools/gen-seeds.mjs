#!/usr/bin/env node
// Gera os seeds iniciais do mundo falso da serie (empresa "Glacial Cold Brasil", Niteroi/RJ) em seeds/gen-*.json.
//   node rec/fakebase/tools/gen-seeds.mjs
//
// Os arquivos gen-*.json sao SAIDA deste script (sobrescritos a cada execucao). Para acrescentar dados sem
// risco de perder, crie outro arquivo em seeds/ (qualquer nome que nao comece com "gen-"). Tokens aceitos nos
// valores: @id:chave  @today+3d  @now-2h  @at:+2d 09:30  @month:+0:05  @seq:nome  (ver core/util.mjs).
//
// Todo CPF/CNPJ aqui tem digito verificador valido (o app valida) — ver tools/docs.mjs.
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { cnpj, cpf } from './docs.mjs';
import { shortCode } from '../core/util.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const SEEDS = path.resolve(here, '../seeds');
const id = (k) => `@id:${k}`;
const CO = id('company.glacial');

const out = {}; // arquivo -> { tabela: [linhas] }
const add = (file, table, rows) => {
  (out[file] ||= {})[table] ||= [];
  out[file][table].push(...(Array.isArray(rows) ? rows : [rows]));
};

// ============================================================================================
// 1) Tenant: empresa, assinatura, modulos, usuarios
// ============================================================================================
const F1 = 'gen-01-tenant';
const GLACIAL_CNPJ = cnpj('91520340');
// Logos da Glacial Cold Brasil (brand-fix/assets, reduzidos) servidos pelo storage falso: rec/fakebase/storage/company-logos/glacial/
const LOGO_URL = '@storage:company-logos/glacial/logo-horizontal.png';
const ICON_URL = '@storage:company-logos/glacial/icone.png';

add(F1, 'companies', {
  id: CO,
  name: 'Glacial Cold Brasil',
  cnpj: GLACIAL_CNPJ,
  email: 'contato@glacialcold.example',
  phone: '(21) 3000-1000',
  address: 'Rua Moreira César',
  address_number: '200',
  neighborhood: 'Icaraí',
  city: 'Niterói',
  state: 'RJ',
  zip_code: '24230-190',
  segment: 'refrigeracao',
  logo_url: LOGO_URL,
  contact_name: 'Camila Duarte',
  billing_email: 'financeiro@glacialcold.example',
  subscription_status: 'active',
  subscription_plan: 'master',
  subscription_value: 597,
  billing_cycle: 'monthly',
  subscription_expires_at: '@now+23d',
  max_users: 20,
  extra_users: 0,
  ltv: 7164,
  payment_lock_bypass: false,
  payment_method: 'credit_card',
  subscription_card_brand: 'visa',
  subscription_card_last4: '4242',
  is_demo: false,
  is_self_service: true,
  created_at: '@now-380d',
  updated_at: '@now-2d',
});

add(F1, 'company_settings', {
  id: id('company_settings.glacial'),
  company_id: CO,
  name: 'Glacial Cold Brasil',
  document: GLACIAL_CNPJ,
  phone: '(21) 3000-1000',
  email: 'contato@glacialcold.example',
  address: 'Rua Moreira César',
  address_number: '200',
  neighborhood: 'Icaraí',
  city: 'Niterói',
  state: 'RJ',
  zip_code: '24230-190',
  segment: 'refrigeracao',
  logo_url: LOGO_URL,
  white_label_logo_url: LOGO_URL,
  white_label_icon_url: ICON_URL,
  language: 'pt-br',
  currency: 'BRL',
  country_code: 'BR',
  timezone: 'America/Sao_Paulo',
  white_label_enabled: false,
  show_name_in_documents: true,
  show_cnpj_in_documents: true,
  show_address_in_documents: true,
  show_phone_in_documents: true,
  show_email_in_documents: true,
  os_stock_consumption_enabled: true,
  os_finish_revenue_prompt_enabled: true,
});

// Planos e modulos
const MODULES_ALL = ['basic', 'rh', 'crm', 'contracts', 'nfe', 'pricing_advanced', 'customer_portal', 'white_label', 'video_questions', 'whatsapp', 'cobrancas', 'finance_advanced'];
add(F1, 'subscription_plans', [
  { id: id('plan.start'), code: 'start', name: 'Start', description: 'Para quem está começando', price: 197, max_users: 3, included_modules: ['basic'], is_active: true },
  { id: id('plan.avancado'), code: 'avancado', name: 'Avançado', description: 'Equipe em crescimento', price: 347, max_users: 8, included_modules: ['basic', 'crm', 'contracts'], is_active: true },
  { id: id('plan.master'), code: 'master', name: 'Master', description: 'Operação completa', price: 597, max_users: 20, included_modules: MODULES_ALL, is_active: true },
]);
for (const code of [...MODULES_ALL, 'pdv']) {
  add(F1, 'company_modules', { id: id(`cm.${code}`), company_id: CO, module_code: code, quantity: 1, activated_at: '@now-300d' });
}

// Conta de recebimentos ativa: sem ela a ficha do cliente nao mostra a aba "Cobrancas" (modulo cobrancas + conta ativa)
add(F1, 'tenant_payment_accounts', {
  id: id('tpa.glacial'), company_id: CO, provider: 'asaas', mode: 'production', status: 'active',
  asaas_account_id: 'acc_glacial_demo', wallet_id: 'wallet_glacial_demo', auto_post_to_finance: true, auto_post_fees: false,
  default_fine_percent: 2, default_interest_percent: 1, default_due_days: 3, default_discount_percent: null, default_discount_days: null,
  default_description: null, allow_pix: true, allow_boleto: true, allow_card: true, default_max_installments: 1,
  default_finance_account_id: null, default_income_category: null, default_fee_category: 'Taxas de cobrança',
  card_recurring_enabled: false, pix_auto_enabled: false, card_fee_payer: 'tenant', created_at: '@now-200d', updated_at: '@now-200d',
});

// Pessoas: Camila (gestora administradora) + 6 tecnicos. Todos podem logar com qualquer senha.
const PEOPLE = [
  { key: 'camila', name: 'Camila Duarte', email: 'camila.duarte@glacialcold.example', phone: '(21) 3000-1001', role: 'admin' },
  { key: 'rafael', name: 'Rafael Lima', email: 'rafael.lima@glacialcold.example', phone: '(21) 3000-1002', role: 'tecnico', cpf: '184530927' },
  { key: 'bruno', name: 'Bruno Alves', email: 'bruno.alves@glacialcold.example', phone: '(21) 3000-1003', role: 'tecnico', cpf: '297416385' },
  { key: 'julia', name: 'Júlia Santos', email: 'julia.santos@glacialcold.example', phone: '(21) 3000-1004', role: 'tecnico', cpf: '358209164' },
  { key: 'lucas', name: 'Lucas Ferreira', email: 'lucas.ferreira@glacialcold.example', phone: '(21) 3000-1005', role: 'tecnico', cpf: '416385952' },
  { key: 'marina', name: 'Marina Costa', email: 'marina.costa@glacialcold.example', phone: '(21) 3000-1006', role: 'tecnico', cpf: '523071846' },
  { key: 'paulo', name: 'Paulo Souza', email: 'paulo.souza@glacialcold.example', phone: '(21) 3000-1007', role: 'tecnico', cpf: '631840259' },
];
for (const p of PEOPLE) {
  add(F1, 'profiles', {
    id: id(`profile.${p.key}`),
    user_id: id(`user.${p.key}`),
    company_id: CO,
    full_name: p.name,
    email: p.email,
    phone: p.phone,
    is_active: true,
    navigation_style: 'sidebar',
    terms_accepted_at: '@now-360d',
    created_at: '@now-360d',
  });
  add(F1, 'user_roles', { id: id(`role.${p.key}`), user_id: id(`user.${p.key}`), role: p.role });
}
// A usuaria logada e a Camila (id fixo em core/config.mjs: stableId('user.camila')).
add(F1, 'user_preferences', { user_id: id('user.camila'), language: 'pt-br' });


// ============================================================================================
// 2) Cadastros: clientes, contatos, fornecedores, equipamentos
// ============================================================================================
const F2 = 'gen-02-cadastros';

add(F2, 'customer_origins', [
  { id: id('origin.indicacao'), company_id: CO, name: 'Indicação', icon: 'Users', color: '#22C55E', is_active: true },
  { id: id('origin.instagram'), company_id: CO, name: 'Instagram', icon: 'Instagram', color: '#EC4899', is_active: true },
  { id: id('origin.google'), company_id: CO, name: 'Google', icon: 'Search', color: '#EAB308', is_active: true },
  { id: id('origin.whatsapp'), company_id: CO, name: 'WhatsApp', icon: 'MessageCircle', color: '#10B981', is_active: true },
]);

const CUSTOMERS = [
  { key: 'padaria', type: 'pj', name: 'Padaria Bom Grão', razao: 'Padaria Bom Grão Ltda', base: '91234501', street: 'Rua Gavião Peixoto', num: '112', bairro: 'Icaraí', cep: '24230-092', phone: '(21) 3000-2101', cel: '(21) 93000-2101', contact: ['Dona Neide Barros', 'Proprietária'], origin: 'Indicação', lat: -22.9051, lng: -43.1092, notes: 'Câmara fria e 3 splits no salão. Atendimento preferencial antes das 7h.' },
  { key: 'hotel', type: 'pj', name: 'Hotel Mirante do Mar', razao: 'Mirante do Mar Hotelaria Ltda', base: '91234502', street: 'Avenida Quintino Bocaiúva', num: '770', bairro: 'São Francisco', cep: '24360-000', phone: '(21) 3000-2102', cel: '(21) 93000-2102', contact: ['Sérgio Moraes', 'Gerente de manutenção'], origin: 'Google', lat: -22.9298, lng: -43.0969, notes: 'Contrato de manutenção preventiva mensal. Acesso pela garagem de serviço.' },
  { key: 'mercado', type: 'pj', name: 'Mercado Vila Nova', razao: 'Vila Nova Supermercados Ltda', base: '91234503', street: 'Rua Mariz e Barros', num: '455', bairro: 'Ingá', cep: '24210-125', phone: '(21) 3000-2103', cel: '(21) 93000-2103', contact: ['Adriana Teixeira', 'Gerente'], origin: 'Instagram', lat: -22.8995, lng: -43.1244 },
  { key: 'academia', type: 'pj', name: 'Academia Ponto Forte', razao: 'Ponto Forte Atividades Físicas Ltda', base: '91234504', street: 'Rua Lopes Trovão', num: '88', bairro: 'Icaraí', cep: '24220-071', phone: '(21) 3000-2104', cel: '(21) 93000-2104', contact: ['Ricardo Pimenta', 'Sócio'], origin: 'Indicação', lat: -22.9059, lng: -43.1105 },
  { key: 'restaurante', type: 'pj', name: 'Restaurante Sabor da Serra', razao: 'Sabor da Serra Alimentos Ltda', base: '91234505', street: 'Estrada Caetano Monteiro', num: '800', bairro: 'Pendotiba', cep: '24320-570', phone: '(21) 3000-2105', cel: '(21) 93000-2105', contact: ['Helena Prado', 'Chef e sócia'], origin: 'WhatsApp', lat: -22.9007, lng: -43.0455 },
  { key: 'clinica', type: 'pj', name: 'Clínica Sorriso Leve', razao: 'Sorriso Leve Odontologia Ltda', base: '91234506', street: 'Rua Miguel de Frias', num: '90', bairro: 'Icaraí', cep: '24220-001', phone: '(21) 3000-2106', cel: '(21) 93000-2106', contact: ['Dra. Patrícia Mendes', 'Diretora clínica'], origin: 'Google', lat: -22.9042, lng: -43.1081 },
  { key: 'escritorio', type: 'pj', name: 'Escritório Lemos & Prado', razao: 'Lemos & Prado Advogados Associados', base: '91234507', street: 'Rua da Conceição', num: '188', bairro: 'Centro', cep: '24020-081', phone: '(21) 3000-2107', cel: '(21) 93000-2107', contact: ['Dr. Carlos Lemos', 'Sócio-administrador'], origin: 'Indicação', lat: -22.8946, lng: -43.1239 },
  { key: 'farmacia', type: 'pj', name: 'Farmácia Vida Plena', razao: 'Vida Plena Drogaria Ltda', base: '91234508', street: 'Avenida Roberto Silveira', num: '301', bairro: 'Icaraí', cep: '24230-163', phone: '(21) 3000-2108', cel: '(21) 93000-2108', contact: ['Fábio Couto', 'Farmacêutico responsável'], origin: 'Instagram', lat: -22.9068, lng: -43.1058 },
  { key: 'pousada', type: 'pj', name: 'Pousada Brisa do Mar', razao: 'Brisa do Mar Turismo e Hospedagem Ltda', base: '91234509', street: 'Estrada Francisco da Cruz Nunes', num: '6500', bairro: 'Itaipu', cep: '24342-002', phone: '(21) 3000-2109', cel: '(21) 93000-2109', contact: ['Luciana Reis', 'Proprietária'], origin: 'WhatsApp', lat: -22.9615, lng: -43.0356 },
  { key: 'condominio', type: 'pj', name: 'Condomínio Jardim Azul', razao: 'Condomínio do Edifício Jardim Azul', base: '91234510', street: 'Rua Presidente Domiciano', num: '120', bairro: 'Boa Viagem', cep: '24210-270', phone: '(21) 3000-2110', cel: '(21) 93000-2110', contact: ['Seu Geraldo Antunes', 'Síndico'], origin: 'Indicação', lat: -22.9086, lng: -43.1278 },
  { key: 'mariana', type: 'pf', name: 'Mariana Lopes', cpf: '111444777', street: 'Rua Cinco de Julho', num: '210', bairro: 'Icaraí', cep: '24220-111', phone: '(21) 3000-2111', cel: '(21) 93000-2111', origin: 'Instagram', lat: -22.9029, lng: -43.1087, birth: '1988-04-17' },
  { key: 'roberto', type: 'pf', name: 'Roberto Nunes', cpf: '529982247', street: 'Rua Doutor Celestino', num: '75', bairro: 'Centro', cep: '24020-091', phone: '(21) 3000-2112', cel: '(21) 93000-2112', origin: 'Google', lat: -22.8963, lng: -43.1218, birth: '1975-11-02' },
];
const slugMail = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '');

CUSTOMERS.forEach((c, i) => {
  const isPj = c.type === 'pj';
  const doc = isPj ? cnpj(c.base) : cpf(c.cpf);
  add(F2, 'customers', {
    id: id(`customer.${c.key}`),
    company_id: CO,
    customer_type: c.type,
    name: c.name,
    company_name: isPj ? c.razao : null,
    nome_fantasia: isPj ? c.name : null,
    document: doc,
    email: isPj ? `contato@${slugMail(c.name)}.example` : `${slugMail(c.name)}@email.example`,
    phone: c.phone,
    celular: c.cel,
    whatsapp_notifications_enabled: true,
    address: c.street,
    address_number: c.num,
    street_number: c.num,
    neighborhood: c.bairro,
    city: 'Niterói',
    state: 'RJ',
    zip_code: c.cep,
    ibge_municipality_code: '3303302',
    latitude: c.lat,
    longitude: c.lng,
    lat: c.lat,
    lng: c.lng,
    birth_date: c.birth ?? null,
    origin: c.origin,
    notes: c.notes ?? null,
    is_deleted: false,
    is_service_customer: true,
    is_store_customer: false,
    public_short_code: shortCode(`customer.${c.key}`),
    created_at: `@now-${300 - i * 17}d`,
    updated_at: `@now-${20 - i}d`,
  });
  // gatilho trg_create_customer_portal_on_insert: todo cliente nasce com a linha do portal (token aleatorio, ativo)
  add(F2, 'customer_portals', {
    id: id(`portal.${c.key}`),
    customer_id: id(`customer.${c.key}`),
    token: crypto.createHash('sha256').update(`portal.${c.key}`).digest('hex').slice(0, 32),
    is_active: true,
    is_public: true,
    password_enabled: false,
    permissions: {},
    public_sections: {},
    created_at: `@now-${300 - i * 17}d`,
  });
  if (c.contact) {
    add(F2, 'customer_contacts', {
      id: id(`contact.${c.key}`),
      customer_id: id(`customer.${c.key}`),
      name: c.contact[0],
      position: c.contact[1],
      phone: c.cel,
      email: `${slugMail(c.contact[0])}@${slugMail(c.name)}.example`,
    });
  }
});

// Fornecedores
const SUPPLIERS = [
  { key: 'polar', name: 'Polar Distribuidora de Peças Ltda', base: '91345601', contact: 'Vanessa Moura', addr: 'Avenida Feliciano Sodré, 400, Centro, São Gonçalo/RJ', phone: '(21) 3000-3101' },
  { key: 'gelonorte', name: 'Gelo Norte Componentes Ltda', base: '91345602', contact: 'Anderson Ribeiro', addr: 'Rua Visconde de Itaboraí, 55, Centro, Niterói/RJ', phone: '(21) 3000-3102' },
  { key: 'cobresul', name: 'Cobre Sul Suprimentos Ltda', base: '91345603', contact: 'Tatiane Gomes', addr: 'Avenida Brasil, 12000, Penha, Rio de Janeiro/RJ', phone: '(21) 3000-3103' },
  { key: 'aurora', name: 'Distribuidora Aurora de Peças Ltda', base: '91345604', contact: 'Márcio Teles', addr: 'Rua Teodoro da Silva, 700, Vila Isabel, Rio de Janeiro/RJ', phone: '(21) 3000-3104' },
];
for (const s of SUPPLIERS) {
  add(F2, 'suppliers', {
    id: id(`supplier.${s.key}`),
    company_id: CO,
    name: s.name,
    cpf_cnpj: cnpj(s.base),
    contact_name: s.contact,
    email: `vendas@${slugMail(s.name.split(' ').slice(0, 2).join(''))}.example`,
    phone: s.phone,
    address: s.addr,
    created_at: '@now-250d',
  });
}

// Categorias e equipamentos (marcas ficticias de aparelho: Aerovento, Brisatec, Nevasca)
const CATS = [
  { key: 'hiwall', name: 'Split Hi-Wall', color: '#0ea5e9' },
  { key: 'cassete', name: 'Split Cassete', color: '#8b5cf6' },
  { key: 'pisoteto', name: 'Split Piso-Teto', color: '#f97316' },
];
for (const c of CATS) add(F2, 'equipment_categories', { id: id(`eqcat.${c.key}`), company_id: CO, name: c.name, color: c.color, description: null });

// [cliente, categoria, marca, modelo, BTU, local, instalacao, garantia ate, ativo]
const EQUIPMENT = [
  ['padaria', 'hiwall', 'Aerovento', 'AV-HW12', '12.000', 'Salão de atendimento', '2023-03-14', '2026-03-14'],
  ['padaria', 'hiwall', 'Aerovento', 'AV-HW18', '18.000', 'Salão de atendimento (fundos)', '2023-03-14', '2026-03-14'],
  ['padaria', 'hiwall', 'Brisatec', 'BT-HW09', '9.000', 'Escritório', '2024-08-02', '2027-08-02'],
  ['hotel', 'cassete', 'Nevasca', 'NV-CS36', '36.000', 'Lobby', '2022-11-20', '2025-11-20'],
  ['hotel', 'cassete', 'Nevasca', 'NV-CS36', '36.000', 'Restaurante do hotel', '2022-11-20', '2025-11-20'],
  ['hotel', 'hiwall', 'Brisatec', 'BT-HW12', '12.000', 'Recepção', '2023-06-05', '2026-06-05'],
  ['hotel', 'pisoteto', 'Aerovento', 'AV-PT48', '48.000', 'Salão de eventos', '2021-09-10', '2024-09-10'],
  ['mercado', 'pisoteto', 'Nevasca', 'NV-PT36', '36.000', 'Padaria do mercado', '2023-01-18', '2026-01-18'],
  ['mercado', 'hiwall', 'Aerovento', 'AV-HW24', '24.000', 'Escritório administrativo', '2024-02-27', '2027-02-27'],
  ['academia', 'cassete', 'Brisatec', 'BT-CS36', '36.000', 'Sala de musculação', '2023-09-12', '2026-09-12'],
  ['academia', 'hiwall', 'Brisatec', 'BT-HW18', '18.000', 'Recepção', '2023-09-12', '2026-09-12'],
  ['restaurante', 'hiwall', 'Nevasca', 'NV-HW24', '24.000', 'Salão principal', '2022-05-30', '2025-05-30'],
  ['restaurante', 'hiwall', 'Nevasca', 'NV-HW18', '18.000', 'Salão varanda', '2022-05-30', '2025-05-30'],
  ['clinica', 'hiwall', 'Aerovento', 'AV-HW12', '12.000', 'Consultório 1', '2024-04-09', '2027-04-09'],
  ['clinica', 'hiwall', 'Aerovento', 'AV-HW12', '12.000', 'Consultório 2', '2024-04-09', '2027-04-09'],
  ['escritorio', 'hiwall', 'Brisatec', 'BT-HW18', '18.000', 'Sala de reuniões', '2023-10-23', '2026-10-23'],
  ['escritorio', 'hiwall', 'Brisatec', 'BT-HW09', '9.000', 'Sala do sócio', '2023-10-23', '2026-10-23'],
  ['farmacia', 'hiwall', 'Nevasca', 'NV-HW18', '18.000', 'Balcão', '2024-06-15', '2027-06-15'],
  ['pousada', 'hiwall', 'Brisatec', 'BT-HW09', '9.000', 'Suíte 1', '2022-12-03', '2025-12-03'],
  ['pousada', 'hiwall', 'Brisatec', 'BT-HW09', '9.000', 'Suíte 2', '2022-12-03', '2025-12-03'],
  ['pousada', 'hiwall', 'Aerovento', 'AV-HW12', '12.000', 'Recepção', '2023-02-11', '2026-02-11'],
  ['condominio', 'pisoteto', 'Nevasca', 'NV-PT36', '36.000', 'Salão de festas', '2021-12-14', '2024-12-14'],
  ['mariana', 'hiwall', 'Aerovento', 'AV-HW12', '12.000', 'Quarto', '2024-11-08', '2027-11-08'],
  ['mariana', 'hiwall', 'Aerovento', 'AV-HW09', '9.000', 'Escritório', '2025-01-20', '2028-01-20'],
  ['roberto', 'hiwall', 'Brisatec', 'BT-HW18', '18.000', 'Sala', '2023-07-29', '2026-07-29'],
];
const cust = Object.fromEntries(CUSTOMERS.map((c) => [c.key, c]));
const eqSeen = {};
EQUIPMENT.forEach(([ck, cat, brand, model, btu, loc, inst, war], i) => {
  const catName = CATS.find((c) => c.key === cat).name;
  const n = (eqSeen[ck] = (eqSeen[ck] || 0) + 1);
  add(F2, 'equipment', {
    id: id(`equipment.${ck}.${n}`),
    company_id: CO,
    customer_id: id(`customer.${ck}`),
    category_id: id(`eqcat.${cat}`),
    name: `${catName.replace('Split ', '')} ${btu} BTUs - ${loc}`,
    brand,
    model,
    capacity: `${btu} BTU/h`,
    identifier: String(i + 1).padStart(4, '0'), // padrao do gatilho next_equipment_identifier: 0001, 0002...
    serial_number: `${brand.slice(0, 2).toUpperCase()}${2200000 + i * 137}`,
    location: loc,
    install_date: inst,
    warranty_until: war,
    status: 'active',
    public_short_code: shortCode(`equipment.${i + 1}.${model}`),
    created_at: `@now-${280 - i * 6}d`,
    updated_at: `@now-${15}d`,
  });
});

// Campos padrao do equipamento (gatilho trg_seed_equipment_field_config_on_company_insert: 6 linhas, todas visiveis)
[
  ['brand', 'Marca', 'text'],
  ['model', 'Modelo', 'text'],
  ['serial_number', 'Nº de Série', 'text'],
  ['capacity', 'Capacidade/Especificação', 'text'],
  ['location', 'Local', 'text'],
  ['install_date', 'Data de Instalação', 'date'],
].forEach(([key, label, type], i) => {
  add(F2, 'equipment_field_config', {
    id: id(`eqfield.${key}`),
    company_id: CO,
    field_key: key,
    label,
    field_type: type,
    options: null,
    is_visible: true,
    is_required: false,
    position: i + 1,
    created_at: '@now-300d',
    updated_at: '@now-300d',
  });
});
// Contador do identificador (next_equipment_identifier): os 25 equipamentos usaram 0001..0025; o proximo e 0026
add(F2, 'equipment_number_counters', { company_id: CO, next_value: EQUIPMENT.length + 1 });

// ============================================================================================
// escrita
// ============================================================================================
if (process.argv[1] && process.argv[1].endsWith('gen-seeds.mjs')) {
  fs.mkdirSync(SEEDS, { recursive: true });
  for (const f of fs.readdirSync(SEEDS)) if (f.startsWith('gen-') && f.endsWith('.json')) fs.rmSync(path.join(SEEDS, f));
  for (const [file, tables] of Object.entries(out)) {
    fs.writeFileSync(path.join(SEEDS, `${file}.json`), JSON.stringify(tables, null, 1) + '\n');
  }
  const counts = {};
  for (const tables of Object.values(out)) for (const [t, rows] of Object.entries(tables)) counts[t] = (counts[t] || 0) + rows.length;
  console.log('seeds gerados:', JSON.stringify(counts));
}
