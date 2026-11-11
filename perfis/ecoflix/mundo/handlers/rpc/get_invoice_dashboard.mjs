// Estoque Fiscal > "Relatório fiscal" (T17 cap09), como a RPC do banco (migration 20260930220000): cartões Entrada (notas
// próprias + recebidas com lançamento fiscal), Saída, Pendentes + Rejeitadas, série mensal, distribuição por status e os rankings
// de fornecedores e clientes. Notas de homologação e arquivadas ficam de fora.
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const ini = new Date(a.p_start_date).getTime();
  const fim = new Date(a.p_end_date).getTime();
  const noPeriodo = (v) => { const t = new Date(v).getTime(); return t >= ini && t <= fim; };
  const notas = store.rows('invoices').filter((i) => i.company_id === cid && i.environment !== 'homologacao' && !i.archived_at && noPeriodo(i.issue_date));
  const comEntrada = new Set(store.rows('inbound_nfe_fiscal_entries').filter((e) => e.company_id === cid).map((e) => e.inbound_nfe_id));
  const recebidas = store.rows('inbound_nfe').filter((n) => n.company_id === cid && n.situacao_sefaz === 'autorizada'
    && (n.manifestacao || 'nenhuma') !== 'desconhecida' && noPeriodo(n.data_emissao));
  const recLanc = recebidas.filter((n) => comEntrada.has(n.id));
  const recNao = recebidas.filter((n) => !comEntrada.has(n.id));
  const soma = (l, f) => Math.round(l.reduce((s, x) => s + (Number(f(x)) || 0), 0) * 100) / 100;
  const entProp = notas.filter((i) => i.invoice_type === 'entrada' && i.status === 'emitida');
  const saida = notas.filter((i) => i.invoice_type === 'saida' && i.status === 'emitida');
  const nome = (tab, id) => (id ? store.rows(tab).find((r) => r.id === id)?.name : null);
  const avulso = (i) => (i.destinatario_avulso && String(i.destinatario_avulso.name || '').trim()) || null;
  const mes = (v) => { const d = new Date(v); return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}`; };
  const serie = new Map();
  const somaMes = (m, campo, v) => { if (!serie.has(m)) serie.set(m, { mes: m, entrada_valor: 0, saida_valor: 0 }); serie.get(m)[campo] += Number(v) || 0; };
  for (const i of [...entProp, ...saida]) somaMes(mes(i.issue_date), i.invoice_type === 'entrada' ? 'entrada_valor' : 'saida_valor', i.total_amount);
  for (const n of recLanc) somaMes(mes(n.data_emissao), 'entrada_valor', n.valor);
  const status = new Map();
  for (const i of notas) status.set(i.status, (status.get(i.status) || 0) + 1);
  const ranking = (lista) => {
    const g = new Map();
    for (const [n, v] of lista) { const x = g.get(n) || { nome: n, valor: 0, qtd: 0 }; x.valor += Number(v) || 0; x.qtd += 1; g.set(n, x); }
    return [...g.values()].map((x) => ({ ...x, valor: Math.round(x.valor * 100) / 100 })).sort((x, y) => y.valor - x.valor).slice(0, 5);
  };
  return {
    entrada: { qtd: entProp.length + recLanc.length, valor: soma(entProp, (x) => x.total_amount) + soma(recLanc, (x) => x.valor),
      qtd_propria: entProp.length, valor_propria: soma(entProp, (x) => x.total_amount), qtd_recebida: recLanc.length,
      valor_recebida: soma(recLanc, (x) => x.valor), qtd_nao_classificada: recNao.length, valor_nao_classificada: soma(recNao, (x) => x.valor) },
    saida: { qtd: saida.length, valor: soma(saida, (x) => x.total_amount) },
    pendencias: { qtd: notas.filter((i) => ['pendente', 'rejeitada'].includes(i.status)).length },
    serie_mensal: [...serie.values()].sort((x, y) => x.mes.localeCompare(y.mes)).map((x) => ({ ...x, entrada_valor: Math.round(x.entrada_valor * 100) / 100, saida_valor: Math.round(x.saida_valor * 100) / 100 })),
    distribuicao_status: [...status.entries()].map(([s, q]) => ({ status: s, qtd: q })).sort((x, y) => y.qtd - x.qtd),
    top_fornecedores: ranking([...entProp.map((i) => [nome('suppliers', i.supplier_id) || avulso(i) || 'Sem identificação', i.total_amount]),
      ...recLanc.map((n) => [(n.emitente_nome || '').trim() || 'Sem identificação', n.valor])]),
    top_clientes: ranking(saida.map((i) => [nome('customers', i.customer_id) || avulso(i) || 'Sem identificação', i.total_amount])),
  };
};
