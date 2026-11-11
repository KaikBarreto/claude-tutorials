// Edge ibge-cities (utils/resolveIbgeCode.ts, fetchCitiesForState: a lista de cidades do CitySelector do endereço do parceiro,
// com o código IBGE de 7 dígitos). Responde { cities: [{ name, ibgeCode }] } como a função real (tabela brazilian_cities).
// Não é a lista inteira do IBGE (o ambiente de gravação não acessa a base): a mesma de handlers/ext/servicodados.ibge.gov.br.mjs
// (Vale do Paraíba e cidades grandes de SP, com Taubaté 3554102 da busca do CNPJ do T4); outra UF volta vazia.
const POR_UF = {
  SP: [
    ['Aparecida', 3502507], ['Bauru', 3506003], ['Caçapava', 3508504], ['Campinas', 3509502], ['Campos do Jordão', 3509700],
    ['Caraguatatuba', 3510500], ['Guaratinguetá', 3518404], ['Guarulhos', 3518800], ['Jacareí', 3524402], ['Jundiaí', 3525904],
    ['Lorena', 3527207], ['Mogi das Cruzes', 3530607], ['Osasco', 3534401], ['Pindamonhangaba', 3538006], ['Piracicaba', 3538709],
    ['Ribeirão Preto', 3543402], ['Santo André', 3547809], ['Santos', 3548500], ['São Bernardo do Campo', 3548708],
    ['São José do Rio Preto', 3549805], ['São José dos Campos', 3549904], ['São Paulo', 3550308], ['Sorocaba', 3552205],
    ['Taubaté', 3554102], ['Tremembé', 3554805], ['Ubatuba', 3555406],
  ],
};

export default (body) => {
  const uf = String(body?.uf || '').trim().toUpperCase();
  return { cities: (POR_UF[uf] || []).map(([name, id]) => ({ name, ibgeCode: String(id) })) };
};
