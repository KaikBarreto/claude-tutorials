// publica.cnpj.ws falso (T4, 1.59.157+): a lupa do CNPJ consulta também a inscrição estadual, e essa chamada sai DIRETO do navegador para
// `GET https://publica.cnpj.ws/cnpj/<14 dígitos>` (utils/consultaIe.ts), fora do Supabase. Formato lido em consultaIe.ts: um objeto com
// `estabelecimento.situacao_cadastral` e `estabelecimento.inscricoes_estaduais[]` (`inscricao_estadual`, `ativo`, `atualizado_em`,
// `estado.sigla`). Só os CNPJs do mundo fictício que a aula T4 busca; qualquer outro responde 404 (o app fica mudo: "falha de consulta" não
// é "sem inscrição"). Nada sai para a internet.
//   46.280.719/0001-24  Serralheria Bem-Te-Vi   Ativa, IE 688412573032 em SP (cap. 3 e 4: "Usar a da Sintegra")
//   98.463.027/0001-15  Aços Quiririm           Ativa, IE 688042711117 em SP (cap. 5: a ficha tem uma com um dígito trocado)
//   52.917.384/0001-05  Oficina do Tonho        Baixada, sem inscrição (cap. 6: alerta vermelho e "sem inscrição estadual ativa")
const BASE = {
  46280719000124: { situacao_cadastral: 'Ativa', inscricoes_estaduais: [{ inscricao_estadual: '688412573032', ativo: true, atualizado_em: '2026-10-02T00:00:00Z', estado: { sigla: 'SP' } }] },
  98463027000115: { situacao_cadastral: 'Ativa', inscricoes_estaduais: [{ inscricao_estadual: '688042711117', ativo: true, atualizado_em: '2026-09-14T00:00:00Z', estado: { sigla: 'SP' } }] },
  52917384000105: { situacao_cadastral: 'Baixada', inscricoes_estaduais: [] },
};

export default async function publica({ path }) {
  const m = String(path || '').match(/^\/cnpj\/(\d{14})\/?$/);
  const est = m && BASE[m[1]];
  await new Promise((r) => setTimeout(r, 400));
  if (!est) return { __status: 404, body: { titulo: 'Não encontrado', detalhes: 'CNPJ sem handler no mundo da T4' } };
  return { cnpj_raiz: m[1].slice(0, 8), estabelecimento: { cnpj: m[1], ...est } };
}
