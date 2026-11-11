#!/usr/bin/env node
// T0 · gera as sementes do catálogo da EcoFlix e dos estados S1/S2/S3/S13 em rec/mundo/seeds-extra/t00/.
// Uso: node rec/t00/t00_catalogo.mjs   (determinístico; os ids usam @id:<chave>, como as sementes do mundo)
// Tudo fictício: as 26 aulas da TRILHA.md (planejamento/ecoflix), títulos como nas aulas; vídeo = o arquivo local do ext handler
// handlers/ext/drive.usercontent.google.com.mjs (mudo, sem YouTube).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(AQUI, '..', 'mundo', 'seeds-extra', 't00');
fs.mkdirSync(OUT, { recursive: true });

// [id da aula, título, minutos (alvo da fonte), grupo, module_code, descrição curta]
const AULAS = [
  ['t00', 'Bem-vindo ao EcoSistema', 12, 'core', null, 'Os combinados da parceria, uma volta pelo sistema e o seu plano.'],
  ['t01', 'Sua conta e sua empresa', 18, 'core', null, 'Os dados da empresa, o logo e as preferências para o sistema ficar com a sua cara.'],
  ['t02', 'Usuários e permissões', 13, 'core', null, 'Quem usa o sistema na sua empresa e o que cada pessoa pode ver e fazer.'],
  ['t03', 'Materiais e tabelas de preço', 15, 'core', null, 'O cardápio de materiais e o preço do quilo de cada um.'],
  ['t04', 'Clientes, fornecedores e a ficha do parceiro', 17, 'core', null, 'O cadastro de quem compra e de quem vende, e o saldo de cada parceiro.'],
  ['t05', 'Balança e impressora: o EcoTray', 13, 'core', null, 'O peso da balança direto no sistema e a impressão do comprovante.'],
  ['t06', 'Caixa: abrir, fechar e o cofre', 14, 'core', null, 'O dia do caixa, do primeiro troco ao fechamento, e o cofre da empresa.'],
  ['t07', 'Comprar e vender sucata', 22, 'core', null, 'O pedido de compra e de venda, passo a passo, com o comprovante.'],
  ['t08', 'Ticket de Pesagem', 11, 'core', null, 'A pesagem dos caminhões, com impureza e valorização.'],
  ['t09', 'Pedidos e histórico do caixa', 12, 'core', null, 'Encontrar, conferir e corrigir pedidos e caixas antigos.'],
  ['t10', 'Estoque: saldo, histórico e posição', 16, 'core', null, 'O saldo de cada material, o histórico de movimentações e a posição em uma data.'],
  ['t13', 'Contas a Pagar e Receber', 16, 'core', null, 'As contas da empresa, as recorrentes e o fiado parcelado.'],
  ['t14', 'Bancos, cofre e conciliação bancária', 18, 'core', null, 'As contas bancárias, o cofre e a conferência do extrato.'],
  ['t15', 'Relatório Financeiro e DRE', 17, 'core', null, 'Como está o resultado da empresa, por caixa e por competência.'],
  ['t21', 'Cato, o assistente', 8, 'core', null, 'O assistente do EcoSistema para tirar dúvidas e consultar números.'],
  ['t25', 'Dashboard, Agenda e rotina', 13, 'core', null, 'O painel do dia, a agenda de tarefas e a rotina da empresa.'],
  ['t16', 'Nota Fiscal de mercadoria (NF-e)', 25, 'plan', 'notas_fiscais', 'A emissão da NF-e de venda, do cadastro fiscal à nota autorizada.'],
  ['t17', 'Transporte, serviço e o contador', 16, 'plan', 'notas_fiscais', 'MDF-e, NFS-e e a entrega dos documentos ao contador.'],
  ['t18', 'Ambiental: MTR e CDF', 12, 'plan', 'notas_fiscais', 'O manifesto de transporte de resíduos e o certificado de destinação final.'],
  ['t19', 'Funcionários e ponto eletrônico', 16, 'plan', 'funcionarios', 'A equipe, os vales e o ponto eletrônico pelo celular.'],
  ['t27', 'White Label', 7, 'plan', 'white_label', 'O sistema com a marca e as cores da sua empresa.'],
  ['t20', 'Portal do Cliente e Fornecedor', 12, 'plan', 'portal_cliente', 'A página em que o parceiro acompanha pedidos, saldos e fotos.'],
  ['t22', 'Gerencial: matriz e filiais', 16, 'plan', 'modulo_gerencial', 'A visão consolidada da matriz e das filiais.'],
  ['t12', 'Coletas e Logística', 15, 'plan', 'coletas', 'As ordens de coleta, a frota e a agenda do caminhão.'],
  ['t11', 'Produção', 20, 'plan', 'producao', 'Fichas técnicas, ordens de produção e o custo por peça.'],
  ['t26', 'CRM/Kanban', 16, 'plan', 'crm_kanban', 'As oportunidades comerciais em funis e no quadro Kanban.'],
];

