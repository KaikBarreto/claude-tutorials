// Triggers de cash_transactions: data lógica (BRT), saldo derivado da gaveta do caixa e saldo do cofre (fórmula única). A lógica mora em lib/eco.mjs (GATILHOS), a mesma que os handlers usam ao gravar.
import { GATILHOS } from '../lib/eco.mjs';
export default GATILHOS.cash_transactions;
