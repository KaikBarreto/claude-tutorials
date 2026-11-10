// Triggers de bank_transactions: sinal canônico pelo tipo, data lógica, balance_after e saldo gravado da conta. A lógica mora em lib/eco.mjs (GATILHOS), a mesma que os handlers usam ao gravar.
import { GATILHOS } from '../lib/eco.mjs';
export default GATILHOS.bank_transactions;
