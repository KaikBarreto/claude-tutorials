# Plano · T14 — Notas Fiscais (NFS-e e NF-e)

- **Título final da aula:** Notas Fiscais: emitir NFS-e e receber as notas dos fornecedores
- **Áreas das vinhetas:** NOTAS FISCAIS · CONFIGURAÇÃO · EMISSÃO · NOTAS RECEBIDAS · RESUMO
- **Objetivo (uma frase):** configurar a parte fiscal uma vez, emitir a nota de serviço do cliente e acompanhar as notas que
  os fornecedores emitem contra o CNPJ da empresa.
- **Pré-requisito:** T20 na ordem de exibição; a base é o T13 (Financeiro) e o cadastro de serviços do T4. Aviso: "Antes:
  Relatório Financeiro e DRE".
- **Próximo:** T15 (Funcionários: Financeiro do Funcionário e Ponto Eletrônico). Aviso: "Próximo: Funcionários e Ponto".
- **Duração estimada:** ~15 min de fala natural (14 blocos). 🔒 Módulo **Emissão de Notas Fiscais**.
- Base: `T14/inventario.md` (código 1.38.6). Rótulos entre aspas = exatamente como na tela. Emissor, prefeitura e Receita
  **simulados**; certificado, CNPJ e inscrições fictícios.

## Capítulos propostos

