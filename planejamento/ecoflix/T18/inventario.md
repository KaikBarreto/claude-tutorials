# Inventário · T18 Ambiental: MTR e CDF (EcoSistema 1.59.154)

Código lido em `/home/claude/ecoflix/app-src-1.59.154/` (só leitura). Caminhos relativos a `src/`. Rótulo entre aspas =
texto exato da tela. 🔒 Módulo **Notas Fiscais** (`screen_notas_fiscais`; emitir e cancelar pedem `action_emit_ambiental`).
Para SP o sistema é o **SIGOR** (`utils/mtrSistema.ts:11-17`: `sigor_sp` → "SIGOR"); todo rótulo com `{sistemaNomeCurto}` sai
"SIGOR" na Recicla Vale.

## 0. Fonte × código (o que muda no roteiro)
| Ponto da fonte | No código | Roteiro |
|---|---|---|
| Papel da empresa | **MTR**: a empresa é a **geradora** (a lista mostra "Destinador"; o gerador é a própria unidade do acesso). **CDF**: a empresa é a **destinadora** ("O destinador é a sua empresa (quem recebeu o resíduo).", `cdf/NovoCdfModal.tsx` passo 2) e informa o gerador e os MTRs recebidos | a ilustração da cadeia mostra a Recicla Vale nos dois papéis |
| ⚠️ "unidade do órgão no formato SIGLA - Nome, copie exatamente" | Não se digita: a unidade é escolhida na lista sincronizada do órgão, que vem como "TON - Tonelada", "KG - Quilograma" (`mtr/mtrNotaFiscal.ts:41-50`) | a fala mostra a unidade como o órgão escreve, sem "copiar" |
| ⚠️ "não existe Usuário de API no SIGOR" | Bate: "CPF da pessoa usuária do SIGOR *" + "Senha do SIGOR" ("É a mesma senha que você usa para entrar no portal do SIGOR.") (`mtr/MtrConfigCard.tsx:340-398`) | dito no cap03 |
| "Acompanhar o manifesto" | Status "Emitido", "Rascunho", "Cancelado", "Erro", "Confirmar no órgão" (`mtr/mtrShared.ts:19-35`); "Ver tentativas" → "Histórico de tentativas" | não há status de "recebido": o recebimento é dado no portal do órgão |
| "Cancelar e quando é possível" | Só MTR "Emitido" tem "Cancelar MTR" (`mtr/MtrTab.tsx:375-376`; edge `sigor-mtr-cancel`: "Só é possível cancelar um manifesto já emitido."); irreversível | dito assim |
| CDF "por status" | A lista usa os mesmos selos do MTR (`cdf/CdfTab.tsx:340`); "A emissão do CDF é definitiva e não pode ser cancelada pelo sistema." | dito no cap07 |
| 🚫 MTR, CDF e NF-e independentes | Bate: "Puxar da nota fiscal" só monta as linhas de resíduo a partir de NF-e autorizada e leva a chave para as observações (`mtr/MtrPuxarDaNotaDialog.tsx:1-12,175-176`); exige o material ligado a um resíduo salvo em Materiais | usado no cap04, explicado no cap09 |

## 1. Menu e tela
- Menu "Fiscal & Ambiental" › "Ambiental (MTR/CDF)" → `/fiscal-ambiental/ambiental/mtr` (`config/routes.ts:442`); título "Ambiental"
  (`pages/NotasFiscais.tsx:210-217`); sub-abas "MTR" e "CDF" (`:181-184`); selo da cota "<usados>/<limite> Documentos" no cabeçalho
  (`:1846-1890`), a mesma das notas.
- MTR: título "Manifesto de Transporte de Resíduos (MTR)" (`pages/NotasFiscais.tsx:1974-1980`); sub-abas sublinhadas "Manifestos" e
  "Configurações" (`mtr/MtrTab.tsx:252-275`).
- CDF: título "Certificado de Destinação Final (CDF)" (`pages/NotasFiscais.tsx:1981-1987`). Nessa aba aparecem os cartões de NF-e
  "Notas Emitidas / Notas Pendentes / Rejeitadas/Canceladas" (`:1916` não esconde no CDF): a câmera não para neles (handoff H1).

