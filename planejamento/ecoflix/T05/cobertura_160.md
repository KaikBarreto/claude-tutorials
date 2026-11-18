# Cobertura 1.60.10 · T5 Balança e impressora: o EcoTray

Auditoria de 18/11/2026, só leitura de código. Base: `/dev/shm/ecoflix-src` (`APP_VERSION = "1.60.10"`; EcoTray
`APP_VERSION = "1.7.25"`, `ecotray/version.py:113`) contra o roteiro (1.59.154 e EcoTray 1.7.22), com
`git diff f37573ea0 5290be4cd`. Caminhos do app relativos a `src/`; linhas do 1.60.10. A varredura do robô
(`rec/varredura/t05.txt`) está parcial (caps. 00 a 04w): o que depende de tela leva `[TESTAR]`.

Arquivos da aula **sem mudança** entre as duas versões: `pages/Settings.tsx`, `SidebarMenuContent.tsx`,
`EcoTrayDownloadModal.tsx`, `EcoTrayHowItWorksModal.tsx`, `EcoTrayGuideModal.tsx`, `ReceiptScaleModal.tsx`,
`TesteConexaoBalanca.tsx`, `BalancaStatusBar.tsx`, `Footer.tsx`, `InputPesoBalanca.tsx`, `useBalanca.ts`,
`useDirectPrint.tsx`, `useSmartPrint.tsx`, `usePaymentPreferences.ts`, `ecotrayService.ts`; no EcoTray,
`installer_gui.py`, `tray_app.py`, `print_manager.py`, `ecotray.py`. Em `SettingsIntegrationsContent.tsx` só mudou a
chave "Peso somente pela balança". Ou seja: **caps. 0, 1, 4, 5 e 10 batem como estão**; mudam 2, 3, 6, 7, 8, 9 e 11.

## 1. Mudou no app (por capítulo)

**Todos os capítulos com janela do EcoTray ou selo de versão (2, 3, 9, 11)**

1. **EcoTray 1.7.22 → 1.7.25** (`ecotray/version.py:113`). O número aparece em: rodapé do instalador **"EcoTray v1.7.25"**
   (`installer_win/installer_gui.py:254`; o `APP_VERSION = "1.7.22"` da linha 26 é só reserva, a linha 34 lê o
   `version.py`), rodapé do painel **"EcoTray  v1.7.25"** (`dashboard.py`, rodapé), item do menu da bandeja
   **"EcoTray v1.7.25"** (`tray_app.py:298`). No app, o selo do cartão (**"v1.7.25"**, vem do `get_status` do EcoTray) e
   a janela **"Instalador v1.7.25"** (vem de `app_config.ecotray_version`) dependem do mundo falso: subir os dois para
   1.7.25. Também trocam: a ilustração do cap03 ("Aqui! v1.7.22"), a montagem do cap11, `plano.md:9,18,44`,
   `MUNDO_FICTICIO.md:138`, `rec/gerar.py:335,421-438`, `rec/cap03.json`, `cap04.json`, `cap04w.json` e
   `windows/capturas.json:136-231` (seis ocorrências). Nenhuma fala cita o número.

**cap06 · Conectar a balança**

2. Janela "Nova balança": o botão **"OK" virou "Aplicar"** (`dashboard.py:1874`). **Fala errada**: "OK e Gravar." passa a
   "Aplicar e Gravar." (`tts_textos.py`, cap. 6, linha 8). Trocar também `windows/cap06_6_configurar.json:152`
   (`dialogo:OK`) e `windows/capturas.json:363` (`"clique": "OK"`).
3. Mesma janela, campo "Correção (×)" (`dashboard.py:1617-1660`): a frase "1,0 = normal. Ex.: 10 corrige balança 10× menor."
   **saiu**. Entraram três botões embaixo do campo, **"÷10  (0,1×)"**, **"Normal  (1×)"** e **"×10"**, e a frase
   **"Se 600 kg no sistema correspondem a 60 kg no indicador, use ÷10 (0,1×). Depois clique Aplicar e Gravar."** O campo
   seleciona o valor inteiro ao receber o foco. A coluna Tela da linha 7 do cap06 (zoom em "Protocolo" com a frase antiga
   embaixo) fica errada. A janela continua 420×520 com uma linha a mais no formulário: `[TESTAR]` na captura se o
   "Aplicar" e o "Cancelar" continuam inteiros.

