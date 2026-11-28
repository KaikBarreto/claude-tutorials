// RPC list_fiscal_document_history (1.60.39, migration 20261126183000_fiscal_document_history; hooks/useFiscalDocumentHistory.ts):
// o "Histórico" da NF-e (Visualizar e menu da nota, T16 cap15), da NFS-e e do MDF-e (menu Ações, T17) e do MTR, num diálogo só
// (FiscalDocumentHistoryDialog). Mesmas fontes e textos da função do banco: fiscal_document_events (os eventos novos) +
// nfe_events e nfe_direct_attempt_logs (NF-e) + reconstrução "legacy" do cadastro do MDF-e, dos jobs de contingência e da NFS-e
// quando o documento ainda não tem evento novo + mtr_manifest_attempts. Ordem: created_at e event_id decrescentes; cursor e limite
// (1 a 100, padrão 50) como no SQL. Sem triggers no falso: o que o banco grava por trigger aparece pela reconstrução legacy.
const TIPOS = ['nfe', 'nfce', 'nfse', 'mdfe', 'mtr'];
const iso = (v) => (v ? new Date(v).toISOString() : null);

function linha(o) {
  return {
    event_id: o.event_id, category: o.category, stage: o.stage, severity: o.severity, attempt_no: o.attempt_no ?? null,
    channel: o.channel ?? null, title: o.title, message: o.message ?? null, technical_code: o.technical_code ?? null, cstat: o.cstat ?? null,
    started_at: o.started_at ?? null, finished_at: o.finished_at ?? null, duration_ms: o.duration_ms ?? null, source: o.source,
    metadata: o.metadata || {}, approximate: !!o.approximate, created_at: iso(o.created_at) || new Date(0).toISOString(),
  };
}

const NFE_CAT = { consulta: 'query', emissao: 'transmission', autorizacao: 'authorization', rejeicao: 'rejection', cancelamento: 'cancellation' };
const NFE_TIT = {
  consulta: 'Consulta à administração tributária', emissao: 'Transmissão do documento fiscal', autorizacao: 'Documento autorizado',
  rejeicao: 'Documento rejeitado', cancelamento: 'Cancelamento do documento',
};
const initcap = (s) => String(s).toLowerCase().replace(/(^|[^a-zà-ú0-9])([a-zà-ú])/g, (m, a, b) => a + b.toUpperCase());
function sevNfe(st) {
  if (['success', 'sucesso', 'autorizada', 'autorizado'].includes(st)) return 'success';
  if (['error', 'erro', 'rejeitada', 'rejeitado'].includes(st)) return 'error';
  if (['pending', 'pendente', 'aviso'].includes(st)) return 'warning';
  return 'info';
}

const MDFE_CAT = {
  autorizado: 'authorization', rejeitado: 'rejection', cancelado: 'cancellation', cancelamento_pendente: 'cancellation',
  cancelamento_rejeitado: 'cancellation', preparando_contingencia: 'contingency', contingencia: 'contingency', contingencia_erro: 'contingency',
  contingencia_rejeitada: 'rejection',
};
const MDFE_SEV = {
  autorizado: 'success', encerrado: 'success', cancelado: 'success', rejeitado: 'error', encerramento_rejeitado: 'error',
  cancelamento_rejeitado: 'error', contingencia_erro: 'error', contingencia_rejeitada: 'error', aguardando_sefaz: 'warning',
  encerramento_pendente: 'warning', cancelamento_pendente: 'warning',
};
const MDFE_TIT = {
  autorizado: 'MDF-e autorizado', rejeitado: 'MDF-e rejeitado', encerrado: 'MDF-e encerrado', encerramento_pendente: 'Encerramento aguardando confirmação',
  encerramento_rejeitado: 'Encerramento recusado', cancelado: 'MDF-e cancelado', cancelamento_pendente: 'Cancelamento aguardando confirmação',
  cancelamento_rejeitado: 'Cancelamento recusado', contingencia: 'MDF-e emitido em contingência',
};
const JOB_CAT = { prepare: 'preparation', reconcile: 'query', transmit: 'transmission', cancel: 'cancellation' };
const JOB_TIT = {
  prepare: 'Preparação fiscal do MDF-e', reconcile: 'Consulta de situação oficial', transmit: 'Tentativa de transmissão do MDF-e',
  cancel: 'Tentativa de cancelamento do MDF-e', enclose: 'Tentativa de encerramento do MDF-e',
};
const JOB_SEV = { done: 'success', rejected: 'error', failed: 'error', queued: 'warning', processing: 'warning' };
const NFSE_CAT = { emitida: 'authorization', rejeitada: 'rejection', cancelada: 'cancellation', cancelamento_pendente: 'cancellation', cancelamento_rejeitado: 'cancellation' };
const NFSE_SEV = { emitida: 'success', cancelada: 'success', rejeitada: 'error', cancelamento_rejeitado: 'error', cancelamento_pendente: 'warning', processando: 'warning' };
const NFSE_TIT = {
  emitida: 'NFS-e autorizada', rejeitada: 'NFS-e rejeitada', cancelada: 'NFS-e cancelada', cancelamento_pendente: 'Cancelamento aguardando confirmação',
  cancelamento_rejeitado: 'Cancelamento recusado', processando: 'NFS-e em processamento',
};
const MTR_CAT = { authorized: 'authorization', rejected: 'rejection', validation_error: 'validation', blocked: 'validation' };
const MTR_SEV = { authorized: 'success', rejected: 'error', validation_error: 'warning', blocked: 'warning', uncertain: 'warning' };
const MTR_TIT = {
  authorized: 'MTR autorizado', rejected: 'MTR rejeitado', validation_error: 'Validação do MTR', blocked: 'Emissão bloqueada antes do envio',
  uncertain: 'Resultado da emissão ainda incerto',
};

