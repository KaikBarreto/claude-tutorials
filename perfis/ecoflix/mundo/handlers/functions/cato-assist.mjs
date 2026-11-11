// Edge cato-assist (T21). A 1.59.154 só chama esta edge, na tela, para as sugestões de próxima pergunta: mode "followups" com a
// pergunta e a resposta (useCato.tsx:207-225) -> { suggestions: [...] } (as 3 da resposta simulada, lib/cato.mjs). As perguntas vão
// pela cato-background. Outro modo: { suggestions: [] } (a tela não mostra nada, como numa falha silenciosa).
import { acharResposta } from '../../lib/cato.mjs';

export default (body) => {
  if (body?.mode !== 'followups') return { suggestions: [] };
  const r = acharResposta(body?.message);
  return { suggestions: r ? r.sugestoes.slice(0, 3) : [] };
};