**cap07 · Peso somente pela balança**

4. Subtítulo da chave: "Regra da empresa, independente da integração deste computador" virou **"Padrão da empresa;
   exceções ficam em Usuários e Permissões"** (`components/settings/SettingsIntegrationsContent.tsx:665`). Coluna Tela
   da linha 1.
5. Dica do "?" (`:658-659`): **"Ativo: Por padrão, os usuários ficam impedidos de digitar ou alterar o peso bruto."** /
   **"Exceções: Em Usuários e Permissões, você pode exigir balança ou liberar digitação manual para uma pessoa
   específica."** Sumiram "Todos os usuários da empresa..." e a linha "Desativado: ...". Coluna Tela da linha 3 e
   **fala errada**: "E ela é uma regra da empresa: vale pra todos os usuários, em todos os computadores." Agora é o
   padrão da empresa, com exceção por pessoa (`hooks/useScaleWeightLock.ts:58-77`, tabela
   `user_scale_weight_policies`, migration `20261117124500_scale_weight_lock_per_user.sql`). O aviso de erro
   "Não foi possível atualizar a regra de peso da balança" não mudou (`:674`).
6. **Backend falso** (quebra a gravação desta e das aulas de pedido): a regra é lida pela RPC nova
   **`get_my_scale_weight_lock`**, que devolve `{company_default, override, enabled}`. A varredura já acusa
   `RPC_SEM_HANDLER get_my_scale_weight_lock` (`t05.unknowns-parcial.json`). Sem resposta, o gancho **trava o peso**
   ("falha fechado", `useScaleWeightLock.ts:104`): o campo de peso de compra, venda e pesagem avançada fica bloqueado nas
   T7 e T8. A chave de Integrações usa `company_default` e aparece desligada.

**cap08 · O indicador de peso**

7. O rodapé mostra **"EcoSistema v1.60.10"** (`components/Footer.tsx:44`, `config/version.ts:16`): coluna Tela da linha 1
   e `storage.app_version` / `notification_shown_version` de todos os `rec/cap*.json` e `rec/gerar.py:5,50,52`.

**cap01 · pendência de teste**

8. A varredura falhou no cap01, passo 2: `alvo nao encontrado em 12s: {"role":"tab","name":"Integrações"}`. O código da
   aba não mudou (`pages/Settings.tsx:42`, `lib/configTabsPermissions.ts`); os caps. 02 a 04w, que abrem a mesma aba,
   passaram. `hooks/usePermissions.tsx` mudou (+180 linhas, restrições por usuário): `[TESTAR]` se a aba demora a aparecer
   enquanto as permissões carregam no mundo falso. Sem mudança de rótulo a registrar.

### Cenas de Windows: o que refazer

| Cena | Mostra | Refaz? |
|---|---|---|
| 1 `cap02_1_download` | navegador e aviso do download | Não (nada do EcoTray; só a página, quando entrar a gravação do robô no 1.60.10) |
| 2 `cap02_2_smartscreen` | SmartScreen | Não |
| 3 `cap02_3_instalador` | instalador "EcoTray v1.7.22" e painel "EcoTray  v1.7.22" | **Sim** (versão) |
| 4 `cap04_4_impressao` | painel com o rodapé da versão | **Sim** (versão) |
| 5 `cap06_5_destrava` | painel | **Sim** (versão) |
| 6 `cap06_6_configurar` | painel, "Configurar Balanças", "Nova balança" | **Sim** (versão, "Aplicar", botões e frase da correção) |
| 7 `cap09_7_sair` | menu da bandeja "EcoTray v1.7.22" | **Sim** (versão) |
| 8 `cap09_8_atalho` | atalho e ícone na bandeja | Não |

