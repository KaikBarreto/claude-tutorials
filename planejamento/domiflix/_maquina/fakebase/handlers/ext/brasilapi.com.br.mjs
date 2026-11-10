// BrasilAPI falsa: /api/cnpj/v1/<cnpj>, /api/cep/v1|v2/<cep>, /api/banks/v1
import { CITY, findByCep, fmtCep, norm, onlyDigits, pointNear } from '../../lib/geo.mjs';

const digitsOf = (s) => onlyDigits(s);

function fromRow(r, kind) {
  const doc = digitsOf(r.document || r.cnpj);
  const [logr, num] = [r.address || '', r.address_number || ''];
  const isStreet = /^(rua|avenida|av\.?|estrada|alameda|travessa|praça|praca)\s/i.test(logr);
  const tipo = isStreet ? logr.split(' ')[0].toUpperCase() : '';
  return {
    cnpj: doc,
    razao_social: kind === 'supplier' ? r.name : `${r.name} Ltda`,
    nome_fantasia: r.name,
    descricao_situacao_cadastral: 'ATIVA',
    email: r.email || '',
    ddd_telefone_1: digitsOf(r.phone || '').slice(0, 10),
    cep: digitsOf(r.zip_code || ''),
    descricao_tipo_de_logradouro: tipo === 'AV' || tipo === 'AV.' ? 'AVENIDA' : tipo,
    logradouro: isStreet ? logr.replace(/^\S+\s/, '') : logr,
    numero: num,
    complemento: '',
    bairro: r.neighborhood || 'Centro',
    municipio: r.city || CITY.name,
    uf: r.state || CITY.uf,
    codigo_municipio_ibge: Number(r.ibge_municipality_code || CITY.ibge),
    cnae_fiscal: 4322302,
    cnae_fiscal_descricao: 'Instalação e manutenção de sistemas centrais de ar condicionado, de ventilação e refrigeração',
  };
}

// Linha da base "Receita" (seeds/receita.json, tabela receita_cnpj) -> resposta da BrasilAPI
function fromReceita(r) {
  return {
    cnpj: digitsOf(r.cnpj),
    razao_social: r.razao_social,
    nome_fantasia: r.nome_fantasia || '',
    descricao_situacao_cadastral: r.situacao || 'ATIVA',
    email: r.email || '',
    ddd_telefone_1: digitsOf(r.ddd_telefone_1 || ''),
    cep: digitsOf(r.cep || ''),
    descricao_tipo_de_logradouro: r.tipo_logradouro || '',
    logradouro: r.logradouro || '',
    numero: r.numero || '',
    complemento: r.complemento || '',
    bairro: r.bairro || '',
    municipio: r.municipio || CITY.name,
    uf: r.uf || CITY.uf,
    codigo_municipio_ibge: Number(r.codigo_municipio_ibge || CITY.ibge),
    cnae_fiscal: r.cnae_fiscal || 4322302,
    cnae_fiscal_descricao: r.cnae_fiscal_descricao || '',
  };
}

export default async function brasilapi({ path, store }) {
  let m = path.match(/^\/api\/cnpj\/v1\/(\d{14})\/?$/);
  if (m) {
    const doc = m[1];
    // 1) base da Receita (empresas que ainda nao sao cliente), 2) o que ja esta cadastrado no mundo falso
    const rec = store.rows('receita_cnpj').find((r) => digitsOf(r.cnpj) === doc);
    if (rec) return fromReceita(rec);
    const pool = [
      ...store.rows('customers').map((r) => [r, 'customer']),
      ...store.rows('suppliers').map((r) => [r, 'supplier']),
      ...store.rows('company_settings').map((r) => [r, 'company']),
    ];
    const hit = pool.find(([r]) => digitsOf(r.document || r.cnpj) === doc);
    if (hit) return fromRow(hit[0], hit[1]);
    return { __status: 404, body: { name: 'CnpjNaoEncontrado', message: 'CNPJ não encontrado', type: 'not_found' } };
  }

  m = path.match(/^\/api\/cep\/v([12])\/(\d{8})\/?$/);
  if (m) {
    const g = findByCep(m[2]);
    if (!g && !m[2].startsWith('24')) return { __status: 404, body: { name: 'CepPromiseError', message: 'Todos os serviços de CEP retornaram erro.', type: 'service_error' } };
    const road = g?.road || 'Rua Exemplo';
    const hood = g?.hood || 'Centro';
    const [lat, lon] = g ? [g.lat, g.lon] : pointNear(hood, m[2]);
    return {
      cep: m[2], state: CITY.uf, city: CITY.name, neighborhood: hood, street: road, service: 'open-cep',
      location: { type: 'Point', coordinates: { longitude: String(lon), latitude: String(lat) } },
    };
  }

  if (/^\/api\/banks\/v1\/?$/.test(path)) {
    // lista curta e generica (sem marcas): suficiente para o seletor de banco nas telas financeiras
    return [
      { ispb: '00000000', name: 'BCO DO BRASIL S.A.', code: 1, fullName: 'Banco do Brasil S.A.' },
      { ispb: '60746948', name: 'BCO BRADESCO S.A.', code: 237, fullName: 'Banco Bradesco S.A.' },
      { ispb: '60701190', name: 'ITAÚ UNIBANCO S.A.', code: 341, fullName: 'Itaú Unibanco S.A.' },
      { ispb: '00360305', name: 'CAIXA ECONOMICA FEDERAL', code: 104, fullName: 'Caixa Econômica Federal' },
      { ispb: '90400888', name: 'BCO SANTANDER (BRASIL) S.A.', code: 33, fullName: 'Banco Santander (Brasil) S.A.' },
      { ispb: '18236120', name: 'NU PAGAMENTOS - IP', code: 260, fullName: 'Nu Pagamentos S.A. - Instituição de Pagamento' },
      { ispb: '01181521', name: 'BCO COOPERATIVO SICREDI S.A.', code: 748, fullName: 'Banco Cooperativo Sicredi S.A.' },
      { ispb: '00000001', name: 'COOPERATIVA DE CRÉDITO EXEMPLO', code: 756, fullName: 'Cooperativa de Crédito Exemplo' },
    ];
  }
  return { __status: 404, body: { message: 'rota BrasilAPI sem handler no fakebase: ' + path } };
}
void norm; void fmtCep;
