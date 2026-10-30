# Trilha Domiflix · plano de produção (todos os tutoriais de funções)

Pedido do Kaik (30/10/2026, 20:33): planejar já todos os tutoriais da trilha, **exceto a Introdução (T0)**, que terá
outro teor; levantar todas as telas e arquivos e guardar tudo para não perder entre sessões.
T0 definido depois (21:16 e 21:19): vídeo **ilustrado** de 2 a 4 min, sem tela de sistema (tutoriais, Guia Técnico,
suporte, assinatura, plano e cobrança proporcional). Plano em `T00/plano.md`; roteiro no doc
https://claude.ai/artifact/UQjsgSUXMRz34vCAh2qW3w.
Padrão de produção: perfil Domiflix (`perfis/domiflix/PERFIL.md`), idêntico ao T3.

- Código de referência: Dominex **1.38.6** (`origin/main` 5f0b64ea), extraído em `/home/claude/domiflix/src-1.38.6`
  (somente leitura). Para recriar numa sessão nova: ver "Como retomar" no fim.
- Trilha oficial do app (validada na 1.22.5): `_referencia/trilha-de-tutoriais_v1.22.5.md`.
- Briefing do levantamento (fontes, entregáveis, regras): `_BRIEF.md`. Cada tutorial tem `<Tnn>/inventario.md`
  (telas, rótulos, regras, backend, pegadinhas, `arquivo:linha`) e `<Tnn>/plano.md` (capítulos, mundo fictício,
  gravação, pronúncias, decisões).

## Situação

| Ordem de exibição | Tutorial | Área (vinheta) | Módulo pago | Levantamento | Produção |
|---|---|---|---|---|---|
| T0 | Boas-vindas à Dominex (ilustrado, ~3 min 40 s, sem tela) | COMEÇANDO / AJUDA / ASSINATURA | — | feito | roteiro em aprovação |
| T1 | Configurações e identidade da empresa | CONFIGURAÇÕES | White Label (parcial) | em andamento (lote A2) | — |
| T2 | Usuários, cargos e permissões | USUÁRIOS | — | feito (lote B1) | — |
| T3 | Clientes, Fornecedores e Equipamentos | CLIENTES / FORNECEDORES / EQUIPAMENTOS | — | feito | **entregue 30/10** |
| T4 | Serviços, tarefas e checklists | SERVIÇOS | Vídeo em checklist (parcial) | em andamento (lote A1) | — |
| T5 | Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo | ORDENS DE SERVIÇO / AGENDA | RH (Equipes) | em andamento (lote A1) | — |
| T7 | O técnico em campo | TÉCNICO EM CAMPO | — | em andamento (lote A1) | — |
| T18 | Área do Técnico: Refrigeração e Climatização | ÁREA DO TÉCNICO | Segmento específico | em andamento (lote A2) | — |
| T8 | Estoque, compras e inventário | ESTOQUE | — | em andamento (lote A2) | — |
| T9 | Orçamentos, Precificação e Proposta | ORÇAMENTOS | Precificação Avançada (parcial) | em andamento (lote A2) | — |
| T10 | CRM: funil, leads e captação | CRM | CRM | feito (lote B1) | — |
| T11 | Contratos e PMOC | CONTRATOS | Contratos e PMOC | feito (lote B1) | — |
| T12 | Portal do Cliente e Portal do Contrato | PORTAL | Portal do Cliente + Contratos/PMOC | feito (lote B1) | — |
| T13 | Financeiro | FINANCEIRO | — | feito (lote B2) | — |
| T19 | Integração com Asaas, Assinaturas e Cobranças | COBRANÇAS | Cobranças | feito (lote B2) | — |
| T20 | Relatório Financeiro e DRE | FINANCEIRO | — | feito (lote B2) | — |
| T14 | Notas Fiscais (NFS-e e NF-e) | NOTAS FISCAIS | Emissão de Notas Fiscais | feito (lote B2) | — |
| T15 | Funcionários: Financeiro do Funcionário e Ponto Eletrônico | FUNCIONÁRIOS | Funcionários / RH | lote C | — |
| T22 | Ferramentas de RH: DISC, Organograma, Fluxograma | RH | Funcionários / RH | lote C | — |
| T21 | Integração com WhatsApp | WHATSAPP | WhatsApp | lote C | — |
| T17 | Dashboard, relatórios e exportações | DASHBOARD | — | lote C | — |

