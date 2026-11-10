// Edge function crm-lead-webhook falsa (supabase/functions/crm-lead-webhook/index.ts) · T10, cap. 8 ("Contatos que chegam sozinhos").
// So POST. Token na URL (?token=), no cabecalho x-webhook-token ou no corpo; webhook ativo ou 401 "Webhook inválido ou inativo".
// Exige ao menos um de name/phone/email. Titulo = title ou "Lead via {nome do webhook}"; origem = a do webhook, senao source, senao "Webhook Externo";
// etapa = a configurada (no funil configurado), senao a 1a etapa aberta do funil; cria a oportunidade SEM cliente e SEM responsavel, com
// "Nome:", "Telefone:", "Email:" e "Origem: {webhook}" nas observacoes. Resposta { success: true, lead } (mais duplicate: true na reentrega).
// O corpo chega ja lido (http/functions.mjs); o metodo e a URL vem em `req`/`url`.
import crypto from 'node:crypto';
import { FunctionError } from '../../http/functions.mjs';
import { insertRows } from '../../core/mutate.mjs';

const pick = (o, chaves) => {
  for (const k of chaves) if (typeof o?.[k] === 'string' && o[k].trim()) return o[k].trim();
  return null;
};
const clamp = (s, n) => (s == null ? null : String(s).slice(0, n));

export default async function crmLeadWebhook(body, { db, req, url }) {
  if (req.method !== 'POST') throw new FunctionError('Método não permitido', 405);
  const raiz = body && typeof body === 'object' && !Array.isArray(body) ? body : {};
  const p = raiz.lead && typeof raiz.lead === 'object' && !Array.isArray(raiz.lead) ? raiz.lead : raiz;

  const token = url.searchParams.get('token') || req.headers['x-webhook-token'] || pick(p, ['token', 'webhook_token']);
  if (!token) throw new FunctionError('Token do webhook ausente', 401);
  const hook = db.first('crm_webhooks', (w) => w.token === token && w.is_active === true);
  if (!hook) throw new FunctionError('Webhook inválido ou inativo', 401);
  const empresa = hook.company_id;

  const name = clamp(pick(p, ['name', 'full_name', 'nome']), 200);
  const phone = clamp(pick(p, ['phone', 'phone_number', 'telefone', 'whatsapp']), 40);
  const email = clamp(pick(p, ['email']), 200);
  if (!name && !phone && !email) throw new FunctionError('Informe ao menos um destes campos: name, phone ou email', 400);

  const titulo = clamp(pick(p, ['title', 'titulo', 'subject']), 200) || `Lead via ${hook.name}`;
  const detalhes = clamp(pick(p, ['notes', 'observations', 'message', 'mensagem']), 5000);
  const origem = clamp(hook.origin || pick(p, ['source', 'origem']) || 'Webhook Externo', 100);
  const valor = typeof p.value === 'number' ? p.value : typeof p.valor === 'number' ? p.valor : null;

  let etapa = null;
  if (hook.stage_id) etapa = db.first('crm_stages', (s) => s.id === hook.stage_id && s.company_id === empresa && s.pipeline_id === hook.pipeline_id);
  if (!etapa && hook.pipeline_id) {
    etapa = db.rows('crm_stages')
      .filter((s) => s.company_id === empresa && s.pipeline_id === hook.pipeline_id && !s.is_won && !s.is_lost)
      .sort((a, b) => a.position - b.position)[0] || null;
  }
  if (!etapa && !hook.pipeline_id) {
    const padrao = db.first('crm_pipelines', (f) => f.company_id === empresa && f.is_default);
    etapa = db.rows('crm_stages')
      .filter((s) => s.company_id === empresa && !s.is_won && !s.is_lost && (!padrao || s.pipeline_id === padrao.id))
      .sort((a, b) => a.position - b.position)[0] || null;
  }

  const notes = [detalhes, name && `Nome: ${name}`, phone && `Telefone: ${phone}`, email && `Email: ${email}`, `Origem: ${hook.name}`].filter(Boolean).join('\n');
  const chave = (req.headers['x-idempotency-key'] || pick(p, ['event_id', 'external_id', 'idempotency_key']) || '').toString().trim();
  const linha = { company_id: empresa, title: titulo, source: origem, stage_id: etapa?.id ?? null, status: 'lead', notes, value: valor };
  if (chave) {
    const h = crypto.createHash('sha1').update(`${empresa}:${chave}`).digest('hex');
    linha.id = `${h.slice(0, 8)}-${h.slice(8, 12)}-5${h.slice(13, 16)}-8${h.slice(17, 20)}-${h.slice(20, 32)}`;
    const ja = db.first('leads', { id: linha.id });
    if (ja) return { success: true, duplicate: true, lead: { id: ja.id, title: ja.title, source: ja.source, stage_id: ja.stage_id } };
  }
  const [lead] = insertRows('leads', linha, { columns: null }, { companyId: empresa, userId: null });
  return { success: true, lead: { id: lead.id, title: lead.title, source: lead.source, stage_id: lead.stage_id } };
}
