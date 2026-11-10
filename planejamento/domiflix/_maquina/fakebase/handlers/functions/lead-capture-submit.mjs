// Edge function lead-capture-submit falsa (a edge real delega tudo a RPC submit_lead_capture_form; aqui as duas viram uma).
// Contrato: { short_code, fields, consent, honeypot } -> { success: true }  |  { error } com 400.
// Regras copiadas do banco: whitelist de campos habilitados no formulario, obrigatorios, e-mail, CPF/CNPJ com digito
// verificador, telefone com 10/11 digitos, CEP com 8; origin = 'public_form'; lead_consent_at; sobe submission_count.
// Diferenca deliberada: o banco real grava documento/telefone/celular/CEP so com digitos (o app ainda nao formata
// na exibicao: handoff-correcoes-app.md, item 2). Aqui gravamos COM mascara, como o cadastro feito dentro do app,
// para a lista de clientes nao mostrar numero cru no video; com a correcao do app o resultado e o mesmo.
import { FunctionError } from '../../http/functions.mjs';
import { insertRows } from '../../core/mutate.mjs';
import { nowIso } from '../../core/util.mjs';
import { validateCPF, validateCNPJ } from '../../tools/docs.mjs';

const ALLOWED = [
  'name', 'customer_type', 'document', 'email', 'phone', 'celular', 'company_name', 'nome_fantasia',
  'zip_code', 'address', 'address_number', 'neighborhood', 'complement', 'city', 'state', 'notes', 'photo_url',
];

const onlyDigits = (s) => String(s).replace(/\D/g, '');
const maskPhone = (d) => (d.length === 11 ? `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}` : `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`);
const maskCep = (d) => `${d.slice(0, 5)}-${d.slice(5)}`;
const maskCpf = (d) => `${d.slice(0, 3)}.${d.slice(3, 6)}.${d.slice(6, 9)}-${d.slice(9)}`;
const maskCnpj = (d) => `${d.slice(0, 2)}.${d.slice(2, 5)}.${d.slice(5, 8)}/${d.slice(8, 12)}-${d.slice(12)}`;

export default async function leadCaptureSubmit(body, { db }) {
  const raw = body || {};
  if (typeof raw.honeypot === 'string' && raw.honeypot.trim() !== '') return { success: true };
  const code = typeof raw.short_code === 'string' ? raw.short_code.trim() : '';
  const fields = raw.fields;
  if (!code || typeof fields !== 'object' || fields === null || Array.isArray(fields) || typeof raw.consent !== 'boolean') {
    throw new FunctionError('Formulário indisponível', 400);
  }
  const now = new Date();
  const form = db.first(
    'lead_capture_forms',
    (f) =>
      f.short_code === code &&
      f.is_active === true &&
      (!f.expires_at || new Date(f.expires_at) > now) &&
      (f.max_submissions == null || f.submission_count < f.max_submissions),
  );
  if (!form) throw new FunctionError('Formulário indisponível', 400);
  if (form.require_consent && !raw.consent) throw new FunctionError('Consentimento obrigatório', 400);

  const cfg = form.field_config || {};
  let ctype = String(fields.customer_type ?? '').trim().toLowerCase();
  if (ctype !== 'pf' && ctype !== 'pj') ctype = 'pf';

  const ins = {};
  for (const col of ALLOWED) {
    if (!cfg[col]?.enabled) continue;
    let v = String(fields[col] ?? '').replace(/[\x00-\x1F\x7F]/g, '').trim();
    if (!v) v = null;
    if (cfg[col]?.required && v === null) throw new FunctionError(`Campo obrigatório ausente: ${col}`, 400);
    if (v === null) continue;
    if (col === 'email') {
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) throw new FunctionError('E-mail inválido', 400);
      v = v.slice(0, 255);
    } else if (col === 'document') {
      const d = onlyDigits(v);
      if (ctype === 'pj') {
        if (!validateCNPJ(d)) throw new FunctionError('CNPJ inválido', 400);
        v = maskCnpj(d);
      } else {
        if (!validateCPF(d)) throw new FunctionError('CPF inválido', 400);
        v = maskCpf(d);
      }
    } else if (col === 'phone' || col === 'celular') {
      const d = onlyDigits(v);
      if (d.length !== 10 && d.length !== 11) throw new FunctionError('Telefone inválido', 400);
      v = maskPhone(d);
    } else if (col === 'zip_code') {
      const d = onlyDigits(v);
      if (d.length !== 8) throw new FunctionError('CEP inválido', 400);
      v = maskCep(d);
    } else if (col === 'customer_type') {
      v = ctype;
    } else if (col === 'name') {
      v = v.slice(0, 200);
    } else if (col === 'notes') {
      v = v.slice(0, 1000);
    } else {
      v = v.slice(0, 255);
    }
    ins[col] = v;
  }
  if (!('customer_type' in ins)) ins.customer_type = ctype;
  if (!('name' in ins)) ins.name = 'Cliente (formulário)';

  const [customer] = insertRows(
    'customers',
    { ...ins, company_id: form.company_id, origin: 'public_form', is_deleted: false, lead_consent_at: raw.consent ? nowIso() : null },
    {},
    { companyId: form.company_id },
  );
  db.update('lead_capture_forms', { id: form.id }, { submission_count: (form.submission_count || 0) + 1 });
  void customer;
  return { success: true };
}