Para recapturar: no comando do `windows/LEIA.md`, `--app $TUT_HOME/app-src-1.59.154/ecotray` passa a apontar para o
`ecotray/` do 1.60.10 (`/dev/shm/ecoflix-src/ecotray` ou cópia), e `capturas.json` troca "1.7.22" e "OK". Os tempos das
cenas 3, 4, 5, 7 não mudam; a 6 muda se entrar o trecho P2.

## 2. Falta cobrir

| # | O que é (código) | Quando o cliente usa | Vale? |
|---|---|---|---|
| L1 | **Correção do peso por balança**: "Correção (×)" com "÷10  (0,1×)", "Normal  (1×)", "×10"; erro "Informe uma correção maior que zero. Use 0,1 para dividir o peso por 10." (`dashboard.py:1617-1660,1845-1856`) | O peso chega 10 vezes maior ou menor que o do visor | **Sim**, trecho no cap06 (P2). É a novidade do 1.7.25 |
| L2 | **Exceção da trava por pessoa**: "Peso dos pedidos" com "Herdar padrão da empresa", "Exigir peso da balança", "Permitir digitação manual"; "A exceção vale para compras e vendas deste usuário. Sem exceção, futuras mudanças no padrão da empresa são aplicadas automaticamente." (`pages/UserManagement.tsx:1312-1333`); no detalhe, "Padrão da empresa" / "Balança obrigatória" / "Digitação manual liberada" (`UsersMasterDetail.tsx:322-337`) | Dono libera o gerente para digitar, ou obriga só o balanceiro | **Só citar** no cap07 (P3). A tela é da **T2** (`T02/cobertura_160.md`, L3 e item 4): não repetir |
| L3 | **"Imprimir Automaticamente"** ("Envia o comprovante direto para a impressora ao finalizar pedidos"); sem a impressão direta o rótulo é "Gerar Comprovante Automaticamente" ("Gera e abre o PDF do comprovante automaticamente ao finalizar pedidos") (`SettingsIntegrationsContent.tsx:511-547`) | Balcão que imprime todo pedido | **Sim**, trecho no cap05 (P4). Nenhum roteiro da trilha mostra essa chave |
| L4 | **"Imprimir comprovante do Ticket de Pesagem"** ("Envia o comprovante térmico direto pra impressora ao salvar um ticket") (`:549-584`) | Quem usa ticket | **Só citar** em P4; o uso é da **T8** |
| L5 | **Renomear a balança pelo sistema**: lápis "Renomear balança", Enter ou "Salvar nome"; aviso `Balança renomeada para "..."` (`:116,821-838`) | Trocar o nome sem abrir o EcoTray | **Sim**, curto (P5) |
| L6 | **Balança padrão com mais de uma**: lista de escolha em "Balanças"; aviso "Balança padrão definida: ..." (`:140,784`); no EcoTray, "Definir padrão" | Pátio com duas balanças | **Só citar** em P5. O mundo tem uma balança só (`MUNDO_FICTICIO.md:101`) |
| L7 | **"Editar" e "Remover"** em "Configurar Balanças"; sem seleção, "Selecione uma balança." (`dashboard.py:1907-1928`) | Trocar a porta ou tirar uma balança | **Só citar** em P5 |
| L8 | **Lista de protocolos**: "Automático", "WeighTech (wn…kg)", "Toledo", "Filizola", "UPX", "Micheletti", "Genérico", "Extração por delimitador" (`dashboard.py:1401-1410`); "Detectar automaticamente"; "Nenhuma balança detectada nessa porta." | Balança que o Automático não reconhece | **Só citar** as marcas (P2, uma frase). Abrir a lista: não, é assunto de suporte |
| L9 | **Aba "Logs" do painel**: "Registro do EcoTray" ("últimas ~200 linhas  •  inclui bytes crus [RAW] da balança"), subabas "Geral" e uma por balança, "Copiar tudo", "Abrir pasta do log", "Rodar diagnóstico", "Atualizar" (`dashboard.py:894-1158`) | O suporte pede o registro | **Sim**, no capítulo novo (P6) |
| L10 | **"Atualizar Versão"** (rodapé do painel e menu): "Verificando..." → "✓ Já atualizado" / "↑ Atualizando para v..." / "✗ Erro ao verificar" (`dashboard.py:374-409`); o EcoTray também procura versão nova a cada 6 horas (`ecotray.py:236`) | Selo "EcoTray desatualizado" no sistema | **Sim**, no capítulo novo (P6) |
| L11 | **"Reconectar balança"** no menu da bandeja (`tray_app.py:306`) | Cabo trocado, balança religada | **Sim**, uma frase em P6 |
| L12 | **"Desinstalar"** no menu: "Desinstalar EcoTray", "Deseja desinstalar o EcoTray?" (`tray_app.py:353-385`) | Trocar de computador | **Só citar** em P6 (não clicar) |
| L13 | **"Testar conexão" / "Testar novamente" / "Desconectar"** do cartão de teste (`TesteConexaoBalanca.tsx`) | Conferir a balança sem abrir um pedido | **Só citar**: uma frase no cap06, linha do teste verde (P5) |
| L14 | **"Restaurar padrão"** no "Ajuste do Comprovante Térmico" (`ReceiptScaleModal.tsx`) | Voltar a 80 mm e 100% | **Só citar** no cap05, sem trecho próprio |
| L15 | **Pesos acima de 10 toneladas** (1.7.23 e 1.7.24: Filizola, genérico e WeighTech aceitam seis dígitos) | Balança rodoviária ligada no EcoTray | **Não**: sem tela, e no mundo a rodoviária fica fora do EcoTray (`MUNDO_FICTICIO.md:142`). Decisão D3 |
| L16 | **"Guia de Instalação"** (`EcoTrayGuideModal.tsx:22`) | (ainda fala em ZIP e "Instalar EcoTray.cmd") | **Não**: continua divergente do instalador `.exe` (handoff H1) |
| L17 | Captura do peso no pedido, botão da balança, mensagens "O peso bruto deve ser capturado pela balança" | Compra e venda | **Não aqui**: T7 (`T07/cobertura_160.md`, L14 e L15) e T8 |
| L18 | Cartão de contratação da balança (tem preço) | Sem o módulo | **Não** (preço de plano); o cap06 já cita |

