# Plano · T5 Balança e impressora: o EcoTray

- **Título:** Balança e impressora: o EcoTray (fonte). 🔒 só a parte da balança (módulo `balanca_integration`).
- **Antes:** T4 "Clientes, fornecedores e a ficha do parceiro". **Próximo:** T6 "Caixa: abrir, fechar e o cofre"
  ("abrir o caixa e começar o dia").
- **Objetivo:** instalar o EcoTray no computador do escritório da Recicla Vale Metais, ligar a impressora de cupom (58 mm)
  e a balança do pátio, e saber ler o rodapé e o que fazer quando o EcoTray fecha ou o driver da impressora é o errado.
- **Duração:** alvo da fonte 13 min; fala ~1.625 palavras (~10,4 min) + 11 vinhetas, cenas de Windows e ilustrações ≈ 12 min.
- **Base:** `T05/inventario.md` (código 1.59.154 e EcoTray 1.7.22). Computador 1280×800, logado como **Rafael Nogueira**
  (MASTER). `FAKE_NOW=2026-11-10T08:30:00-03:00` em todos os capítulos.

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área / título) | O que se mostra | Duração |
|---|---|---|---|
| 0 | (sem vinheta) | Dashboard; ilustração do peso digitado errado (312 → 321) e do PDF; cartões "Antes" e o aviso do plano | 0:35 |
| 1 | ECOTRAY / O que é o EcoTray | Configurações › "Integrações"; ilustração da ponte (balança → EcoTray → sistema → impressora); selo "EcoTray não detectado nesta estação"; tour | 1:15 |
| 2 | INSTALAÇÃO / Baixar e instalar | "Baixar Instalador" › "Windows"; cenas de Windows: aviso do navegador ("Manter"), SmartScreen ("Mais informações", "Executar assim mesmo"), instalador, painel e bandeja; Mac falado | 1:50 |
| 3 | CONEXÃO / O pareamento automático | selo "v1.7.22"; ilustração do pareamento dentro do mesmo computador | 0:50 |
| 4 | IMPRESSORA / Conectar a impressora | "Integração com Impressora" → "Conectado ao EcoTray"; "POS-58"; "Testar"; cena: "✓  Impresso em POS-58"; ilustração do cupom de teste | 1:05 |
| 5 | IMPRESSORA / Largura do papel e impressão turbo | "Ajustar Escala" › "58 mm", "Testar impressão", "Salvar"; ilustração do cupom cortado; "Impressão térmica turbo (beta)" | 1:15 |
| 6 | BALANÇA / Conectar a balança | 🔒 dito; "Integração com Balança Digital"; cenas: painel destrava, "Configurar Balanças" › "Adicionar" ("Balança do pátio", "COM3  ✓ balança", "Automático") › "Gravar"; "Peso atual: 18,600 kg"; unidade, casas, "Leitura contínua" (ilustração) | 2:00 |
| 7 | BALANÇA / Peso somente pela balança | a chave e a dica; ilustração do peso com cadeado; quando ligar (fica desligada) | 0:50 |
| 8 | BALANÇA / O indicador de peso | rodapé: "Balança do pátio · Aguardando peso" → "Balança do pátio · 312 kg"; ilustração computador × celular | 0:55 |
| 9 | CONEXÃO / Quando o EcoTray cai | cena: bandeja › "Sair"; "Balança desconectada"; ilustração do PDF e do peso digitado; "EcoTray não encontrado"; cena: atalho "EcoTray"; reconexão sozinha | 1:15 |
| 10 | IMPRESSORA / Driver incompatível | lista com "Generic / Text Only" (triângulo); caixa "Driver incompatível"; ilustração do driver; volta à "POS-58"; a folha em branco sem aviso | 1:05 |
| 11 | RESUMO / Recapitulando | montagem; cartão "Próximo: Caixa: abrir, fechar e o cofre" | 0:40 |

