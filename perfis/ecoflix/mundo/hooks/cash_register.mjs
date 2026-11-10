// Triggers de cash_register: numeração do caixa por empresa (#87), moeda e abertura. A lógica mora em lib/eco.mjs (GATILHOS), a mesma que os handlers usam ao gravar.
import { GATILHOS } from '../lib/eco.mjs';
export default GATILHOS.cash_register;
