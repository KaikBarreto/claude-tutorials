// Geografia falsa de Niteroi/RJ para os handlers externos (CEP, geocodificacao, rotas, mapa).
// Os enderecos sao ficticios; so os nomes de rua/bairro sao reais para o mapa "parecer" a cidade.
import crypto from 'node:crypto';
import { store } from '../core/store.mjs';

export const CITY = { name: 'Niterói', uf: 'RJ', state: 'Rio de Janeiro', ibge: '3303302', ddd: '21', lat: -22.8833, lon: -43.1036 };

// bairro -> ponto central aproximado
export const HOODS = {
  'Icaraí': [-22.9045, -43.1095],
  'Centro': [-22.8940, -43.1235],
  'Ingá': [-22.8995, -43.1250],
  'São Francisco': [-22.9300, -43.0965],
  'Charitas': [-22.9365, -43.0950],
  'Santa Rosa': [-22.8980, -43.0990],
  'Pendotiba': [-22.9005, -43.0455],
  'Itaipu': [-22.9615, -43.0356],
  'Piratininga': [-22.9230, -43.0350],
  'Boa Viagem': [-22.9085, -43.1280],
  'Fonseca': [-22.8790, -43.0980],
  'Barreto': [-22.8760, -43.1190],
};

// ruas "de verdade" da cidade (numeracao e CEP sao inventados e servem de base para o autocompletar)
const BASE_STREETS = [
  ['Rua Moreira César', 'Icaraí', '24230-190'],
  ['Rua Gavião Peixoto', 'Icaraí', '24230-092'],
  ['Rua Lopes Trovão', 'Icaraí', '24220-071'],
  ['Rua Miguel de Frias', 'Icaraí', '24220-001'],
  ['Rua Cinco de Julho', 'Icaraí', '24220-111'],
  ['Avenida Roberto Silveira', 'Icaraí', '24230-163'],
  ['Rua Mariz e Barros', 'Ingá', '24210-125'],
  ['Rua Presidente Domiciano', 'Boa Viagem', '24210-270'],
  ['Rua da Conceição', 'Centro', '24020-081'],
  ['Rua Doutor Celestino', 'Centro', '24020-091'],
  ['Rua Visconde de Itaboraí', 'Centro', '24030-090'],
  ['Avenida Amaral Peixoto', 'Centro', '24020-072'],
  ['Avenida Quintino Bocaiúva', 'São Francisco', '24360-000'],
  ['Rua Tiradentes', 'Ingá', '24210-510'],
  ['Estrada Caetano Monteiro', 'Pendotiba', '24320-570'],
  ['Estrada Francisco da Cruz Nunes', 'Itaipu', '24342-002'],
  ['Avenida Almirante Ary Parreiras', 'Icaraí', '24230-322'],
  ['Rua Coronel Moreira César', 'Icaraí', '24230-052'],
  ['Rua Gastão Gonçalves', 'Santa Rosa', '24240-030'],
  ['Rua Noronha Torrezão', 'Santa Rosa', '24240-181'],
  ['Alameda São Boaventura', 'Fonseca', '24120-191'],
  ['Rua Marechal Deodoro', 'Centro', '24030-060'],
  // T3 (clientes): CEP do Marcos (Icaraí) e do cadastro pelo formulário público (Luana)
  ['Rua Otávio Carneiro', 'Icaraí', '24230-340'],
  ['Rua Tavares de Macedo', 'Icaraí', '24220-250'],
];

const asciiLower = (s) =>
  String(s ?? '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase();

export const norm = (s) => asciiLower(s).replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();

export function hash01(seed, salt = '') {
  const h = crypto.createHash('sha1').update(String(seed) + salt).digest();
  return h.readUInt32BE(0) / 0xffffffff;
}

/** Ponto deterministico perto do bairro (varia ~300 m). */
export function pointNear(hood, seed) {
  const [lat, lon] = HOODS[hood] || [CITY.lat, CITY.lon];
  return [lat + (hash01(seed, 'a') - 0.5) * 0.006, lon + (hash01(seed, 'b') - 0.5) * 0.006];
}

/** Lista de logradouros conhecidos: base + enderecos dos cadastros carregados no fakebase. */
export function gazetteer() {
  const out = new Map();
  const put = (road, hood, cep, lat, lon, city = CITY.name) => {
    if (!road) return;
    const key = norm(`${road} ${hood}`);
    if (out.has(key)) return;
    const [la, lo] = lat != null && lon != null ? [Number(lat), Number(lon)] : pointNear(hood, road);
    out.set(key, { road, hood: hood || 'Centro', cep: cep || '', lat: la, lon: lo, city });
  };
  for (const [road, hood, cep] of BASE_STREETS) put(road, hood, cep);
  for (const tbl of ['customers', 'company_settings', 'companies']) {
    for (const r of store.rows(tbl)) {
      if (r.address && r.neighborhood) put(r.address, r.neighborhood, r.zip_code, r.latitude ?? r.lat, r.longitude ?? r.lng, r.city || CITY.name);
    }
  }
  return [...out.values()];
}

export const onlyDigits = (s) => String(s ?? '').replace(/\D/g, '');
export const fmtCep = (d) => (d.length === 8 ? `${d.slice(0, 5)}-${d.slice(5)}` : d);

export function findByCep(digits) {
  return gazetteer().find((g) => onlyDigits(g.cep) === digits) || null;
}

const STOP = new Set(['rua', 'r', 'av', 'avenida', 'estrada', 'alameda', 'de', 'da', 'do', 'das', 'dos', 'e', 'niteroi', 'rj', 'brasil', 'brazil', 'rio', 'janeiro']);

/** Busca por texto livre: devolve ate `limit` logradouros, mais parecidos primeiro. */
export function searchStreets(query, limit = 5) {
  const q = norm(query);
  const tokens = q.split(' ').filter((t) => t.length >= 3 && !STOP.has(t) && !/^\d+$/.test(t));
  if (!tokens.length) return [];
  const scored = [];
  for (const g of gazetteer()) {
    const hay = norm(`${g.road} ${g.hood}`);
    let hit = 0;
    for (const t of tokens) if (hay.includes(t)) hit++;
    // prefixos digitados ("moreira ce") tambem contam
    const last = tokens[tokens.length - 1];
    if (hit < tokens.length && last && hay.split(' ').some((w) => w.startsWith(last))) hit += 0.5;
    if (hit > 0) scored.push({ g, score: hit / tokens.length });
  }
  scored.sort((a, b) => b.score - a.score || a.g.road.localeCompare(b.g.road, 'pt-BR'));
  return scored.filter((s) => s.score >= Math.min(1, scored[0]?.score ?? 1)).slice(0, limit).map((s) => s.g);
}

/** Numero de casa citado na busca ("rua x, 200"), se houver. */
export function houseNumber(query) {
  const m = String(query).match(/(?:,|\s)\s*(\d{1,5})(?!\d|-\d)/);
  return m ? m[1] : '';
}

/** Distancia em km (haversine). */
export function km(a, b) {
  const R = 6371;
  const rad = (x) => (x * Math.PI) / 180;
  const dLat = rad(b[0] - a[0]);
  const dLon = rad(b[1] - a[1]);
  const s = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a[0])) * Math.cos(rad(b[0])) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}