Avisos da fonte e onde entram: navegador e SmartScreen (cap. 2, "Uma dica:" e os dois cliques mostrados); cupom cortado é
largura (cap. 5, "Uma dica:"); chave da balança nasce desligada e a empresa em teste já tem a balança (cap. 6, "Uma
dica:"); 🔒 dito no cap. 0 e no cap. 6, com o cartão de contratação e o "Pesar automático" só falados; indicador (cap. 8,
"Uma dica:", ver decisão 1); regra dura do EcoTray fechado (cap. 9, com o caso da trava de peso); checagem de driver só
pelo nome (cap. 10, "Uma dica:").

## Estado de partida (fim do T4)
Mundo base da Recicla Vale Metais. Sem EcoTray no computador (EcoTray falso desligado). Perfil do Rafael:
`direct_print_enabled` false, `direct_print_printer_name` vazio, `receipt_paper_width_mm` 80, `receipt_scale` 100,
`thermal_print_mode` 'pdf', `balanca_ativada` false, `balanca_unidade` 'kg', `balanca_decimais` 3, `balanca_continua`
false. Empresa: `scale_weight_lock_enabled` false; módulo `balanca_integration` ativo (contratado, sem teste).

## Mundo: o que esta aula precisa
| Item | Valores (fictícios) |
|---|---|
| Computador | o do escritório da balança, Windows; relógio da cena = o do app (10/11/2026, 08:3x) |
| EcoTray | v1.7.22 (`app_config.ecotray_version` = "1.7.22", a mesma: o selo fica "v1.7.22", sem aviso de atualização) |
| Impressora | **POS-58**, térmica de cupom 58 mm, USB, driver do fabricante (compatível); a única do computador até o cap. 9 |
| Impressora do cap. 10 | **Generic / Text Only** (driver "Generic / Text Only", incompatível), instalada "depois", só nesse capítulo |
| Porta da balança | **COM3** (cabo USB-serial), 9600, 8 bits, sem paridade, 1 stop; a detecção marca "COM3  ✓ balança" |
| Balança | **Balança do pátio** (plataforma), cadastrada no cap. 6, protocolo "Automático", padrão |
| Pesos | saco de latinha da Dona Cida **18,6 kg** (cap. 6); carroça de ferro do Valdir **312 kg** (cap. 7 a 9; o 321 do cap. 0 é o erro de digitação da ilustração) |
| Criado na tela | impressão direta ligada com "POS-58"; papel **58 mm**, escala 100%; turbo desligado; balança ligada (kg, 3 casas, leitura contínua desligada); "Peso somente pela balança" desligado |

**Fica para as próximas:** essas chaves são **por usuário** (`profiles`): o Rafael termina com impressora e balança
ligadas; se T6 a T10 gravarem com o Marcos, a semente dele precisa das mesmas. O EcoTray falso segue com a "Balança do
pátio" e a "POS-58" (o T7 e o T8 usam). A trava de peso fica desligada (o T7 digita peso à mão no modo sem internet).

## Gravação
- **Rotas:** `/dashboard`, `/configuracoes?tab=integrations`.
- **Banco e RPC:** `app_config` (leitura); `profiles` (leitura e gravação das chaves); `companies.scale_weight_lock_enabled`
  (leitura; a RPC `set_company_scale_weight_lock` não é chamada); módulos da empresa.
- **EcoTray falso** (o navegador fala com ele; o resto é cena): `ws://127.0.0.1:8054` responde `get_status`
  (`version` "1.7.22", `printers`, `printers_meta`, `default_printer`, `scales_lock_state`), `list_printers` (`data`,
  `data_meta`), `print` e `print_image` (`print_result` success; também `print_notification` e `activity` para a cena),
  `unlock_scales` (`unlock_result` unlocked, sem chamar a edge `verify-balanca-module`); `ws://127.0.0.1:8053` manda
  `scale_lock_status`, `scales_list` e `weight`. Estados por capítulo, trocados por bastidor (`/__dev` ou semente):
  desligado (cap. 0 a 2 e meio do 9); ligado sem balança cadastrada (3 a 5); com a "Balança do pátio" (a partir do
  meio do 6); peso 0 → 18,6 (6); sem peso, depois 0 → 312 (8); 312 (9); duas impressoras (10).
