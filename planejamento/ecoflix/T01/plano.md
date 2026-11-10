# Plano · T1 · Sua conta e sua empresa

- **Título final:** Sua conta e sua empresa (o da fonte).
- **Áreas das vinhetas:** CONTA · ACESSO · EMPRESA · PEDIDOS · COMPROVANTE · USABILIDADE · PAGAMENTO · APARÊNCIA ·
  SEGURANÇA · RESUMO.
- **Objetivo (uma frase):** criar a conta da Recicla Vale Metais, entrar no sistema e deixar o EcoSistema com a cara dela:
  logo, CNPJ, contato, endereço, número do pedido, frase do comprovante, preferências do pátio e a condição 30/60/90.
- **Pré-requisito:** T0. Cartão "Antes: Bem-vindo ao EcoSistema".
- **Próximo:** T2. Cartão "Próximo: Usuários e permissões".
- **Duração:** alvo da fonte ~18 min; a fala natural dá ~15 min de voz (2.351 palavras, ver `roteiro.md`), ~17 min de
  vídeo com as 13 vinhetas e o tempo das ações.
- **Base:** `T01/inventario.md` (código 1.59.154). App no tema claro, desktop (janela 1280×800, como na Domiflix).
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` em todos os capítulos (os exemplos do "Formato do número" saem com 11/26).
- 🔒: só o White Label, como menção (a aula inteira é a T27). Nada de preço de plano.

## Capítulos (os 12 da fonte, na ordem; cap00 abertura e cap13 recapitulando)

| # | Vinheta (área / título) | O que a tela mostra | Estado de partida | Duração |
|---|---|---|---|---|
| 0 | (sem vinheta) | [ILUSTRAÇÃO: comprovante sem e com a identidade da empresa]; `/cadastro` sem login. | sem sessão | 0:35 |
| 1 | CONTA / Criar a conta | `/cadastro`: "Dados" (nome da empresa, responsável, e-mail, telefone), "Continuar", "Acesso" (senha e confirmação), "Criar Conta" → toast. | sem sessão | 1:30 |
| 2 | CONTA / Os 7 dias de teste | Etapa "Acesso" de novo: cartão "Teste Grátis · Acesso Total"; [ILUSTRAÇÃO: os 7 dias]; zoom no "Teste grátis por 7 dias". | sem sessão; o `setup` passa da etapa "Dados" fora do vídeo | 1:00 |
| 3 | ACESSO / Entrar no sistema | `/login`: e-mail, senha, "Lembrar de mim", "Entrar com Google" (sem clicar), "Entrar"; card com o nome, menu, trocador ("Adicionar conta"); [ILUSTRAÇÃO: contas salvas no computador do escritório]. | sem sessão; semente `inicio` | 1:15 |
| 4 | ACESSO / Esqueci minha senha | "Esqueci minha senha" → "Enviar Código" → [ILUSTRAÇÃO: o código pelo e-mail] → 6 casas → "Verificar" → "Nova Senha" → "Alterar Senha e Entrar". | sem sessão; semente `inicio` | 1:10 |
| 5 | EMPRESA / Logo, ícone, nome e CNPJ | Rodapé do menu → "Configurações"; tour das abas; "Identidade Visual": logo, ícone, White Label (menção), nome, CNPJ; [ILUSTRAÇÃO: para onde vão os dados]. | logado; semente `inicio` | 2:00 |
| 6 | EMPRESA / Contato e endereço | "Informações de Contato" (troca o e-mail); "Exibir nos documentos" + [ILUSTRAÇÃO: cadastrado × impresso]; CEP → endereço; "Prévia no comprovante" sem o complemento. | `apos-cap05` | 1:50 |
| 7 | PEDIDOS / Numeração de pedidos | "Reinício da numeração", "Formato do número" (Barras, Zeros, volta ao Padrão), "Numeração separada para compras e vendas" (abre e cancela); 2 ilustrações. | `apos-cap06` | 1:45 |
| 8 | COMPROVANTE / A frase do comprovante | "Frase Personalizada" + "No comprovante", "Alinhar à esquerda"; [ILUSTRAÇÃO: o comprovante]; "Salvar alterações". | `apos-cap06` | 1:00 |
| 9 | USABILIDADE / O jeito do pátio | Inverter os termos (🚫), "Multi-Caixas", "Formato do Comprovante", "Forma de Pagamento Padrão", "Arredondar Pagamentos", "Impureza/Tara Desconta no Valor" (⚠️), "Lucro no Comprovante", "Exigir cliente/fornecedor no Ticket de Pesagem"; 2 ilustrações. Só mostra, não muda. | `apos-cap08` | 2:40 |
| 10 | PAGAMENTO / Condições de pagamento | "Nova condição" → "30/60/90 dias", "Definir como condição padrão", desmarca "À vista", 3 parcelas, "Soma dos percentuais" 100% → "Criar condição"; [ILUSTRAÇÃO: 30/60/90]. | `apos-cap08` | 1:40 |
| 11 | APARÊNCIA / Aparência e atalhos | "Menu Superior" e volta, "Menu (lateral e superior)", "Tema Escuro" e volta; "Atalhos"; Ctrl+K e a busca "cobre". | `apos-cap10` | 1:20 |
| 12 | SEGURANÇA / Senha, termos e Zona de Perigo | "Alterar Senha" (abre e cancela), "Ver Contrato" ("Aceito em", "Baixar PDF", "Fechar"), "Zona de Perigo" → "Zerar Sistema" → "Sim, continuar" → janela mostrada com calma → "Cancelar". | `apos-cap10` | 1:30 |
| 13 | RESUMO / Recapitulando | Montagem dos trechos; "Próximo: Usuários e permissões". | (reaproveita) | 0:50 |

Transições faladas: 0→1 "Vamos criar a conta"; 1→2 "Lembra desse cartão"; 2→3 "Conta criada, agora é entrar"; 3→4 "E se
um dia você esquecer a senha?"; 4→5 "Agora, os dados da empresa"; 5→6 "Logo abaixo ficam o contato e o endereço"; 6→7 "Cada
compra e cada venda ganha um número"; 7→8 "Agora, a frase do comprovante"; 8→9 "Agora, a aba Usabilidade"; 9→10 "as
Condições de Pagamento"; 10→11 "Na aba Aparência"; 11→12 "Pra fechar, a parte de baixo da aba Empresa".

**Cuidados da fonte na fala**

| Marca | Fala (resumo) | Na tela |
|---|---|---|
| ⚠️ CNPJ fora do cadastro | cap01 "Repara que não tem CNPJ aqui"; cap05 "Uma dica: ele não é pedido no cadastro, ele entra aqui. E vai na nota fiscal da assinatura" | zoom no CNPJ |
| ⚠️ Impureza e tara | cap09 "Uma dica: a impureza e a tara sempre descontam do peso que entra ou sai do estoque. Essa chave decide só se descontam também do valor pago" + as duas situações com o Valdir | ilustração |
| ⚠️ Prefixo do material | não está nesta aba na 1.59.154 (fica no cadastro do material): vai para o T3 | (nada) |
| ⚠️ Teste com mais dias | cap02 "Uma dica: se você entrou por um link do nosso comercial, o teste pode ter mais dias. O que vale é o que está escrito aqui em cima" | zoom no subtítulo |
| ⚠️ Zerar Sistema | cap12 mostrado devagar; "Uma dica: zerar não tem volta"; "Aqui a gente só olhou" | zoom no aviso e no nome |
| 🚫 Inverter os termos | cap09 "troca as palavras na tela. O cadastro, o saldo e a nota fiscal continuam iguais" | chave desligada |
| 🔒 White Label | cap05 "Ele depende do plano contratado, e tem um tutorial só dele" | cartão recolhido |

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)

**Identidade da empresa** (é o que o resto da trilha herda; o T1 a preenche na tela):

| Campo | Valor (fictício) |
|---|---|
| `companies.name` | Recicla Vale Metais (a razão social "Recicla Vale Metais Ltda" fica para a configuração fiscal do T16) |
| CNPJ (matriz) | **47.318.506/0001-07** (dígitos conferidos); sugestão para a filial do T22: 47.318.506/0002-98 |
| Telefone | (12) 90000-4410 (o do cadastro; formato do mundo) |
| E-mail de contato | contato@reciclavalemetais.example (o cap06 troca o e-mail do cadastro por este) |
| Login do Rafael | rafael@reciclavalemetais.example; senha do mundo `ReciclaVale#26`; nova senha do cap04 `PatioTaubate#26` (só no cap04) |
| Endereço | CEP 12086-410, Rua das Oficinas, 1250, Galpão 2, Jardim Vale do Sol, Taubaté/SP, IBGE 3554102; fuso America/Sao_Paulo; na prévia, sem o complemento (`address_visibility_settings.complemento = false`) |
| Logo e ícone | `recicla-vale-logo.png` (horizontal, ~600×240, fundo transparente) e `recicla-vale-icone.png` (1:1, 128×128): marca fictícia (símbolo próprio + "Recicla Vale Metais"), sem lembrar o símbolo de reciclagem do EcoSistema nem marca real |
| Frase do comprovante | "Obrigado pela parceria! Atendemos de segunda a sexta, das 7h às 17h." (68 caracteres; junção: sem sábado, como o histórico), "No comprovante" ligado, centralizada |
| Numeração | padrão: "Nenhum (segue direto)", "#{NUM}", contagem única (o T1 mostra as opções e volta ao padrão) |
| Condição de pagamento | "30/60/90 dias", padrão, ativa: 30 dias 33,33%, 60 dias 33,33%, 90 dias 33,34% |
| Usabilidade (sem mudança) | "Multi-Caixas" ligado; cofre ligado; "Formato do Comprovante" Térmico nos dois; "Forma de Pagamento Padrão" "Perguntar sempre"; "Permitir Edição de Itens" e "Múltiplas Tabelas de Preço" ligados; arredondar desligado; "Impureza/Tara Desconta no Valor" ligado; "Lucro no Comprovante" desligado; "Exigir cliente/fornecedor no Ticket de Pesagem" desligado; termos não invertidos |
| Termos | `profiles.terms_accepted_at` do Rafael = 03/08/2026 08:47:12 (a conta "nasceu" no começo do histórico; a fala não lê a data) |
| OTP do cap04 | 481207 |

