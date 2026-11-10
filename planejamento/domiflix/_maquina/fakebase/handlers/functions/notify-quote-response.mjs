// Edge function `notify-quote-response` falsa (T9): a página pública da proposta a chama depois que o cliente aprova ou rejeita.
// A real avisa a empresa por notificação; no falso só confirma (nenhuma aula mostra o aviso).
export default async function notifyQuoteResponse() {
  return { success: true };
}
