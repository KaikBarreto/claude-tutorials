# T16 · andamento (app 1.60.22, tela 1600x900; passadas de 18/11, 19/11 e 20/11)

## Feito
- 18/11 (1.60.10): 25 capítulos (eram 19), sementes `seeds-extra/t16/`, `t16_lote160.sh`, handlers `rpc/nfe_emissao_sem_rede.mjs` e
  `functions/plugnotas-upload-certificate.mjs` (ver `cobertura_160.md` e `inventario.md` seção 15).
- 20/11 (1.60.18 e 1.60.22; handoff fiscal de 19/11; `inventario.md` seção 16): 14 linhas de fala trocadas e 1 tirada no `roteiro.md`
  e no `narracao/tts_textos.py` (5.261 → 5.264 palavras; os dois conferidos linha a linha):
  cap01 L2 "Relatório/Estoque Fiscal" (uma tela só); cap04 L2 a lupa do CNPJ (sem clicar) e L4 o endereço próprio do CNPJ padrão;
  cap06 L6 dica do número já usado (rejeição 539 → Rejeitada, 1.60.21); cap09 L3 sem anunciar Homologação ("Toda nota nova abre em
  Produção"); cap11 sem a linha da Pré-visualização (no 1.60.22 a aba só tem a DANFE real, que o backend falso não gera: proposta em
  `propostas_fala.md`); cap15 L9 "Reemitir NF-e"; cap16 L3 "Cancelamento enviado"; cap16 L9 sem o PDF da CC-e (não existe no motor
  próprio) e sem "vale sempre a última" (não está no código); cap17 L6 sem citar o DANFE (lê o aviso da tela); cap20 L3 Comprovante
  (Notinha) com o PDF, L4 DANFE só "pronto pra imprimir" (saíram "visual mais limpo" e "1º de dezembro"), L9 sem a aba Homologação;
  cap22 L3 sem o DANFE recebido (o falso não gera); cap24 L3 sem "a pré-visualização".
- Robô (`$TUT_HOME/rec/t16/gerar.py`, `VERSAO = '1.60.22'`): cap01 um item só no submenu; cap04 a lupa e as duas opções do Endereço
  Fiscal; cap06 a última nota na dica; cap11 sem a Pré-visualização (L11 = Emitir Nota); cap15 `emite_e_espera(..., botao='Reemitir
  NF-e')`; cap16 sem o "PDF"; cap17 zoom no aviso da coluna Item; cap20 `POPS` no setup, clique em "Comprovante (Notinha)" e `PDF_JS`
  depois dele e do "Download DANFE", sem a aba Homologação. `t16_pdf.py` (novo) grava os PDFs em `rec/t16/arquivos/` (o lote roda
  ele depois do cap20). `t16_lote160.sh`: `--completo` no meio da lista e trava de versão do build (`T16_VERSAO`).
- Handler novo (só da T16): `rec/mundo/handlers/rpc/get_invoice_for_print.mjs` (migration 20260925042000).
- `cenas/ilustracoes.json`: 3 entradas `"tipo": "comprovante"`, `"cena": "pdf"` (ilu20b Notinha, ilu20c DANFE, ilu24b DANFE no resumo).

## Ensaio (instância 54316, FAKE_NOW 2026-11-10T08:30:00-03:00)
```bash
cd /home/claude/ecoflix
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54316 bash rec/run.sh fake
bash rec/t16/t16_lote160.sh --junto 0 1 2 ... 24 --completo 15 16 20   # rápido em ordem (a cadeia de sementes depende da ordem), depois completos
cat rec/t16/_ens/_lote.txt rec/t16/_lote.txt                    # uma linha por capítulo; resumo em t16-capNN.resumo.txt
FAKE_PORT=54316 bash rec/run.sh down
```

## Estado dos ensaios
- Lote 1 (20/11, 1.60.22, uma senha da fila por capítulo): morreu nas 2 h com só cap00 e cap01 feitos (rápido, 0 falho); cada
  capítulo esperava ~50 min na fila.
