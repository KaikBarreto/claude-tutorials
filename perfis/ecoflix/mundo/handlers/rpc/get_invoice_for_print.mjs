// RPC get_invoice_for_print (migration 20260925042000_get_invoice_for_print_destinatario_avulso; pages/NotasFiscais.tsx,
// handlePrintReceipt: o "Comprovante (Notinha)" da nota autorizada, T16 cap20). Devolve a nota, os itens (por created_at), a
// configuração fiscal do emitente da nota (ou a padrão da empresa) e o parceiro: entrada -> fornecedor; senão -> cliente; sem
// cadastro nenhum -> o destinatário avulso. Mesmas chaves da função do banco.
export default (a, { db }) => {
  const id = a?.p_invoice_id;
  if (!id) return null;
  const n = db.first('invoices', { id });
  if (!n) return null;
  const items = db.find('invoice_items', { invoice_id: id })
    .slice().sort((x, y) => String(x.created_at || '').localeCompare(String(y.created_at || '')));
  const cfg = (n.fiscal_config_id && db.first('company_fiscal_config', { id: n.fiscal_config_id }))
    || db.first('company_fiscal_config', (r) => r.company_id === n.company_id && r.is_default === true) || null;
  const fiscal = cfg && {
    razao_social: cfg.razao_social, nome_fantasia: cfg.nome_fantasia, inscricao_estadual: cfg.inscricao_estadual, cnpj: cfg.cnpj,
    logradouro: cfg.logradouro, numero: cfg.numero, complemento: cfg.complemento, bairro: cfg.bairro, cidade: cfg.cidade, uf: cfg.uf,
    cep: cfg.cep,
  };
  const parte = (p) => p && { name: p.name, cpf_cnpj: p.cpf_cnpj, razao_social: p.razao_social, inscricao_estadual: p.inscricao_estadual };
  let counterparty = null;
  let kind = null;
  if (n.invoice_type === 'entrada' && n.supplier_id) {
    counterparty = parte(db.first('suppliers', { id: n.supplier_id })) || null;
    if (counterparty) kind = 'supplier';
  } else if (n.invoice_type !== 'entrada' && n.customer_id) {
    counterparty = parte(db.first('customers', { id: n.customer_id })) || null;
    if (counterparty) kind = 'customer';
  } else if (!n.customer_id && !n.supplier_id && n.destinatario_avulso && typeof n.destinatario_avulso === 'object') {
    counterparty = parte(n.destinatario_avulso);
    kind = 'avulso';
  }
  return { invoice: n, items, fiscal_config: fiscal, counterparty, counterparty_kind: kind };
};
