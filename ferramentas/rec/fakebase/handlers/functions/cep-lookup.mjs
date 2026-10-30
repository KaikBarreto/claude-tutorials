// Edge function `cep-lookup` falsa. Mesmo contrato da real (app/supabase/functions/cep-lookup):
//   { cep } -> { logradouro, bairro, cidade, estado, ibge }     (400 "CEP inválido", 404 "CEP não encontrado")
// Os dados vem do ViaCEP falso (handlers/ext/viacep.com.br.mjs), que conhece as ruas de Niteroi do mundo falso.
import viacep from '../ext/viacep.com.br.mjs';
import { FunctionError } from '../../http/functions.mjs';

export default async function cepLookup(body) {
  const cep = typeof body?.cep === 'string' ? body.cep.replace(/\D/g, '').slice(0, 8) : '';
  if (cep.length !== 8) throw new FunctionError('CEP inválido', 400);
  const v = await viacep({ path: `/ws/${cep}/json/` });
  if (!v || v.erro) throw new FunctionError('CEP não encontrado', 404);
  return {
    logradouro: String(v.logradouro || '').slice(0, 200),
    bairro: String(v.bairro || '').slice(0, 100),
    cidade: String(v.localidade || '').slice(0, 100),
    estado: String(v.uf || '').slice(0, 2),
    ibge: String(v.ibge || '').replace(/\D/g, '').slice(0, 7),
  };
}
