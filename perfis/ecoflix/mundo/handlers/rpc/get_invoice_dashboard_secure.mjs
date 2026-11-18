// Relatórios Fiscais > "NF-e" (T17, app 1.60.10; migration 20261111231500_relatorios_fiscais_nfse.sql): a mesma conta da
// get_invoice_dashboard, com `can_view_values` (quem não tem a permissão de ver valores recebe os valores nulos e a tela mostra
// "Valores protegidos"). No mundo, o Rafael é MASTER: vê tudo.
import painel from './get_invoice_dashboard.mjs';

export default (a, ctx) => ({ ...painel(a, ctx), can_view_values: true });
