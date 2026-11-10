// ViaCEP falso: GET /ws/<cep>/json/
import { CITY, findByCep, fmtCep, onlyDigits, HOODS } from '../../lib/geo.mjs';

export default async function viacep({ path }) {
  const m = path.match(/^\/ws\/(\d{8})\/json\/?$/);
  if (!m) return { __status: 400, body: { erro: true } };
  const cep = m[1];
  const g = findByCep(cep);
  if (g) {
    return { cep: fmtCep(cep), logradouro: g.road, complemento: '', bairro: g.hood, localidade: CITY.name, uf: CITY.uf, ibge: CITY.ibge, gia: '', ddd: CITY.ddd, siafi: '5859' };
  }
  // qualquer CEP da faixa de Niteroi (24xxx-xxx) responde com um endereco generico, para a demonstracao nao travar
  if (cep.startsWith('24')) {
    const hood = Object.keys(HOODS)[Number(cep.slice(5, 7)) % Object.keys(HOODS).length];
    return { cep: fmtCep(cep), logradouro: 'Rua Exemplo', complemento: '', bairro: hood, localidade: CITY.name, uf: CITY.uf, ibge: CITY.ibge, gia: '', ddd: CITY.ddd, siafi: '5859' };
  }
  return { erro: true };
}
void onlyDigits;