// capa 16:9 em SVG (data URI): gradiente verde-escuro com o número da aula e o título; sem logo de terceiros
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
function capa(n, titulo) {
  const linhas = [];
  let atual = '';
  for (const w of titulo.split(' ')) {
    if ((atual + ' ' + w).trim().length > 22) { linhas.push(atual); atual = w; } else atual = (atual + ' ' + w).trim();
  }
  if (atual) linhas.push(atual);
  const tx = linhas.slice(0, 3).map((l, i) => `<text x="40" y="${250 + i * 44}" font-family="Montserrat,Arial,sans-serif" font-size="38" font-weight="700" fill="#ffffff">${esc(l)}</text>`).join('');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1f5e43"/><stop offset="1" stop-color="#0d1f17"/></linearGradient></defs><rect width="640" height="360" fill="url(#g)"/><circle cx="560" cy="80" r="150" fill="#50d088" opacity="0.10"/><text x="40" y="70" font-family="Montserrat,Arial,sans-serif" font-size="22" font-weight="700" fill="#50d088" letter-spacing="3">AULA ${n}</text>${tx}</svg>`;
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
}

const titles = [], seasons = [], episodes = [], tmods = [];
AULAS.forEach(([id, titulo, min, grupo, code, desc], i) => {
  const capaUrl = capa(i, titulo);
  titles.push({
    id: `@id:ecoflix.title.${id}`, type: 'series', title: titulo, description: desc, banner_url: capaUrl, thumbnail_url: capaUrl, logo_url: null,
    tags: [], is_featured: false, is_active: true, order_index: i, live_url: null, live_scheduled_at: null, created_at: '2026-10-20T12:00:00.000Z',
    track_group: grupo, track_order: i + 1, learning_path_id: '@id:ecoflix.path.tutoriais',
  });
  seasons.push({ id: `@id:ecoflix.season.${id}`, title_id: `@id:ecoflix.title.${id}`, season_number: 1, title: 'Temporada 1', description: null, order_index: 0, created_at: '2026-10-20T12:00:00.000Z' });
  episodes.push({
    id: `@id:ecoflix.episode.${id}`, title_id: `@id:ecoflix.title.${id}`, season_id: `@id:ecoflix.season.${id}`, episode_number: 1, title: titulo, description: desc,
    video_id: `ecoflix-aula-${id}`, video_type: 'drive', duration_minutes: min, thumbnail_url: capaUrl, order_index: 0, recorded_at: '2026-10-25T12:00:00.000Z',
    created_at: '2026-10-20T12:00:00.000Z', is_active: true,
    ...(id === 't00' ? { mobile_video_id: 'ecoflix-aula-t00-vertical', mobile_video_type: 'drive' } : {}),
  });
  if (code) tmods.push({ id: `@id:ecoflix.titlemod.${id}`, title_id: `@id:ecoflix.title.${id}`, module_code: code });
});

const REMOVE_MARCOS_JULIANA = {
  profiles: [{ id: '@id:user.marcos' }, { id: '@id:user.juliana' }],
  user_roles: [{ user_id: '@id:user.marcos' }, { user_id: '@id:user.juliana' }],
  user_permissions: [{ user_id: '@id:user.marcos' }, { user_id: '@id:user.juliana' }],
  user_shortcuts: [{ user_id: '@id:user.marcos' }, { user_id: '@id:user.juliana' }],
};

const grava = (nome, obj) => fs.writeFileSync(path.join(OUT, nome + '.json'), JSON.stringify(obj, null, 1));

grava('catalogo', {
  _doc: 'T0 (Bem-vindo ao EcoSistema): o catálogo da EcoFlix (trilha tutoriais-do-sistema, 26 aulas na ordem da TRILHA.md, um episódio por aula, vídeo fictício local) e só o Rafael como usuário (o T2 cria Juliana e Marcos). Gerado por rec/t00/t00_catalogo.mjs.',
  ecoflix_learning_paths: [{ id: '@id:ecoflix.path.tutoriais', slug: 'tutoriais-do-sistema', title: 'Tutoriais do sistema', description: null, cover_url: null, is_onboarding: true, is_active: true, order_index: 0 }],
  ecoflix_titles: titles, ecoflix_seasons: seasons, ecoflix_episodes: episodes, ecoflix_title_modules: tmods,
  _patch: { companies: [{ match: { id: '@id:company.reciclavale' }, set: { name: 'Recicla Vale Metais Ltda' } }], profiles: [{ match: { id: '@id:user.rafael' }, set: { navigation_style: 'sidebar' } }] },
  _remove: REMOVE_MARCOS_JULIANA,
});