- Lote 2 (`--junto`, uma senha só): **25 de 25 no rápido com 0 passo falho**, conferências tela × fala sem DIFERENTE, sementes
  `apos-cap03` a `apos-cap23` recapturadas no 1.60.22 (a cadeia 1252 → 1253 → 1254 fechou). Completos 15, 16 e 20: 0 falho; maxLate
  1,76 s (cap15, "#1252 Autorizada": espera da consulta de status de 5 s), 1,03 s (cap16, reabrir a Carta de Correção), 1,67 s
  (cap20, L9). Avisos na tela só os pedidos pelo roteiro (cap12 "Nenhum caixa...", cap14 NCM), mais o cap15 (NCM inválido no meio da
  digitação: agora o NCM é colado de uma vez). O PDF do Comprovante (Notinha) não veio ("SEM JANELA": a aba abre depois da RPC; o
  `PDF_JS` agora espera até 20 s). O DANFE veio: `rec/t16/arquivos/cap20-danfe-1250.pdf` (o fictício do backend falso).
- Lote 3 (`--junto`): rápido 15 e 20 com 0 falho (cap15 sem aviso; os dois PDFs do cap20 em `rec/t16/arquivos/`: o Comprovante
  (Notinha) real da 1250 e o DANFE fictício). Completos 05 09 11 12 13 14 15 17 18 20 22 24 (e 16 do lote 2): **0 passo falho em
  todos**, conferências sem DIFERENTE. Atraso acima de ~1 s, com a voz ESTIMADA e a máquina dividida: cap11 4,2 s ("Soma das
  parcelas", depois do calendário dos vencimentos), cap12 5,7 s (o caixa do Marcos, depois da troca de data), cap13 5,4 s (Incluir o
  papelão, trecho acelerado), cap14 3,3 s (os itens), cap20 1,9 s (L9), caps 15, 17 e 18 ~1,6 s (a autorização chega na consulta de
  status de 5 s), cap22 1,3 s, caps 05 e 24 1,2 s; 09 e 16 ~1,0 s.
- Só no rápido: 00 01 02 03 04 06 07 08 10 19 21 23.

## Falta
- Voz de verdade: depois do ElevenLabs, `python3 -I rec/t16/gerar.py` e completos dos capítulos acima de 1 s (11, 12, 13, 14 primeiro).
- Mundo base (pedido): `plugnotas-emit` falso atender `action: "preview_danfe_fiscal"` (a Pré-visualização do 1.60.21+ só tem a DANFE
  real; proposta de fala em `propostas_fala.md`) e um DANFE realista no `plugnotas-download` (o de hoje é um PDF de 5 linhas, no
  modelo de antes de 01/12). A IE da Fundição no mundo (6846208254) tem 10 dígitos e aparece no comprovante; SP usa 12.
- Ilustrações: as 3 entradas `comprovante` estão com `"v3": "pendente"` (a cena é do coordenador).
- Instância 54316 derrubada no fim de 20/11.

## 28/11 · 1.60.39

Etapa 1 (preparação, sem build, sem ensaio, sem voz). App `origin/main` de 26/11 (`bab2eb1e8`, 1.60.39), comparado com o 1.60.22
(`bea545ecf`) só por `git show`/`git diff` (repositório do app intocado). Backups do antes em
`/tmp/claude-0/-home-claude/5ab7153e-b0bb-5f91-8e7e-f0df5c647505/scratchpad/T16_*` (somem no reinício).

**O que mudou no app para a T16** (arquivo do 1.60.39):
- `pages/ConfiguracaoFiscal.tsx`: a seção "Impostos (padrão)" virou **"Impostos"** (sublabel "NF-e, NFC-e e NFS-e") com as abas internas
  "NF-e e NFC-e" (o `ImpostosTab` de sempre) e "NFS-e" (`nfse/NfseIbsCbsFields.tsx`, "IBS e CBS da NFS-e", desligado). Seletores por id
  (`#tab-btn-impostos`): o robô não quebra. `ImpostosTab.tsx` só mudou o Crédito do Simples (fora do Lucro Real).
