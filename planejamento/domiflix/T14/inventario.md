# Inventário funcional · T14 — Notas Fiscais (NFS-e e NF-e) (Dominex)

> Base para o roteiro do tutorial "T14 · Notas Fiscais (NFS-e e NF-e)". Levantado em 30/10/2026 contra o código publicado
> `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3/T12.
> O Guia Técnico (`docs/guia-tecnico/secoes/T14.html`, 1.37.36) ajudou a achar as telas; onde diverge, vale o código.
> Gravação só com emissor, prefeitura e Receita **simulados** no backend falso; certificado, CNPJ e inscrições fictícios.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). **nf** = `lib/i18n/messages/app/nfse.ts` (bloco pt-br `:12-941`).
- A Dominex **emite NFS-e** (serviço) e **recebe** NF-e e NFS-e emitidas contra o CNPJ da empresa. NF-e de produto não é
  emitida por esta tela (`components/ModuleGateModal.tsx:125-128`: "Emissão de NFS-e (nota fiscal de serviço)…").
- Provedor por trás das edges: Fisqal (`https://api.fisqal.com.br`) por padrão, com opção da API nacional
  (`https://adn.nfse.gov.br`) (`supabase/functions/_shared/nfse-provider.ts:2-16`). O navegador só fala com as edges `nfse-*` e
  `dfe-*`; as `fisqal-*` não são chamadas pelo app.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | O que é NFS-e e por que configurar antes | **Bate, sem o bloco** | O acordeão "Como funciona?" **saiu** da tela em 1.37.42 (`pages/Changelog.tsx:382`); os textos ficaram no i18n sem uso (nf `:303-327`). Conceito vira fala + ilustração. Sem configuração, estado guiado **"Configure seus dados fiscais"** (`pages/NotasFiscais.tsx:266-275`). |
