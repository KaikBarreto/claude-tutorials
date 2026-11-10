// T26 · primeira abertura do CRM/Kanban (hooks/useTenantCrm.ts): sem funil padrão, o banco cria o "Funil de vendas" (#22c55e, padrão)
// com Novo, Em contato, Proposta, Ganho (is_won) e Perdido (is_lost) e devolve o id (migration 20260929180000). Lógica em lib/crm.mjs.
import { garanteFunilPadrao } from '../../lib/crm.mjs';

export default (_a, { companyId }) => garanteFunilPadrao(companyId);