Lotes do levantamento (2 por vez): A1 = T4, T5, T7 · B1 = T2, T10, T11, T12 · A2 = T1, T18, T8, T9 ·
B2 = T13, T19, T20, T14 · C = T15, T22, T21, T17.

## Ordem de produção recomendada
O T0 sai assim que o roteiro for aprovado (não depende de gravação nem de backend falso; só ilustrações e voz).
O T1 (configurações) vem logo depois: telas de formulário, pouco backend falso.
Depois, a da trilha oficial (menor risco primeiro: o miolo operacional está estável; integrações e fiscal dependem de
simular serviços externos), sem T3:
**T0 → T1 → T4 → T5 → T7 → T18 → T2 → T8 → T9 → T12 → T13 → T20 → T10 → T11 → T15 → T22 → T19 → T21 → T14 → T17**.
Cada aula parte do estado final da anterior no mundo fictício (Glacial Cold Brasil), na ordem de exibição.

## Trabalho comum a vários tutoriais (antes ou durante a produção)
1. **Backend falso por tutorial**: sementes do estado inicial (`seeds-extra/<id>/apos-capNN.json`), RPCs, edge
   functions e serviços externos simulados (mapa e posição dos técnicos, PDF, links públicos, cobrança, nota fiscal,
   WhatsApp). Lista exata em cada `plano.md` → "Gravação".
2. **Gravação no celular** (T7 é gravado no celular pela trilha; outras telas de técnico/ponto podem ser): robô com
   viewport de celular + apresentação do aparelho no palco (moldura genérica, sem marca de terceiros). Precisa ser
   desenvolvido e aprovado com um capítulo de prévia antes.
3. **Pronúncias** novas (PMOC, NFS-e, NF-e, DISC, BDI...): testar num trecho curto e registrar no
   `perfis/domiflix/narracao/config_narracao.json` e no `PERFIL.md`.
4. **Duração**: a trilha estimava 18 a 70 min por aula (gravação humana); no nosso padrão (fala natural, robô no
   ritmo da voz, cortes de pausa) o T3 previsto para 35 min saiu com 12:13. Esperar ~10 a 25 min por aula.
5. **Relógio do navegador**: o fakebase congela a data (`FAKE_NOW`), mas o navegador da gravação usa o relógio real.
   Congelar o navegador na mesma data (Playwright 1.63: `page.clock`) para as datas do mundo (visitas do PMOC,
   vencimentos) não envelhecerem entre o planejamento e a gravação (T11, T12).
6. **Gravador**: hoje não grava página sem login (contexto anônimo), nova aba (PDF, link público) nem download
   (T11, T12). Desenvolver e testar no exemplo do T3 antes.
7. **Endereço do app nos links**: o app gravado roda em `127.0.0.1:8080`, e isso aparece em "Link do portal", no
   webhook do CRM etc. Proposta: servir num nome de produto mapeado para a máquina local (Chromium
   `--host-resolver-rules`), sem tocar a rede (T10, T12).
8. **Backend falso**: criar e gerenciar usuário (T2), CRM e captação (T10), PMOC com PDFs e numeração de OS (T11),
   páginas públicas do portal (T12): lista exata em cada `plano.md` → "Gravação".

