# T05 · andamento da aplicação no 1.60.22 (21/11) · etapa 1 (fala e capítulos web)

**Feito:** `tts_textos.py` (13 caps, 2.004 palavras, 11.363 caracteres com títulos), `config_narracao.json` (+ "Lógs", "sessenta quilos", "seiscentos"), `roteiro.md`, `plano.md`, `inventario.md`, `cenas/ilustracoes.json`
(ilu03 EcoTray 1.7.26; ilu06 linha 13; driver virou cap11/`ilu11_driver`; todas `v3: pendente`, nenhuma nova), `preparar_aula.sh T05`, `rec/t05/gerar.py` (13 caps; 1600x900; EcoTray falso com `versao` 1.7.26),
sementes `rec/mundo/seeds-extra/t05/*` (patch `app_config.ecotray_version` = 1.7.26), `t05_corpo.sh` e `t05_lote.sh` (gravam em `/dev/shm/t05_ens`; modos `r` rápido, `c` completo, `p` sonda).
**EcoTray = 1.7.26** (`ecotray/version.py:122`, hotfix do runtime MFC; a 1.7.25 trouxe os botões da correção). App 1.60.22.
**Capítulos:** 0 a 9 como eram; **10 novo** "Atualizar e pedir ajuda" (só cenas de Windows; a tela web descansa em Integrações); antigo 10 (Driver) = 11; antigo 11 (Recap) = 12.
Mudanças de fala: cap05 (Restaurar padrão, Imprimir Automaticamente, Ticket de Pesagem; só mostra, não liga), cap06 (marcas Toledo/Filizola, correção ÷10, "Aplicar e Gravar", cartão de teste, lápis e padrão), cap07 (padrão da empresa + exceção por pessoa), cap10, cap12.
**Robô:** cap01 aba é `#tab-btn-integrations` (sem role=tab); cap09 não clica mais em "Tentar conectar" (o app reconecta a cada ~6 s e segura 3 s após falha: clique cai no erro); cap05 clique em "Testar impressão" na palavra "um" (ver ping abaixo); `TRECHOS_WINDOWS` 6 agora corta em L12.

**Ensaios (rápido: 0 falho em 00 a 12; completo com voz estimada, 0 falho):** 01, 03, 04, 05, 06, 07, 09, 10. Usados 5 lotes (o brief pedia 2: correções do cap05 e do cap09 mais um teste de sonda). Atrasos só da voz estimada.
Não reensaiados depois de ajuste mínimo: cap06 (cursor 1 s mais cedo na L15). cap04 completo: cupom 08:41:09 (alvo 08:41:07, refazer com a voz real). `fake_now.json`: rodar `gerar.py` SEM argumentos (com argumento, o relógio do cap04 volta a 08:30).

**Cenas de Windows (etapa 2), o que muda** (EcoTray 1.7.26; refazer `capturas` com `--app /dev/shm/ecoflix-src22/ecotray`):
1. `cap02_1_download`: nada. 2. `cap02_2_smartscreen`: nada.
3. `cap02_3_instalador`: rodapé do instalador "EcoTray v1.7.26" e do painel "EcoTray  v1.7.26" (`capturas.json:136,139,174,177,228,231`).
4. `cap04_4_impressao`: versão do rodapé do painel. 5. `cap06_5_destrava`: versão.
6. `cap06_6_configurar`: versão; botão "OK" vira "Aplicar" (`cap06_6_configurar.json:151-152`, `capturas.json:363`); em "Nova balança" sem a frase antiga, com "÷10  (0,1×)", "Normal  (1×)", "×10" e "Se 600 kg no sistema correspondem a 60 kg no indicador, use ÷10 (0,1×). Depois clique Aplicar e Gravar."; abrir a lista "Protocolo" (Toledo, Filizola) na L7. Cena mais longa: da L5 (~37 s) à L10 (~94 s, estimado), ~57 s em vez de 30,5; `t0` e gestos presos às palavras novas; cap06w corta em L12.
7. `cap09_7_sair`: menu "EcoTray v1.7.26". 8. `cap09_8_atalho`: nada.
9. NOVA (cap10, L1 e L2): clique no ícone, painel; zoom no rodapé "EcoTray  v1.7.26" e "Atualizar Versão"; clique: "Verificando..." e "✓ Já atualizado" (verde); aba "Logs" (L3: "Registro do EcoTray", subabas "Geral" e "Balança do pátio", "Copiar tudo", "Abrir pasta do log", "Rodar diagnóstico", "Atualizar"; registro fictício 10 a 15 linhas com [RAW] de peso 312); "Copiar tudo" mostra "✓ Copiado" (L4).
10. NOVA (cap10, L5): botão direito: "EcoTray v1.7.26", "Balança: COM3@9600", "Impressora: POS-58", "Reconectar balança", "Configurações", "Atualizar Versão", "Desinstalar", "Sair"; cursor em Reconectar e em Desinstalar, sem clicar; Esc.
Recap (cap12): a montagem ganha "Atualizar Versão" e a aba "Logs".

