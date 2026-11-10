// IBGE falso do mundo da Recicla Vale Metais (sobrescreve o do núcleo para este host): municípios de SP para o seletor de cidade
// do endereço (components/StateCitySelector.tsx busca a lista por `fetch` direto do navegador). A lista NÃO é a do IBGE inteira
// (o ambiente de gravação não acessa servicodados.ibge.gov.br): só o Vale do Paraíba e cidades grandes, com os códigos do IBGE.
// Tem de trazer Taubaté (3554102, T1) e Pindamonhangaba (3538006, filial do T22). Outra UF: a lista do núcleo.
import nucleo from '../../../fakebase/handlers/ext/servicodados.ibge.gov.br.mjs';

const SP = [
  ['Aparecida', 3502507], ['Bauru', 3506003], ['Caçapava', 3508504], ['Campinas', 3509502], ['Campos do Jordão', 3509700],
  ['Caraguatatuba', 3510500], ['Guaratinguetá', 3518404], ['Guarulhos', 3518800], ['Jacareí', 3524402], ['Jundiaí', 3525904],
  ['Lorena', 3527207], ['Mogi das Cruzes', 3530607], ['Osasco', 3534401], ['Pindamonhangaba', 3538006], ['Piracicaba', 3538709],
  ['Ribeirão Preto', 3543402], ['Santo André', 3547809], ['Santos', 3548500], ['São Bernardo do Campo', 3548708],
  ['São José do Rio Preto', 3549805], ['São José dos Campos', 3549904], ['São Paulo', 3550308], ['Sorocaba', 3552205],
  ['Taubaté', 3554102], ['Tremembé', 3554805], ['Ubatuba', 3555406],
];

export default async function ibge(ctx) {
  const m = ctx.path.match(/^\/api\/v1\/localidades\/estados\/([A-Za-z0-9]+)\/municipios\/?$/);
  if (m && (m[1].toUpperCase() === 'SP' || m[1] === '35')) return SP.map(([nome, id]) => ({ id, nome }));
  if (/^\/api\/v1\/localidades\/estados\/?$/.test(ctx.path)) {
    return [{ id: 35, sigla: 'SP', nome: 'São Paulo' }, { id: 33, sigla: 'RJ', nome: 'Rio de Janeiro' }, { id: 31, sigla: 'MG', nome: 'Minas Gerais' }];
  }
  return nucleo(ctx);
}
