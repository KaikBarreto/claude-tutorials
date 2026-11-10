// Edge password-reset (T1): "Enviar Código" do Esqueci minha senha responde sucesso sem mandar e-mail nenhum (o código 481207 do
// mundo só aparece na ilustração; o auth falso aceita o código em /auth/v1/verify). Primeiro acesso (`check_first_access`, chamado
// só quando a senha falha no login): ninguém do mundo está com troca de senha pendente.
export default (body) => {
  const action = body?.action;
  if (action === 'send') return { success: true };
  if (action === 'check_first_access') return { firstAccess: false };
  return { success: true };
};