**Frases sem tela:** cap06 L7 "marcas ... Toledo e Filizola" (só se a cena abrir a lista); cap07 L4 (exceção por pessoa: a tela é da T2); cap03 L5 e cap10 L1 ("selo avisa desatualizado": o aviso "EcoTray desatualizado (v..., atual é v...)" não aparece, só o selo normal); cap06 L9 (o clique em ÷10 só é falado).
**Hardware:** nada depende de hardware real; peso, impressão e menus saem do EcoTray falso e das cenas de Windows.
**Achados para o MELHORIAS/mundo:** (1) EcoTray falso (`recorder/ecotray-falso.mjs`) responde `error` ao `ping` do app (30 s): derruba uma impressão que esteja em curso nesse instante (no cap05 caiu em ~56 s do capítulo; pings em 26+30k s). Pedido: ignorar `ping`. Conferir "Testar" (cap04) e "Testar impressão" (cap05) com a voz real. (2) "Tentar conectar": clique frágil (throttle de 3 s do `ecotrayService`). (3) Aba de Configurações virou `<button>`, sem role=tab. (4) "Restaurar padrão" do ajuste do comprovante só volta a escala a 100% (a cobertura dizia 80 mm também). (5) cap06 acusa "Balança desconectada" no rodapé antes do "Gravar" (comportamento real). (6) `app_config.app_version` do mundo base ainda 1.60.10.
**Comandos:** lote: `cd /home/claude/ecoflix && bash rec/t05/t05_lote.sh 06:c 11:r ... > /dev/shm/t05_loteN.log 2>&1` (porta 54305, sobe sozinha; derrubar com `FAKE_PORT=54305 bash rec/run.sh down`). Instância derrubada.

---
# Etapa 2 (26/11) · cenas de Windows do EcoTray 1.7.26 e frases sem tela

**Capturas** refeitas (`capturar_ecotray.py --app /dev/shm/ecoflix-src22/ecotray`, 53 quadros, 0 erro) em `$TUT_HOME/t05/windows/capturas`; planos em `windows/capturas.json` (todas as versões 1.7.26; sessão nova `painel_ecotray`).
**Cenas (JSON em `windows/`, conferidas por quadros com `--mira`; MP4 só depois da voz real, os `at` seguem a voz ESTIMADA):**
3 a 5, 7, 8: só a captura mudou (rodapé "EcoTray  v1.7.26", menu "EcoTray v1.7.26"; JSON igual). 6 `cap06_6_configurar` reescrita, 58,3 s (era 30,5): lista Protocolo aberta na L7 (Automático, WeighTech, Toledo, Filizola, UPX, Micheletti, Genérico, Extração), cursor em Toledo e Filizola; correção na L8; clique em ÷10 (campo 0,1) e depois em Normal (1,0) na L9; "Aplicar" no lugar de "OK"; Gravar. 9 NOVA `cap10_9_atualizar` (29,3 s): painel, rodapé com a versão, "Verificando..." e "✓ Já atualizado", aba Logs (Geral e Balança do pátio, registro FICTÍCIO no formato do ecotray.log, [RAW] com peso 312), "✓ Copiado", "–". 10 NOVA `cap10_10_menu` (13,8 s): menu com "EcoTray v1.7.26", "Balança: COM3@9600", "Impressora: POS-58", Reconectar balança, Configurações, Atualizar Versão, Desinstalar, Sair; cursor em Reconectar e Desinstalar, Esc. Textos todos do `dashboard.py` e `tray_app.py`.
**Ferramentas:** `ferramentas/windows/ecotray_sim.py` (`estado.atualizacao` atrasa o `check_update`; `aba` acha subabas); `rec/recorder/ecotray-falso.mjs` (`definirVersao`; `up-to-date` com hífen) e `runner.mjs` (passo `ecotray` aceita `versao`). Exemplo `exemplos/ecoflix-ecotray` não reexecutado (mudanças compatíveis, comportamento padrão igual).

