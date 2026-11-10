# Propostas de fala · T1 · Sua conta e sua empresa

Do ensaio do robô (10/11/2026, EcoSistema 1.59.154, voz ainda estimada). O que a fala precisa mudar para bater com a tela ou caber
no gesto. Nada aqui foi aplicado: `roteiro.md` e `tts_textos.py` ficam para a revisão geral. Linha = número da linha do capítulo
(1 = primeira linha da tabela Tela × Fala).

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 03 | 5 | Lá embaixo, no menu, fica o card com o seu nome e o nome da empresa. O selo Master é de quem administra a conta. | Lá embaixo, no menu, fica o card com o seu nome e o nome da empresa. | O selo "MASTER" não aparece no card na 1.59.154 (defeito, ver Achados 1). Fala que vale nas duas versões. |
| 03 | 6 | Clicando nele, abre esse menu. Em Perfil ficam a sua foto e o seu nome. | Clicando nele, abre esse menu. Em Meu Perfil ficam a sua foto e o seu nome. | O item do menu é "Meu Perfil". |

## Achados do app

1. **Selo "MASTER" some do card da conta.** `components/layout/SidebarMenuContent.tsx:127` busca o perfil com `role` na chave
   `["user-profile", id]`, mas `components/support/SupportTriageDialog.tsx:181` (montado pelo botão flutuante de suporte em
   toda tela) usa a mesma chave com outra consulta, sem `role`; quem chega primeiro enche o cache e o card fica sem o selo
   (visto em todo login do ensaio). `TopNavbar.tsx:143` e `MoreMenuDrawer.tsx:106` também dividem a chave com formatos diferentes.
2. **Esqueci minha senha entra no sistema sem pedir a senha nova (navegador nunca usado).** Depois de "Verificar", o código
   abre a sessão; o `EntityTerminologyProvider` (`contexts/EntityTerminologyContext.tsx:141-148`) troca a árvore inteira por
   "Carregando empresa..." enquanto lê a nomenclatura (não há o instantâneo `entity_terminology_snapshot` no navegador), a
   tela de login é remontada com `showForgotPassword` falso e o efeito de redirecionamento (`pages/Auth.tsx:352`) leva ao
   painel. Medido no ensaio: "Código verificado com sucesso!" e "Nova Senha" aparecem por ~40 ms, a tela some, volta "Acesse sua
   conta" e vai para /inicio; a senha antiga continua valendo. Num navegador que o usuário já usou (instantâneo de até 7 dias)
   o fluxo segue certo: o cap04 grava nesse estado (o `storage` do capítulo traz o instantâneo, como no computador do
   escritório do Rafael), para a aula mostrar o fluxo como foi feito. Mesmo efeito, inofensivo, no login comum: um piscar de
   "Carregando empresa..." entre "Entrar" e o painel.
3. **Painel do login com dados que parecem reais.** A imagem do `LoginShowcase` (`/guia-tecnico/img/t6-caixa.jpg`) mostra
   "Kaik Barreto", "Maicon Silva", "Jonas" e saldos em bancos reais. A câmera fica no formulário (plano), mas a imagem aparece
   no plano geral do /login (caps 3 e 4).
