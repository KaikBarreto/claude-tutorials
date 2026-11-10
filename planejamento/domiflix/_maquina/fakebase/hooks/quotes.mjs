// T9 · DEFAULTs e gatilhos do banco real em `quotes` que o fakebase precisa imitar (migration 20260308135145_...sql:5,7,17):
//  - `status` nasce 'rascunho' (o "Criar Orçamento" e o "Salvar rascunho" não mandam status; só "Gerar link da proposta" promove a Enviado);
//  - `quote_number` pela sequência (a base do T9 semeia 1 a 8, o primeiro orçamento criado ao vivo nasce #9);
//  - `token` de 64 caracteres hexadecimais. No banco é aleatório; aqui é PREVISÍVEL (sha256 do número), para o roteiro do robô saber o
//    endereço da página pública da proposta (`/proposta/<token>`) sem ler o banco. A mesma conta vive em rec/t9/gerar.py.
import { createHash } from 'node:crypto';
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

export const tokenDoOrcamento = (n) => createHash('sha256').update(`dominex-fake-quote-${n}`).digest('hex');

TABLE_DEFAULTS.quotes = {
  ...(TABLE_DEFAULTS.quotes || {}),
  status: 'rascunho',
};

export default {
  beforeInsert(row, hc) {
    if (!row.quote_number) row.quote_number = hc.nextSeq('quotes', 'quote_number', hc.store.rows('quotes'));
    if (!row.token) row.token = tokenDoOrcamento(row.quote_number);
  },
};
