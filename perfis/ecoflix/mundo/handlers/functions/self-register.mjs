// Edge self-register (T1, cadastro em /cadastro): a pré-checagem do e-mail ("Continuar") diz que ele está livre, e o cadastro
// ("Criar Conta") responde sucesso de teste grátis SEM criar nada: a Recicla Vale Metais já existe no mundo, com histórico desde
// agosto. O login automático que o app faz logo depois (signInWithPassword) entra com o e-mail do Rafael. A senha que vem no corpo
// nunca é lida nem gravada.
export default (body) => {
  if (body?.check_email_only) return { available: true };
  return { success: true, requires_payment: false };
};