## 2. MTR › Configurações · `mtr/MtrConfigCard.tsx`, `mtr/MtrResiduosSalvosCard.tsx`
- "Configuração do MTR" (`:244-248`); "Sistema:" + nome do sistema do banco (`:250-254`); sem acesso: "Configure o acesso ao SIGOR para
  emitir MTR." (`:256-264`); com acesso: "Acesso validado" / "Acesso salvo, teste pendente" / "Acesso recusado no último teste" e
  "Teste o acesso salvo antes da próxima emissão." (`:265-300`).
- Campos (modo senha, `:340-433`): "CPF da pessoa usuária do SIGOR *" ("É o CPF da pessoa cadastrada que acessa o portal. Não use o CNPJ
  da empresa nem o e-mail de acesso."), "Senha do SIGOR *" ("É a mesma senha que você usa para entrar no portal do SIGOR..."),
  "Código da unidade geradora *" ("Ex: 12345"; "É o número exibido no portal do MTR ao lado do nome da empresa."), "Ambiente"
  ("Produção" / "Homologação (testes)"). Botões "Salvar acesso" (`:436-449`) e "Testar acesso salvo" (`:450-464`).
- "Dados do SIGOR" (só com acesso, `:468-509`): "Sincronize os códigos oficiais de resíduo, classe, unidade e tratamento do SIGOR.
  Transportadores e destinadores continuam sendo cadastrados por você no próprio formulário." + "Sincronizar dados do SIGOR".
- "Resíduos salvos" (só com acesso e dados sincronizados, `MtrResiduosSalvosCard.tsx:186-370`): "Novo resíduo"; "Salve aqui o resíduo que
  você mais emite (ex.: Vidro, Sucata de ferro) com classe, estado físico, acondicionamento e tratamento já preenchidos. Na hora de emitir
  o MTR, basta escolher o resíduo salvo em vez de garimpar entre os 895 códigos do IBAMA."; formulário "Novo resíduo salvo": "Nome do
  resíduo *" ("Ex: Vidro"), "Código IBAMA *" ("Buscar código IBAMA...", busca "Digite o código ou descrição..."), "Classe *" ("Lista
  oficial filtrada pelo resíduo selecionado."), "Estado físico *", "Acondicionamento *", "Tratamento *", "Unidade *", "Densidade"
  ("Obrigatório quando a unidade é Litro ou m³."); "Cancelar" / "Salvar resíduo"; vazio "Nenhum resíduo salvo ainda.".
- Toasts (`hooks/useMtr.tsx`, `hooks/useMtrResiduoPresets.tsx`): "Acesso ao SIGOR salvo" (`:377`), "Acesso ao SIGOR validado" (`:440`),
  "Dados do SIGOR sincronizados" (`:408`), "Resíduo salvo" (`useMtrResiduoPresets.tsx:103`).
- Backend: `company_fiscal_config.uf`, `mtr_uf_sistema`, `mtr_sistemas` (`useMtr.tsx:163-210`), `mtr_credentials` + RPC
  `mtr_set_credential` (`:350-377`), edge `sigor-mtr-sync-ref` (sincronizar, testar acesso e classes permitidas, `:390-470`), tabelas de
  referência `mtr_ref_*`, `mtr_residuo_presets`.

## 3. Materiais → "Resíduo do MTR" (ligar o material ao resíduo salvo)
- `pages/Materiais.tsx:2185-2215`: no "Editar Material" (`:2447`), campo "Resíduo do MTR" ("— Nenhum —" ou o resíduo salvo; sem resíduo:
  "Nenhum resíduo salvo. Cadastre em Ambiental → MTR → Configurações → Resíduos salvos."); botão "Atualizar" (`:2466`); toast "Material
  atualizado!" (`i18n/locales/pt-BR/materials.json:144`). Tabela `materials.mtr_residuo_preset_id`.

## 4. MTR › Manifestos · `mtr/MtrTab.tsx`
- "Manifestos de Transporte de Resíduos" e "Novo MTR" (`:244-305`); bloqueado, com dica: "Configure a UF da empresa em Configurações
  Fiscais.", "Configure o acesso ao SIGOR primeiro", "Sincronize os dados do órgão na aba Configurações antes de emitir." (`:226-242`);
  vazio "Nenhum MTR emitido ainda." / "Clique em Novo MTR para emitir seu primeiro manifesto." (`:318-327`).
- Colunas "Nº MTR", "Destinador", "Resíduo", "Data", "Status", "Ações" (`:349-357`); ações (ícones com título, `:386-450`): "Baixar PDF",
  "Cancelar MTR" (só "Emitido"), "Usar como modelo" ("Corrigir e tentar novamente" no erro), "Tentar novamente", "Ver tentativas".
- "Cancelar MTR <nº>": "O cancelamento será enviado ao sistema ambiental e é irreversível. Deseja continuar?", "Voltar", "Cancelar MTR"
  (`:490-516`); toast "MTR cancelado" (`hooks/useMtr.tsx:551`).
- "Histórico de tentativas" ("MTR <nº>"; selos "Autorizada", "Rejeitada", "Revisar campos", "Confirmar no órgão"...; "Fechar")
  (`mtr/MtrAttemptHistoryDialog.tsx:18-70`). Tabela `mtr_manifest_attempts`.
- PDF: link assinado do storage `nfe-danfes` aberto em aba nova (`MtrTab.tsx:146-160`, `useMtr.tsx:676`).

## 5. "Novo MTR" · `mtr/NovoMtrModal.tsx`
- Título "Novo MTR", "Manifesto de Transporte de Resíduos." (`:1273-1279`); etapas "Transporte e destino", "Resíduos", "Responsável"
  (`:207-211`); rodapé "Cancelar"/"Voltar", "Avançar", "Emitir MTR" ("Emitindo...") (`:1243-1268`); "Resumo do MTR" com "Transportador",
  "Destinador", "Expedição", "Motorista", "Placa", "Resíduos" ("1 pronto"), "Responsável" (`:870-889`) e "Tudo pronto para emitir o MTR".
- Etapa 1 (`:1336-1432`): "TRANSPORTE E DESTINO"; "Transportador *" e "Destinador *" ("Selecione o transportador", busca "Buscar
  transportador...", "Cadastrar novo transportador" → "Razão social *", "CNPJ *", "Código da unidade no SIGOR *", "Cancelar", "Salvar e
  usar"; toast "Parceiro salvo") (`:456-640`; `useMtr.tsx:581-603`); "Os códigos das unidades são obtidos no cadastro de cada parceiro no
  SIGOR/SINIR."; "Motorista", "Veículo / placa" (frota), "Data de expedição *" ("A data de expedição não pode ser anterior a hoje");
  "Use a mesma frota do MDF-e e das Coletas, ou digite motorista e placa livremente.".
- Etapa 2 (`:1436-1772`): "RESÍDUOS", "Puxar da nota fiscal", "Adicionar resíduo"; por linha "Usar resíduo salvo" ("Preencher a partir de
  um resíduo salvo"), "Código IBAMA *", "Classe *", "Estado físico *", "Acondicionamento *", "Tratamento *", "Quantidade *", "Unidade *",
  "Densidade", "Observação do resíduo".
- "Puxar da nota fiscal" (`mtr/MtrPuxarDaNotaDialog.tsx`): "Monta os resíduos do MTR a partir das NF-e autorizadas e leva a chave pra
  Observações do Gerador."; busca "Buscar por número, parceiro ou chave..."; "Cancelar" / "Conferir (1)"; prévia "1 nota escolhida: <nº>",
  "Resíduos que serão criados", "<resíduo salvo>" / "IBAMA <código> · 1 item · <material>", "1 item convertido de quilo para tonelada.",
  "Vai pra Observações do Gerador" + a chave; "Voltar" / "Usar no MTR" (`:130-330`). Só NF-e autorizada com chave; material sem resíduo
  ligado fica de fora ("Vincule o material ao resíduo salvo em Materiais").
- Etapa 3 (`:1794-1835`): "RESPONSÁVEL", "Nome do responsável *", "Cargo *" ("Ex: Gerente ambiental"), "Observação".
- Sucesso (`:1197-1240`): "MTR emitido" / "O manifesto foi enviado ao sistema ambiental com sucesso.", "MTR emitido com sucesso", "Nº do
  manifesto: <nº>", "Baixar PDF", "Concluir"; toast "MTR emitido" (`useMtr.tsx:522`).
- Backend: `mtr_manifests`, `mtr_manifest_items`, `mtr_parceiros`, `drivers`, `vehicles`, `invoices`/`invoice_items` (puxar), edge
  `sigor-mtr-emit` (`useMtr.tsx:486`).

## 6. CDF · `cdf/CdfTab.tsx`, `cdf/NovoCdfModal.tsx`
- "Certificados de Destinação Final" e "Novo CDF" (`CdfTab.tsx:159-252`); bloqueios "Configure a UF da empresa em Configurações Fiscais.",
  "Configure o acesso ao SIGOR na aba MTR primeiro" (`:143-158`); vazio "Nenhum CDF emitido ainda." (`:289-294`); colunas "Nº CDF",
  "Período", "Gerador", "Status", "Ações" (`:321-327`); menu "Ações": "Baixar PDF", "Gerar PDF", "Ver erro", "Tentar novamente", "Excluir
  rascunho" (`:165-232`).
- "Novo CDF" / "Certificado de Destinação Final." (`NovoCdfModal.tsx:404-408`); etapas "Período", "Destinador", "Gerador", "MTRs",
  "Confirmar" (`:48`):
  - "PERÍODO": "Data inicial *", "Data final *" (sem data futura: "O período do CDF não pode estar no futuro. O certificado cobre
    destinação já ocorrida.").
  - "DESTINADOR": "O destinador é a sua empresa (quem recebeu o resíduo). Os dados vêm do seu acesso ao SIGOR/SINIR."; "CNPJ do destinador *"
    (vem com o CNPJ da empresa), "Nome do responsável *".
  - "GERADOR (opcional)": "Informe o gerador se quiser emitir o certificado por gerador..."; "CNPJ do gerador", "Unidade no SIGOR"
    ("Para incluir o gerador, preencha CNPJ e unidade juntos.").
  - "MTRs INCLUÍDOS": "Números dos MTRs" ("Um número por linha, ou separados por vírgula"; "<n> MTR(s) informado(s) (duplicados removidos).").
  - Confirmar: "Atenção: os MTRs informados precisam já ter sido recebidos no SIGOR. Se ainda não deu baixa no recebimento, faça isso no
    portal do órgão antes de emitir o CDF."; "A emissão do CDF é definitiva e não pode ser cancelada pelo sistema. Confira os dados antes de
    confirmar."; "Observação"; resumo "Período:", "Destinador:", "Gerador:", "MTRs:".
  - Rodapé "Cancelar"/"Voltar", "Avançar", "Emitir CDF" ("Emitindo..."); sucesso "CDF emitido" / "O certificado foi emitido no sistema
    ambiental com sucesso.", "Nº do certificado: <nº>", "Baixar PDF" ou "CDF emitido. O PDF ficará disponível na lista em instantes.",
    "Concluir" (`:325-395`).
- Toasts (`hooks/useCdf.tsx`): "CDF emitido" (`:356`), "PDF gerado" (`:414`). Backend: `mtr_cdf`, `mtr_credentials`, `companies`, edge
  `sigor-cdf-emit` (`:292,386`), storage `nfe-danfes`. CDF só com protocolo "sinir" ou "feam" (`:127`).

## 7. Handoffs (o app; a fala não depende)
- H1. A aba CDF mostra os cartões de contagem de NF-e (`pages/NotasFiscais.tsx:1916`).
- H2. A fonte manda "copiar a unidade SIGLA - Nome": no código ela é escolhida na lista; o aviso da fonte está desatualizado.
- H3. O resumo do CDF usa travessão entre as datas ("Período: 01/10/2026 — 31/10/2026", `NovoCdfModal.tsx:669-671`): só na tela, a fala
  não lê.
