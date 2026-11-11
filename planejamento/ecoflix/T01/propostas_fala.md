# Propostas de fala · T1 · Sua conta e sua empresa

Do ensaio do robô (10/11/2026, EcoSistema 1.59.154, voz ainda estimada). O que a fala precisa mudar para bater com a tela ou caber
no gesto. Nada aqui foi aplicado: `roteiro.md` e `tts_textos.py` ficam para a revisão geral. Linha = número da linha do capítulo
(1 = primeira linha da tabela Tela × Fala).

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 03 | 5 | Lá embaixo, no menu, fica o card com o seu nome e o nome da empresa. O selo Master é de quem administra a conta. | Lá embaixo, no menu, fica o card com o seu nome e o nome da empresa. | O selo "MASTER" não aparece no card na 1.59.154 (defeito, ver Achados 1). Fala que vale nas duas versões. |
| 03 | 6 | Clicando nele, abre esse menu. Em Perfil ficam a sua foto e o seu nome. | Clicando nele, abre esse menu. Em Meu Perfil ficam a sua foto e o seu nome. | O item do menu é "Meu Perfil". |

## Roteiro × mundo B (para a revisão; a fala não muda)

- **Bairro:** a coluna Tela do cap06 diz "Jardim Vale do Sol"; o mundo B (`MUNDO_LINHA_DO_TEMPO.md`, seção 3) diz "Parque
  Industrial". O robô segue B (a busca do CEP 12086-410 devolve Parque Industrial), porque o T1 cria a identidade que as outras
  aulas mostram. A fala não diz o bairro.
- **E-mail da empresa:** B (seção 3) traz `rafael@reciclavalemetais.example`; o cap06 L2 troca, na tela e na fala, para
  `contato@reciclavalemetais.example`. O robô segue a fala; a semente `apos-cap06` sai com `contato@`. Decidir qual vale em B.
- **Frase do comprovante:** a de 68 caracteres, sem sábado (junção); o contador mostra "68/2000 caracteres".
- **Complemento:** o cap06 digita "Galpão 2" (a fala diz "galpão dois"); B (seção 3) não tem complemento. Depois do T1 o
  endereço da empresa e o da Configuração Fiscal (Matriz) ficam com "Galpão 2". Decidir se B ganha o galpão.
- **Configuração Fiscal no T1:** a aula parte da Matriz de B. Ao salvar no cap05 (endereço ainda vazio) o app grava o endereço
  vazio nela (sem mexer na UF) e o cap06 grava o completo de novo; nada disso aparece na tela do T1. As sementes `apos-cap05`
  e `apos-cap06` atualizam essa linha (não inserem outra).

## Números da fala × tela (seção 18)

Todos batem: duas etapas (Dados e Acesso), "Mínimo 8 caracteres", os dois links (Termos e Política), "7 dias grátis" e "5
usuários" (cap02), até cinco contas salvas (`MAX_SESSIONS = 5`, não aparece na tela), código de 6 dígitos e "Reenviar código em
60s" (cap04), "#30", "0030" e "30/11/26" nos exemplos da numeração (cap07), "68/2000", 30/60/90 com 33,33 + 33,33 + 33,34 =
100% e "3 parcelas" (caps 10 e 13), Rua das Oficinas, 1250 (cap06). Os exemplos falados do cap09 não estão na tela e fecham
com os preços de B (latinha R$ 6,20/kg: 37 kg = R$ 229,40; ferro misto R$ 0,75/kg: 190 kg = R$ 142,50, 200 kg = R$ 150,00).
Para a junção corrigir na seção 18: o 1.250 do cap06 é o número da rua (seção 3), não o "fechamento do #84"; os "150 dias" dos
caps 10 e 13 são a leitura de "sessenta e noventa dias" (60 e 90).

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