## 3. Proposta

### P1 · Ajustes sem tempo a mais
- cap06, linha 8, fala: **"Aplicar e Gravar. Pronto: a Balança do pátio aparece conectada."** Tela: clique em "Aplicar".
- cap06, linha 7, Tela: embaixo de "Correção (×)" 1,0, os botões "÷10  (0,1×)", "Normal  (1×)", "×10" e a frase nova.
- cap07, linha 1, Tela: subtítulo "Padrão da empresa; exceções ficam em Usuários e Permissões".
- cap08, linha 1, Tela: "EcoSistema v1.60.10". Caps. 2, 3, 9 e 11: "v1.7.25" onde hoje está "v1.7.22".

### P2 · Trecho no cap06, depois da linha do "Protocolo" · A correção do peso (cena de Windows 6, mais longa)

| Tela | Fala |
|---|---|
| (cena) Ainda em "Nova balança", zoom em "Protocolo": "Automático". | Se a sua balança não for reconhecida, a lista tem as marcas mais comuns, como Toledo e Filizola. |
| (cena) A câmera desce até "Correção (×)" 1,0 e os botões "÷10  (0,1×)", "Normal  (1×)" e "×10". [ZOOM: os três botões, a frase inteira] | Embaixo fica a correção. Ela serve quando o peso chega no sistema diferente do visor da balança. |
| (cena) Zoom na frase "Se 600 kg no sistema correspondem a 60 kg no indicador, use ÷10 (0,1×). Depois clique Aplicar e Gravar."; o cursor passa por "÷10  (0,1×)" sem clicar. | Um exemplo: o visor marca sessenta quilos e no sistema aparecem seiscentos. Aí é só clicar em dividir por dez. Aqui o peso bate, então fica no normal. |

