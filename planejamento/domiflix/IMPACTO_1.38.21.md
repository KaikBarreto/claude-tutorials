# Impacto da Dominex 1.38.21 nas aulas da Domiflix

> Levantamento de 05/11/2026, só leitura. Compara `src-1.38.19` (main `24f499ba`, base das gravações) com `src-1.38.21`
> (main `a68adc13`, conferido no `origin/main` do clone antes de exportar: **não avançou além do `a68adc13`**; `.commit` = `a68adc138d3a83ef4344fbad58249f5ade47512b 1.38.21`).
> Cobre `36c6303f` (Domiflix, contratação vai para a assinatura), `b5ebd555` (1.38.20, edição da OS no preenchimento) e `f264b235` + `a68adc13` (1.38.21, NFS-e direto pelo Portal Nacional, Fisqal aposentado).
> Análise estática do código e das migrações: **nada foi rodado**. O que só se confirma na tela está marcado "(a confirmar)".
> Caminhos de código são relativos a `src-1.38.21/src/` (exceto `supabase/...`). Linhas de roteiro: `Tnn/roteiro.md:linha`.
> Nenhum `roteiro.md` nem `tts_textos.py` foi alterado: as falas novas ficam só neste arquivo.
>
> Legenda: **(a)** nada visível muda · **(b)** só o robô muda (rótulo, posição, passo novo; fala intacta) · **(c)** a fala muda ·
> **(d)** aula entregue mostra o que não existe mais ou confunde.

## 1. Resumo

| Aula | Estado | Classe | Falas que mudam | Observação curta |
|---|---|---|---|---|
| T0 / T0 v2 | entregue | (a) | 0 | `DomiflixModuleOffer`: texto e rota novos; o defeito C5 do T0 v2 (botão para endereço que não existe) está **resolvido** |
| T1 | entregue 1.38.19 | (a) | 0 | Nada de Configurações mudou |
| T2 | entregue | (a) | 0 | Permissão "Editar OS em campo": rótulo e descrição iguais; ganha efeito novo no celular (ver T7) |
| T3 v2 | entregue | (a) | 0 | |
| T4 | entregue 1.38.19 | (a) | 0 | A aba Fiscal do tipo de serviço e o handler `nfse-tax-codes` mantêm o contrato |
| T5 | entregue 1.38.19 | (a) | 0 | Assistente, detalhe da OS e "Checklists avulsos" do cap04 intactos |
| **T7** | entregue 1.38.19 | **(b)** + capítulo novo | 1 leve (L68) + 9 do capítulo novo + 1 no recap | Preenchimento da OS em visual neutro; **"Editar OS" refeito**: proposta de capítulo novo (~3 min) |
| T8 | entregue | (a) | 0 | |
| T9 | entregue | (a) | 0 | |
| T10 | só roteiro (agente) | (a) | 0 | |
| T11 | só roteiro (agente) | (a) | 0 | |
| T12 | voz pronta | (a) | 0 | `customer-portal-document-download` só no servidor |
| T13 | só roteiro (agente) | (a) | 0 | |
| **T14** | **não gravado** | por capítulo (seção 4) | 4 + 1 leve (L61, L65, L71, L161; L60 leve) | Sem registro de empresa; abas sem número; novo painel de prontidão; backend falso muda |
| T15 | só roteiro | (a) | 0 | |
| T17 | só roteiro | (a) | 0 | |
| T18 | entregue | **(b)** | 0 | Cartão "Checklists" da OS sem moldura e sem ícone (cap03) |
| T19 | só roteiro (agente) | (a) | 0 | |
| T20 | só roteiro | (a) | 0 | |
| T21 | voz pronta | (a) | 0 | Só comentário em `whatsapp-connect` e `evolution-client` |
| T22 | só roteiro | (a) | 0 | |

Falas novas que valem voz paga **agora**: T7 capítulo novo (9) + recap (1) = **10 falas, 1.860 caracteres**. O T14 não entra: ele reescreve na vez dele.
Se o Kaik quiser regravar a fala já entregue do T7: +1 fala leve (L68, 164 caracteres), recomendo **não**.

## 2. O que mudou e importa para as aulas

| Commit / versão | Efeito nas aulas |
|---|---|
| `36c6303f` Domiflix | `components/domiflix/DomiflixModuleOffer.tsx`: o botão agora vai para `/assinatura` (com `?addModule=<código>` na conta contratada); antes ia para `/billing`, que não existe. O texto de apoio troca "com o valor exato confirmado antes da contratação" por "Antes de pagar, você verá a diferença proporcional até a próxima renovação." Rótulos do botão iguais ("Adicionar ao meu plano", "Escolher meu plano") |
| `b5ebd555` 1.38.20 OS | Modal "Editar OS" refeito (`EditOsScopeDrawer.tsx`, `editOsScopeState.ts`, `hooks/useEditOsScope.ts`); visual do preenchimento do técnico em neutros (`pages/TechnicianOS.tsx`, `components/technician/*`); migration `20261104190000_edit_os_scope_movimenta_respostas_e_ordena.sql`; i18n `lib/i18n/messages/app/os.ts` (`technicianFlow.editScope.*`) |
| `f264b235` + `a68adc13` 1.38.21 NFS-e | Fisqal sai (somem `register-company`, `webhook` e as 10 funções `fisqal-*`); novo motor `providers/sefin.ts`; telas `pages/FiscalSettings.tsx`, `EmpresaSection`, `CertificadoSection`, `NovaNotaModal`, `EmitirStep`, `NotasRecebidasTab`; i18n `nfse.ts`; migration `20261104233000_aposenta_fisqal_motor_fiscal_proprio.sql`. `a68adc13` só mexe no workflow de deploy |
| `config/version.ts` | `APP_VERSION` 1.38.21 e novo `VERSION_NOTES` ("A emissão de NFS-e agora usa diretamente o Portal Nacional, com configuração fiscal mais simples e segura."). Ver G7 |