| # | Vinheta (área / título) | O que a tela mostra | Avisos na tela (positivos) | Duração |
|---|---|---|---|---|
| 0 | — | Menu "Notas Fiscais": estado guiado "Configure seus dados fiscais". Fala: a nota do serviço sai daqui, sem abrir outro sistema. | "Antes: Relatório Financeiro e DRE" · "Módulo Emissão de Notas Fiscais" | 0:35 |
| 1 | NOTAS FISCAIS / A nota do serviço | Ilustração: serviço prestado → NFS-e → prefeitura (ISS) e, do outro lado, fornecedor → NF-e da compra → empresa. Na tela: abas "Notas Fiscais", "Relatório fiscal", "Emissões automáticas", "Notas recebidas" e o selo da cota. | "Configura uma vez, emite sempre" | 0:50 |
| 2 | CONFIGURAÇÃO / Os dados da empresa | "Configurações fiscais" → "1. Empresa": "Razão social / Nome" e "CNPJ" (já vêm do cadastro), "Inscrição Municipal" (fictícia), "CEP" preenche o endereço (zoom), "Ambiente de emissão de NFS-e" (decisão 2); "Verificar cobertura do município" → "Município liberado para emissão de NFS-e."; "Salvar dados da empresa" → "Dados da empresa salvos."; "Status da emissão" (zoom); "Próximo: enviar certificado". | "Dica: confere a cobertura antes de tudo" | 1:20 |
| 3 | CONFIGURAÇÃO / O certificado digital | "2. Certificado A1": "Selecionar arquivo (.pfx / .p12)" (arquivo fictício); "Nome do certificado (opcional)" Certificado da empresa; "Senha do certificado" (mascarada); marca a autorização (zoom em "Ler a Seção 12 dos Termos de Uso"); "Enviar certificado" → "Certificado enviado com sucesso."; "Certificado válido até …"; "Registro de uso do certificado" com "Certificado enviado". | "É o certificado que assina as notas" | 1:15 |
| 4 | CONFIGURAÇÃO / A tributação | "3. Tributação": "Regime tributário" "Simples Nacional"; "Apuração de tributos no Simples Nacional" (1ª opção, zoom na dica); "Percentual de tributos do Simples Nacional (%)" 6,00 (valor do contador, fictício); "Salvar tributação" → "Configurações fiscais salvas."; selo "Apto a emitir". | "O percentual vem do seu contador" | 1:00 |
| 5 | CONFIGURAÇÃO / Os serviços com código | "4. Serviços": dica do topo; abre "Manutenção Preventiva" (T4) na aba fiscal: código de tributação, NBS, código municipal (3 dígitos), alíquota em branco (Simples); salva. | "Preenche uma vez, toda nota já vem pronta" | 1:00 |
| 6 | EMISSÃO / Pessoas e serviço | "Nova Nota" → "Nova NFS-e": "Pessoas": "Data de competência" (mês atual), "Regime de apuração (Simples Nacional)" "Competência", "Tomador do serviço" Hotel Mirante do Mar; "Avançar" → "Serviço": "Serviço" Manutenção Preventiva (grupo "Prontos para emitir") → códigos preenchidos; "Discriminação do serviço" (texto do mundo); zoom no resumo "Pronta para emitir". | "Escolhendo o serviço, os códigos já vêm" | 1:20 |
| 7 | EMISSÃO / Valores e emissão | "Valores": "Valor do serviço" 1.200,00; "Alíquota ISS %" em branco (aviso do Simples, zoom); "Retenção do ISS" "Não retido"; "Percentual…" já preenchido; "Prévia do cálculo"; "Avançar" → "Revisar e Emitir": "Pré-visualização da NFS-e", "Número será atribuído após emissão"; "Emitir NFS-e" → "Processando emissão..." → "NFS-e enviada para emissão.". | "Revisa tudo antes de emitir" | 1:20 |
| 8 | EMISSÃO / Nota autorizada | Detalhe: "Processando…" → "Autorizada": "Nota nº", "Protocolo", "Chave de acesso" (zoom); "Ver PDF" (PDF fictício) → "Voltar"; "Histórico". Lista: linha "Autorizada", zoom em "Baixar PDF" e "Baixar XML"; indicadores "Autorizadas". | "O PDF sai na hora, quando você pedir" | 1:10 |
| 9 | EMISSÃO / Rascunho e cancelamento | "Nova Nota" para Academia Ponto Forte até "Serviço" → "Salvar rascunho" → "Rascunho salvo."; na lista, ações "Continuar preenchendo"/"Excluir rascunho" (zoom). Nota autorizada → "Cancelar nota": janela com o texto e "Motivo do cancelamento" (zoom no limite de caracteres) → "Voltar". | "Rascunho não vai pra prefeitura" | 1:00 |
| 10 | NOTAS FISCAIS / Nota automática do contrato | Contratos → "PMOC - Hotel Mirante do Mar" → "Financeiro" → "Nota fiscal automática" "Ligada", "Quando a nota sai" "No vencimento da parcela"; volta a Notas Fiscais → "Emissões automáticas" com o agendamento "Na fila" (semente). | "Cada parcela gera a sua nota sozinha" | 1:00 |
| 11 | NOTAS RECEBIDAS / As notas dos fornecedores | "Notas recebidas" → "NF-e": "Ligar recebimento automático" → toast; "Sincronizar" → "1 nota(s) nova(s) encontrada(s)."; linha da Ventura Gás e Tubos com selo "Resumo". | "Toda nota contra o seu CNPJ chega aqui" | 1:00 |
| 12 | NOTAS RECEBIDAS / Ciência e conta a pagar | "Manifestar" → "Dar ciência da operação" → "Enviar manifestação" → toast; "Lançar conta a pagar" → formulário preenchido ("Compra · Ventura Gás e Tubos") → "Salvar" → selo "Lançada". | "A compra vira conta a pagar num clique" | 1:05 |
| 13 | RESUMO / Recapitulando | Montagem: "Apto a emitir", nota autorizada, PDF, emissões automáticas, nota recebida "Lançada". | "Próximo: Funcionários e Ponto" | 1:00 |