### P3 · cap07, linha 3 reescrita e uma linha nova · Padrão da empresa e exceções

| Tela | Fala |
|---|---|
| O mouse para no "?" da opção: "Ativo: Por padrão, os usuários ficam impedidos de digitar ou alterar o peso bruto." / "Exceções: Em Usuários e Permissões, você pode exigir balança ou liberar digitação manual para uma pessoa específica." | E ela é o padrão da empresa: vale pra todos os usuários, em todos os computadores. |
| [ZOOM: o subtítulo "Padrão da empresa; exceções ficam em Usuários e Permissões"] | Dá pra abrir exceção por pessoa. Em Usuários e Permissões, você libera a digitação pra um usuário, ou exige a balança só de quem pesa. Isso a gente viu no tutorial de usuários. |

A última frase só vale se a T2 adotar o trecho do "Peso dos pedidos" (decisão 6 da `T02/cobertura_160.md`); senão,
trocar por "Fica no cadastro de cada usuário, no campo Peso dos pedidos."

### P4 · Trecho no fim do cap05 · Imprimir sozinho

| Tela | Fala |
|---|---|
| Fecha a janela do ajuste; a câmera desce até "Imprimir Automaticamente" ("Envia o comprovante direto para a impressora ao finalizar pedidos"), desligada; o mouse para no "?": "Ao finalizar um pedido, o comprovante é enviado direto para a impressora automaticamente, sem nenhuma confirmação." | Mais uma chave: Imprimir Automaticamente. Com ela ligada, todo pedido finalizado já sai na impressora, sem você clicar em nada. |
| Liga a chave. [BACKEND: `profiles` grava `autoPrintReceipts`] Zoom em "Imprimir comprovante do Ticket de Pesagem" ("Envia o comprovante térmico direto pra impressora ao salvar um ticket"), desligada. | Na Recicla Vale, fica ligada. E a de baixo faz o mesmo com o Ticket de Pesagem, que tem um tutorial só dele. |

Ligar a chave muda o estado das aulas seguintes (T7 em diante finaliza pedidos): ver decisão D2. Alternativa sem efeito:
só mostrar, com a fala "Na Recicla Vale, por enquanto, fica desligada."

### P5 · Trecho no cap06, depois da linha "o teste fica verde" · Nome, padrão e teste

| Tela | Fala |
|---|---|
| Em "Balanças", o mouse para no lápis da "Balança do pátio" (dica "Renomear balança"), sem clicar. | No lápis, você troca o nome da balança daqui mesmo, sem abrir o EcoTray. |
| Zoom na bolinha de escolha ao lado do nome e no texto "Escolha a balança padrão desta máquina. É ela que o botão de captura de peso usa quando há mais de uma conectada." | Com mais de uma balança, você marca aqui qual é a padrão deste computador. Pra trocar a porta ou tirar uma balança, é no Configurar Balanças do EcoTray, em Editar e Remover. |
| Zoom nos botões "Testar novamente" e "Desconectar" do cartão de teste. `[TESTAR: quais botões aparecem com o cartão verde]` | E o Testar novamente confere a balança a qualquer hora, sem abrir um pedido. |

### P6 · Capítulo novo, entre o cap09 e o cap10 · Atualizar e pedir ajuda (vinheta: ECOTRAY)