- `NotaFiscalHistorico.tsx` → `FiscalDocumentHistoryDialog.tsx` (RPC nova `list_fiscal_document_history`, migration 20261126183000):
  "Histórico da NF-e", "Tentativas, consultas e respostas do processamento fiscal.", eventos "Transmissão do documento fiscal" (Registro)
  e "Documento rejeitado" (Erro) para os `nfe_events` da 1252, "2 evento(s)", botão "Fechar". Sem handler, o falso devolvia lista vazia.
- `NotaFiscalPreview.tsx`: no Visualizar da rejeitada, o botão "Editar e reemitir com novo número" (o menu continua com os dois).
- `NotaFiscalListFilters.tsx`: o "Filtros" é um painel ("Filtros", "Limpar", seção "Status"); emitente só com mais de um CNPJ
  (`get_invoices_paged` ganhou `p_fiscal_config_ids`, migration 20261126180000).
- `notas-recebidas/NotasRecebidasTab.tsx`: em cima do painel, a escolha "NF-e" / "NFS-e" (`InboundNfseList.tsx`, lista simples sem ações)
  e o botão **"Importar XML"** (`hooks/useInboundXmlImport.ts` → edge `inbound-xml-import`: até 2 MB, sem DOCTYPE, recusa evento fiscal,
  NF-e só com `cStat` 100, chave = protocolo, destinatário = CNPJ da empresa; toast "NF-e importada com sucesso."). O "Importar nota"
  (chave ou XML, fila `dfe_inbound_import_jobs`) continua no painel. Toast "XML solicitado à SEFAZ" virou "Aguardando a Receita".
- `ImportNfeXmlDialog.tsx` (Lançar compra…): quadros "Produtos", "Encargos/descontos" e "Total da nota" e a caixa "Registrar também no
  estoque fiscal (não altera o saldo físico)" (era "Contar também no estoque fiscal"). A compra em si (tela de Compra) não mudou.
- Backend sem tela: motor fiscal próprio para quem tem o módulo (1.60.24), ciência automática (1.60.33), cota sem o histórico do DF-e
  (20261124190000), overrides da nota sobre cenários (fd20b0b7e). Nenhuma frase da aula muda por eles.
- `components/ui/tabs.tsx` e `SettingsSidebarLayout.tsx`: abas com setas de rolagem (`HorizontalScrollArrows`); a barra de seções virou
  `div role=navigation` (não `<nav>`): a T16 usa os ids, a T17 foi corrigida. `SidebarAutoCollapse` (recolhe o menu uma vez entre 1280
  e 1535 px): a gravação é 1600 px, fora da faixa.

**Aula (25 capítulos, nenhum novo nem tirado; 5.264 → 5.318 palavras):**
- cap02 L2/L3 e ilustração: rótulo "Impostos". cap04 L6: Tela com as abas "NF-e e NFC-e" / "NFS-e"; fala nova (abaixo).
- cap15 L4: Tela do Histórico novo (fala igual). cap20 L4: a cena do papel é a DANFE de exemplo do Kaik (pendente); L9: o painel
  "Filtros" (fala igual). cap21 L1: Tela com "Importar XML" e "NF-e"/"NFS-e" (fala igual).
- **cap23 refeito** (8 linhas, era 7): "Importar XML" no lugar do "Importar nota" + aba "Arquivo XML"; nova L4 (o "Importar nota" pela
  chave, sem clicar); a última linha leva para a T17 (a compra é o cap11 de lá). cap24 L5/L6: Tela.
- `narracao/tts_textos.py` e `roteiro.md` conferidos linha a linha (0 diferença, com a tabela de pronúncia).

