// Edge cep-lookup (busca de CEP dos endereços: empresa, parceiros). CEPs do mundo fictício da Recicla Vale Metais; outro CEP
// responde "CEP não encontrado", como a função real quando a base não acha. Para outra aula, acrescente a linha do CEP aqui.
const CEPS = {
  // T1: sede da Recicla Vale Metais (MUNDO_LINHA_DO_TEMPO.md, seção 3: Parque Industrial)
  12086410: { logradouro: 'Rua das Oficinas', bairro: 'Parque Industrial', cidade: 'Taubaté', uf: 'SP', codigoIbge: '3554102' },
};

export default (body) => {
  const cep = String(body?.cep || '').replace(/\D/g, '');
  const d = CEPS[cep];
  if (!d) return { success: false, error: 'CEP não encontrado' };
  return { success: true, data: { cep: `${cep.slice(0, 5)}-${cep.slice(5)}`, complemento: '', ...d } };
};