Transições faladas: 1→2 "Antes da primeira nota, a configuração, que é feita uma vez só"; 3→4 "Com o certificado no lugar,
falta dizer como a empresa paga imposto"; 5→6 "Tudo pronto: bora emitir a nota do PMOC do hotel"; 8→9 "E se a nota ainda
não estiver pronta, ou precisar ser desfeita?"; 9→10 "Pra contrato que se repete todo mês, dá pra deixar a nota sair
sozinha"; 10→11 "Agora o caminho inverso: as notas que chegam pra você". Recap → próximo: "Com o dinheiro e as notas em dia,
o próximo passo é a equipe: o financeiro de cada funcionário e o ponto eletrônico."

**Falas dos cuidados ⚠️** (regra de 30/10 20:56: caminho certo primeiro, consequência numa frase, sem encenar falha):

| Cuidado | Fala sugerida | Na tela |
|---|---|---|
| Certificado | "É só enviar o certificado aqui: é ele que libera a emissão da nota." | Seção "2. Certificado A1" |
| Cobertura do município | "Uma dica: confere se o município está na cobertura antes de emitir, assim a nota passa direto." | "Verificar cobertura do município" |
| Simples Nacional | "No Simples, o percentual de tributos vai em toda nota; ele já vem da tributação que você salvou." | Campo preenchido |
| Alíquota no Simples | "Sem retenção, a alíquota fica em branco, do jeito que a prefeitura pede pro Simples." | Aviso amarelo |
| PDF | "O PDF da nota aparece quando ela está autorizada; dá pra ver aqui ou baixar." | "Ver PDF" |
| Reemitir | "Nota cancelada continua na lista com o número dela; a nota nova sai com outro número." | Zoom no cancelamento (sem cancelar) |
| Cliente sem documento | "Pra emitir, o cliente precisa de CPF ou CNPJ e endereço; os dados ficam na aba Fiscal do cadastro." | Tomador completo |

## Mundo fictício

**Começa com** (fim do T20): Glacial Cold Brasil com CNPJ fictício 91.520.340/0001-07 e endereço do seed (Rua Moreira César,
200, Icaraí, Niterói/RJ, CEP 24230-190); Camila (admin); Hotel Mirante do Mar (CNPJ fictício 91.234.502/0001-32, endereço
completo) e Academia Ponto Forte; tipo de serviço "Manutenção Preventiva" (T4); contrato PMOC do hotel com parcelas (T11/T13);
despesa "Gás R-410A e tubos de cobre" da Ventura Gás e Tubos já paga (T13). Módulo `nfe` ligado. Nada fiscal configurado.

**Esta aula cria:**

| Item | Valores (fictícios) |
|---|---|
| Configuração | IM fictícia "000123-4" · ambiente conforme decisão 2 · município Niterói (IBGE pelo CEP) liberado · empresa registrada |
| Certificado | arquivo `certificado-ficticio.pfx` (bytes aleatórios, não é certificado) · senha fictícia mascarada · válido até +1 ano |
| Tributação | Simples Nacional · apuração "Tributos federais e municipal (ISS) recolhidos pelo Simples Nacional" · percentual 6,00 % |
| Serviço | Manutenção Preventiva com códigos fiscais da fixture do simulado (a validar com um contador; inventário, dúvida 4) |
| NFS-e autorizada | Hotel Mirante do Mar · "Manutenção preventiva mensal do PMOC - <mês>/2026 - Hotel Mirante do Mar" · R$ 1.200,00 · ISS não retido · nº 1 · chave e protocolo fictícios |
| Rascunho | Academia Ponto Forte · "Manutenção mensal dos splits" · R$ 380,00 |
| Nota automática | contrato PMOC do hotel · "No vencimento da parcela" · 1 agendamento "Na fila" (semente) |
| Nota recebida | NF-e da Ventura Gás e Tubos (CNPJ fictício do seed) · R$ 640,00 · ciência dada · conta a pagar lançada e vinculada |

**Fica para as próximas:** a nota no Portal do Cliente do hotel (seção "Notas fiscais", se liberada no T12) e a cota usada.

## Gravação (modo fakebase)