**Frases trocadas** (para o Kaik aprovar antes da voz; as marcadas ★ mudam informação de funcionamento):
| Cap/linha | Antes | Depois |
|---|---|---|
| 04 L6 | Passo três, os impostos. Primeiro, o regime tributário. ... | Passo três, os impostos. Eles ficam separados por documento, e a gente fica na aba da NF-e. Primeiro, o regime tributário. ... |
| ★ 23 L2 | Clico em Importar nota, vou na aba Arquivo XML e escolho o arquivo da cooperativa. | Clico em Importar XML e escolho o arquivo da cooperativa. |
| ★ 23 L3 | Importar nota. Pronto: nota importada, e ela entra na lista com as outras. | Antes de salvar, o sistema confere se a nota foi emitida pro CNPJ da Recicla Vale e se ela está autorizada na SEFAZ. Pronto: NF-e importada, e ela entra na lista com as outras. |
| ★ 23 L4 (nova) | (não havia) | Se você só tem a chave de acesso, é o Importar nota, aqui embaixo: ele traz a nota pelos quarenta e quatro números. |
| 23 L8 (era L7) | ... E Conferir na tela de compra leva os itens pra tela de Compra. Nada é lançado agora: lá você confere os valores e escolhe como pagou. No mesmo menu, ... | ... E Conferir na tela de compra leva os itens pra tela de Compra, onde você confere os valores e escolhe como pagou. No mesmo menu, ... No próximo tutorial, esta nota vira compra. |
Nenhuma frase sobre plano ou cobrança mudou.

**Robô e mundo:**
- `$TUT_HOME/rec/t16/gerar.py` (+ cópia em `T16/rec/`): `VERSAO = '1.60.39'`; `SECAO_ID['Impostos']`; cap04 hover nas abas NF-e/NFS-e;
  cap15 os títulos novos do Histórico e "Fechar"; cap23 novo (`c.upload` no botão "Importar XML", o seletor do navegador). `t16_lote160.sh`:
  `T16_VERSAO=1.60.39`. `capNN.json` regerados com a voz estimada (`preparar_aula.sh T16`).
- Handlers novos (mundo, nas duas cópias `perfis/ecoflix/mundo` e `$TUT_HOME/rec/mundo`): `functions/inbound-xml-import.mjs`,
  `rpc/list_fiscal_document_history.mjs`, `rpc/set_inbound_fiscal_entries.mjs`; mudados `rpc/get_invoices_paged.mjs`
  (`p_fiscal_config_ids`) e `lib/eco.mjs` (`criarPedido` carimba `inbound_nfe.purchase_id`, para a T17). Testados à parte no núcleo do
  falso (importação, destinatário errado, sem protocolo, reimportação sem duplicar, histórico da 1252 e de um MDF-e rejeitado).
- Sementes da T16 intocadas: a `apos-cap23` (entrada do cap24) sai do ensaio no 1.60.39 (a Cooperativa passa a entrar com `origem`
  "manual" e sem número, como a edge real).
- `cenas/ilustracoes.json`: ilu20c e ilu24b apontam para a DANFE do Kaik (pendente, `rec/t16/arquivos/danfe-exemplo-1250-kaik.pdf`), com
  o que conferir ao receber; ilu02_ordem e ilu04_padrao sem "(padrão)"; ilu17_casamento uma linha abaixo.

**Achados do app (MELHORIAS):** (1) `inbound-xml-import/index.ts` não grava `numero`, `serie`, `cfop_principal`, `fin_nfe` nem
`ref_nfe_key` (estão em `values`, fora do `payload`): a nota importada fica sem número (Kardex fiscal e a travessia da compra).
(2) O diálogo diz "O financeiro usa o total oficial da NF-e, incluindo tributos, frete..." (só com encargo ≠ 0), mas o "Conferir na tela
de compra" leva só os itens; a RPC `create_inbound_nfe_purchase_atomic` (que usa o vNF) não é chamada pela tela. A aula usa nota sem
encargo. (3) Notas Recebidas com dois botões de importar e duas escolhas NF-e/NFS-e (a de dentro lista NFS-e sem ação). (4) Na
homologação o motor troca a razão social do destinatário (`nfe-homologation.ts`, `homologation.py`).

**Falta (etapa 2):** build do 1.60.39, ensaio em lote (`t16_lote160.sh --junto 0 ... 24 --completo 04 15 20 23`), DANFE do Kaik, voz
(~30,0 mil créditos: 29.675 caracteres de fala e títulos), cenas e fechamento. Comandos no `T17/andamento_160.md`, mesma seção.
