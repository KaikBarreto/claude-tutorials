# Plano · T2 Usuários e permissões

- **Título:** Usuários e permissões (o da fonte).
- **Objetivo:** colocar a equipe da Recicla Vale Metais no sistema com o acesso certo: criar a Juliana e o Marcos,
  usar os perfis rápidos, montar um acesso na mão, desativar e excluir, entender o master, o limite do plano e as
  permissões de valor.
- **Antes:** T1 "Sua conta e sua empresa". **Próximo:** T3 "Materiais e tabelas de preço".
- **Vinhetas (áreas):** USUÁRIOS · USUÁRIOS · PERMISSÕES · PERMISSÕES · PERMISSÕES · USUÁRIOS · MASTER · PLANO · VALORES · RESUMO.
- **Alvo da fonte:** ~13 min. Desktop 1280×800, logado como Rafael Nogueira (master). Base: `T02/inventario.md`.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça), igual ao mundo.

## Estado de partida (fim do T1)
Recicla Vale Metais com um usuário só: Rafael Nogueira, master (`user_roles` `company_admin`, `permission_preset`
`full_access`, como o `create-company` grava). Assinatura ativa, plano `personalizado`, todos os módulos da trilha,
**`max_users` 3**. Nenhuma foto de usuário.

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área · título) | O que a tela mostra | Cuidados na fala | Fonte |
|---|---|---|---|---|
| 0 | (sem vinheta) | Dashboard → rodapé do menu "Configurações" → aba "Usuários e Permissões". Ilustração da equipe. | "Antes: Sua conta e sua empresa" | abertura |
| 1 | USUÁRIOS · Onde fica | Cabeçalho da aba, "Empresa: Recicla Vale Metais", selo "1 / 3 usuários", "Criar Usuário"; lista com o Rafael (coroa, "Acesso total · Ativo"); detalhe "Master", "Perfil de acesso" "Acesso Total". Ilustração: cada aba das Configurações tem a sua chave. | a aba aparece com a permissão "Gerenciar Usuários" | 00:00 |
| 2 | USUÁRIOS · Criar o usuário | "Criar Usuário" → "Criar Novo Usuário": "Nome Completo" Marcos Antunes, "Email", "Senha" com "Senha forte". | Uma dica: a foto entra depois, no "Editar" | 01:00 |
| 3 | PERMISSÕES · Os três perfis rápidos | "Perfis rápidos": "Acesso Total", "Somente Visualização", "Operador Padrão" (fica este); "Criar Usuário" → "Usuário criado com sucesso!"; selo "2 / 3 usuários". Ilustração: três chaveiros. | o perfil é um ponto de partida | 02:30 |
| 4 | PERMISSÕES · Telas e ações | Juliana Prado criada na mão: tela "Contas a Pagar/Receber" e as ações dela ("Clique para ver 4 ações", "2/4"); busca "Buscar tela ou ação..."; demais telas do escritório; "Criar Usuário". Ilustração: a tela é a porta, as ações são o que se faz lá dentro; as duas travas. | ⚠️ ligar a ação não abre a tela; ⚠️ plano e servidor mandam mais (🔒 módulo) | 04:00 |
| 5 | PERMISSÕES · O balanceiro e o escritório | Marcos → "Editar": foto ("Foto atualizada com sucesso!"), "Tela inicial" "Caixa", desliga "Ver Projeção de Lucro" (o selo vira "Personalizado"), "Atualizar" → "Permissões atualizadas! ...". Juliana: detalhe "Telas (7)", "Ações (8)", sem "Caixa". | o Marcos precisa entrar de novo para ver a mudança | 06:30 |
| 6 | USUÁRIOS · Desativar ou excluir | Menu "..." do Marcos: "Desativar" → "Usuário desativado!", "Inativo", "A conta está impedida de entrar.", selo "2 / 3 usuários"; "Ativar"; "Excluir" → "Excluir usuário" (pede o e-mail) → "Cancelar". Ilustração: crachá guardado × crachá rasgado. | desativado não conta no limite; excluir não tem volta; quem pode o quê | 08:30 |
| 7 | MASTER · Passar o controle | Coroa e "Master"; menu "..." da Juliana → "Tornar master" → "Passar o controle da empresa?" → "Cancelar". Ilustração: a coroa e o escudo. | ⚠️ quem passa o bastão perde a proteção | 09:30 |
| 8 | PLANO · O limite de usuários | Selo "3 / 3 usuários"; "Criar Usuário" → "Sua equipe cresceu! 🎉" ("Adicionar usuários extras", "Novo limite de usuários:", "Continuar") → "Cancelar". Ilustração: as vagas do plano. | 🔒 depende do plano contratado; preço nunca falado | 10:30 |
| 9 | VALORES · Esconder o valor | Marcos → "Editar": "Geral" → "Ver Totais e Valores Financeiros"; no "Caixa", "Ver Projeção de Lucro" (desligada) e "Ver Dinheiro Total em Caixa"; no "Ticket de Pesagem", "Criar Ticket de Pesagem com Valores" → "Cancelar". Ilustração: o que some × o que fica. | ⚠️ esconder valor não trava a operação | 11:30 |
| 10 | RESUMO · Recapitulando | Montagem: Marcos e Juliana na lista, os perfis, o editar, o selo "3 / 3". "Próximo: Materiais e tabelas de preço". | "Até lá!" | recap |