| Tela | Fala |
|---|---|
| Semente `apos-cap06`. [CENA WINDOWS 9, atualizar: clique no ícone da bandeja; o painel abre; zoom no rodapé "EcoTray  v1.7.25" e "Atualizar Versão"; clique em "Atualizar Versão": "Verificando..." e, em seguida, "✓ Já atualizado" (verde, 4 s).] | O EcoTray se atualiza sozinho. Mas, se o sistema avisar que ele está desatualizado, clique em Atualizar Versão, aqui no rodapé da janela. |
| (cena) Clique na aba "Logs": "Registro do EcoTray", "últimas ~200 linhas  •  inclui bytes crus [RAW] da balança", subabas "Geral" e "Balança do pátio", botões "Copiar tudo", "Abrir pasta do log", "Rodar diagnóstico" e "Atualizar". | Na aba Logs fica o registro de tudo que o EcoTray fez. |
| (cena) Clique em "Copiar tudo": o botão mostra "✓ Copiado" por 1,8 s (`dashboard.py:1072-1073`). | Uma dica: se o suporte pedir, clique em Copiar tudo e cole na conversa. Assim a gente vê na hora o que a balança está mandando. |
| [CENA WINDOWS 10, menu: botão direito no ícone da bandeja; o menu com "EcoTray v1.7.25", "Balança: COM3@9600", "Impressora: POS-58", "Reconectar balança", "Configurações", "Atualizar Versão", "Desinstalar", "Sair"; o cursor para em "Reconectar balança" e depois em "Desinstalar", sem clicar; Esc.] | No botão direito do ícone, o Reconectar balança chama a balança de novo, depois de trocar um cabo. E o Desinstalar remove o EcoTray, se o computador da balança mudar. |

Recap (cap11): acrescentar à linha 4 "e onde atualizar o EcoTray e copiar o registro pro suporte".

### O que o mundo fictício precisa
- **Handler RPC `get_my_scale_weight_lock`** → `{"company_default": false, "override": null, "enabled": false}` (todas as
  aulas, não só a T5); `set_company_scale_weight_lock` já existe. Tabela `user_scale_weight_policies` vazia (lida pela
  aba de usuários).
- `app_config.ecotray_version` = "1.7.25"; EcoTray falso: `get_status.version` = "1.7.25".
- `storage.app_version` e `notification_shown_version` = "1.60.10" nos `rec/cap*.json`.
- P4: `profiles` aceita a gravação de `autoPrintReceipts` (mesma gravação silenciosa das outras chaves).
- P6: capturas novas do painel (aba "Logs" com um registro fictício de 10 a 15 linhas, sem dado real: "Impressora padrão:
  POS-58", "[scale:Balança do pátio] conectada", linhas `[RAW]` com peso 312) e do rodapé com "✓ Já atualizado"
  (`check_update` → `{"status": "up-to-date"}` no EcoTray das capturas).
- P2: captura "Nova balança" com os três botões (já sai do código 1.7.25, sem dado novo).
- Pendência antiga, ainda na varredura: `STORAGE_ARQUIVO_AUSENTE bridge-downloads/EcoTray - Instalador.exe` (404 na aba
  nova, que não entra no vídeo).

## 4. Estimativa

| Proposta | Onde | Fala a mais |
|---|---|---|
| P1 | caps. 6, 7, 8 e versões | 0 s |
| P2 | cap06, cena 6 | ~27 s (70 palavras) |
| P3 | cap07 | ~14 s (36 palavras a mais) |
| P4 | cap05 | ~20 s (52 palavras) |
| P5 | cap06 | ~24 s (62 palavras) |
| P6 | capítulo novo | ~45 s (117 palavras), mais a vinheta |

**Total: ~130 s de fala a mais e 1 capítulo novo** (a aula vai de ~12 min para ~14,5 min). Cenas de Windows: 5 refeitas
(3, 4, 5, 6, 7), a 6 mais longa, e 2 novas (9 e 10).

## Decisões pendentes
- **D1** Versão do EcoTray na tela: 1.7.25 em tudo (proposto), inclusive o `app_config` do mundo.
- **D2** P4: ligar "Imprimir Automaticamente" de verdade (muda T7 em diante) ou só mostrar.
- **D3** Citar ou não que o EcoTray 1.7.25 aceita balança rodoviária acima de 10 toneladas (hoje fora do mundo).
- **D4** P3 depende de a T2 mostrar o campo "Peso dos pedidos".
- **D5** P6 como capítulo próprio (proposto) ou como fim do cap09.
