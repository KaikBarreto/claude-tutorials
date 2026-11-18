// cato_corrections_manage(p_action, p_payload) — app 1.60.10, migration 20261117030000_cato_corrections_inbox_and_ticket_items.sql
// (hooks/useCatoCorrections.ts). "Respostas revisadas" do Cato: o botão consulta "status" (paginado de 20 em 20) a cada minuto em
// toda tela logada; sem { inbox: [] } o painel mostra "As respostas revisadas estão indisponíveis agora". Mundo base: nenhuma
// resposta revisada (T00, T21, T25 e toda aula com o botão do Cato). "mark_read" não tem o que marcar.
export default () => ({ inbox: [], unreadCount: 0, hasMore: false });
