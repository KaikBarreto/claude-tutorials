# Plano · T2 Usuários e permissões (EcoSistema 1.60.18)

- **Título:** Usuários e permissões (o da fonte).
- **Objetivo:** colocar a equipe da Recicla Vale Metais no sistema com o acesso certo: criar o Marcos (com foto) e a Juliana, usar
  os perfis rápidos e o Personalizado, montar um acesso na mão, conhecer as restrições e o mapa de todas as permissões, desativar e
  excluir, entender o master, o limite do plano, as permissões de valor e o Relatório por Usuário.
- **Antes:** T1 "Sua conta e sua empresa". **Próximo:** T3 "Materiais e tabelas de preço".
- **Vinhetas (áreas):** USUÁRIOS · USUÁRIOS · PERMISSÕES · PERMISSÕES · PERMISSÕES · PERMISSÕES · PERMISSÕES · USUÁRIOS · MASTER · PLANO · VALORES · USUÁRIOS · RESUMO.
- **Alvo:** ~19 min (14 capítulos; a fonte tinha 13 min; a aula pode ficar mais longa por pedido do Kaik, 18/11). Desktop 1600×900,
  logado como Rafael Nogueira (master). Base: `T02/inventario.md`, `T02/cobertura_160.md`.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça), igual ao mundo.
- **Mudanças da aplicação 1.60.18:** capítulos novos 06 (Restrições e contas do banco), 07 (O mapa das permissões) e 12 (Relatório
  por Usuário); os antigos 06 a 09 viraram 08 a 11 e o antigo 10 (Recapitulando) virou 13. Fala de 1.483 para 2.313 palavras.

## Estado de partida (fim do T1)
Recicla Vale Metais com um usuário só: Rafael Nogueira, master (`user_roles` `company_admin`, `permission_preset`
`full_access`, como o `create-company` grava). Assinatura ativa, plano `personalizado`, todos os módulos da trilha,
**`max_users` 3**. Nenhuma foto de usuário.

## Capítulos
| # | Vinheta (área · título) | O que a tela mostra | Cuidados na fala | Origem |
|---|---|---|---|---|
| 0 | (sem vinheta) | Dashboard → rodapé do menu "Configurações" → aba "Usuários e Permissões". Ilustração da equipe. | "Antes: Sua conta e sua empresa" | abertura |
| 1 | USUÁRIOS · Onde fica | Cabeçalho da aba, "Empresa: Recicla Vale Metais", selo "1 / 3 usuários", "Criar Usuário", busca "Buscar por nome ou e-mail"; lista com o Rafael (coroa); detalhe "Master", "Perfil de acesso", "Última atividade" ("Online agora"), "Peso dos pedidos". Ilustração: cada aba tem a sua chave. | a aba aparece com a permissão "Gerenciar Usuários" | fonte, com busca e coluna nova (L10, L14) |
| 2 | USUÁRIOS · Criar o usuário | "Criar Usuário" → nome, "Email", "Senha" com "Senha forte"; **foto escolhida na criação** (1.60.18: grava); aviso âmbar "Escolha primeiro o perfil deste usuário". | e-mail só em uma empresa; a foto já grava na criação | P1 |
| 3 | PERMISSÕES · Os perfis rápidos | Aviso e lista apagada; "Acesso Total", "Somente Visualização", "Operador Padrão" (selo "Recomendado"; fica este) e "Personalizado"; "Criar Usuário" → "Usuário criado com sucesso!"; selo "2 / 3 usuários"; detalhe do Marcos "Operador Padrão". Ilustração: chaveiros (o quarto, vazio, é o Personalizado). | o perfil é só um ponto de partida | P2 |
| 4 | PERMISSÕES · Telas e ações | Juliana: clica em "Personalizado" (a lista acende); tela "Contas a Pagar/Receber" e as ações ("2/4"); **"Registrar Venda" sem "Caixa" acende "Confira esta combinação"**; busca "nota"; resto do escritório; "Criar Usuário". Ilustrações: a porta e as ações; as duas travas. | 🔒 plano e servidor mandam mais | P3 |
| 5 | PERMISSÕES · O balanceiro e o escritório | Marcos → "Editar": foto trocada, "Tela inicial" "Caixa", ajuda da tela inicial, **"Peso dos pedidos"** (abre e fecha), "Nova Senha", desliga "Ver Projeção de Lucro" ("Personalizado"), "Atualizar". Juliana: "Telas (7)", "Ações (8)". | o Marcos precisa entrar de novo | P5 |
| 6 | PERMISSÕES · Restrições e contas do banco | **Novo.** Editar do Marcos até o fim da lista: "Restrições" (4 chaves); a quarta abre "Contas liberadas para este usuário" ("Conta Principal"); "Cancelar". Ilustração: comprador que só vê os próprios. | só mostrar e cancelar; restrição tira o Cato e não combina com Acesso Total | P4 |
| 7 | PERMISSÕES · O mapa das permissões | **Novo.** Passeio pela lista do Editar do Marcos, abrindo as ações de Caixa, banco, Fiscal (11), Materiais, Cadastros e Sistema; "Cancelar". Ilustração: mapa de quatro bairros. | só mostrar e cancelar; as ações novas só valem no Cato (T21) | P6 |
| 8 | USUÁRIOS · Desativar ou excluir | (era 06) Menu "..." do Marcos: "Desativar", "Ativar", "Excluir" → "Cancelar". | desativado não conta no limite; excluir não tem volta | fonte |
| 9 | MASTER · Passar o controle | (era 07) "Tornar master" → "Passar o controle da empresa?" → "Cancelar". | ⚠️ quem passa o bastão perde a proteção | fonte |
| 10 | PLANO · O limite de usuários | (era 08) Selo "3 / 3 usuários"; "Sua equipe cresceu! 🎉" → "Cancelar". **Frase nova:** o plano diminuiu e a janela "Limite de Usuários Excedido" pede quem desativar (só fala e ilustração). | 🔒 depende do plano; preço nunca falado | fonte + P8 |
| 11 | VALORES · Esconder o valor | (era 09) "Ver Totais e Valores Financeiros", "Caixa", "Ticket de Pesagem" → "Cancelar". | ⚠️ esconder valor não trava a operação | fonte |
| 12 | USUÁRIOS · Relatório por Usuário | **Novo.** Botão "Relatório por Usuário": "Período", "Usuários incluídos", "Excel", "Visualizar / PDF" (o relatório abre em outra aba). Ilustração tipo comprovante: o relatório. | nenhum valor falado | P7 |
| 13 | RESUMO · Recapitulando | (era 10) Montagem: Marcos e Juliana na lista, os perfis, o editar, restrições e mapa, o selo "3 / 3", o relatório. "Próximo: Materiais e tabelas de preço". | "Até lá!" | recap |