export default (a, { store, companyId, RpcError }) => {
  const tipo = String(a?.p_document_type || '').toLowerCase();
  const id = a?.p_document_id;
  if (!TIPOS.includes(tipo)) throw new RpcError('Tipo de documento fiscal inválido.', '22023', 400);
  const tabDoc = tipo === 'nfe' || tipo === 'nfce' ? 'invoices' : tipo === 'nfse' ? 'nfse_invoices' : tipo === 'mdfe' ? 'mdfe_manifests' : 'mtr_manifests';
  const doc = store.rows(tabDoc).find((r) => r.id === id);
  if (!doc) return [];
  if (tipo === 'nfce' && Number(doc.modelo ?? 55) !== 65) return [];
  if (tipo === 'nfe' && Number(doc.modelo ?? 55) === 65) return [];
  const cid = doc.company_id;
  if (cid !== companyId) throw new RpcError('Acesso negado.', '42501', 403);

  const novos = store.rows('fiscal_document_events').filter((f) => f.company_id === cid && f.document_type === tipo && f.document_id === id);
  const out = novos.map((f) => linha({ ...f, event_id: `fiscal:${f.id}` }));

  if (tipo === 'nfe' || tipo === 'nfce') {
    for (const e of store.rows('nfe_events').filter((x) => x.company_id === cid && x.invoice_id === id)) {
      const p = e.payload || {};
      const r = e.plugnotas_response || {};
      const cs = p.cStat ?? p.cstat ?? r.cStat ?? r.cstat ?? '';
      out.push(linha({
        event_id: `nfe-event:${e.id}`, category: NFE_CAT[e.event_type] || 'status', stage: String(e.event_type || 'status').slice(0, 80),
        severity: sevNfe(e.status), channel: p.channel ?? p.canal ?? null,
        title: NFE_TIT[e.event_type] || initcap(String(e.event_type || 'Evento fiscal').replace(/_/g, ' ')), message: e.message ?? null,
        technical_code: p.error_code ?? r.error_code ?? null, cstat: /^[0-9]{3,4}$/.test(String(cs)) ? String(cs) : null, source: 'nfe_events',
        metadata: { provider: p.provider ?? r.provider ?? null, environment: p.environment ?? null, uf: p.uf ?? null, protocol: r.protocolo ?? null },
        created_at: e.created_at,
      }));
    }
    for (const l of store.rows('nfe_direct_attempt_logs').filter((x) => x.company_id === cid && x.invoice_id === id)) {
      const autorizada = l.outcome === 'authorized' || l.cstat === '100';
      out.push(linha({
        event_id: `nfe-attempt:${l.id}`,
        category: ['probe_response', 'probe_error'].includes(l.outcome) ? 'query' : autorizada ? 'authorization' : l.outcome === 'rejected' ? 'rejection' : 'transmission',
        stage: ['probe_response', 'probe_error'].includes(l.outcome) ? 'channel_probe' : 'direct_attempt',
        severity: autorizada ? 'success' : l.outcome === 'rejected' ? 'error' : (l.cstat === '114' || l.error_code) ? 'warning' : 'info',
        attempt_no: l.attempt_no ?? null, channel: l.channel ?? null,
        title: autorizada ? 'NF-e autorizada' : l.outcome === 'rejected' ? 'NF-e rejeitada' : 'Tentativa no motor fiscal direto',
        technical_code: l.error_code ?? null, cstat: l.cstat ?? null, finished_at: iso(l.created_at), duration_ms: l.latency_ms ?? null,
        source: 'nfe_direct_attempt_logs', metadata: { provider: 'motor_proprio', uf: l.uf ?? null, outcome: l.outcome ?? null }, created_at: l.created_at,
      }));
    }
  }

  if (tipo === 'mtr') {
    const tent = store.rows('mtr_manifest_attempts').filter((x) => x.company_id === cid && x.manifest_id === id)
      .sort((x, y) => String(x.created_at).localeCompare(String(y.created_at)) || String(x.id).localeCompare(String(y.id)));
    tent.forEach((t, i) => out.push(linha({
      event_id: `mtr-attempt:${t.id}`, category: MTR_CAT[t.state] || 'transmission', stage: t.stage, severity: MTR_SEV[t.state] || 'info',
      attempt_no: i + 1, channel: 'orgao_ambiental', title: MTR_TIT[t.state] || 'Tentativa de emissão do MTR', message: t.error_message ?? null,
      technical_code: t.error_code ?? null, started_at: iso(t.provider_request_started_at || t.created_at), finished_at: iso(t.finished_at),
      source: 'mtr_manifest_attempts', created_at: t.created_at,
    })));
  }

  if (tipo === 'mdfe' && !novos.length) {
    out.push(linha({
      event_id: `mdfe-legacy-created:${doc.id}`, category: 'preparation', stage: 'legacy_reconstruction', severity: 'info', title: 'Rascunho criado',
      message: 'Evento reconstruído a partir do cadastro do MDF-e; tentativas intermediárias antigas podem não estar disponíveis.',
      source: 'mdfe_legacy', metadata: { environment: doc.environment ?? null, uf: doc.uf_carregamento ?? null }, approximate: true, created_at: doc.created_at,
    }));
    const conf = doc.fiscal_status_confirmation || {};
    out.push(linha({
      event_id: `mdfe-legacy-status:${doc.id}`, category: MDFE_CAT[doc.status] || 'status', stage: 'legacy_reconstruction',
      severity: MDFE_SEV[doc.status] || 'info', title: MDFE_TIT[doc.status] || 'Estado atual do MDF-e', message: doc.error_message ?? null,
      cstat: /^[0-9]{3,4}$/.test(String(conf.cstat ?? '')) ? String(conf.cstat) : null, source: 'mdfe_legacy',
      metadata: { provider: doc.fiscal_provider ?? conf.source ?? null, environment: doc.environment ?? null, uf: doc.uf_carregamento ?? null, protocol: doc.mdfe_protocol ?? conf.protocol ?? null },
      approximate: true, created_at: doc.authorized_at || doc.enclosed_at || doc.updated_at || doc.created_at,
    }));
  }
  if (tipo === 'mdfe') {
    const job = store.rows('mdfe_contingency_jobs').find((j) => j.id === id);
    if (job && !novos.some((f) => f.source === 'mdfe_contingency_jobs_trigger')) {
      out.push(linha({
        event_id: `mdfe-job-current:${job.id}:${job.attempts ?? 0}`, category: JOB_CAT[job.action] || 'status', stage: 'legacy_reconstruction',
        severity: JOB_SEV[job.state] || 'info', attempt_no: Math.max(job.attempts ?? 1, 1), channel: 'sefaz',
        title: JOB_TIT[job.action] || 'Processamento fiscal do MDF-e', message: job.last_error ?? null, started_at: iso(job.emitted_at),
        finished_at: ['done', 'rejected', 'failed'].includes(job.state) ? iso(job.updated_at) : null, source: 'mdfe_contingency_jobs',
        metadata: { provider: 'motor_proprio', environment: job.environment ?? null, outcome: job.state ?? null, protocol: job.event_protocol ?? job.protocol ?? null },
        approximate: true, created_at: job.updated_at,
      }));
    }
  }

  if (tipo === 'nfse' && !novos.length) {
    out.push(linha({
      event_id: `nfse-legacy-created:${doc.id}`, category: 'preparation', stage: 'legacy_reconstruction', severity: 'info', title: 'Rascunho criado',
      message: 'Evento reconstruído a partir do cadastro da NFS-e; tentativas intermediárias antigas podem não estar disponíveis.',
      source: 'nfse_legacy', metadata: { environment: doc.environment ?? null }, approximate: true, created_at: doc.created_at,
    }));
    out.push(linha({
      event_id: `nfse-legacy-status:${doc.id}`, category: NFSE_CAT[doc.status] || 'status', stage: 'legacy_reconstruction',
      severity: NFSE_SEV[doc.status] || 'info', title: NFSE_TIT[doc.status] || 'Estado atual da NFS-e', message: doc.error_message ?? null,
      source: 'nfse_legacy', metadata: { environment: doc.environment ?? null, official_number: doc.nfse_numero_oficial ?? null, protocol: doc.protocol ?? null },
      approximate: true, created_at: doc.authorized_at || doc.updated_at || doc.created_at,
    }));
  }

  const limite = Math.min(Math.max(Number(a?.p_limit) || 50, 1), 100);
  const cAt = a?.p_cursor_created_at ? iso(a.p_cursor_created_at) : null;
  const cId = a?.p_cursor_event_id || '';
  return out
    .filter((e) => !cAt || e.created_at < cAt || (e.created_at === cAt && e.event_id < cId))
    .sort((x, y) => y.created_at.localeCompare(x.created_at) || y.event_id.localeCompare(x.event_id))
    .slice(0, limite);
};
