// Códigos de tributação nacional do município (T17 cap07: "Selecionar código de tributação"; supabase/functions/
// plugnotas-nfse-servicos-municipio): a lista de Taubaté (3554102) simulada, com a alíquota de ISS que o município informa. Só
// alguns itens da lista nacional (os que uma recicladora usa); outro município volta vazio.
const TAUBATE = [
  ['070901', 'Varrição, coleta, remoção, incineração, tratamento, reciclagem, separação e destinação final de lixo, rejeitos e outros resíduos quaisquer', 3],
  ['071001', 'Limpeza, manutenção e conservação de vias e logradouros públicos, imóveis, chaminés, piscinas, parques, jardins e congêneres', 3],
  ['071201', 'Controle e tratamento de efluentes de qualquer natureza e de agentes físicos, químicos e biológicos', 3],
  ['140101', 'Lubrificação, limpeza, lustração, revisão, carga e recarga, conserto, restauração, blindagem, manutenção e conservação de máquinas, veículos, aparelhos, equipamentos, motores, elevadores ou de qualquer objeto', 3],
  ['140601', 'Instalação e montagem de aparelhos, máquinas e equipamentos, inclusive montagem industrial, prestados ao usuário final, exclusivamente com material por ele fornecido', 3],
  ['160201', 'Outros serviços de transporte de natureza municipal', 2],
];

export default (body) => {
  const ibge = String(body?.codigoIbge || '').trim();
  if (ibge !== '3554102') return { servicos: [] };
  return { servicos: TAUBATE.map(([ctribnac, descricao, aliquotaIss]) => ({ ctribnac, descricao, aliquotaIss })) };
};