## 3. Riscos transversais (somam aos G1 a G5 do `IMPACTO_1.38.19.md`, que continuam valendo)

**G6. `MobilePillTabs.tsx`.** O botão da aba ganhou `focus:outline-none focus-visible:bg-muted/60`. Só aparece com foco de teclado; clique de mouse do robô não dispara `:focus-visible`. Nenhuma aula muda. Só observar se algum passo do robô navega abas por teclado (a confirmar).

**G7. Gaveta "novidades da versão" no celular.** O texto novo de `VERSION_NOTES` não aparece em aula nenhuma, mas a gaveta (`components/pwa/VersionUpdateNotification.tsx`) abre quando a versão vista é diferente da atual. O `setup` das gravações no celular (T7, T15 cap9) tem de gravar a versão **1.38.21** como vista; se ele tem "1.38.19" escrito à mão, a gaveta cobre a tela (a confirmar no `setup` do robô: ler `APP_VERSION` em vez de número fixo).

**G8. Relógio do navegador e certificado.** A prontidão fiscal agora compara `certificate_expires_at` com `Date.now()` do navegador (`hooks/useFiscalSettings.ts`, `isFiscalReadyToEmit`; `NovaNotaModal`; `NotasRecebidasTab`). Com o certificado fictício válido até 10/11/2027 e o relógio do robô em `FAKE_NOW` (nov/2026), passa. Só quebra se algum capítulo avançar o relógio para depois de 10/11/2027.

**G9. Regerar o schema do fakebase.** `service_order_equipment` ganha `equipment_position` e `checklist_position` (inteiros, padrão 0); `nfse_emissions` ganha `referencia_fiscal` e `requisicao_fiscal_id` (e as 4 colunas `status_fiscal_*`, agora na tabela certa); RPC nova `nfse_next_dps_number`. `rec/fakebase/schema.json` hoje não tem as duas colunas de posição. Comando: `rec/fakebase/tools/gen-schema.mjs` apontando para `src-1.38.21` (sob `flock $TUT_HOME/.heavy.lock` se for pesado).

## 4. Detalhe por aula

### T7 · O técnico em campo (entregue 1.38.19) · **(b)** nas linhas existentes + **capítulo novo "Editar OS"**

#### 4.1 Linhas do roteiro cuja tela ou fala muda

Visual do preenchimento (`pages/TechnicianOS.tsx:3944-4090`, `components/technician/*`): as cores de ação passam de "cor da marca" para neutros (preto/branco do tema); verde só em sucesso e conclusão; o contexto da OS (check-in, cliente, descrição, observações) vira **um bloco contínuo sem cartões**; "Checklists" é título, sem moldura e sem ícone. Rótulos novos no código: `sectionDescriptionTitle` = "Descrição do serviço" (era "Descrição do Serviço"); `sectionClientTitle` = "Cliente"; `sectionNotesTitle` = "Observações"; `checkInStamp` = "Check-in:"; `panelTitle` = "Checklists"; `servicesLabel` = "Serviços desta OS" (continua igual, só perde a caixa alta).