**Já coberto:** schema das tabelas fiscais; `cep-lookup` e ViaCEP falsos; cadastro do T3/T4; Financeiro do T13.

**Falta** (inventário 4.3), em ordem de prioridade:

1. Handlers de edge: `nfse-register-company` (grava `provider_company_id`), `nfse-check-coverage` (`{pode_emitir:true}` e grava em
   `company_fiscal_settings`), `nfse-upload-certificate` (multipart; grava `provider_certificate_id`, `certificate_expires_at`
   +1 ano e o evento "upload" em `fiscal_certificate_audit`), `nfse-tax-codes` (lista curta de códigos), `nfse-save-draft`,
   `nfse-emit` (202, status `processando`), `nfse-status` (vira `autorizada` com número, protocolo, chave, `pdf_url`, `xml_url`,
   evento em `nfse_events`), `nfse-danfse`, `nfse-delete-draft`, `dfe-sync` (cria `inbound_nfe` e devolve `{ok, novas:1}`),
   `dfe-manifestar`.
2. RPCs `nfse_can_emit` (nível 1, limite 200, usadas no mês), `record_certificate_custody_consent` (void); seed `nfse_tiers`.
3. Arquivos fictícios no storage: PDF da nota (layout próprio, sem brasão real, "SEM VALOR FISCAL") e XML.
4. Upload do `.pfx` no gravador (passo de escolher arquivo); se não der, semear o certificado e mostrar só o formulário (decisão 3).
5. Semente de `nfse_auto_jobs` para a aba "Emissões automáticas" e, se preciso, `inbound_nfe` antes do "Sincronizar".
6. Relógio do navegador congelado (TRILHA 5): competência não pode ser futura; validade do certificado.
7. Estados `seeds-extra/t14/apos-capNN.json`. Desktop 1280×800. "Baixar PDF/XML" (nova aba/download) só com zoom.

## Pronúncias novas para o TTS

| Tela / legenda | Texto do TTS |
|---|---|
| NFS-e | éne-éfe-ésse-é (testar; alternativa "nota fiscal de serviço") |
| NF-e | éne-éfe-é |
| ISS | i-ésse-ésse |
| NBS | éne-bê-ésse |
| IBGE | i-bê-gê-é |
| Certificado A1 / .pfx | certificado á um / pê-éfe-xis |
| XML / PDF | xis-ême-éle / pê-dê-éfe |
| Simples Nacional | simples nacional |
| 6,00 % / R$ 1.200,00 | seis por cento / mil e duzentos reais |

## Riscos e decisões para o Kaik

1. **Nome da empresa:** "Glacial Cold Brasil" aparece no código e nas migrações do app como uma empresa cliente real (o CNPJ
   real não foi copiado). Nesta aula o nome sai num documento fiscal (PDF da nota, "Prestador"). Confirmar que é intencional.
2. **Ambiente:** gravar em "Produção" (as falas dizem "nota que vale", tudo simulado) ou em "Homologação" (padrão do app, "notas
   de teste")? Proposta: Produção na tela, com o simulado garantindo que nada sai.
3. **Upload do certificado:** desenvolver o passo de escolher arquivo no gravador (proposta) ou semear o certificado e mostrar
   só o formulário preenchido?
4. **Cancelar de verdade?** Cancelamento é irreversível; proposta: só abrir a janela e voltar (mundo intacto). Manifestação:
   só "Dar ciência".
5. **Códigos fiscais** (cTribNac, NBS, código municipal de Niterói): usar uma fixture plausível conferida por contador ou
   enquadrar sem ler os números?
6. **PDF da nota:** se o `iframe` não renderizar no Chromium da gravação, substituir por ilustração de uma nota fictícia.
7. **Achado de segurança** (inventário 5.1): repassar ao time do app antes da gravação (não afeta o vídeo).
8. **Duração (~15 min):** dá para juntar os caps. 4 e 5 ou tirar o cap. 10 (automática) se ficar longo.