**Exemplos falados** (com os preços do mundo): Dona Cida, 37 kg de alumínio latinha a R$ 6,20 = R$ 229,40 (arredondado: recebe
R$ 229,00, R$ 0,40 de saldo a pagar); Valdir, 200 kg de ferro misto com 10 kg de terra a R$ 0,75: chave ligada R$ 142,50 (190 kg),
desligada R$ 150,00 (200 kg), estoque 190 kg nos dois; Fundição Bandeira do Vale paga cobre em 30/60/90.

**Sementes:** `inicio` = mundo base com a empresa **como sai de um cadastro novo** (nome, e-mail do Rafael e telefone;
sem CNPJ, endereço, logo, ícone, frase nem condição de pagamento), o resto do mundo como está; `apos-cap05` (+ logo, ícone,
CNPJ); `apos-cap06` (+ e-mail de contato, endereço, prévia sem complemento; serve ao 7 e ao 8); `apos-cap08` (+ frase;
serve ao 9 e ao 10); `apos-cap10` (+ condição 30/60/90; serve ao 11 e ao 12). O estado final (`apos-cap12` = `apos-cap10`) é a
identidade da empresa que todas as outras aulas usam: consolidar no `MUNDO_FICTICIO.md` e nas sementes base.

## Gravação

- **Páginas públicas, sem sessão** (caps 0 a 4): `/cadastro` e `/login`. O navegador começa sem nada no `localStorage`
  (sem `rememberedEmail`, sem sessões salvas). Câmera no formulário: o painel da direita do login (`LoginShowcase`) só no plano
  geral, sem ler "5,0 no Google"; não clicar no botão flutuante do WhatsApp do cadastro.
