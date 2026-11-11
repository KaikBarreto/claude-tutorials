// Edge collection-report ("Relatório de Coleta N" da ordem concluída): ?code=<public_short_code> (logado) ou ?order_id=<id> (público).
// Só ordem concluída; o corpo é o build_collection_order_snapshot (empresa, ordem, parceiro, endereço, agendamento, coleta, equipamentos),
// sem checklist, assinatura nem foto (o mundo não usa). Ordem aberta ou inexistente: 404 "Relatório não encontrado", como a edge.
import { relatorio } from '../../lib/coletas.mjs';

export default (body, { store, url, FunctionError }) => {
  const code = String(url.searchParams.get('code') || body?.code || '').trim().toLowerCase();
  const id = url.searchParams.get('order_id') || body?.order_id || null;
  const o = store.rows('collection_orders').find((x) => (code ? String(x.public_short_code || '').toLowerCase() === code : x.id === id));
  if (!o || o.status !== 'coletada') throw new FunctionError('Relatório não encontrado', 404);
  return { ...relatorio(store, o), acesso: code ? 'membro' : 'publico' };
};