| Linha | Classe | Tela agora (rótulos do código) | Fala |
|---|---|---|---|
| 46 | (b) | Cabeçalho na cor da marca igual; o rótulo "Serviços desta OS" deixa de ser caixa alta (11 px, peso médio) | Mantém |
| 47 | (b) | Cartão "Ir para o Atendimento" igual, sem a borda colorida. "Cliente" deixa de ser cartão: rótulo pequeno cinza, sem ícone, e o nome em destaque; telefone sublinhado em tom neutro (não mais azul) com o atalho verde de WhatsApp; endereço. "Descrição do serviço" (s minúsculo), em negrito e sem cartão; "Observações" idem, se a OS tiver | Mantém: "os dados do cliente... e a descrição do serviço" continua certa |
| 56 | (b) | Cartão "Iniciar Atendimento" com ícone neutro; o botão "Fazer Check-in" passa a **neutro** (preto no tema claro) em vez da cor da marca | Mantém |
| 60 | (b) | Mesmo cartão, botão "Fazer Check-in" neutro | Mantém |
| 66 | (b) | Toque em "Fazer Check-in" (botão neutro) | Mantém |
| 67 | (b) | Sem a faixa cinza: texto "Check-in: dd/MM/aaaa às HH:mm" com ícone de relógio; o **endereço vai para a linha de baixo**, com pino, quebrando linha (antes ficava à direita, truncado). O carimbo é a primeira linha do bloco único, acima de "Cliente" | Mantém |
| 68 | (b) + **(c) leve** | O que aparece é o **título** "Checklists" (sem ícone, sem moldura) sobre o acordeão do equipamento. Rodapé preto: "Finalizar OS" **segue verde** (mobile), "Finalizar Parcial" laranja, hambúrguer | Fala atual: "a tela ganha o cartão de Checklists, com um checklist pra cada equipamento da ordem...". **Proposta (opcional):** "Assim que o check-in é feito, a tela ganha a área de Checklists, com um checklist pra cada equipamento da ordem, e o rodapé preto, com Finalizar OS, Finalizar Parcial e o menu de mais ações." (substitui "o cartão de Checklists" por "a área de Checklists"; 164 caracteres a mais de voz se regravar) |
| 74 | (b) | Título "Checklists" sem cartão; acordeão do equipamento com borda; o subtítulo (selo do serviço) em cinza em vez da cor da marca; contador "0 de 13" | Mantém |
| 75, 78 | (b) | Perguntas **sem fundo cinza por pergunta** (linhas soltas), seção sem caixa alta; interruptor "Sim" e caixa "Normal" marcados em preto/neutro (antes cor da marca); asterisco vermelho igual | Mantém |
| 79 | (b) | O visto "Fechar edição" fica neutro (antes cor da marca) | Mantém |
| 94 | (b) | Pílulas do menu agora branco/card com borda, ícone e texto neutros (antes na cor da marca); ao tocar invertem para preto com texto branco. **"Editar OS" aparece como primeira pílula** para quem pode (o Rafael sem permissões gravadas pode, `hasPermission` devolve `roles.length > 0`); a fala não a cita neste ponto, e o capítulo novo a apresenta | Mantém |
| 105, 106, 115 | (b) | "Retomar OS" (rodapé do celular) passa a **neutro** (`bg-foreground text-background`) sobre o rodapé em degradê preto. No tema claro vira botão quase preto sobre fundo quase preto: **(a confirmar o contraste na tela)**; se ficar ilegível, é defeito do app a reportar | Mantém |
| 123 | (b) | Assinatura: o `[TESTAR P23]` continua valendo (o trecho do `DynamicFormQuestions.tsx` que imprime o valor cru não foi tocado; só mudaram classes). O selo "Concluído" do equipamento é o mesmo | Mantém |
| 157 a 159 | (b) | Montagens do recap pedem o novo visual (títulos sem moldura, botões neutros) | Mantém, mais o acréscimo da seção 4.3 |

Fora dessas linhas: cap00, cap05 (foto e vídeo), cap06 (janela "Consumir do estoque"), cap10 a cap12 (resumo do consumo, relatório, PDF, link do cliente e pesquisa) usam arquivos **sem mudança**: (a).
Cabeçalho do `roteiro.md` a atualizar quando o capítulo entrar: "versão 1.38.21" e a decisão "Editar OS pode aparecer no menu do Rafael e a fala não a cita" (passa a ter o capítulo novo).

#### 4.2 Proposta: capítulo novo "Editar OS" (cap14 no roteiro, exibido antes do recap)

**Onde entra e por quê.** Capítulo novo, **depois do cap12 (o link do cliente) e antes do recap**, com vinheta "TÉCNICO EM CAMPO". Motivos:
1. O T7 está entregue; assim ele vira **remendo** como os de T1, T4 e T5 em 04/11: grava só o capítulo novo e remonta, sem regravar cap00 a cap12 nem mexer nas sementes `apos-capNN`.
2. O principal caso de uso (checklist sem equipamento arrastado para um equipamento, com respostas) pede uma OS **diferente da #16**. Na #16 o checklist já nasce dentro do Hi-Wall, e acrescentar um segundo checklist nela mudaria as perguntas obrigatórias do cap10 (a OS só conclui com tudo respondido) e o relatório do cap11.
3. O menu "Mais ações" já foi apresentado no cap06; aqui só se mostra a pílula "Editar OS".
Numeração: usar **cap14** no roteiro e no `tts_textos.py` (chave nova), sem renumerar o recap (cap13) que já tem arquivos em `rec/t7`; a montagem coloca o cap14 antes do cap13 (decisão do Kaik na seção 6).

**Duração estimada:** ~3 min de vídeo (9 falas, 1.724 caracteres, ~2 min de voz a 2,6 palavras/s, mais vinheta e os tempos do robô para navegar e arrastar).