**Frases sem tela, todas resolvidas; NENHUMA frase trocada** (`tts_textos.py` intacto):
- cap06 L7 (Toledo e Filizola): a cena 6 abre a lista Protocolo. cap06 L9 (÷10): a cena 6 clica em ÷10 e volta ao Normal.
- cap03 L5 e cap10 L1 ("selo avisa desatualizado"): no app 1.60.22 o aviso "EcoTray desatualizado (v..., atual é v...). Feche e abra o EcoTray pra atualizar." (`SettingsIntegrationsContent.tsx:219-232`) aparece quando a versão da estação é menor que `app_config.ecotray_version`. O EcoTray falso passa a informar 1.7.20 só nesse trecho: cap03 L5 (informa a versão antiga e recarrega a página) e cap10 (começa com o aviso e, em "ou se você só quiser conferir", volta a 1.7.26 e recarrega, para o selo bater com o painel da cena 9). Custo: o recarregamento mostra ~2,5 s de "Carregando configurações..." (no cap10 isso cai atrás da cena de Windows).
- cap07 L4 (exceção por pessoa): a tela existe (Usuários > Editar do Marcos > "Peso dos pedidos": Herdar padrão da empresa, Exigir peso da balança, Permitir digitação manual). O robô vai a ela em "Em Usuários e Permissões", abre a lista, passa por duas opções, fecha sem salvar e volta às Integrações antes da L5.

**Robô (`rec/t05/gerar.py`):** ECO[10] com `versao` 1.7.20; cap03, cap07 e cap10 reescritos como acima (`goto` com `reload: true` para a versão: sem isso a navegação é interna e o cache de 60 s do app esconde a mudança). `cenas/ilustracoes.json`: sem mudança (as ilustrações não se sobrepõem a esses trechos).
**Ensaio rápido (fila, prio 5; o 1º lote caiu em 2 falhos por erro meu, corrigido):** 03, 07, 10 e 06 com **0 falho**; atrasos 0. Cap06 não mudou no robô (a lista e o ÷10 são da cena de Windows).
**Fala:** 2.004 palavras, 11.363 caracteres com títulos (11.101 de capítulos + 262 de títulos), igual ao anterior.

## Pronta para a voz
Sim. Pode gerar a voz da T05 (cap00 a cap12). Depois: refazer os `at` das cenas de Windows 6, 9 e 10 e os gestos do robô com os tempos reais, trocar `navegador.pagina` das cenas pela gravação (`cap10` inteiro é a fonte das cenas 9 e 10; cap06w já existe), montar e renderizar.
**Achados do app:** em `MELHORIAS_ECOSISTEMA.md` (T05, 26/11): "Atualizar Versão" trata a resposta `checking` como erro; frase de ajuda da correção e botão "Atualizar" da aba Logs cortados; selo só relê a versão ao montar. Diferença assumida: na captura o `check_update` responde só depois de 2 s, sem o `checking`.