- **Edges e auth a simular** (detalhes na coluna Tela):
  1. `self-register`: `check_email_only` → `{available: true}`; cadastro → `{success: true, requires_payment: false}` sem criar
     empresa (ela já existe); o login automático que vem logo depois usa o e-mail e a senha do Rafael. O cap01 corta no toast.
  2. `password-reset` `{action: 'send'}` → sucesso sem e-mail; `auth.verifyOtp` (`recovery`) aceita 481207; `auth.updateUser` aceita.
  3. `cep-lookup` (12086410 → Rua das Oficinas, Jardim Vale do Sol, Taubaté, SP, `codigoIbge` 3554102); `geocode-company` e
     `sync-asaas-customer` sem efeito (esta só é chamada se a empresa do mundo tiver `asaas_customer_id`).
  4. `fetch` direto do navegador para `servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios`: responder por fixture
     (a lista de SP do próprio IBGE, salva uma vez; tem de trazer Taubaté 3554102 e Pindamonhangaba, para o T22).
  5. Storage `avatars`: upload e URL pública dos dois PNGs (o logo tem de aparecer na tela).
  6. Tabelas: `companies` (update com auto-save), `company_fiscal_config` (insert/update), `payment_conditions` (insert),
     `profiles` (preferências, `navigation_style`, `terms_accepted_at`), `active_sessions` sem acesso na última hora (para não
     abrir a janela "Você já está conectado em outro lugar"), `biometric_credentials` vazia.