| 2 | Abrir "Configurações" (é um modal) — passo Empresa | **Mudou** | É uma **tela própria** `/notas-fiscais/configuracoes` desde 1.25.10 (`pages/Changelog.tsx:2820`), aberta pelo botão **"Configurações fiscais"** (`pages/NotasFiscais.tsx:232-243`); seções **"1. Empresa"**, **"2. Certificado A1"**, **"3. Tributação"**, **"4. Serviços"** (`pages/FiscalSettings.tsx:495-499`). |
| 3 | Certificado: A1 (.pfx), senha e consentimento | **Bate, com ordem forçada** | Só depois de registrar a empresa ("Passo 1 de 2… Só depois libera o certificado.", nf `:513-518,559-561`). Autorização registrada antes do envio (RPC `record_certificate_custody_consent`, `hooks/useCertificateCustodyConsent.ts:32`; `FiscalSettings.tsx:459-466`). Novo: "Registro de uso do certificado". |
| 4 | Impostos: regime, IM, município (IBGE), alíquota do ISS | **Mudou** | Seção chama **"3. Tributação"**: "Regime tributário", "Apuração de tributos no Simples Nacional", **"Percentual de tributos do Simples Nacional (%)"** (novo), "Inscrição Municipal", "Inscrição Estadual" (nf `:634-663`). IBGE vem do CEP na seção Empresa; a alíquota do ISS fica no serviço ou na nota. |
| 5 | Serviços: código de serviço padrão e NBS | **Mudou** | **"4. Serviços"** reaproveita o cadastro de tipos de serviço (T4) aberto na aba fiscal (`components/fiscal/ServicosSection.tsx`): cTribNac, NBS, cTribMun, alíquota de ISS. |
| 6 | Cota mensal | **Bate** | Selo "{n} / {limite} emitidas este mês" ou "Notas ilimitadas" (nf `:206-217`); níveis 200/500/1000/ilimitado (`supabase/migrations/20260615210000_nfse_tiers_and_quota.sql:36-40`). Modal "Limite de notas atingido" com upgrade (nf `:476-495`). |
| 7 | Emitir: Pessoas → Serviço → Valores → Emitir | **Bate** | **"Nova Nota"** → **"Nova NFS-e"** com abas "Pessoas", "Serviço", "Valores", **"Revisar e Emitir"**; resumo "Total da nota", "Base ISS", "n pendência(s) para emitir"/"Pronta para emitir"; rascunho (nf `:677-940`). |
| 8 | Simples Nacional: o percentual obrigatório | **Bate, mais fácil** | O percentual vem preenchido da Tributação e pode mudar na nota (nf `:878-886`); aviso de deixar a alíquota em branco com ISS não retido (nf `:861-862`). |
| 9 | Autorizada: número, protocolo, chave; PDF e XML | **Bate** | Detalhe com "Protocolo", "Chave de acesso", **"Ver PDF"**/**"Ver XML"** (visualizador dentro do app); lista com **"Baixar PDF"** (nova aba) e **"Baixar XML"** (nf `:218-234,419-474`). |
| 10 | Cancelar com motivo e reemitir (número novo) | **Bate** | "Cancelar nota" só em nota autorizada; motivo de 15 a 255 caracteres (`components/fiscal/NfseDetailModal.tsx:140-144,390-396`). Rejeitada se reenvia na mesma linha ("Reenviar NFS-e"). |
| 11 | Notas recebidas: consultar NF-e e NFS-e | **Bate, tela nova** | Aba **"Notas recebidas"** com "NF-e"/"NFS-e", **"Ligar recebimento automático"**, **"Sincronizar"** (nf `:93-205`). Depende só do certificado (`pages/NotasFiscais.tsx:330-337`). |
| 12 | Manifestar NF-e e lançar como despesa | **Bate** | **"Manifestar"** (4 tipos, justificativa 15 a 255) e **"Lançar conta a pagar"** (parcelas da nota) (nf `:163-204`). |

Novos sem capítulo na trilha: aba **"Emissões automáticas"** (nota de cada parcela de contrato, ligada na aba Financeiro do
contrato, `lib/i18n/messages/app/contracts.ts:781-811`; nf `:29-91`), aba **"Relatório fiscal"** ("Últimas emissões"), tomador
"Digitar manualmente", "Registro de uso do certificado" e NFS-e no Portal do Cliente (1.37.22, `pages/Changelog.tsx:762`).

Avisos da trilha:

- ⚠️ "Sem certificado a tela volta ao estado guiado e não emite" → **bate**: emitir exige município liberado + empresa registrada +
  certificado (`hooks/useFiscalSettings.ts:44-52`); a etapa "Revisar e Emitir" mostra "Emissão bloqueada" com o motivo (nf `:901-907`).
- ⚠️ "Município sem cobertura bloqueia a emissão" → **bate**: "Verificar cobertura do município" (nf `:546-556`). No vídeo o
  município é simulado como liberado.
- ⚠️ "Simples exige o percentual" → **bate** (nf `:884-885`).
- ⚠️ "Baixar PDF só em autorizada, cancelamento pendente ou cancelada" → **bate** (`components/fiscal/NfseListTab.tsx:448-468`).
- ⚠️ "Reemitir depois de cancelar gera número novo" → **bate**; nota autorizada igual devolve "Nota fiscal já emitida para este
  cliente e valor." (`supabase/functions/_shared/nfse-handlers/emit.ts:849-853`).
- 🚫 "Configuração fiscal não é página separada" → **desatualizado** (agora é tela). 🚫 "Não emite NF-e de produto" → **continua**.

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.24.35 | Nota emitida à noite não cai mais no mês seguinte | `:3648` |
| 1.25.10 | Notas recebidas buscadas sozinhas; lançar conta a pagar; configuração fiscal vira tela inteira | `:2800-2820` |
| 1.35.2 | Dados da nota completos mesmo sem rascunho | `:1723` |
| 1.36.2 | Notas Fiscais com item próprio no menu (saiu do Financeiro) | `:1607` |
| 1.37.22 | Notas fiscais no Portal do Cliente | `:762` |
| 1.37.42 | Abas no topo; o bloco "Como funciona?" saiu | `:372,382` |
| 1.37.51 | NFS-e da assinatura da Dominex (tela Assinatura, não é desta aula) | `:224` |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. O ambiente padrão é **"Homologação"** (notas de teste) (`hooks/useFiscalSettings.ts:107`; nf `:532-536`). A aula precisa
   decidir o que mostrar no interruptor (plano, decisão 2).
2. Salvar a seção Empresa **reescreve o cadastro da empresa** (nome, CNPJ, endereço em `company_settings`, que também aparecem
   em documentos e no portal) e registra a empresa no emissor automaticamente (`pages/FiscalSettings.tsx:327-376`).
3. "Ver PDF" abre o arquivo num `iframe` dentro do app (`NfseDetailModal.tsx:178,280-299`); "Baixar PDF" abre nova aba
   (`NfseListTab.tsx:363-387`). Em Chromium sem interface o visualizador de PDF pode não renderizar (dúvida 2).
4. Intermediário do serviço é aceito no rascunho e **sempre bloqueia a emissão** (`components/fiscal/NovaNotaModal.tsx:340-351`).
5. **[handoff, segurança]** `nfse_can_emit(p_company_id)` e `nfse_month_usage(p_company_id)` respondem para qualquer empresa
   (seção 5, pegadinha 1).

---

## 1. Rotas e navegação

| Tela | Como chegar | Rota / componente |
|---|---|---|
| Notas Fiscais | Menu **"Notas Fiscais"** (item próprio, fora do Financeiro) | `/notas-fiscais` (`lib/i18n/appRouteSlugs.ts:162`; `components/layout/SidebarMenuContent.tsx:184-186`) → `pages/NotasFiscais.tsx` |
| Abas | **"Notas Fiscais"** (padrão), **"Relatório fiscal"**, **"Emissões automáticas"**, **"Notas recebidas"** | estado local (`pages/NotasFiscais.tsx:86,257-262`; nf `:21-26`) |
| Configurações fiscais | Botão **"Configurações fiscais"** no topo ou do estado guiado | `/notas-fiscais/configuracoes` (`appRouteSlugs.ts:161`) → `pages/FiscalSettings.tsx`; `?config=1` antigo redireciona (`NotasFiscais.tsx:104-112`) |
| Ligar a nota automática | Contratos → contrato → aba "Financeiro" → **"Nota fiscal automática"** | `contracts.ts:781-811` |
| Dados fiscais do cliente | Cliente → "Editar" → aba **"Fiscal"** (T3) | `components/customers/CustomerFormDialog.tsx:124,370-378,595-596` |

- Cabeçalho: **"Notas Fiscais"** / "Emita e acompanhe suas NFS-e." (nf `:13-16`); filtro de período abre em **"Todos os
  tempos"** (`NotasFiscais.tsx:95`); botões "Configurações fiscais" e **"Nova Nota"** (no celular, botão flutuante)
  (`:232-252,375-384`); selo da cota logo abaixo (`:310-314`).

---

## 2. Permissões e módulos

| Item | Regra | Fonte |
|---|---|---|
| 🔒 Módulo `nfe` "Emissão de Notas Fiscais" | Gate duplo com a permissão de tela; sem um dos dois: "Você não tem acesso ao módulo de Notas Fiscais. Fale com o administrador da sua empresa." | `App.tsx:855-857`; `pages/NotasFiscais.tsx:200-212`; nf `:17-20`; `components/ModuleGateModal.tsx:125-128` |
| Tela | `screen:fiscal_notes` "Notas Fiscais" ("Emissão e consulta de notas fiscais de serviço (também exige o módulo contratado).") | `hooks/usePermissions.ts:88`; `components/fiscal/fiscalPermissions.ts` |
| Emitir | "Você não tem permissão para emitir notas fiscais." (nf `:255`) | `NfseListTab.tsx` |
| Cota | Servidor bloqueia por nível (HTTP 402 `nfse_quota_exceeded`) | `emit.ts:861-880`; `hooks/useNfseQuota.ts:7-12` |
| Notas recebidas | Só o certificado A1 (não depende de poder emitir) | `NotasFiscais.tsx:330-337`; nf `:120-125` |

---

## 3. Por tela

### 3.1 Notas Fiscais — tela principal (`pages/NotasFiscais.tsx`)

- **Estado guiado** (sem atividade fiscal, `:264-290`): "Configure seus dados fiscais" / "Configure seus dados fiscais para
  começar a emitir notas." + "Configurações fiscais"; configurado e sem nota: "Nenhuma nota emitida ainda" / "Emita sua primeira
  nota fiscal para acompanhá-la aqui." + "Nova Nota" (nf `:350-357`). As abas aparecem sempre (`:330-343`).
- **Selo da cota** (`components/fiscal/NfseQuotaBadge.tsx`; nf `:206-217`): "{used} / {limit} emitidas este mês", "Notas
  ilimitadas", "Nível {tier}"; dicas "Consumo tranquilo…", "Você já passou de 80% do limite do mês…", "Limite do mês atingido…",
  "Ainda dá para emitir {n} notas neste mês.", "Próximo nível: {nome}, até {n} notas por mês, por R$ …".
- **Indicadores** (só nas abas de emissão, `:326-328`; nf `:341-345`): "Autorizadas", "Processando", "Rejeitadas", "Canceladas".
- **Aba "Notas Fiscais"** (`components/fiscal/NfseListTab.tsx`): busca "Buscar por número, cliente, descrição, chave..." (aviso
  "Buscando em todas as notas — o filtro de status fica suspenso enquanto há busca."), "Filtros" → "Status"; colunas "Número",
  "Data", "Tomador", "Valor", "Status", "Ações" (e "Autor", "Serviço"); linha expandida com "Tomador", "Identificação",
  "Valores", "Ocorrência" (nf `:241-301`). Status: "Pendente", "Processando", "Autorizada", "Rejeitada", "Cancelada", "Falhou",
  "Rascunho", "Cancelamento em andamento" (nf `:329-339`).
- Ações por linha (`:448-572`): "Ver detalhe"; rascunho → **"Continuar preenchendo"**, **"Emitir NFS-e"**, **"Excluir rascunho"**;
  rejeitada/falhou → **"Reenviar NFS-e"**; pendente/processando → **"Atualizar status"** ("Consultando o status na
  prefeitura..." → "Status atualizado."); autorizada/cancelamento/cancelada → **"Baixar PDF"** ("Gerando o PDF da nota...",
  nova aba; erro "Não foi possível gerar o PDF agora. A nota continua válida, tente de novo em instantes.") e **"Baixar XML"**
  (só com XML; "O XML desta nota ainda não está disponível.") (nf `:246-265`).
- A tela consulta sozinha as notas não terminadas enquanto está aberta (`:182-192`).
- **Aba "Relatório fiscal"** (`components/fiscal/NfseVisaoGeral.tsx`): **"Últimas emissões"** (5 mais recentes); vazio "Nenhuma nota
  fiscal emitida ainda. Clique em "Nova Nota" para começar." (nf `:346-347`).

### 3.2 Configurações fiscais (`pages/FiscalSettings.tsx`; nf `:497-664`)

- Cabeçalho **"Configurações fiscais"** / "Dados da empresa, certificado digital e tributação para emitir suas notas.", botão
  "Voltar", selo **"Apto a emitir"** / **"Configuração incompleta"**. Seções em abas `1. Empresa`, `2. Certificado A1`,
  `3. Tributação`, `4. Serviços` (`:495-499`).
- **1. Empresa** (`components/fiscal/EmpresaSection.tsx`; nf `:519-557`): dica "Passo 1 de 2: preencha os dados e registre a
  empresa. Só depois libera o certificado."; **"Razão social / Nome"**, **"CNPJ"** ("00.000.000/0000-00"; consulta de CNPJ só
  preenche campos vazios, `FiscalSettings.tsx:401-430`), **"Inscrição Municipal"** ("Exigida pela prefeitura para registrar a
  empresa e emitir notas. É o mesmo campo da aba Tributação."), **"Endereço fiscal"**: "CEP" ("Preenche endereço, cidade e o
  código do município automaticamente."), "Logradouro", "Número", "Complemento", "Bairro", "Cidade / UF"; **"Ambiente de
  emissão de NFS-e"** "Homologação"/"Produção" ("Produção: as notas valem de verdade (têm efeito fiscal)." / "Homologação: notas
  de teste, sem valor fiscal."); **"Salvar dados da empresa"**; bloco **"Status da emissão"** ("Município: liberado para emitir
  notas" / "…liberação ainda não confirmada", "Empresa: registrada"/"não registrada", "Certificado: enviado"/"pendente");
  **"Verificar cobertura do município"** → "Município liberado para emissão de NFS-e." ou "Município ainda sem emissão de NFS-e"
  / "Não foi possível confirmar a liberação do município"; **"Próximo: enviar certificado"**.
- Salvar (`FiscalSettings.tsx:327-376`): grava `company_settings` + `company_fiscal_settings`, chama `nfse-register-company` e,
  em silêncio, a checagem de cobertura; sucesso "Dados da empresa salvos."; falha "Dados salvos, mas o registro para emissão
  falhou: …" com o quadro "Empresa ainda não registrada para emissão" (dado × plataforma) (nf `:623-632`).
- **2. Certificado A1** (`components/fiscal/CertificadoSection.tsx`; nf `:558-633`): sem registro, "Registre a empresa antes de
  subir o certificado. Volte ao passo 1. Empresa…"; **"Arquivo do certificado"** → **"Selecionar arquivo (.pfx / .p12)"**, **"Nome
  do certificado (opcional)"** ("Ex: Certificado da empresa"), **"Senha do certificado"** ("Use a senha do próprio certificado, não
  a senha do sistema.", "Mostrar senha"), **"Autorização para guardar o certificado"** com a caixa "Autorizo o Dominex a guardar
  meu certificado digital de forma criptografada e a usá-lo somente para assinar as notas fiscais que a minha empresa mandar
  emitir." e "Ler a Seção 12 dos Termos de Uso", **"Enviar certificado"** → "Certificado enviado com sucesso."; depois
  "Certificado válido até dd/mm/aaaa" (" — vence em n dia(s)." nos últimos 30 dias; "Certificado vencido em … Envie um novo.").
  Erros "Selecione o arquivo do certificado.", "Informe a senha do certificado.", "O certificado deve ser um arquivo .pfx ou
  .p12.", "Marque a autorização de guarda do certificado para continuar.".
- **"Registro de uso do certificado"** (`components/fiscal/CertificateAuditList.tsx`; nf `:584-612`): "Cada envio, uso ou remoção do
  certificado fica registrado aqui…", eventos "Certificado enviado", "Certificado usado para emitir", "…consultar a nota",
  "…cancelar a nota", "…gerar o PDF da nota", "Certificado removido"; vazio "Nenhum uso registrado ainda.".
- **3. Tributação** (`components/fiscal/ImpostosSection.tsx`; nf `:634-663`): **"Regime tributário"** ("Simples Nacional", "Lucro
  Presumido", "Lucro Real", "MEI"); no Simples, **"Apuração de tributos no Simples Nacional"** (3 opções; "Na dúvida, escolha a
  primeira opção…") e **"Percentual de tributos do Simples Nacional (%)"** ("Usado como padrão em toda nota nova… Peça o número ao
  seu contador, a gente não estima isso."); "Inscrição Municipal", "Inscrição Estadual"; **"Salvar tributação"** →
  "Configurações fiscais salvas." (`FiscalSettings.tsx:304-320`).
- **4. Serviços** (`ServicosSection.tsx`): dica "Cadastre aqui os serviços que você fatura, com os códigos fiscais de cada um. É a
  mesma lista usada nas ordens de serviço e na agenda…" + o painel de tipos de serviço abrindo na aba fiscal (código de
  tributação, NBS, código municipal de 3 dígitos, alíquota de ISS) (nf `:509-512`).

### 3.3 Nova NFS-e (`components/fiscal/NovaNotaModal.tsx`, `components/fiscal/nova-nota/*`; nf `:677-940`)

- Título **"Nova NFS-e"**; abas **"Pessoas"**, **"Serviço"**, **"Valores"**, **"Revisar e Emitir"**; resumo **"Total da nota"**,
  **"Base ISS"**, **"n pendência(s) para emitir"** / **"Pronta para emitir"** (toque mostra "Falta resolver:"); rodapé "Cancelar",
  **"Salvar rascunho"**, "Voltar", **"Avançar"** e, na última, **"Emitir NFS-e"**. Fechar com dados: "Descartar nota?" / "Você tem
  dados preenchidos. Ao cancelar, o progresso será perdido." → "Descartar"/"Voltar".
- **Pessoas**: **"Data de competência"** (não pode ser futura), **"Regime de apuração (Simples Nacional)"** "Competência"/"Caixa",
  **"Tomador do serviço"** ("Selecionar cadastrado" / "Digitar manualmente" — "Dados avulsos — não criam um cadastro de cliente,
  valem só nesta nota."), "Intermediário do serviço (opcional)" (aviso: ainda não vai na nota). Cliente sem documento: "Este
  cliente está sem CPF/CNPJ. Complete os dados fiscais antes de emitir." + "Completar cadastro" (nf `:713-773`).
- **Serviço**: **"Serviço"** ("Escolha um serviço cadastrado"; grupos **"Prontos para emitir"** e **"Sem códigos fiscais"**; dica
  "Escolha um serviço e preenchemos os códigos fiscais, a descrição e a alíquota de ISS pra você…"; depois "Preenchemos os campos
  com os dados deste serviço…"), **"Município de incidência (IBGE)"** ("Ex.: 3550308 (São Paulo)"), "Classificação fiscal":
  **"Código de tributação (cTribNac)"**, **"Código NBS"** (busca a partir de 2 caracteres), **"Código de tributação municipal
  (cTribMun)"** ("Ex.: 001"), **"Situação do ISSQN"** ("Tributada normalmente"…), **"Discriminação do serviço"** (obrigatória).
  Ajustar código que o serviço não tinha abre **"Salvar estes dados em "{serviço}"?"** → "Salvar no cadastro"/"Agora não" (nf `:776-848`).
- **Valores**: **"Valor do serviço"**, "ISS" → **"Alíquota ISS %"** (aviso do Simples sem retenção: deixar em branco), **"Retenção
  do ISS"** ("Não retido", "Retido pelo tomador", "Retido pelo intermediário"), "Retenções federais" ("PIS retido (R$)", "COFINS
  retido (R$)", "CSLL retido (R$)"; "INSS e IRRF não se aplicam neste provedor."), **"Percentual de tributos do Simples Nacional
  (%)"** (vem da Tributação), **"Prévia do cálculo (ISS x%)"** ("Valor do serviço", "ISS (devido)", "Valor líquido") (nf `:851-896`).
- **Revisar e Emitir**: **"Pré-visualização da NFS-e"** / "Número será atribuído após emissão"; blocos "Prestador", "Tomador",
  "Serviço", "Valores"; bloqueio **"Emissão bloqueada"** com "Configure o certificado digital nas Configurações Fiscais.",
  "Conclua o cadastro da empresa…", "O município ainda não está liberado…"; durante o envio "Processando emissão..."; sucesso
  **"NFS-e enviada para emissão."**; com pendência "Corrija as pendências antes de emitir." (nf `:898-939,705-711`).
- Fluxo (`NovaNotaModal.tsx:535-576`): salva rascunho (`nfse-save-draft`) e emite pelo id (`nfse-emit`); a tela abre o detalhe da
  nota nova em consulta automática (`NotasFiscais.tsx:194-198`).
- Cota estourada: **"Limite de notas atingido"** / "Você emitiu {n} de {m} notas fiscais este mês no seu nível atual…",
  "Próximo nível", **"Fazer upgrade para {nome}"** / "Agora não"; "Nível atualizado! Você já pode emitir." (nf `:476-495`).

### 3.4 Detalhe da nota (`components/fiscal/NfseDetailModal.tsx`; nf `:419-474`)

- "Nota nº {n}", "Processando…" / "Ainda em processamento — toque para atualizar."; campos "Tomador", "Valor do serviço", "ISS",
  "Emitida em", "Criada em", **"Protocolo"**, **"Chave de acesso"**, "Descrição"; **"Histórico"** (eventos de `nfse_events`).
- **"Documentos da nota"**: **"Ver PDF"** / **"Ver XML"** (só com `pdf_url`/`xml_url`) abrem "PDF da nota"/"XML da nota" dentro
  da janela, com "Voltar" e "Baixar arquivo" (`:178,280-299`). **"Atualizar status"**.
- **"Cancelar nota"** (só autorizada, `:140,306-314`): "Cancelar esta nota fiscal?" / "Esta nota já foi enviada e registrada na
  prefeitura. O cancelamento também é registrado lá e não tem volta: para cobrar de novo, será preciso emitir uma nota nova.";
  "Nota nº {n}, {cliente}, {valor}."; **"Motivo do cancelamento"** ("Obrigatório por exigência legal. Escreva entre 15 e 255
  caracteres…"; "Ex: Serviço não realizado, cobrança em duplicidade, valor incorreto."; contador "Faltam n caracteres para o
  mínimo exigido."); **"Cancelar nota"** / "Voltar" → "Cancelamento solicitado.".

### 3.5 Emissões automáticas (`components/fiscal/AutoEmissoesTab.tsx`; nf `:29-91`; contrato `contracts.ts:781-811`)

- No contrato, aba "Financeiro": **"Nota fiscal automática"** ("Ligada, o sistema emite a nota fiscal de cada parcela deste
  contrato sozinho…"), "Desligada"/"Ligada", **"Quando a nota sai"** ("Em um dia fixo do mês", "No vencimento da parcela",
  "Quando o cliente pagar"), "Dia do mês", "Descrição do serviço na nota", "Dados fiscais" (herdados do tipo de serviço:
  "Herdado do tipo de serviço:"), salvamento automático ("Salvando...", "Salvo").
- Aba **"Emissões automáticas"**: "O que está acontecendo com as notas das parcelas de contrato que têm emissão automática
  ligada."; grupos "Bloqueadas", "Falharam", "Aguardando decisão", "Em andamento", "Emitidas", "Canceladas"; status "Na fila",
  "Emitindo agora", "Emitida"…; ações **"Tentar de novo"**, **"Emitir mesmo assim"** (competência fechada), **"Ver nota"**; vazio
  "Nenhuma emissão automática ainda" / "Ligue a emissão automática na aba Financeiro de um contrato para ver os agendamentos aqui.".

### 3.6 Notas recebidas (`components/fiscal/inboundNotes/*`; nf `:93-205`)

- Sub-abas **"NF-e"** e **"NFS-e"**; sem certificado: **"Certificado digital necessário"** + "Ir para configurações fiscais"
  (`NotasRecebidasTab.tsx:182`); sem opt-in: **"Receber NF-e de fornecedores automaticamente"** / "Ligue para consultar, direto na
  Receita Federal…" (NFS-e: "…no Ambiente de Dados Nacional…") → **"Ligar recebimento automático"** → "Recebimento automático
  ligado. A primeira sincronização pode levar alguns minutos.".
- Lista: busca "Buscar por fornecedor, número ou CNPJ..."; **"Sincronizar"** ("Última sincronização: …"; "n nota(s) nova(s)
  encontrada(s)." / "Nenhuma nota nova. Está tudo em dia."); colunas "Emissão", "Fornecedor", "Número", "Valor", "Situação"
  ("Autorizada", "Cancelada", "Denegada", "Substituída"), "Manifestação" ("Sem manifestação", "Ciência dada"…), "Ações".
  Selos "Resumo" ("Só temos o resumo desta nota. Dê ciência para liberar o documento completo."), "Lançada" + "Ver lançamento".
  Vazio "Nenhuma nota recebida ainda".
- **"Manifestar"** → "Manifestar sobre a nota" / "…é enviada à Receita Federal e é irreversível."; "Dar ciência da operação",
  "Confirmar a operação", "Desconheço esta operação", "Operação não realizada"; "Justificativa" (15 a 255); **"Enviar
  manifestação"** → "Manifestação enviada. O status desta nota atualiza assim que a Receita confirmar." (nf `:167-189`).
- **"Lançar conta a pagar"** → formulário de despesa preenchido ("Os dados abaixo vieram da nota recebida. Revise antes de
  lançar."; "Compra · {fornecedor}"); com parcelas na nota, "Antes de lançar" explica as datas; "Despesa lançada e vinculada à
  nota." (nf `:190-204`).

---

## 4. Backend por tela (o que o emissor simulado precisa responder)

### 4.1 Chamadas

| Onde | Chamada | Fonte |
|---|---|---|
| Configuração | `GET/PATCH company_fiscal_settings` (regime, IM, IE, `municipio_ibge`, `fiscal_ambiente`, `reg_ap_trib_sn`, `percentual_trib_sn`; só leitura: `provider_company_id`, `provider_certificate_id`, `certificate_expires_at`, `pode_emitir`) | `hooks/useFiscalSettings.ts:11-17,57-112` |
| Empresa | `PATCH company_settings` (nome, CNPJ, endereço); edge `nfse-register-company` (sem corpo) → ok ou `{error:'missing_fields', message}` | `FiscalSettings.tsx:327-376` |
| CEP | edge `cep-lookup` (já no fakebase) → endereço + IBGE | `FiscalSettings.tsx:381-399` |
| Cobertura | edge `nfse-check-coverage` `{ibge}` → `{pode_emitir: true|false}` | `FiscalSettings.tsx:276-300` |
| Autorização | RPC `record_certificate_custody_consent {p_version}` → void | `hooks/useCertificateCustodyConsent.ts:32-57` |
| Certificado | edge `nfse-upload-certificate` (multipart `file`, `password`, `nome`) → ok/`{message}` | `FiscalSettings.tsx:468-477` |
| Registro de uso | `GET fiscal_certificate_audit` | `hooks/useFiscalCertificateAudit.ts` |
| Cota | RPC `nfse_can_emit {p_company_id}` → `{allowed, used, limit, tier, unlimited, next_tier:{tier,name,limit,price}}`; `nfse_tiers`; edge `change-nfse-tier` | `hooks/useNfseQuota.ts:30-63`; `hooks/useNfseTiers.ts`; `hooks/useNfseTierChange.ts` |
| Lista | `GET nfse_emissions` (colunas `id, …, status, numero_nfse, chave_acesso, protocolo, pdf_url, xml_url, valor_servico, valor_iss, descricao_servico, error_message, emitida_em, data_competencia…`); `nfse_events` | `hooks/useNfse.ts:57-77`; `hooks/useNfseEmissionsPaged.ts` |
| Códigos | edge `nfse-tax-codes` (busca cTribNac/NBS) | `components/fiscal/TaxCodeCombobox.tsx` |
| Rascunho | edge `nfse-save-draft` → `{emission:{id}}`; `nfse-delete-draft` | `NovaNotaModal.tsx:535-576`; `NfseListTab.tsx` |
| Emitir | edge `nfse-emit` (por `emissionId` ou corpo) → HTTP 202 `{emission, message:"Nota fiscal enviada para emissão. Acompanhe o status."}`; duplicada → `{already_emitted:true, message:"Nota fiscal já emitida para este cliente e valor."}`; cota → 402 `nfse_quota_exceeded` | `supabase/functions/_shared/nfse-handlers/emit.ts:849-880,1600-1606` |
| Status | edge `nfse-status {emissionId}` → emissão atualizada | `hooks/useNfse.ts:320` |
| PDF | edge `nfse-danfse` → `{pdfBase64 | pdfUrl, nomeArquivo}` | `NfseListTab.tsx:363-387` |
| Cancelar | edge `nfse-cancel` (motivo) | `hooks/useNfse.ts` |
| Automáticas | `nfse_auto_jobs`; RPC `nfse_auto_enfileirar {p_financial_transaction_id, p_motivo}` | `hooks/useNfseAutoJobs.ts` |
| Recebidas | `company_fiscal_settings.dfe_nfe_ativo/dfe_nfse_ativo`; `dfe_sync_state`, `inbound_nfe`, `inbound_nfse`; edges `dfe-sync` (→ `{ok, novas, aviso?}`), `dfe-manifestar` | `hooks/useInboundNotes.ts:120-440` |

### 4.2 Estados da nota (contrato para o simulado)

| Estado (`nfse_emissions.status`) | Como chega | Na tela |
|---|---|---|
| `rascunho` | `nfse-save-draft` | "Rascunho"; "Continuar preenchendo", "Emitir NFS-e", "Excluir rascunho" |
| `processando` / `pendente` | `nfse-emit` (202) | "Processando"; detalhe "Ainda em processamento — toque para atualizar." |
| `autorizada` | `nfse-status` preenche `numero_nfse`, `protocolo`, `chave_acesso`, `pdf_url`, `xml_url`, `emitida_em` | "Autorizada", "Nota nº", "Baixar PDF/XML", "Ver PDF/XML", "Cancelar nota" |
| `rejeitada` / `falhou` | `nfse-status` com `error_message` | "Reenviar NFS-e" (não usar no vídeo) |
| `cancelamento_pendente` → `cancelada` | `nfse-cancel` e depois `nfse-status` | "Cancelamento em andamento" → "Cancelada" |

### 4.3 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Hoje | Falta |
|---|---|---|
| Tabelas fiscais (`company_fiscal_settings`, `nfse_*`, `fiscal_certificate_audit`, `inbound_*`, `dfe_sync_state`) | No schema, sem seed | `nfse_tiers` (4 níveis) e o estado inicial de `company_fiscal_settings` (vazio, `fiscal_ambiente` a decidir) |
| Edges `nfse-*`, `dfe-*` | **Sem handler** (`{}` com 200, `rec/fakebase/http/functions.mjs:32-35`): registrar "funciona" sem preencher `provider_company_id`; cobertura volta sem `pode_emitir`; emitir não cria nota | Handlers listados no plano (registro, cobertura, certificado, códigos, rascunho, emitir, status, PDF, cancelar, sync, manifestar) |
| RPCs `nfse_can_emit`, `record_certificate_custody_consent`, `nfse_auto_enfileirar` | `nfse_can_emit` devolve `{}` → selo sem limite (a confirmar) | Handler da cota (`used` = autorizadas do mês, `limit 200`, nível 1) e do consentimento (void) |
| CEP → IBGE | `handlers/functions/cep-lookup.mjs` e `handlers/ext/viacep.com.br.mjs` existem | Conferir se devolvem o IBGE de Niterói (3303302) |
| PDF/XML da nota | Nada | DANFSe fictícia (PDF) e XML fictício no storage do fakebase, com CNPJ/IM fictícios e marca d'água "SEM VALOR FISCAL" |
| Upload do .pfx | O gravador não escolhe arquivos (a confirmar com `setInputFiles`) | Arquivo fictício `certificado-ficticio.pfx` (bytes aleatórios) + passo de upload no gravador |

---

## 5. Pegadinhas para roteiro e gravação

**[handoff]** = vale pedir correção ao time do app.

1. **[handoff, segurança]** `nfse_can_emit(p_company_id)` (`supabase/migrations/20260615210000_nfse_tiers_and_quota.sql:115-190`)
   e `nfse_month_usage(p_company_id)` (`supabase/migrations/20260825140000_nfse_month_usage_exclui_rascunho.sql:21-35`) são
   `SECURITY DEFINER`, não conferem se a empresa é a do usuário e ficam liberadas para qualquer usuário logado
   (`supabase/migrations/20260912150000_fecha_execute_anon_rpcs_security_definer.sql:94-137`). Quem souber o id de outra empresa lê
   o nível e quantas notas ela emitiu no mês. Gravidade baixa (dado comercial, exige o id). Comparar com
   `cash_flow_opening_balances`, que usa `get_user_company_id(auth.uid())` (`20261018230000_...:264-268`).
2. **[handoff]** Textos do "Como funciona?" e do modal antigo "Nova Nota Fiscal" seguem no i18n sem uso (nf `:303-327,359-417`);
   e o Guia Técnico ainda descreve o bloco (limpeza).
3. Salvar "1. Empresa" muda o nome, CNPJ e endereço da empresa no sistema todo (`FiscalSettings.tsx:322-349`): no mundo
   fictício os dados precisam ser os mesmos do cadastro (Glacial Cold Brasil, CNPJ fictício do seed).
4. Ambiente padrão "Homologação" (`useFiscalSettings.ts:107`): emitir em homologação gera nota "de teste"; a fala precisa
   combinar com o que o interruptor mostra (plano, decisão 2).
5. O certificado só aceita depois de registrar a empresa; na gravação seguir a ordem 1 → 2 (sem encenar o aviso).
6. "Baixar PDF" abre nova aba (não aparece no vídeo); usar "Ver PDF" no detalhe (`NfseDetailModal.tsx:280-299`).
7. Intermediário bloqueia a emissão sempre (`NovaNotaModal.tsx:340-351`): não preencher.
8. No Simples com ISS "Não retido", a alíquota fica em branco (aviso amarelo); o serviço do T4 não deve trazer alíquota
   preenchida, senão o aviso aparece (`nf :861-862`).
9. "Relatório fiscal" é só "Últimas emissões" (5 notas): o nome promete mais do que mostra.
10. A competência da nota não pode ser futura; com o relógio do navegador solto, a data do mundo pode virar "futura" (TRILHA 5).
11. Status "Cancelamento em andamento" conta junto de "Autorizadas" nos indicadores (Guia T14, cap. 1).
12. Notas recebidas dependem do certificado, não da emissão: a aba funciona mesmo sem nota emitida.
13. Manifestação e cancelamento são irreversíveis (textos da própria tela): no vídeo, manifestar só "Dar ciência da operação" numa
    nota fictícia e não cancelar nota (plano, decisão 4).

---

## 6. 🚫 Não prometer

- 🚫 Emitir NF-e de produto (a emissão é NFS-e; NF-e só como nota recebida).
- 🚫 Intermediário na nota emitida. 🚫 INSS e IRRF retidos ("não se aplicam neste provedor").
- 🚫 Município fora do padrão nacional emitindo pela Dominex.
- 🚫 Link fixo do PDF da nota (é gerado sob demanda). 🚫 Carta de correção (não há tela).
- 🚫 Que o sistema calcula o percentual do Simples (o contador informa).
- 🚫 Configuração fiscal num item próprio do menu (só pelo botão dentro de Notas Fiscais).

---

## 7. Dúvidas em aberto (só rodando)

1. Com `nfse_can_emit` sem handler (`{}`), o selo mostra "0 / … emitidas" ou some? (`parseQuota` dá `limit null` sem `unlimited`)
2. O `iframe` do "Ver PDF" renderiza PDF no Chromium da gravação (sem visualizador embutido no modo sem interface)?
3. O `cep-lookup` do fakebase devolve o código IBGE (o app usa `ibge`/`codigo_ibge`, `FiscalSettings.tsx:390`)?
4. O painel "4. Serviços" com o T4 gravado: qual tipo de serviço já existe ("Manutenção Preventiva") e com quais campos fiscais?
5. "Emissões automáticas" precisa de parcela de contrato com nota ligada e uma execução da fila (`nfse-auto-runner`): vale semear
   um agendamento "Emitida" para a aba não ficar vazia?
6. A sincronização de notas recebidas cria as linhas pela própria edge (handler) ou basta semear `inbound_nfe` antes?

## 8. Termos e pronúncias

| Termo | Na tela | Leitura sugerida |
|---|---|---|
| NFS-e | "Nova NFS-e" | nota fiscal de serviço (na 1ª vez) / éne-éfe-ésse-é |
| NF-e | sub-aba "NF-e" | éne-éfe-é |
| ISS / ISSQN | "Alíquota ISS %", "Situação do ISSQN" | i-ésse-ésse |
| NBS | "Código NBS" | éne-bê-ésse |
| cTribNac / cTribMun | rótulos dos códigos | "código de tributação nacional/municipal" (não soletrar) |
| IBGE | "Município de incidência (IBGE)" | i-bê-gê-é |
| A1 / .pfx / .p12 | "Certificado A1", "(.pfx / .p12)" | á um / pê-éfe-xis / pê-doze |
| DANFSe | (Guia) | "o PDF da nota" (evitar a sigla) |
| XML | "Ver XML" | xis-ême-éle |
| MEI | "MEI" | mêi |
| PIS / COFINS / CSLL | retenções | pis / cófins / cê-ésse-éle-éle |