## Decisões para o Kaik
1. ~~"Mostrar o erro de propósito" × "só possibilidades"~~ **Decidido pelo Kaik (30/10 20:56)**: nos ⚠️, pode
   mostrar como informação o que dá errado se a pessoa não fizer, mas focado nas possibilidades: primeiro o caminho
   certo, depois a consequência numa frase; sem encenar a falha. Avisos normais do fluxo aparecem como parte do uso.
2. Gravação no celular (T7 e afins): aprovar o visual numa prévia antes de produzir.
3. Integrações externas (Asaas, NFS-e/NF-e, WhatsApp): gravar só com o serviço simulado no backend falso (nada de
   conta real), mostrando telas e respostas fiéis ao código. Confirmar.
4. Pendências de validação da trilha oficial (seção "⚠️ Pendências de validação antes de gravar"): os levantamentos
   respondem o que o código responde; o resto fica em "Dúvidas" de cada `inventario.md`.
5. ~~Configurações da empresa sem aula com o T0 novo~~ **Decidido pelo Kaik (30/10 21:55)**: vira o **T1
   "Configurações e identidade da empresa"** (com tela), logo depois do T0 (Guia Técnico T1: aba Empresa, documentos,
   White Label, Regional, Usabilidade, Origens, Atalhos, Aparência, Integrações, Zona de Perigo). Levantamento no lote A2.
6. **Decidido pelo Kaik (30/10 21:55)**: nenhum vídeo mostra preço de plano (só o desconto de 20% do anual).
7. **Glacial Cold Brasil é cliente real** (aparece no código em incidentes de produção). O nome foi escolha do Kaik para a
   empresa de exemplo; no T14 ele sairia no PDF de uma nota fiscal simulada: confirmar antes de gravar o T14.

## Achados de segurança para o time do app (conferidos no código 1.38.6)
1. **Cargos valem para todas as empresas.** A tabela `permission_presets` não tem `company_id`; a leitura é liberada
   para qualquer usuário logado (`20260418163700_...sql:99`, `USING (true)`) e a edição/exclusão para qualquer gestor
   de qualquer empresa (`20260308205452_...sql:71-76`); a tela busca todos, sem filtro (`src/hooks/usePermissions.ts:206-212`).
   Na prática, "Configurações de Cargos" e os "Perfis rápidos" de cada cliente mostram os cargos das outras empresas.
2. **Usuário sem permissões gravadas vê tudo.** Sem linha em `user_permissions`, qualquer papel libera todas as telas
   e ações (`src/contexts/AuthContext.tsx:383-395`, modo legado); o cadastro só grava permissões quando alguma é
   marcada (`supabase/functions/create-user/index.ts:61`). Um técnico criado sem marcar nada fica com acesso total
   dentro dos módulos da empresa.
3. **Uso de notas fiscais de outra empresa (gravidade baixa).** `nfse_month_usage(p_company_id)` e `nfse_can_emit(p_company_id)`
   são `SECURITY DEFINER`, liberadas para qualquer usuário logado e não conferem se a empresa é a dele
   (`20260825140000_...sql:21-38`, `20260615210000_...sql:91-190`): quem tiver o código de outra empresa vê o nível e o uso
   mensal de notas dela.
Os demais ajustes de texto e comportamento estão em "Pegadinhas" de cada `inventario.md` (marcados como handoff).

## Como retomar numa sessão nova
```bash
git clone https://github.com/KaikBarreto/claude-tutorials            # esta skill + este planejamento
git -C <clone do dominextecnologia> fetch origin main && \
  mkdir -p ~/domiflix/src && git -C <clone do dominextecnologia> archive <commit> | tar -x -C ~/domiflix/src
TUT_HOME=~/domiflix TUTORIAL=t4 PERFIL=domiflix bash claude-tutorials/instalar.sh
```
Depois: ler `PERFIL.md`, este `TRILHA.md` e `planejamento/domiflix/T04/{inventario,plano}.md`; roteiro em doc para
aprovação; narração; sementes e handlers do backend falso; gravação; edição; entrega.