Transições faladas: 0→1 "Vamos ver onde fica"; 1→2 "A equipe começa pelo Marcos"; 2→3 "Agora, o que o Marcos vai poder fazer";
3→4 "A Juliana, a gente monta na mão"; 4→5 "Os dois casos do pátio"; 5→6 "Até aqui a gente liberou coisas"; 6→7 "Antes de
seguir, vale um passeio pela lista"; 7→8 "E quando alguém sai de férias?"; 8→9 "E o master?"; 9→10 "Agora o tamanho da equipe"; 10→11
"Pra fechar, os valores"; 11→12 "Ainda nesta aba tem um botão".

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)
| Item | Valor |
|---|---|
| Plano da empresa | `companies.subscription_plan` `personalizado`, **`max_users` 3** (Rafael, Juliana e Marcos: no fim do T2 a empresa fica em 3/3, e o cap10 mostra a janela de usuário extra) |
| Nome na aba | `companies.name` "Recicla Vale Metais" (a linha "Empresa: ...") |
| E-mails | `rafael@reciclavalemetais.example` (o do T1; junção), `marcos.antunes@reciclavalemetais.example`, `juliana.prado@reciclavalemetais.example` |
| Senhas (digitadas, nunca faladas) | Marcos `Balanca#2026`, Juliana `Escritorio#2026` (as duas dão "Senha forte") |
| Marcos Antunes (criado no cap02-03, ajustado no cap05) | criado com "Operador Padrão" (32 permissões, `permission_preset` `standard_operator`) e a foto (1.60.18: grava na criação; avatar desenhado, sem rosto real); depois do cap05, sem "Ver Projeção de Lucro" = 31 permissões, `permission_preset` nulo ("Personalizado"), tela inicial `/caixa`; ativo; role `operator`; sem restrição, sem conta liberada, sem exceção de peso |
| Contas bancárias (B) | "Conta Principal" (padrão), "Conta Secundária" e "Poupança antiga" (`kind` `bank`, ativas): os cartões do cap06 |
| Pedidos do mês (B) | compras e vendas de novembro com `created_by` do Marcos e do Rafael: o Relatório por Usuário (cap12) |
| Juliana Prado (criada no cap04, a partir do "Personalizado") | 7 telas: "Dashboard", "Movimentações Bancárias", "Relatório Financeiro", "Contas a Pagar/Receber", "Pedidos", "Fiscal & Ambiental", "Clientes e Fornecedores"; 8 ações: "Ver Totais e Valores Financeiros", "Gerenciar Contas Bancárias", "Conciliar Extrato Bancário", "Criar Conta a Pagar/Receber", "Dar Baixa em Conta", "Emitir NF-e (Produto)", "Emitir NFS-e (Serviço)", "Ver saldos de cliente/fornecedor"; tela inicial automática; sem foto; ativa; role `operator` |
| Estado final (para o T3 em diante) | os três usuários ativos, Rafael master; selo "3 / 3 usuários" |