- **Download:** o "Windows" abre `bridge-downloads/EcoTray - Instalador.exe` numa aba nova; a aba não entra no vídeo (a
  cena cobre).
- **Cenas de Windows** (outro agente; textos, cores, fonte e medidas do código: `T05/inventario.md` §4): área de trabalho
  genérica no estilo Windows, sem logo nem ícones da Microsoft, com a barra de tarefas, a bandeja perto do relógio e a
  janela de navegador com a gravação do app. Oito momentos: 1 aviso do download ("Manter"); 2 SmartScreen ("Mais
  informações", "Executar assim mesmo"); 3 instalador (de "Pronto para instalar" a "✓  Instalado com sucesso!"); 4 painel
  e aviso "✓  Impresso em POS-58"; 5 painel destravando a balança; 6 "Configurar Balanças" e "Nova balança"; 7 menu da
  bandeja › "Sair"; 8 atalho "EcoTray" na área de trabalho. O painel é "sempre por cima": fica à direita, sobre o
  navegador, quando aparece. Textos do navegador e do Windows: os que o próprio app cita ("pode ser perigoso",
  "Manter", "Mais informações", "Executar assim mesmo") e o padrão do SmartScreen em português (decisão 3).
- **Ilustrações** (estilo da marca, `docs/09-aula-ilustrada.md`): o peso digitado errado e o PDF (cap. 0); a ponte do
  EcoTray (1); o pareamento dentro do computador (3); o cupom de teste (4); a largura do papel (5); a leitura contínua
  (6); o peso só pela balança (7); computador × celular (8); sem EcoTray: PDF e peso digitado (9); o driver (10).
- **Celular:** nenhum (decisão 1).

## Riscos e decisões para o Kaik
1. **Indicador no celular:** a fonte pede gravar no celular, mas na 1.59.154 o indicador só existe no computador (tela
   ≥ 1024 px: `AppLayout.tsx:512`, `useBalancaHabilitada.ts`); balança e impressão direta ficam desligadas no celular.
   Proposta: sem trecho de celular; a fala diz que o indicador fica no computador do EcoTray, com ilustração.
2. **Preço:** o cartão de contratação da balança mostra o preço; não é gravado. A fala cita o cartão e o "Pesar
   automático".
3. **Telas que não são do EcoTray:** o aviso do navegador e o SmartScreen variam com a versão; a cena usa um aviso genérico
   de navegador com os textos que o app ensina e o SmartScreen padrão em português, sem logo.
4. **Papel de 58 mm** para a Recicla Vale (dá ação ao capítulo 5 e encaixa a dica do cupom cortado). Alternativa: 80 mm, e
   o capítulo só mostra a escolha.
5. **Trava de peso, leitura contínua e turbo** mostrados e deixados desligados, para não mudar o T7.
6. **Mac** só falado (instalador `.dmg`, "Instalar", barra de menus).

## Handoffs (a fala não depende deles)
- H1 "Guia de Instalação" fala em ZIP e "Instalar EcoTray.cmd"; o download é um `.exe` (`EcoTrayGuideModal.tsx:22`).
- H2 O "● N cliente(s)" do painel conta as conexões da própria janela: sem navegador já mostra "1 cliente(s)".
- H3 O cartão "Parcialmente ativo"/"Conectado e operando" e a faixa colorida do painel ficam como estavam quando a janela
  abriu (`dashboard.py:212,356-357,477-488`): depois de ligar a balança, só mudam ao fechar e reabrir.
- H4 A fonte diz "o EcoTray acha o sistema sozinho"; no código é o navegador que procura o EcoTray no próprio computador.
- H5 A regra dura da fonte ("o peso é digitado à mão") só vale com "Peso somente pela balança" desligado: ligado, o campo
  de peso fica travado mesmo sem o EcoTray (`InputPesoBalanca.tsx:69,262`).
