# Inventário · T5 Balança e impressora: o EcoTray

Levantado em 10/11/2026 contra o código gravado (`APP_VERSION = "1.59.154"`, `src/config/version.ts:16`; EcoTray
`APP_VERSION = "1.7.22"`, `ecotray/version.py:98`), cópia em `/home/claude/ecoflix/app-src-1.59.154/`. Caminhos
relativos a `src/`, exceto `ecotray/...`. Rótulo entre aspas = texto exato.

## 1. Configurações › Integrações (`/configuracoes?tab=integrations`)
- Menu: botão "Configurações" (engrenagem) no rodapé do menu lateral, ao lado de "Sair"
  (`components/layout/SidebarMenuContent.tsx:806-820`). Página "Configurações do Sistema" ("Personalize as preferências e
  comportamento do sistema"), abas "Empresa", "Usuários e Permissões", "Usabilidade", "Condições de Pagamento",
  "Aparência", "Integrações", "Atalhos" (`pages/Settings.tsx:36-44`, `i18n/locales/pt-BR/settings.json`). A aba aparece
  com a permissão `action_config_integracoes` (`lib/configTabsPermissions.ts:11`).
- Componente: `components/settings/SettingsIntegrationsContent.tsx`. Cabeçalho "Integrações" ("Configure integrações com
  impressora e balança digital") `:192-197`.
- **Cartão do EcoTray** `:200-260`: logo; selo da versão DA ESTAÇÃO (consultada uma vez, ao abrir a tela):
  "EcoTray não detectado nesta estação" | "v1.7.22" | "EcoTray desatualizado (v…, atual é v…). Feche e abra o EcoTray pra
  atualizar." `:218-236`; "Programa para Windows e macOS que conecta impressora térmica e balança digital ao sistema. Leve
  (~20MB), inicia automaticamente com o computador/notebook e roda em segundo plano." `:238-241`; itens "Impressão direta
  sem abrir PDF no navegador", "Leitura de balança com auto-detecção de porta", "Configurações visuais via bandeja do
  sistema" `:242-246`; botões **"Baixar Instalador"** e "Guia de Instalação" `:249-256`.
- **Impressora** `:265-585`: título "Impressora" + "Como funciona?"; "Configure a integração com impressora térmica via
  EcoTray".
  - Chave **"Integração com Impressora"** ("Conecta ao EcoTray para envio de comprovantes à impressora térmica") `:287-320`.
    Ligada: "Conectando ao EcoTray..." → "Conectado ao EcoTray" (verde) | "EcoTray não encontrado" + "Tentar conectar" e
    "Verifique se o EcoTray está aberto e rodando na bandeja do sistema (canto inferior direito do Windows). Após instalar,
    clique no ícone do EcoTray para iniciá-lo." `:322-351`. Toasts: "Conectado ao EcoTray!" | "Não foi possível conectar
    ao EcoTray. Verifique se o programa está instalado e rodando." (`hooks/useDirectPrint.tsx:79,81`).
  - Lista "Selecione a impressora" (triângulo amarelo na impressora de driver incompatível), botões "Atualizar" e
    **"Testar"** `:353-412`. "Testar" imprime um PDF na largura escolhida ("Teste de Impressão", "Se você vê isso, está
    funcionando!", data e hora) `:158-176` → toast "Comprovante enviado para a impressora!" (`useDirectPrint.tsx:120`).
  - Driver incompatível: ao escolher, toast amarelo (10 s) com o motivo; caixa âmbar fixa **"Driver incompatível
    (Generic / Text Only)"** + o motivo `:363-370,419-435`. Motivo (`ecotray/print_manager.py:87-92`): "Driver "Generic /
    Text Only" só imprime texto puro — não suporta o cupom térmico (que é gerado como imagem). Troque pelo driver térmico
    real da sua impressora (ex: POS-58, GP-58, Elgin i9, Bematech, ou o driver oficial do fabricante)." Detecção só pelo
    nome do driver: "generic / text only", "generic text only", "text only" (`print_manager.py:81-85`); outro driver ruim
    passa como compatível.
  - **"Escala e Largura do Comprovante"** ("Papel 80mm · Escala 100%") + **"Ajustar Escala"** `:444-474`.
  - **"Impressão térmica turbo (beta)"** ("Gera o comprovante mais rápido; se algo sair diferente, desligue"), só com a
    impressão direta ligada `:476-508`.
  - "Imprimir Automaticamente" / "Gerar Comprovante Automaticamente" `:512-547` e "Imprimir comprovante do Ticket de
    Pesagem" `:549-584` (fora da aula; o T8 usa o segundo).
- **Balança** `:589-852`, só com o módulo `balanca_integration`; sem ele, `BalancaModuleUpsellCard` (nome "Integração com
  Balança", preço por mês, botão "Pesar automático"; `lib/moduleUpsellCopy.ts:24-29`): **não gravar** (tem preço).
  - Título "Integração com Balança Digital" (+ selo "Liberado no seu teste" só em empresa em teste) e "Como funciona?";
    "Configure a conexão com balança digital via EcoTray" `:595-619`.
  - Chave **"Integração com Balança Digital"** ("Requer EcoTray instalado e rodando neste computador") `:622-638`; nasce
    desligada (`profiles.balanca_ativada`); em teste: "Ligue a chave para o EcoSistema começar a ler o peso da sua
    balança." `:640-645`.
  - Chave **"Peso somente pela balança"** ("Regra da empresa, independente da integração deste computador"); dica:
    "Ativo: Todos os usuários da empresa ficam impedidos de digitar ou alterar o peso bruto. Somente uma nova leitura da
    balança troca o peso." / "Desativado: O usuário pode digitar o peso manualmente ou capturar da balança." `:647-678`.
    Ligada, o campo de peso fica travado mesmo com o EcoTray fechado (`components/InputPesoBalanca.tsx:69,262`).
  - Com a chave da balança ligada `:680-849`: **"Unidade de medida padrão"** ("Quilograma (kg)", "Grama (g)", "Tonelada
    (t)"); **"Casas decimais no peso"** (0 a 3, padrão 3; o peso capturado entra com essas casas,
    `InputPesoBalanca.tsx:133-140`); **"Leitura contínua"** ("Após capturar, o peso continua atualizando em tempo real até
    incluir"; dica "Ativo: Após capturar, o campo peso continua se atualizando conforme a balança lê em tempo real, até
    incluir a pesagem." / "Desativado: Ao capturar, o peso fica fixo. Só muda ao capturar novamente.").
  - Cartão de teste (`components/configuracoes/TesteConexaoBalanca.tsx:31-151`): "Desconectada" | "Conectando..." |
    "Conectada, aguardando peso da balança" (âmbar: "Conectada, mas sem peso chegando ainda" / "Verifique se a balança está
    ligada e configurada para envio contínuo de peso.") | "Conectada" (verde: "Peso atual: **18,600 kg** — última leitura
    às 08:47:12") | "Erro na conexão"; botões "Testar conexão", "Testar novamente", "Desconectar".
  - "Balanças" ("Escolha a balança padrão desta máquina. É ela que o botão de captura de peso usa quando há mais de uma
    conectada.") `:754-847`: "EcoTray não conectado. Abra o app EcoTray na bandeja do sistema para listar as balanças." |
    "Nenhuma balança configurada no EcoTray. Abra as configurações do EcoTray (ícone na bandeja) para cadastrar." | lista
    com o nome, "Conectada"/"Desconectada" e o lápis de renomear.
- Modais: **"Baixar Instalador"** (`components/settings/EcoTrayDownloadModal.tsx`): "Instalador v1.7.22", "Selecione o
  sistema operacional do seu computador", "Windows" (".exe instalador") e "macOS" (".dmg instalador"); abre numa aba nova
  `bridge-downloads/EcoTray - Instalador.exe` (ou `.dmg`) `:28-34`. **"Como funciona?"**
  (`components/settings/EcoTrayHowItWorksModal.tsx`, passos em `ecoTrayHowItWorksSteps.ts`): "Como configurar sua
  impressora" / "Como configurar sua balança"; passo amarelo "O navegador pode avisar que o arquivo "pode ser perigoso""
  ("No Chrome ou Edge: clique na setinha/nos três pontinhos ao lado do aviso do download e escolha "Manter". Se o Windows
  mostrar uma tela azul (SmartScreen), clique em "Mais informações" e depois em "Executar assim mesmo".") `:20-28`; botão
  "Entendi". **"Ajuste do Comprovante Térmico"** (`components/ReceiptScaleModal.tsx:186-417`): "Largura do papel da
  impressora" com **"58 mm"** ("bobina pequena") e **"80 mm"** ("padrão"); "O comprovante será gerado no tamanho exato do
  papel selecionado, ocupando 100% da largura quando a escala estiver em 100%."; régua "Papel: 58 mm", "Impressão: 58.0 mm
  (100%)"; "Prévia do comprovante"; "Escala fina" (50 a 100%); "Restaurar padrão", "Testar impressão" ("Enviado direto
  via EcoTray."), "Cancelar", "Salvar". Teste: toasts "Comprovante enviado para a impressora!" e "Comprovante de teste
  enviado para a impressora!" `:114-115`.
- O "Guia de Instalação" (`EcoTrayGuideModal.tsx:22`) ainda fala em "Extraia o ZIP e execute "Instalar EcoTray.cmd"";
  o "Baixar Instalador" entrega um `.exe`. A aula não abre o guia (handoff H1).

## 2. Rodapé (todas as telas, só no computador)
`components/layout/BalancaStatusBar.tsx:54-85`, montado só fora do celular (`components/layout/AppLayout.tsx:512`;
`hooks/useBalancaHabilitada.ts`: tela ≥ 1024 px + módulo `balanca_integration` + chave "Integração com Balança Digital").
Ao centro "EcoSistema v1.59.154" (`components/Footer.tsx:44`); à direita: "Balança desconectada" | "Balança do pátio ·
Aguardando peso" (sem leitura há mais de 4 s) | "Balança do pátio · 312 kg" (ponto verde). **No celular não há
indicador** (a fonte pedia gravar no celular: vale o código).

## 3. Quando o EcoTray fecha
- Balança: toast **"Balança desconectada. Verifique se o EcoTray está rodando."** (um por queda) e reconexão sozinha,
  1 s, 2 s, 4 s, 8 s e depois a cada 10 s, sem desistir (`hooks/useBalanca.ts:44-56,464-483`).
- Impressora: a tela mostra "EcoTray não encontrado"; o sistema tenta de novo em 5 s, 10 s, 20 s… até 60 s
  (`useDirectPrint.tsx:222-278`); "Tentar conectar" força. Comprovante sem EcoTray: abre o PDF numa aba
  (`hooks/useSmartPrint.tsx:27,47-48`).

## 4. EcoTray (Windows; Tkinter, Montserrat; cores `ecotray/dashboard.py:30-42`: fundo #0a0a0a, cartão #121212, verde
#45a167, texto #ebebeb, cinza #999999, âmbar #d7a042, vermelho #bf4040)
- **Instalador** `ecotray/installer_win/installer_gui.py` (`EcoTray - Instalador.exe`, `build_installer.bat:47`): janela
  520×420 sem barra de título; cabeçalho com o logo e "Instalador — Balança & Impressora", "✕"; "O EcoTray conecta sua
  balança serial e impressora / diretamente ao sistema web, rodando silenciosamente / na bandeja do Windows."; "Pronto
  para instalar"; barra 0%; botão "  Instalar  "; "EcoTray v1.7.22" `:143-257`. Passos `:91-97,294-322`: "Verificando
  versão mais recente..." ("Verificando servidor de downloads...", 5%; "Pronto para baixar", 15%) → "Baixando EcoTray..."
  ("Baixando EcoTray.exe...", 20%; "9.7 MB / 19.4 MB" até 75%) → "Instalando arquivos..." ("Copiando arquivos...", 78%) →
  "Configurando inicialização automática..." ("Criando atalho de inicialização...", 88%; "Criando atalho na Área de
  Trabalho...", 92%) → "Finalizando..." ("EcoTray instalado com sucesso!", 100%) → "✓  Instalado com sucesso!" (verde),
  "EcoTray está iniciando na bandeja do sistema.", botão "  Fechar  ", rodapé "Iniciando na bandeja do sistema..."
  `:523-545`. Botão durante: "  Instalando...". Cria o atalho "EcoTray" na Área de Trabalho e o início automático com o
  Windows; abre o EcoTray com o painel (`--show-dashboard`, 2 s depois, `ecotray/ecotray.py:664-665`).
- **Bandeja** `ecotray/tray_app.py`: ícone do EcoTray (`assets/icon.png`), dica "EcoTray"; bolinha amarela "sem balança"
  (#eab308), vermelha "erro" (#ef4444), sem bolinha com a balança conectada `:50-98`. Clique abre o painel. Menu
  `:297-321`: **"Abrir EcoTray"** (negrito) · — · "EcoTray v1.7.22" · "Sem balança conectada" | "Balança: COM3@9600" ·
  "Impressora: POS-58" (cinza, sem clique) · — · "Reconectar balança" · "Configurações" · — · "Atualizar Versão" · — ·
  "Desinstalar" · **"Sair"**.
- **Painel** `ecotray/dashboard.py` (520×720, sem barra de título, sempre por cima): cabeçalho com o logo, "Ponte Desktop —
  Balança & Impressora", "● N cliente(s)", "–" (esconde na bandeja), "✕" `:287-353`; faixa de 3 px na cor do estado
  `:355-357`; abas **"Integrações"** e "Logs" `:439-446`; cartão de estado "Conectado e operando" (verde) | "Parcialmente
  ativo" (âmbar) | "Erro detectado" + "ws://127.0.0.1:8054" `:477-488` (estado de quando a janela abriu).
  - **"Balanças"** (+ "↻") `:512-736`: "⏳ Aguardando o sistema" + "Abra o EcoSistema no navegador e ligue a Balança em
    Configurações › Integrações. Assim que o sistema confirmar, as balanças aparecem aqui." e o botão cinza "Configuração
    indisponível" (antes de o navegador ligar a balança) → "Nenhuma balança configurada" + **"Configurar Balanças"** (verde)
    → linha "● Balança do pátio   18,6 kg  conectada  ✓ padrão". Sem o módulo: "🔒 Módulo Integração com Balança não
    contratado" (não gravar).
  - **"Impressora"** (+ "↻") `:738-846`: "✓  POS-58"; "1 impressora(s) — clique para definir padrão"; "✓ POS-58" realçada
    (impressora única: o EcoTray escolhe sozinho).
  - **"Atividade Recente"** `:848-880` (5 linhas, hora + mensagem): "Impressora padrão: POS-58", "Módulo Integração com
    Balança destravado", "[scale:Balança do pátio] conectada", "Impresso em POS-58" (`ecotray/ecotray.py:767,772,1017,
    1076,1260`).
  - "WebSocket" "balança :8053  •  comandos :8054" `:882-891`. Rodapé "EcoTray  v1.7.22" e "Atualizar Versão" `:360-409`.
  - Aviso de impressão `:1190-1202,1317-1319`: faixa verde "✓  Impresso em POS-58" (3 s).
  - **"Configurar Balanças"** (janela 640×500 com barra de título) `:1332-2098`: tabela "Nome", "Porta", "Protocolo",
    "Padrão"; "Adicionar", "Editar", "Remover", "Definir padrão", "Detectar automaticamente"; ao abrir, "Detectando
    balanças…" → "1 balança(s) detectada(s) — marcadas com ✓."; rodapé "Cancelar" e **"Gravar"**. **"Nova balança"**
    (420×520) `:1524-1838`: "Nome", "Porta Serial" ("COM3  ✓ balança"), "Protocolo" ("Automático", "WeighTech (wn…kg)",
    "Toledo", "Filizola", "UPX", "Micheletti", "Genérico", "Extração por delimitador"), "Baud rate" 9600, "Data Bits" 8,
    "Parity" none, "Stop Bits" 1, "Correção (×)" 1,0 ("1,0 = normal. Ex.: 10 corrige balança 10× menor."), "Detectar
    automaticamente", dica "detectado automaticamente — ajuste se precisar", "OK", "Cancelar".
  - Handoff H2: o "● N cliente(s)" conta as duas conexões da própria janela (`dashboard.py:347-353` + `_ws_request`): sem
    navegador já mostra "1 cliente(s)". A aula não usa esse ponto.
- **Mac** (fala só): `.dmg` com o instalador "Bem-vindo ao EcoTray!" → "Instalar" → "✓ EcoTray instalado com sucesso!";
  fica na barra de menus (`ecotray/packaging/build_dmg_mac.sh:92-150`).

## 5. Backend e integrações
- `app_config` (`key = ecotray_version` → "1.7.22") `services/ecotrayService.ts:70-77`.
- `profiles` (do usuário logado): `direct_print_enabled`, `direct_print_printer_name`, `receipt_paper_width_mm`,
  `receipt_scale`, `thermal_print_mode`, `balanca_ativada`, `balanca_url`, `balanca_unidade`, `balanca_decimais`,
  `balanca_continua` (`hooks/usePaymentPreferences.ts:74-145`, gravação silenciosa). As chaves são **por usuário**.
- `companies.scale_weight_lock_enabled` + RPC `set_company_scale_weight_lock` (`hooks/useScaleWeightLock.ts`).
- Módulos da empresa (`useCompanyModules`, `balanca_integration`).
- EcoTray local: `ws://127.0.0.1:8054` (comandos: `get_status`, `list_printers`, `print`, `print_image`,
  `unlock_scales`, `rename_scale`) e `ws://127.0.0.1:8053` (peso: `scales_list`, `weight`, `scale_status`,
  `scale_lock_status`). O `unlock_scales` leva o token da sessão; quem chama a edge `verify-balanca-module` é o EcoTray.
- Storage `bridge-downloads` (o link do instalador, numa aba nova).