## Gravação
- **Rotas:** `/dashboard`, `/configuracoes?tab=users`. Tudo no computador 1600×900, um usuário só (Rafael). Sem celular, sem
  página pública, sem login de outro usuário. O relatório do cap12 abre em outra aba (`window.open`): o robô guarda a janela
  (`POPS`) e devolve o relatório (`HTML_JS`) para a ilustração; a gravação fica na aba do sistema.
- **Sementes:** `inicio` (só o Rafael; caps 0 a 3), `apos-cap03` (+ Marcos com o "Operador Padrão" e a foto; cap04),
  `apos-cap04` (+ Juliana; cap05), `apos-cap05` (Marcos ajustado, tela inicial Caixa, sem a projeção de lucro; caps 6 a 13). Os
  caps 6 a 12 terminam no mesmo estado em que começam (cancela, cancela, ativa de novo, cancela, cancela, cancela, só o relatório).
- **Setup fora do vídeo:** cap03 reabre "Criar Usuário" e preenche nome, e-mail, senha e foto do Marcos (continuação do cap02);
  caps 6 e 7 abrem o "Editar" do Marcos; cap12 guarda os `window.open`.
- **Edge functions a simular:** `create-company-user` (1.60.18: corpo com `preset` e `bank_account_ids`; `profiles.company_id` e
  `permission_preset`, `user_roles` operator, `user_permissions`, contas liberadas; resposta `{success, userId, user:{...}}`);
  `manage-company-users` (`update_email` com o mesmo e-mail devolve 200; `delete_user` não é chamado); `change-subscription` não é chamado.
- **RPCs:** `save_user_permissions_and_bank_accounts` (cap05; chama `save_user_permissions` e `set_user_scale_weight_policy`);
  `set_user_scale_weight_policy` (toda criação e todo "Atualizar"); `transfer_company_master` não é chamado.
- **Tabelas:** `profiles` (update de `full_name`, `initial_screen_path`, `avatar_url`, `is_active`, embute
  `user_bank_account_access`), `user_permissions`, `user_roles`, `user_bank_account_access`, `user_scale_weight_policies`,
  `bank_accounts`, `active_sessions` (a do Rafael, para "Online agora"), contagem de `profiles` ativos, `companies`, `sales`,
  `purchases` e itens (relatório).
- **Storage:** bucket `avatars` (upload + `getPublicUrl`) para a foto do Marcos (criação e troca).
- **Arquivo:** `marcos-antunes.jpg`, 512×512, avatar desenhado por código no estilo da marca (sem rosto real, sem logo).
- **Câmera:** sem zoom no bloco do Cato (fim da lista: fica para o T21), sem zoom nos valores em R$ da janela do limite; o bloco
  de contas do cap06 mostra só os nomes das contas, nunca saldos.
- **Ilustrações** (`cenas/ilustracoes.json`, estilo v3 pendente): cap00 a equipe; cap01 as abas e as chaves; cap03 os chaveiros (e
  o quarto, vazio); cap04 a porta e os botões, e as duas travas; cap06 o comprador que só vê os próprios; cap07 o mapa dos
  grupos; cap08 desativar × excluir; cap09 a coroa e o escudo; cap10 as vagas do plano (e o limite excedido); cap11 o que some ×
  o que fica; cap12 o relatório (tipo comprovante).

## Riscos e decisões para o Kaik
1. **`max_users` 3** para o cap10 abrir a janela "Sua equipe cresceu! 🎉". Se outra aula precisar de um quarto usuário,
   subir para 5 e o cap10 fica só no selo "3 / 5 usuários" e na fala.
2. A janela do limite mostra o preço do usuário extra e a mensalidade estimada (a fala não diz valor; a câmera não dá
   zoom neles). Alternativa sem preço na tela: não abrir a janela.
3. **Decididas pelo coordenador (JUNCAO_160):** restrição de contas e "Exigir peso da balança" só mostrados e cancelados (o Marcos
   segue com todas as contas e sem trava de peso); a Juliana segue com 15 permissões (sem as ações novas do banco).
4. A fala do cap07 cita as ações "novas" só como chaves; o detalhe de cada uma fica na aula da tela dela.
