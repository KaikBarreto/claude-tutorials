// Edge cnpj-lookup (lupa "Buscar dados da empresa pelo CNPJ" do cadastro de parceiro; utils/cnpjLookup.ts). Simulada: nada sai
// para a Receita. Só os CNPJs do mundo fictício que uma aula busca na tela; outro CNPJ responde como a função real quando a base
// não acha ("CNPJ não encontrado"), e o app pede para preencher à mão. T4 (cap03): Serralheria Bem-Te-Vi, com o número em branco
// (o campo fica vermelho) e optante pelo Simples. A espera de ~1 s deixa a lupa girar como na consulta de verdade.
const EMPRESAS = {
  46280719000124: {
    razao_social: 'BEM-TE-VI SERRALHERIA E ESTRUTURAS LTDA', nome_fantasia: 'SERRALHERIA BEM-TE-VI',
    logradouro: 'RUA DAS PALMEIRAS', numero: '', complemento: '', bairro: 'JARDIM SANTA LUZIA', cidade: 'TAUBATE', uf: 'SP',
    cep: '12062150', phone: '12900002742', email: 'contato@serralheriabemtevi.example', opcao_pelo_simples: true, opcao_pelo_mei: false,
  },
};

export default async (body) => {
  const cnpj = String(body?.cnpj || '').replace(/\D/g, '');
  await new Promise((r) => setTimeout(r, 1000));
  const d = EMPRESAS[cnpj];
  if (!d) return { success: false, error: 'CNPJ não encontrado. Preencha os dados manualmente.' };
  return { success: true, data: { ...d } };
};