Transições faladas: 0→1 "Vamos ver onde fica"; 1→2 "A equipe começa pelo Marcos"; 2→3 "Agora o que ele pode fazer";
3→4 "A Juliana, a gente monta na mão"; 4→5 "Os dois casos do pátio"; 5→6 "E quando alguém sai de férias?"; 6→7 "E o
master?"; 7→8 "Agora o tamanho da equipe"; 8→9 "Pra fechar, os valores".

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)
| Item | Valor |
|---|---|
| Plano da empresa | `companies.subscription_plan` `personalizado`, **`max_users` 3** (Rafael, Juliana e Marcos: no fim do T2 a empresa fica em 3/3, e o cap08 mostra a janela de usuário extra) |
| Nome na aba | `companies.name` "Recicla Vale Metais" (a linha "Empresa: ...") |
| E-mails | `rafael@reciclavalemetais.example` (o do T1; junção), `marcos.antunes@reciclavalemetais.example`, `juliana.prado@reciclavalemetais.example` |
| Senhas (digitadas, nunca faladas) | Marcos `Balanca#2026`, Juliana `Escritorio#2026` (as duas dão "Senha forte") |
| Marcos Antunes (criado no cap02-03, ajustado no cap05) | "Operador Padrão" menos "Ver Projeção de Lucro" = 31 permissões, `permission_preset` nulo ("Personalizado"); tela inicial `/caixa`; foto (avatar desenhado, sem rosto real); ativo; role `operator` |
| Juliana Prado (criada no cap04) | 7 telas: "Dashboard", "Movimentações Bancárias", "Relatório Financeiro", "Contas a Pagar/Receber", "Pedidos", "Fiscal & Ambiental", "Clientes e Fornecedores"; 8 ações: "Ver Totais e Valores Financeiros", "Gerenciar Contas Bancárias", "Conciliar Extrato Bancário", "Criar Conta a Pagar/Receber", "Dar Baixa em Conta", "Emitir NF-e (Produto)", "Emitir NFS-e (Serviço)", "Ver saldos de cliente/fornecedor"; tela inicial automática; sem foto; ativa; role `operator` |
| Estado final (para o T3 em diante) | os três usuários ativos, Rafael master; selo "3 / 3 usuários" |

## Gravação
- **Rotas:** `/dashboard`, `/configuracoes?tab=users`. Tudo no computador, um usuário só (Rafael). Sem celular, sem
  página pública, sem login de outro usuário.
- **Sementes:** `inicio` (só o Rafael; caps 0 a 3), `apos-cap03` (+ Marcos com o "Operador Padrão"; cap04),
  `apos-cap04` (+ Juliana; cap05), `apos-cap05` (Marcos ajustado, com foto; caps 6 a 10). Os caps 6 a 9 terminam no
  mesmo estado em que começam (ativa de novo, cancela, cancela, cancela).
- **Setup fora do vídeo:** cap03 reabre "Criar Usuário" e preenche nome, e-mail e senha do Marcos (continuação do cap02).
- **Edge functions a simular:** `create-company-user` (auth, `profiles.company_id`, `user_roles` operator,
  `user_permissions`; resposta igual à real, `{success, user:{id,email,full_name}}`); `manage-company-users`
  (`update_email` com o mesmo e-mail devolve 200; `delete_user` não é chamado); `change-subscription` não é chamado.
- **RPCs:** `save_user_permissions` (cap05); `transfer_company_master` não é chamado.
- **Tabelas:** `profiles` (update de `full_name`, `initial_screen_path`, `avatar_url`, `is_active`), `user_permissions`,
  `user_roles`, `active_sessions` (a do Rafael, para "Online agora"), contagem de `profiles` ativos, `companies`.
- **Storage:** bucket `avatars` (upload + `getPublicUrl`) para a foto do Marcos.
- **Arquivo:** `marcos-antunes.jpg`, 512×512, avatar desenhado por código no estilo da marca (sem rosto real, sem logo).
- **Câmera:** sem zoom no bloco do Cato (fim da lista: fica para o T21), sem zoom nos valores em R$ da janela do limite.
- **Ilustrações** (desenho por código ou cena HTML, `docs/09-aula-ilustrada.md`): cap00 a equipe e as portas de cada
  um; cap01 as abas e as chaves; cap03 os três chaveiros; cap04 a porta e os botões, e as duas travas; cap06 desativar ×
  excluir; cap07 a coroa e o escudo; cap08 as vagas do plano; cap09 o que some × o que fica.

## Riscos e decisões para o Kaik
1. **`max_users` 3** para o cap08 abrir a janela "Sua equipe cresceu! 🎉". Se outra aula precisar de um quarto usuário,
   subir para 5 e o cap08 fica só no selo "3 / 5 usuários" e na fala.
2. A janela do limite mostra o preço do usuário extra e a mensalidade estimada (a fala não diz valor; a câmera não dá
   zoom neles). Alternativa sem preço na tela: não abrir a janela.
3. Foto e tela inicial vão pelo "Editar" porque na criação elas não gravam (inventário, achado 1).
