// Edge function `get-tenant-payment-checkout` falsa (T19 · cap. 8, página pública /pagar/<código>). Espelha
// supabase/functions/get-tenant-payment-checkout (1.38.19): POST { short_code } -> { company, charge } (allowlist estrita: nunca valor líquido).
// Marca: o NOME é sempre o da empresa; logo e cor só com white-label ligado. Endereço, telefone, e-mail e CNPJ saem se a chave
// `show_*_in_documents` não for `false`. `allow_card`: conta ativa e cartão permitido. Cobrança cancelada/excluída: 404.
import { FunctionError } from '../../http/functions.mjs';

export default async function getTenantPaymentCheckout(b, { db }) {
  const codigo = String(b?.short_code ?? '').trim();
  if (!/^[a-z2-9]{6,24}$/.test(codigo)) throw new FunctionError('Cobrança não encontrada.', 404);
  const c = db.first('tenant_charges', { public_short_code: codigo });
  if (!c) throw new FunctionError('Cobrança não encontrada.', 404);
  if (['CANCELLED', 'DELETED'].includes(String(c.status).toUpperCase())) throw new FunctionError('Esta cobrança não está mais disponível.', 404);
  const conta = db.first('tenant_payment_accounts', (r) => String(r.company_id) === String(c.company_id));
  const s = db.first('company_settings', (r) => String(r.company_id) === String(c.company_id)) || {};
  const wl = s.white_label_enabled === true;
  let endereco = null;
  if (s.show_address_in_documents !== false && s.address) {
    endereco = String(s.address);
    if (s.address_number) endereco += `, ${s.address_number}`;
    if (s.complement) endereco += ` ${s.complement}`;
    if (s.neighborhood) endereco += ` - ${s.neighborhood}`;
    if (s.city) endereco += ` - ${s.city}`;
    if (s.state) endereco += `/${s.state}`;
    if (s.zip_code) endereco += ` - CEP: ${s.zip_code}`;
  }
  return {
    company: {
      name: String(s.name || '').trim() || 'Dominex', logo_url: wl ? s.white_label_logo_url ?? null : null, primary_color: wl ? s.white_label_primary_color ?? null : null,
      address_line: endereco, phone: s.show_phone_in_documents !== false && s.phone ? String(s.phone) : null,
      email: s.show_email_in_documents !== false && s.email ? String(s.email) : null, document: s.show_cnpj_in_documents !== false && s.document ? String(s.document) : null,
    },
    charge: {
      value: c.value, due_date: c.due_date, description: c.description, status: c.status, billing_type: c.billing_type, invoice_url: c.invoice_url,
      pix_copy_paste: c.pix_copy_paste, boleto_url: c.boleto_url, public_short_code: c.public_short_code,
      allow_card: conta?.status === 'active' && conta?.allow_card !== false,
    },
  };
}
