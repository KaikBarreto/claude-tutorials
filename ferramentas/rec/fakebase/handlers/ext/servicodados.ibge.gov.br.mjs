// IBGE falso: municipios por UF (seletor de cidade) e malhas (mapa admin, nao usado nos tutoriais)
const RJ = [
  ['Angra dos Reis', 3300100], ['Araruama', 3300209], ['Armação dos Búzios', 3300233], ['Belford Roxo', 3300456],
  ['Cabo Frio', 3300704], ['Campos dos Goytacazes', 3301009], ['Duque de Caxias', 3301702], ['Itaboraí', 3301900],
  ['Macaé', 3302403], ['Magé', 3302502], ['Maricá', 3302700], ['Mesquita', 3302858], ['Nilópolis', 3303203],
  ['Niterói', 3303302], ['Nova Friburgo', 3303401], ['Nova Iguaçu', 3303500], ['Paraty', 3303807], ['Petrópolis', 3303906],
  ['Resende', 3304201], ['Rio das Ostras', 3304524], ['Rio de Janeiro', 3304557], ['Saquarema', 3305505],
  ['São Gonçalo', 3304904], ['São João de Meriti', 3305109], ['Teresópolis', 3305802], ['Volta Redonda', 3306305],
];

export default async function ibge({ path }) {
  const m = path.match(/^\/api\/v1\/localidades\/estados\/([A-Za-z0-9]+)\/municipios\/?$/);
  if (m) {
    const uf = m[1].toUpperCase();
    if (uf === 'RJ' || uf === '33') return RJ.map(([nome, id]) => ({ id, nome }));
    return [];
  }
  if (/^\/api\/v1\/localidades\/estados\/?$/.test(path)) return [{ id: 33, sigla: 'RJ', nome: 'Rio de Janeiro' }];
  return [];
}
