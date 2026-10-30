# Trilha Domiflix · plano de produção (todos os tutoriais de funções)

Pedido do Kaik (30/10/2026, 20:33): planejar já todos os tutoriais da trilha, **exceto a Introdução (T0)**, que terá
outro teor; levantar todas as telas e arquivos e guardar tudo para não perder entre sessões.
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
| T0 | Bem-vindo, configuração, identidade e assinatura | — | White Label (parcial) | fora (teor diferente) | — |
| T2 | Usuários, cargos e permissões | USUÁRIOS | — | em andamento (lote B1) | — |
| T3 | Clientes, Fornecedores e Equipamentos | CLIENTES / FORNECEDORES / EQUIPAMENTOS | — | feito | **entregue 30/10** |
| T4 | Serviços, tarefas e checklists | SERVIÇOS | Vídeo em checklist (parcial) | em andamento (lote A1) | — |
| T5 | Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo | ORDENS DE SERVIÇO / AGENDA | RH (Equipes) | em andamento (lote A1) | — |
| T7 | O técnico em campo | TÉCNICO EM CAMPO | — | em andamento (lote A1) | — |
| T18 | Área do Técnico: Refrigeração e Climatização | ÁREA DO TÉCNICO | Segmento específico | lote A2 | — |
| T8 | Estoque, compras e inventário | ESTOQUE | — | lote A2 | — |
| T9 | Orçamentos, Precificação e Proposta | ORÇAMENTOS | Precificação Avançada (parcial) | lote A2 | — |
| T10 | CRM: funil, leads e captação | CRM | CRM | em andamento (lote B1) | — |
| T11 | Contratos e PMOC | CONTRATOS | Contratos e PMOC | em andamento (lote B1) | — |
| T12 | Portal do Cliente e Portal do Contrato | PORTAL | Portal do Cliente + Contratos/PMOC | em andamento (lote B1) | — |
| T13 | Financeiro | FINANCEIRO | — | lote B2 | — |
| T19 | Integração com Asaas, Assinaturas e Cobranças | COBRANÇAS | Cobranças | lote B2 | — |
| T20 | Relatório Financeiro e DRE | FINANCEIRO | — | lote B2 | — |
| T14 | Notas Fiscais (NFS-e e NF-e) | NOTAS FISCAIS | Emissão de Notas Fiscais | lote B2 | — |
| T15 | Funcionários: Financeiro do Funcionário e Ponto Eletrônico | FUNCIONÁRIOS | Funcionários / RH | lote C | — |
| T22 | Ferramentas de RH: DISC, Organograma, Fluxograma | RH | Funcionários / RH | lote C | — |
| T21 | Integração com WhatsApp | WHATSAPP | WhatsApp | lote C | — |
| T17 | Dashboard, relatórios e exportações | DASHBOARD | — | lote C | — |

Lotes do levantamento (2 por vez): A1 = T4, T5, T7 · B1 = T2, T10, T11, T12 · A2 = T18, T8, T9 ·
B2 = T13, T19, T20, T14 · C = T15, T22, T21, T17.

## Ordem de produção recomendada
A da trilha oficial (menor risco primeiro: o miolo operacional está estável; integrações e fiscal dependem de
simular serviços externos), sem T0 e T3:
**T4 → T5 → T7 → T18 → T2 → T8 → T9 → T12 → T13 → T20 → T10 → T11 → T15 → T22 → T19 → T21 → T14 → T17**.
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

## Decisões para o Kaik
1. ~~"Mostrar o erro de propósito" × "só possibilidades"~~ **Decidido pelo Kaik (30/10 20:56)**: nos ⚠️, pode
   mostrar como informação o que dá errado se a pessoa não fizer, mas focado nas possibilidades: primeiro o caminho
   certo, depois a consequência numa frase; sem encenar a falha. Avisos normais do fluxo aparecem como parte do uso.
2. Gravação no celular (T7 e afins): aprovar o visual numa prévia antes de produzir.
3. Integrações externas (Asaas, NFS-e/NF-e, WhatsApp): gravar só com o serviço simulado no backend falso (nada de
   conta real), mostrando telas e respostas fiéis ao código. Confirmar.
4. Pendências de validação da trilha oficial (seção "⚠️ Pendências de validação antes de gravar"): os levantamentos
   respondem o que o código responde; o resto fica em "Dúvidas" de cada `inventario.md`.

## Como retomar numa sessão nova
```bash
git clone https://github.com/KaikBarreto/claude-tutorials            # esta skill + este planejamento
git -C <clone do dominextecnologia> fetch origin main && \
  mkdir -p ~/domiflix/src && git -C <clone do dominextecnologia> archive <commit> | tar -x -C ~/domiflix/src
TUT_HOME=~/domiflix TUTORIAL=t4 PERFIL=domiflix bash claude-tutorials/instalar.sh
```
Depois: ler `PERFIL.md`, este `TRILHA.md` e `planejamento/domiflix/T04/{inventario,plano}.md`; roteiro em doc para
aprovação; narração; sementes e handlers do backend falso; gravação; edição; entrega.
