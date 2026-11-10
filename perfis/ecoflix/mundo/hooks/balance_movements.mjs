// Triggers de balance_movements: transaction_date é o dia (BRT) de transaction_at. A lógica mora em lib/eco.mjs (GATILHOS), a mesma que os handlers usam ao gravar.
import { GATILHOS } from '../lib/eco.mjs';
export default GATILHOS.balance_movements;