- **Chegada no sistema limpa** (caps 3 a 12): sem a janela "Personalize sua experiência", sem o aceite de termos, sem lembrete
  da EcoFlix, sem aviso de versão nova, sem NPS. O trocador de contas do cap03 precisa do login pelo formulário (é ele que
  salva a sessão); não injetar sessão nesse capítulo.
- **Nada destrutivo:** "Zerar Sistema" só aberto e cancelado (RPCs `reset_company_*` nunca chamadas); "Alterar Senha" (logado)
  abre e cancela; "Numeração separada" abre e cancela; nenhuma chave da Usabilidade muda.
- **Arquivos do `public/`:** a cópia 1.59.154 só tem `src/` (sem `public/`): o painel do login usa `/guia-tecnico/img/t6-caixa.jpg`,
  `/guia-tecnico/img/t9-pedidos.jpg` e `/images/Logo 3D EcoSistema.png`. Copiar o `public/` do commit `f37573ea0` no
  `setup-app`, ou a imagem sai quebrada no plano geral.
- **Ilustrações** (cenas HTML no estilo da marca, `docs/09-aula-ilustrada.md`; nenhuma imita tela do app): cap00 comprovante sem
  e com identidade; cap02 os 7 dias; cap03 contas salvas no computador; cap04 o código pelo e-mail (caixa genérica, sem marca de
  provedor); cap05 para onde vão os dados; cap06 cadastrado × impresso; cap07 reinício da numeração e contagem única × separada;
  cap08 o comprovante com a frase (cupom genérico desenhado); cap09 arredondar (Dona Cida) e impureza/tara (Valdir); cap10 30/60/90.
- Celular, outro usuário, cena de Windows: não há.

## Riscos e decisões para o Kaik

1. **Usabilidade só mostrada:** mudar forma de pagamento, arredondar, lucro ou exigir parceiro no ticket mudaria o que T7 e T8
   esperam. Se ele quiser uma ação de verdade ali, a mais segura é ligar "Exigir cliente/fornecedor no Ticket de Pesagem" (o T8
   acompanha).
2. **Numeração no padrão:** o T1 mostra os modelos e volta ao "Padrão", para os números de pedido das outras aulas não mudarem.
3. **Opções de pedido por usuário** (inventário, divergência 6): a fala avisa que ficam no usuário do Rafael. Handoff: a tela
   não diz isso, e quem não tem a permissão da aba não ajusta as suas.
4. **Biometria fora da fala** (sem tela de cadastro na 1.59.154) e **sem "aviso fixo"** de cadastro incompleto (não existe).
5. **Cadastro "de mentira":** o cap01 preenche e envia o cadastro, mas a empresa do mundo já existe (com histórico desde agosto);
   o vídeo corta no toast, antes do painel.