// S2: o mundo base da trilha antes do T1: assinatura ativa, Rafael já confirmou a introdução (T0 concluído)
const rafael = '@id:user.rafael';
const progT0 = { id: '@id:ecoflix.progress.t00', user_id: rafael, episode_id: '@id:ecoflix.episode.t00', title_id: '@id:ecoflix.title.t00', completed: true, progress_seconds: 720, duration_seconds: 720, watched_at: '2026-11-09T18:00:00.000Z', last_progress_at: '2026-11-09T18:00:00.000Z', company_id: '@id:company.reciclavale' };
grava('s2', {
  _doc: 'S2: conta ativa; o T0 concluído e a introdução confirmada (sem portão). Faça seedExtra [t00/catalogo, t00/s2, t00/pagamentos].',
  ecoflix_user_progress: [progT0],
  ecoflix_intro_acknowledgements: [{ id: '@id:ecoflix.ack.rafael', user_id: rafael, learning_path_id: '@id:ecoflix.path.tutoriais', episode_id: '@id:ecoflix.episode.t00', acknowledged_at: '2026-11-09T18:01:00.000Z' }],
});

// S3: S2 sem o módulo crm_kanban no plano (o selo "Não tem no seu plano" no fim da trilha)
grava('s3', {
  _doc: 'S3: S2 sem crm_kanban em company_modules (só o cap03). seedExtra [t00/catalogo, t00/s2, t00/pagamentos, t00/s3].',
  _remove: { company_modules: [{ module_code: 'crm_kanban' }] },
});

// S1: empresa em teste, sem progresso nem confirmação (o portão abre sozinho)
grava('s1', {
  _doc: 'S1: período de teste (5 dias restantes), Rafael sem confirmação da introdução, T0 sem progresso. seedExtra [t00/catalogo, t00/s1].',
  _patch: { companies: [{ match: { id: '@id:company.reciclavale' }, set: { subscription_status: 'testing', subscription_expires_at: '2026-11-15T23:59:59.000Z' } }] },
});

// S13: S1 com o vídeo do T0 já assistido (a caixa liga e o botão vira "Confirmar e começar a primeira aula")
grava('s13', {
  _doc: 'S13: S1 com o vídeo do T0 já visto (progresso concluído). seedExtra [t00/catalogo, t00/s1, t00/s13].',
  ecoflix_user_progress: [{ ...progT0, id: '@id:ecoflix.progress.t00.s13', watched_at: '2026-11-10T08:20:00.000Z', last_progress_at: '2026-11-10T08:20:00.000Z' }],
});

// Pagamentos do histórico: quatro mensalidades pagas pelo Asaas (boleto, Pix, cartão e cartão), nota emitida (PDF), 05/08 a 05/11
const pag = (n, mes, tipo, valor) => ({
  id: `@id:ecoflix.pagto.${n}`, company_id: '@id:company.reciclavale', asaas_payment_id: `pay_ficticio_${mes.replace(/-/g, '')}`, asaas_customer_id: 'cus_ficticio_recicla',
  amount: valor, billing_type: tipo, payment_method: tipo, status: 'RECEIVED', due_date: `${mes}T12:00:00.000Z`, paid_at: `${mes}T15:20:00.000Z`,
  created_at: `${mes}T09:00:00.000Z`, updated_at: `${mes}T15:20:00.000Z`, nfse_status: 'issued', nfse_number: String(310 + n), nfse_pdf_url: `https://notas.exemplo.example/nfse-${mes}.pdf`,
  nfse_xml_url: `https://notas.exemplo.example/nfse-${mes}.xml`,
});
grava('pagamentos', {
  _doc: 'Histórico de Pagamentos (S2): quatro mensalidades de R$ 1.025,00 pagas pelo Asaas (valor = subscription_value da empresa), com nota. O cartão de 05/11 acende a faixa "Débito recorrente ativo no cartão de crédito" (a empresa tem asaas_subscription_id).',
  subscription_payments: [pag(1, '2026-08-05', 'BOLETO', 1025), pag(2, '2026-09-05', 'PIX', 1025), pag(3, '2026-10-05', 'CREDIT_CARD', 1025), pag(4, '2026-11-05', 'CREDIT_CARD', 1025)],
  _patch: { companies: [{ match: { id: '@id:company.reciclavale' }, set: { asaas_subscription_id: 'sub_ficticio_recicla', asaas_customer_id: 'cus_ficticio_recicla' } }] },
});
console.log(`t00: ${AULAS.length} aulas; sementes em ${path.relative(process.cwd(), OUT)}`);