**Estado do capítulo (OS de bastidor).** OS nova "Em Andamento" do Rafael Lima, da **Pousada Sol Nascente**, serviço Manutenção Preventiva, equipamento **Cassete 36.000 BTUs - Recepção** (do T3), com: check-in carimbado às 08:15 (antes do `FAKE_NOW` 08:50 da #16, para não colidir), agenda da quarta 08:00 a 09:00, o Cassete **sem checklist** e o checklist "Manutenção preventiva de split" **sem equipamento**, com **5 respostas** (as 5 Sim/Não). O robô entra pela Agenda em "Dia" (cartão da OS, "Preencher OS"). Número da OS e `public_short_code`: a combinar com o agente do backend.

Tabela Tela | Fala (formato do roteiro; marcas `[BACKEND]`, `[TESTAR]`):

### cap14 · Editar a OS em campo (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Capítulo novo, logado como Rafael Lima, celular. Agenda em "Dia" (quarta): toque no cartão da OS da Pousada Sol Nascente (selo "Em Andamento"), "Preencher OS". Rolagem até o título "Checklists": um só grupo, "Manutenção preventiva de split" (com ícone de checklist, sem foto de equipamento), contador "5 de 13". [BACKEND: OS de bastidor da seção "Estado do capítulo"] | Pra fechar, um recurso que ajuda quando a ordem muda no meio do atendimento. Esta é uma ordem da Pousada Sol Nascente, já em andamento. Repara que o checklist de Manutenção preventiva de split está solto, sem equipamento, e o técnico já respondeu cinco perguntas. |
| Toque no hambúrguer do rodapé (aria "Mais ações"): a primeira pílula é "Editar OS"; toque nela: sobe a gaveta "Editar OS" (botão "Fechar" no canto) com as abas "Equipamentos" e "Data e horários"; câmera em "Estrutura da OS" e no texto "Arraste para reordenar ou mover um checklist entre equipamentos. As respostas acompanham o checklist." [TESTAR: no celular a primeira aba se chama "Equipamentos"; "Equipamentos e checklists" só no computador] | O ajuste fica no menu de mais ações. Toco em Editar OS, e abre a gaveta com a Estrutura da OS. Quem libera essa opção é o gestor, pela permissão Editar OS em campo. |
| Zoom nos dois blocos: o cartão "Cassete 36.000 BTUs - Recepção" com o contador 0 e o texto "Nenhum checklist. Arraste um item para cá ou selecione abaixo."; e o bloco tracejado "Checklists sem equipamento" ("Checklists a nível de OS, sem equipamento vinculado.") com contador 1, a linha "Manutenção preventiva de split" e o visto verde de "Respondido" (no celular aparece só o ícone). | Aqui estão o Cassete trinta e seis mil BTUs da recepção, que ainda não tem checklist, e o bloco Checklists sem equipamento, com o de Manutenção preventiva de split. O visto verde mostra que ele já tem respostas. |
| Câmera nos botões "Adicionar equipamento" (no alto) e "Selecionar checklists" (dentro do Cassete), sem tocar; passa pela lixeira de "Remover equipamento". | Na mesma gaveta, dá pra adicionar equipamento, escolher mais checklists e remover o que não vale. Se uma remoção for apagar respostas, o aplicativo pede confirmação antes. |
| Arrasto: segura a alça do checklist (aria "Arrastar checklist Manutenção preventiva de split") e leva até o cartão do Cassete: o cartão fica com contorno escuro e mostra "Solte aqui para vincular"; solta: o checklist aparece dentro do Cassete (contador 1), o bloco sem equipamento fica vazio ("Nenhum checklist...") e o botão "Salvar equipamentos e checklists" habilita. [TESTAR: o arrasto é do `@dnd-kit` com `PointerSensor` (move mais de 8 px); passo `drag` com `mouse.down`, vários `mouse.move` e `mouse.up` na emulação de celular; plano B: "Ações do checklist" > "Mover para" > "Cassete 36.000 BTUs - Recepção", mesmo efeito] | Agora, o principal. Seguro pela alça do checklist e arrasto até o Cassete. O cartão acende e mostra Solte aqui para vincular. Solto, e o checklist passa pra dentro do equipamento. |
| Toque nos três pontos do checklist (aria "Ações do checklist"): o menu mostra "Mover para" com "Checklists sem equipamento" e "Cassete 36.000 BTUs - Recepção" (o atual, apagado) e, em vermelho, "Remover checklist"; fecha com Esc, sem escolher. | Uma dica: se arrastar no celular não ajudar, o menu de três pontos do checklist faz o mesmo. Em Mover para, é só escolher o destino. |
| Toque em "Salvar equipamentos e checklists": o botão mostra "Salvando..." e aparece o aviso "OS atualizada" com "5 resposta(s) acompanhou(aram) o checklist movido." [BACKEND: RPC `edit_service_order_scope` com `moves`, devolvendo `responses_moved` = 5] | Com o checklist no lugar, toco em Salvar equipamentos e checklists. O aplicativo avisa: OS atualizada, e conta quantas respostas acompanharam o checklist movido. |
| Toque em "Fechar": a gaveta fecha. Câmera no título "Checklists": agora o acordeão é o do "Cassete 36.000 BTUs - Recepção", com "Manutenção preventiva de split" dentro e o contador "5 de 13"; abre o checklist: as 5 respostas "Sim" continuam. [BACKEND: o `onSaved` da tela recarrega `service_order_equipment` e `form_responses`; as respostas precisam ter passado a `equipment_id` do Cassete] | Fecho a gaveta. O checklist agora está dentro do Cassete, e as cinco respostas continuam lá, cinco de treze. Foi só uma troca de vínculo: nada foi apagado, e ninguém precisou responder de novo. |
| Hambúrguer, "Editar OS" de novo; toque na aba "Data e horários": "Período da OS", "Data inicial", "Data final", "Horário de cada dia" (ajuda "Ajuste o período e os horários planejados para cada dia da OS."), os campos "Início" e "Fim", "Repetir primeiro horário" e o botão "Salvar data e horários" (sem tocar). Fecha em "Fechar". [TESTAR: a aba só aparece se o Rafael tiver a permissão "Editar OS" (`fn:edit_os`) ou nenhuma permissão gravada; com o cargo "Técnico de Campo" do T2 (só "Editar OS em campo") ela some, e a fala continua certa se for cortada] [Sem internet o `isOnline` desativa a pílula e troca o texto para "Disponível apenas online"; não encenar] | Na outra aba, Data e horários, o técnico remarca a ordem sem sair do preenchimento: a data, e o início e o fim de cada dia. Lembrando que a edição precisa de internet: sem conexão, o Editar OS aparece desativado, com o aviso Disponível apenas online. |

Se faltar a aba "Data e horários" por permissão, cortar só a primeira frase da última fala (a de internet continua valendo).

Pronúncias novas para o TTS: "Cassete" (já pronunciado no T3); BTUs "bê-tê-ús" como no restante do T7.

#### 4.3 Acréscimo no recap (cap13, 1 linha nova)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a gaveta "Editar OS" com o checklist indo para o "Cassete 36.000 BTUs - Recepção" e o aviso "OS atualizada". (entra depois da linha do "Resumo do consumo" e antes do cartão "Próximo") | E, quando a ordem muda no meio do atendimento, ele ajusta os equipamentos e os checklists na gaveta Editar OS, e as respostas vão junto. |

Totais de voz nova: capítulo 1.724 caracteres (9 falas, 305 palavras) + recap 136 caracteres = **1.860 caracteres**. Nenhuma fala tem travessão, preço de plano, nem rótulo fora do código.

#### 4.4 O que o backend falso precisa para o capítulo novo

Base: `rec/fakebase` (RPC sem handler devolve vazio pelo tipo; coluna fora do schema é salva sem padrão).

1. **Schema:** regerar com `gen-schema.mjs` apontando para `src-1.38.21` (G9) para `service_order_equipment.equipment_position` e `checklist_position` (padrão 0). A tela do técnico agora faz `.order('equipment_position').order('checklist_position')` (`TechnicianOS.tsx:1105-1125`); o fakebase precisa ordenar por essas colunas com desempate estável (a confirmar em `core/select.mjs`). Sem a coluna no schema o `select` pode falhar ou ordenar errado (a confirmar).
2. **Handler novo `rec/fakebase/handlers/rpc/edit_service_order_scope.mjs`** (hoje **não existe**; só `preview_service_order_scope_removal` e `sync_service_order_scope_with_services`). Assinatura da migration: `edit_service_order_scope(_service_order_id uuid, _items jsonb)`, cada item `{ equipment_id|null, form_template_ids: uuid[], moves?: [{ form_template_id, from_equipment_id|null }] }`. Comportamento (espelhar `supabase/migrations/20261104190000_...sql`):
   - valida OS, empresa, equipamento do mesmo cliente e template da mesma empresa; erros em português, usando os textos que `mapRpcError` reconhece: "Ordem de serviço não encontrada", "Sem acesso a esta ordem de serviço", "Sem permissão para editar o escopo desta ordem de serviço", "Edição manual indisponível em OS de PMOC", "Este checklist já existe no destino";
   - estado desejado = pares (equipamento, checklist) com `equipment_position` = índice do item e `checklist_position` = índice na lista; item sem checklist grava uma linha com `form_template_id` nulo;
   - **moves:** atualiza `service_order_equipment.equipment_id` da linha existente (não apaga nem recria) **e** `form_responses.equipment_id` de todas as respostas da OS cujas perguntas pertencem ao template, de `from_equipment_id` para o destino; conta em `responses_moved`;
   - pares que saíram do desejado: apaga as respostas (`responses_deleted`) e a linha; pares novos: insere; por fim regrava as posições;
   - devolve `{ service_order_id, removed, inserted, moved, responses_deleted, responses_moved, scope: [{ id, equipment_id, form_template_id, equipment_position, checklist_position }] }`.
3. **Sementes novas** (arquivo `seeds-extra/t7/inicio-editar-os.json` ou equivalente): `service_orders` (a OS de bastidor, `status` em andamento, `started_at` 08:15, Rafael como técnico, Pousada Sol Nascente, `scheduled_date` da quarta, 08:00, 60 min, `public_short_code` fixo), `service_order_assignees` (Rafael), `service_order_service_types` (Manutenção Preventiva), `service_order_equipment` com **duas linhas** `(Cassete, null)` e `(null, Manutenção preventiva de split)` (positions 0), `service_order_equipment_service_types` (Cassete com Manutenção Preventiva, para o selo), `technician_locations` com o ponto `check_in` (endereço da pousada) e **5 `form_responses` com `equipment_id` nulo** nas 5 perguntas Sim/Não (`response_value` "true"). `equipment` Cassete e os templates já existem (T3 e T4).
4. **Leituras:** `form_responses` com `equipment_id` nulo precisa responder aos filtros de `is null` que `DynamicFormQuestions.tsx` e `TechnicianOS.tsx:1044-1058` usam (a confirmar); `useFormTemplates` e `useEquipment(customerId)` só leem tabelas existentes.
5. **Permissão do Rafael:** sem `user_permissions` gravadas ele já vê "Editar OS" e a aba "Data e horários". Se a semente do T7 grava permissões, precisa conter `fn:editar_os_campo` e, para a segunda aba, `fn:edit_os`.
6. **Não precisa** para este capítulo: `schedule_book_service_order_plan` (a aba "Data e horários" só é olhada, sem salvar); `preview_service_order_scope_removal` (a gaveta não chama).

### T5 · Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo · entregue 1.38.19 · **(a)**

Conferido: o assistente "Nova Ordem de Serviço" (`ServiceOrderFormDialog.tsx`), o detalhe da OS e o Kanban **não estão no diff**. Em `os.ts` só mudaram `technicianFlow.editScope.*` e `sectionDescriptionTitle`. O bloco "Checklists avulsos" do cap04 (T5:76; `os.ts:247`, `standaloneSectionTitle` do assistente) segue igual; o nome novo "Checklists sem equipamento" é só da gaveta "Editar OS" do técnico, e o capítulo novo do T7 o apresenta, então não há conflito. A migration só acrescenta colunas com padrão 0 em `service_order_equipment`, então o `sync_service_order_scope_with_services` do T5 continua certo (as posições nascem 0). Falas: 0.

### T18 · Área do Técnico, cap03 · entregue · **(b)**

A câmera do cap03 fica no "cartão Checklists" da ordem: agora é o título **"Checklists" sem moldura e sem ícone** (`VisitChecklistPanel`/`TechnicianOS`, `panelTitle`), e a tela da OS usa o bloco único de contexto (seção 4.1 do T7). O botão redondo da Área do Técnico e o "Voltar para OS" não mudaram. Fala: nenhuma cita "cartão" (a palavra é da coluna Tela). Se o cap03 for refeito, o robô só ajusta a descrição do enquadramento. Falas: 0.

### T2 · Usuários, cargos e permissões · **(a)**

`hooks/usePermissions.ts` é idêntico: "Editar OS em campo" (`fn:editar_os_campo`, "Editar equipamentos e checklists dentro de uma OS em andamento") e "Editar OS" (`fn:edit_os`, "Editar ordens de serviço existentes") não mudaram. O que muda é o efeito: "Editar OS em campo" libera a nova gaveta "Equipamentos e checklists" (mover entre equipamentos), e a aba "Data e horários" depende de "Editar OS" (`TechnicianOS.tsx:823-824`): o cargo "Técnico de Campo" do T2 (só "Editar OS em campo") **não** vê a segunda aba. As falas do T2 (T02:62 "É assim que o técnico preenche o checklist da ordem...") já eram genéricas e não são contrariadas. Falas: 0.

### T12, T21 · **(a)** (só a classe)

- **T12** (`customer-portal-document-download`): mudança só no servidor (usa `getNfseEngine`, lê `referencia_fiscal` como segunda opção; ajuste de formatação). O T12 deixa "Notas fiscais" e "Documentos" desligadas no portal e nunca clica em "Baixar PDF" (T12:25), então não passa por esse download. O teste `customerPortalDocumentsSecurity.test.ts` mudou só por quebra de linha. Nada visível.
- **T21** (`whatsapp-connect`): só comentário (a menção ao Fisqal saiu do texto). Nada visível.

### T0 / T0 v2 / T19 · `DomiflixModuleOffer` · **(a)** (só a classe)

Tela real R06 do T0 v2 (`T00v2/roteiro.md:199-201`): rótulos "Conheça agora. Ative quando fizer sentido.", "Esta aula está liberada, mas a função ... ainda não faz parte do seu plano.", "Adicionar ao meu plano" e "Escolher meu plano" **iguais**. O que muda: a segunda frase (conta contratada) termina com "Antes de pagar, você verá a diferença proporcional até a próxima renovação." no lugar de "com o valor exato confirmado antes da contratação", e o clique agora leva à tela de Assinatura (`/assinatura?addModule=...`), que existe. Consequências:
- O vídeo entregue do T0 v2 continua correto; a nota "hoje o botão abre um endereço que não existe (C5)" do roteiro **caiu**: a cena pode continuar depois do clique, se o Kaik quiser (opcional, fala "solicitar a contratação por ali mesmo" passa a ser literal).
- O valor "A partir de R$ .../mês" já é coberto na edição; a frase nova é maior que a antiga, então numa recaptura é preciso conferir a máscara (a confirmar).
- **T19** não mostra esse componente (nenhum rótulo dele no roteiro): (a).

### T14 · Notas Fiscais (ainda não gravado) · classificação por capítulo

Só classificação, sem reescrever falas. O T14 foi escrito sobre a 1.38.6/1.38.19 (registro da empresa no integrador); o fluxo mudou assim:

**Mudanças visíveis (`pages/FiscalSettings.tsx`, `EmpresaSection`, `CertificadoSection`, `lib/i18n/messages/app/nfse.ts`)**
- Sem registro de empresa. Somem: "Empresa: registrada / não registrada", o bloco "Status da emissão", o botão que só aparecia "depois de registrar", os avisos de falha de registro. O botão "Salvar dados da empresa" vira **"Salvar dados fiscais"** e agora exige razão social, CNPJ (14 dígitos), Inscrição Municipal, CEP (8 dígitos), logradouro, cidade, UF e código do município; senão o aviso "Preencha razão social, CNPJ, Inscrição Municipal e o endereço fiscal completo antes de salvar.". O aviso de sucesso continua "Dados da empresa salvos." e em seguida o app checa a cobertura sozinho.
- Abas sem número: "Empresa", "Certificado A1", "Tributação", "Serviços" (antes "1. Empresa" a "4. Serviços").
- Dicas novas: aba Empresa "Confira e salve os dados fiscais da empresa. Eles identificam o prestador em cada nota."; aba Certificado "Envie o certificado A1 (.pfx/.p12) usado para assinar as notas no Padrão Nacional."; Inscrição Municipal "Exigida pelo município para emitir notas. É o mesmo campo da aba Tributação."
- **Painel de prontidão no alto** (substitui o selo e o bloco "Status da emissão"): linha com "Configuração incompleta" ou "Apto a emitir" e duas linhas: "Município: liberação ainda não confirmada" / "Município: liberado para emitir notas" (botão "Verificar") e "Certificado A1: pendente" / "Certificado válido até {data}" (botão "Enviar certificado" ou "Enviar novo"). "Próximo: enviar certificado" fica sempre visível. "Apto a emitir" passa a exigir município confirmado **e** A1 com validade futura (não existe mais "empresa registrada").
- Tela de falha nova ao carregar: "Não foi possível carregar as configurações fiscais" com "Tentar novamente" (só em erro; o robô não passa por ela).
- **Ambiente padrão passou a Produção** (`hooks/useFiscalSettings.ts`, `DEFAULT_SETTINGS.fiscal_ambiente`; antes `homologacao`). O T14 grava em Homologação (decisão do `PRODUCAO.md`): a semente `inicio` precisa trazer `company_fiscal_settings.fiscal_ambiente = 'homologacao'`, senão a chave abre em "Produção".
- `NovaNotaModal`: o bloqueio ganhou o link "Abrir Configurações Fiscais" e mensagens de certificado vencido/sem validade (não aparecem no caminho feliz). O bloco "Prestador" da pré-visualização lê nome, CNPJ, cidade e UF de `company_settings` (não mais de `company_fiscal_settings`).

| Cap | Tela | Fala | Backend falso | Classe |
|---|---|---|---|---|
| 00 Abertura | Igual (estado guiado "Configure seus dados fiscais", abas, botões) | Mantém | Semente `inicio` sem linha fiscal ou com `fiscal_ambiente: homologacao`; `nfse_can_emit` igual | (a) |
| 01 A nota do serviço | Igual (ilustração; abas e selo da cota) | Mantém | Igual | (a) |
| 02 Dados da empresa | **Muda**: abas sem número (L60, L81, L89...), nova dica "Confira e salve...", dica da Inscrição Municipal com "município", **sem** o bloco "Status da emissão" (L64) e **sem** "Empresa: registrada" (L65); "Salvar dados fiscais"; painel de prontidão no alto; "Próximo: enviar certificado" sempre presente | **Muda**: L61 ("é ela que permite o registro pra emitir") e L65 ("ela fica registrada pra emissão") falam de registro que não existe; L60 leve ("são quatro passos, e o primeiro é a empresa": agora são quatro abas, não passos numerados). L64 (cobertura do município) continua certa | **Não precisa** de `nfse-register-company`. `nfse-check-coverage` (`{ibge}` → `{pode_emitir}`) continua e deve gravar `municipio_ibge` e `pode_emitir` em `company_fiscal_settings`; o app salva `company_settings` e `company_fiscal_settings` e chama a cobertura outra vez em silêncio. Semente `apos-cap02` sem `provider_company_id`/`fisqal_company_id` (guardar `municipio_ibge`, `pode_emitir`, `inscricao_municipal`) | **(c)** |
| 03 Certificado | **Muda**: dica "Envie o certificado A1 (.pfx/.p12) usado para assinar as notas no Padrão Nacional."; o campo de arquivo não depende mais de registro; após o envio o painel do alto mostra "Certificado válido até 10/11/2027" e "Apto a emitir" (linha com check, não mais o selo) | **Muda**: L71 ("Com a empresa registrada, vem o certificado digital A1") | `nfse-upload-certificate` precisa gravar `certificado_ref` (texto qualquer) **e** `certificate_expires_at` (10/11/2027); sem a validade a tela mostra "A validade do certificado não foi confirmada. Envie o A1 novamente." em vermelho e o selo não acende. Mantém `record_certificate_custody_consent` e o evento `upload` em `fiscal_certificate_audit` | **(c)** |
| 04 Tributação | Só o nome da aba ("Tributação", sem "3.") | Mantém | `PATCH company_fiscal_settings` igual | (b) |
| 05 Serviços | Só o nome da aba ("Serviços", sem "4.") | Mantém | `nfse-tax-codes` igual (mesmo contrato, só ficou o catálogo local) | (b) |
| 06 Pessoas e serviço | Igual | Mantém | `company_settings` (nome, CNPJ, cidade, UF da Glacial) alimentam o "Prestador"; "Nova Nota" exige `pode_emitir`, `certificado_ref` e validade futura na semente `apos-cap05` | (b) |
| 07 Valores e emissão | Igual | Mantém | `nfse-emit` falso: seguir o gate novo (município + `certificado_ref` + validade) e gravar `referencia_fiscal` (= chave) em vez de `fisqal_dps_id`; mantém 202/`processando` e a prova fiscal da 1.38.19 | (b) |
| 08 Nota autorizada | Igual | Mantém | `nfse-status`/`nfse-danfse`: colunas `referencia_fiscal`/`requisicao_fiscal_id` (as `fisqal_*` somem do tipo); `status_fiscal_*` já eram requisito da 1.38.19 | (b) |
| 09 Rascunho e cancelamento | Igual (textos do cancelamento sem diff) | Mantém | `nfse-cancel` com a orientação nos erros (sem efeito no caminho feliz) | (b) |
| 10 Nota automática do contrato | Igual | Mantém | Igual | (a) |
| 11 Notas dos fornecedores | Igual | Mantém | "Ligar recebimento automático" agora exige `certificado_ref` **e** `certificate_expires_at` futura na semente; `dfe-sync` igual | (b) |
| 12 Ciência e conta a pagar | Igual | Mantém | Igual ao cap11 | (b) |
| 13 Recap | Montagem "Configurações fiscais" com "Apto a emitir" (painel novo) e abas sem número | **Muda**: L161 ("você registrou a empresa, enviou o certificado...") | Igual | **(c)** |

Total do T14: falas que mudam **4** (L61, L65, L71, L161) + 1 leve (L60); as reescritas ficam para a vez dele, com o código assentado. O arquivo de sementes do T14 que dependia do integrador (`apos-cap02`, `apos-cap03`) e o handler `nfse-register-company` previstos no roteiro saem do plano.
Pendências (a confirmar): (i) se a semente fiscal do T14 já existe em `rec/fakebase/seeds-extra/t14` (não há pasta hoje); (ii) a tabela de rótulos do painel de prontidão na tela (a ordem das duas linhas e os botões); (iii) o comportamento do botão "Verificar" no painel quando o município já foi confirmado na sessão.

### T10, T11, T13, T15, T17, T19, T20, T22 · confirmados **(a)**

Nenhum dos arquivos que essas aulas mostram mudou entre 1.38.19 e 1.38.21: o diff de `src/` toca só OS do técnico (`TechnicianOS`, `EditOsScopeDrawer`, `components/technician/*`), fiscal (`components/fiscal/*`, `pages/FiscalSettings`, `pages/NotasFiscais`, `nfse.ts`), `DomiflixModuleOffer`, `MobilePillTabs` (G6), `version.ts`, `Changelog.tsx`, `os.ts` e `types.ts`. T13 e T20 não abrem nada fiscal; T15 e T20 só citam "Notas Fiscais" no cartão de "Antes/Próximo". T19 não mostra `DomiflixModuleOffer`. Atenção apenas ao G7 nas aulas gravadas no celular (T15 cap9).

## 5. Backend falso: consolidado da 1.38.21

| Item | Aula | O quê |
|---|---|---|
| Regerar schema (G9) | T7 novo, T14 | `service_order_equipment.equipment_position/checklist_position`; `nfse_emissions.referencia_fiscal/requisicao_fiscal_id`; RPC `nfse_next_dps_number` (sem handler: ninguém a chama pela tela) |
| Handler novo `edit_service_order_scope` | T7 novo | Seção 4.4, item 2 |
| Sementes de bastidor "Editar OS" | T7 novo | Seção 4.4, item 3 |
| `nfse-upload-certificate` grava `certificado_ref` e `certificate_expires_at` | T14 | Substitui `provider_certificate_id`/`fisqal_certificate_id` |
| Remover o plano do `nfse-register-company` | T14 | A tela não chama mais; semente `apos-cap02` sem registro |
| `fiscal_ambiente: homologacao` na semente `inicio` | T14 | O padrão do app agora é Produção |
| `nfse-emit`, `nfse-status`, `nfse-cancel`, `nfse-danfse` | T14 | Gravar `referencia_fiscal`; manter prova fiscal da 1.38.19; gate de prontidão com validade |
| `setup` do celular grava versão vista 1.38.21 | T7 novo, T15 | G7 |
| Nada novo | T0, T1 a T5, T8 a T13 (sem T14), T15 a T22 | Handlers atuais atendem |

## 6. Ordem sugerida e dúvidas para o Kaik

1. Backend falso: regerar o schema, escrever `edit_service_order_scope`, semear a OS de bastidor da Pousada, conferir o arrasto (`@dnd-kit`) no robô de celular. Gravar só o cap14 do T7 e remontar (remendo): ~10 falas, 1.860 caracteres de voz.
2. T14: aproveitar para escrever o backend novo (sem registro) antes da gravação; reescrever as 4 falas (e 1 leve) na vez dele.
3. Dúvidas:
   - **T7: remendo ou regravação inteira?** O vídeo entregue mostra a cor da marca nos botões e interruptores; o capítulo novo mostra o visual neutro. A diferença é pequena. Recomendo remendo (só cap14 + montagem do recap).
   - **Capítulo na #16 ou OS separada?** Recomendo a OS da Pousada (seção 4.2). Se o Kaik preferir o caso literal do handoff com cadastro rápido de equipamento ("Adicionar equipamento" > formulário), são ~25 s a mais, e o formulário de equipamento precisa ser testado no celular (a confirmar).
   - **Posição:** cap14 exibido antes do recap (sem renumerar o cap13), ou renumerar o roteiro e os arquivos de `rec/t7`?
   - **Publicação:** o handoff do Kaik diz que a mudança de OS estava sem commit e a migration pendente de aplicação. O `origin/main` já tem o commit `b5ebd555` e a migration; antes de publicar o T7 novo, confirmar o deploy da migration no ambiente real, porque o espectador usará o app de verdade.
   - **"Retomar OS" no rodapé escuro:** conferir na tela o contraste do botão neutro (T7 cap07 e cap08); se ficar ilegível, vale avisar o time do app.
   - **T7 L68:** regravar a fala por causa de "cartão de Checklists"? Recomendo aceitar.
