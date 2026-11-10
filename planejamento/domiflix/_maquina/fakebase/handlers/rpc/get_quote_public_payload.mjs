// RPC get_quote_public_payload(_token) · 20261013023000_quote_public_payload_country_regional.sql:7-159
// Payload da página pública da proposta (/proposta/<token>, sem login): orçamento (lista fixa de colunas, SEM custo nem margem), itens,
// cliente (ou null no prospecto), empresa (identidade + marca + região) e o código da cobrança ligada (null: sem cobrança no T9).
// Token que não existe -> null ("Proposta não encontrada.").
const QUOTE = ['id', 'quote_number', 'status', 'prospect_name', 'prospect_email', 'prospect_phone', 'customer_id', 'notes', 'terms', 'valid_until',
  'subtotal', 'total_value', 'discount_type', 'discount_value', 'discount_amount', 'tax_rate', 'card_discount_rate', 'card_installments',
  'displacement_cost', 'distance_km', 'include_gifts', 'proposal_template_id', 'created_at', 'token'];
const ITEM = ['id', 'position', 'item_type', 'description', 'details', 'quantity', 'unit_price', 'total_price'];
const CLIENTE = ['name', 'email', 'phone', 'document', 'address', 'address_number', 'complement', 'neighborhood', 'city', 'state', 'zip_code'];
const EMPRESA = ['name', 'document', 'logo_url', 'phone', 'email', 'address', 'address_number', 'complement', 'neighborhood', 'city', 'state', 'zip_code',
  'proposal_customization', 'white_label_enabled', 'white_label_logo_url', 'white_label_icon_url', 'white_label_primary_color', 'country_code',
  'language', 'currency', 'timezone'];

const pick = (row, cols) => Object.fromEntries(cols.map((c) => [c, row?.[c] ?? null]));

export default async function getQuotePublicPayload({ _token }, { db }) {
  if (!_token) return null;
  const q = db.first('quotes', { token: _token });
  if (!q) return null;
  const items = db
    .find('quote_items', { quote_id: q.id })
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)) || String(a.id).localeCompare(String(b.id)))
    .map((i) => pick(i, ITEM));
  const cliente = q.customer_id ? db.first('customers', { id: q.customer_id }) : null;
  const empresa = db.first('company_settings', { company_id: q.company_id });
  return {
    quote: pick(q, QUOTE),
    items,
    customer: cliente ? pick(cliente, CLIENTE) : null,
    company: empresa ? pick(empresa, EMPRESA) : null,
    charge_public_short_code: null,
  };
}
