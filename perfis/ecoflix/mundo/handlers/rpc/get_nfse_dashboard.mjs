// Relatórios Fiscais > "NFS-e" (T17, app 1.60.10; migration 20261111231500_relatorios_fiscais_nfse.sql): cartões "Serviços
// autorizados", "ISS apurado", "Retenções federais" e "Pendentes + rejeitadas", série mensal, distribuição por status e os
// rankings de tomadores e de serviços, das NFS-e do período (pela data de emissão; fora homologação e arquivadas).
const OK = ['emitida', 'cancelamento_pendente', 'cancelamento_rejeitado'];
const r2 = (n) => Math.round((Number(n) || 0) * 100) / 100;

export default (a, { store, companyId, RpcError }) => {
  const cid = a.p_company_id || companyId;
  const ini = new Date(a.p_start_date).getTime();
  const fim = new Date(a.p_end_date).getTime();
  if (!Number.isFinite(ini) || !Number.isFinite(fim)) throw new RpcError('Período obrigatório');
  const notas = store.rows('nfse_invoices').filter((n) => n.company_id === cid && n.environment !== 'homologacao' && !n.archived_at
    && n.issue_date && new Date(n.issue_date).getTime() >= ini && new Date(n.issue_date).getTime() <= fim);
  const aut = notas.filter((n) => OK.includes(n.status));
  const soma = (l, f) => r2(l.reduce((s, x) => s + (Number(f(x)) || 0), 0));
  const mes = (v) => { const d = new Date(new Date(v).getTime() - 3 * 3600e3); return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}`; };
  const serie = new Map();
  for (const n of aut) { const k = mes(n.issue_date); const x = serie.get(k) || { mes: k, qtd: 0, valor: 0 }; x.qtd += 1; x.valor = r2(x.valor + (Number(n.total_amount) || 0)); serie.set(k, x); }
  const status = new Map();
  for (const n of notas) status.set(n.status, (status.get(n.status) || 0) + 1);
  const ranking = (pares) => {
    const g = new Map();
    for (const [nome, v] of pares) { const x = g.get(nome) || { nome, valor: 0, qtd: 0 }; x.valor = r2(x.valor + (Number(v) || 0)); x.qtd += 1; g.set(nome, x); }
    return [...g.values()].sort((x, y) => y.valor - x.valor || x.nome.localeCompare(y.nome, 'pt-BR')).slice(0, 5);
  };
  const cliente = (n) => store.rows('customers').find((c) => c.id === n.customer_id && c.company_id === cid)?.name
    || String(n.tomador_avulso?.name || '').trim() || 'Sem identificação';
  const ids = new Set(aut.map((n) => n.id));
  const servicos = store.rows('nfse_invoice_services').filter((s) => ids.has(s.nfse_invoice_id));
  const nomeServico = (s) => store.rows('services').find((x) => x.id === s.service_id)?.name || String(s.discriminacao || '').trim() || 'Serviço sem identificação';
  return {
    can_view_values: true,
    autorizadas: { qtd: aut.length, valor: soma(aut, (n) => n.total_amount) },
    iss: { valor: soma(aut, (n) => n.total_iss) },
    retencoes: { valor: soma(aut, (n) => ['retencao_cofins', 'retencao_csll', 'retencao_inss', 'retencao_irrf', 'retencao_pis'].reduce((s, k) => s + (Number(n[k]) || 0), 0)) },
    pendencias: { qtd: notas.filter((n) => ['pendente', 'processando', 'rejeitada'].includes(n.status)).length },
    serie_mensal: [...serie.values()].sort((x, y) => x.mes.localeCompare(y.mes)),
    distribuicao_status: [...status.entries()].map(([s, q]) => ({ status: s, qtd: q })).sort((x, y) => y.qtd - x.qtd || x.status.localeCompare(y.status)),
    top_tomadores: ranking(aut.map((n) => [cliente(n), n.total_amount])),
    top_servicos: ranking(servicos.map((s) => [nomeServico(s), s.valor_servico])),
  };
};
