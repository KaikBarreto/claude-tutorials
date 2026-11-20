// Edge cnpj-lookup (lupa "Buscar dados da empresa pelo CNPJ" do cadastro de parceiro; utils/cnpjLookup.ts). Simulada: nada sai
// para a Receita. Só os CNPJs do mundo fictício que uma aula busca na tela; outro CNPJ responde como a função real quando a base
// não acha ("CNPJ não encontrado"), e o app pede para preencher à mão. T4 (cap03): Serralheria Bem-Te-Vi, com o número em branco
// (o campo fica vermelho) e optante pelo Simples. A espera de ~1 s deixa a lupa girar como na consulta de verdade.
const EMPRESAS = {
  46280719000124: {
    razao_social: 'BEM-TE-VI SERRALHERIA E ESTRUTURAS LTDA', nome_fantasia: 'SERRALHERIA BEM-TE-VI',
    logradouro: 'RUA DAS PALMEIRAS', numero: '', complemento: '', bairro: 'JARDIM SANTA LUZIA', cidade: 'TAUBATE', uf: 'SP',
    cep: '12062150', phone: '12900002742', email: 'contato@serralheriabemtevi.example', opcao_pelo_simples: true, opcao_pelo_mei: false,
    regime_ecf: null, regime_ecf_ano: null,
  },
  // T4 cap. 5 (1.60.18, "Empresa do Lucro Real"): Aços Quiririm, que o cadastro já tem; a lupa confere o cadastro antigo. Endereço igual ao da
  // ficha (a caixa "Falta isto para emitir NF-e" não abre), não é Simples nem MEI e a escrituração de 2024 diz Lucro Real.
  98463027000115: {
    razao_social: 'AÇOS QUIRIRIM INDUSTRIA E COMERCIO LTDA', nome_fantasia: '',
    logradouro: 'RODOVIA VEREADOR ABEL FABRICIO DIAS', numero: '3400', complemento: '', bairro: 'QUIRIRIM', cidade: 'TAUBATE', uf: 'SP',
    cep: '12043300', phone: '', email: '', opcao_pelo_simples: false, opcao_pelo_mei: false, regime_ecf: 'lucro_real', regime_ecf_ano: 2024,
  },
  // T4 cap. 6 ("Os avisos da consulta"): Oficina do Tonho, CNPJ fictício de dígitos válidos. A Receita responde como se fosse Simples; quem
  // acusa "Baixada" é o publica.cnpj.ws simulado (ext/publica.cnpj.ws.mjs). Nada é gravado: a aula cancela a janela.
  52917384000105: {
    razao_social: 'ANTONIO CARLOS MEIRELES OFICINA MECANICA', nome_fantasia: '',
    logradouro: 'RUA DOS IPES', numero: '90', complemento: '', bairro: 'VILA SAO GERALDO', cidade: 'TAUBATE', uf: 'SP',
    cep: '12062150', phone: '', email: '', opcao_pelo_simples: null, opcao_pelo_mei: null, regime_ecf: null, regime_ecf_ano: null,
  },
};

export default async (body) => {
  const cnpj = String(body?.cnpj || '').replace(/\D/g, '');
  await new Promise((r) => setTimeout(r, 1000));
  const d = EMPRESAS[cnpj];
  if (!d) return { success: false, error: 'CNPJ não encontrado. Preencha os dados manualmente.' };
  return { success: true, data: { ...d } };
};
