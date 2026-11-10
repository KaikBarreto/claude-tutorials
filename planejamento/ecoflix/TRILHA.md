# Trilha EcoFlix · ordem, produção e status

Fonte do conteúdo (capítulos, aberturas, recaps, próximos, ⚠️/🚫/🔒): `docs/ecoflix/trilha-de-tutoriais.md` no
repositório do EcoSistema (origin/main `8ae17c6e5`, 08/11/2026 23:42; é dela que sai a página `/trilha-ecoflix`),
validada contra a versão **1.59.154** do app (commit de release `f37573ea0`, 07/11): é essa a versão a gravar, salvo
release mais nova publicada antes da gravação.
Não copiar para cá: cada roteiro lê só a seção da sua aula. Perfil: `perfis/ecoflix/PERFIL.md`. Mundo:
`MUNDO_FICTICIO.md`. Decisões e andamento: `PRODUCAO.md`.

## Ordem de exibição (26 aulas + a T0 vertical)
- **Fase 1, formação básica** (todo cliente): T0 · T1 · T2 · T3 · T4 · T5 · T6 · T7 · T8 · T9 · T10 · T13 · T14 · T15 ·
  T21 · T25
- **Fase 2, módulos 🔒**: T16 · T17 · T18 · T19 · T27 · T20 · T22 · T12 · T11 · T26
- Fora da trilha: T23 (Marketplace) e T24 (Assinatura, agora dentro da T0).

## Ordem de produção (proposta de 08/11)
1. **T3** primeiro: é o molde (a prévia de um capítulo congela a identidade) e cria o cardápio de materiais que a trilha
   inteira usa, como o T3 da Domiflix.
2. Miolo operacional: T4 → T6 → T7 → T8 → T9 → T10.
3. Configuração e financeiro: T1 → T2 → T13 → T14 → T15 → T25.
4. Módulos: T19 → T27 → T20 → T22 → T12 → T11 → T26.
5. Fiscal: T16 → T17 → T18. No mundo falso não há certificado, SEFAZ, cota nem numeração para queimar; ficam aqui por
   serem as aulas com mais telas novas para simular, não por risco.
6. Por último: T5 (espera o trecho real de instalação do EcoTray), T21 (Cato), T0 e T0 vertical (resume a trilha).

## Status
| Aula | Título | 🔒 | Antes | Alvo | Notas de produção | Roteiro | Voz | Gravação | Edição | Entrega |
|---|---|---|---|---|---|---|---|---|---|---|
| T0 | Bem-vindo ao EcoSistema | | nenhuma | 12 min | 16:9 + 9:16; tela de Assinatura do mundo, preço não falado | ✅ 10/11 | | | | |
| T1 | Sua conta e sua empresa | | T0 | 18 min | telas sem login (cadastro, login, senha); Zerar Sistema só mostrado | ✅ 10/11 | | | | |
| T2 | Usuários e permissões | | T1 | 13 min | cria Juliana e Marcos (existem do T6 em diante) | ✅ 10/11 | | | | |
| T3 | Materiais e tabelas de preço | | T2 | 15 min | **molde**; cria um material e uma tabela de preço | ✅ 10/11 | | | | |
| T4 | Clientes, fornecedores e a ficha do parceiro | | T3 | 17 min | busca por CNPJ simulada; os 4 casos de saldo | ✅ 10/11 | | | | |
| T5 | Balança e impressora: o EcoTray | balança (parte) | T4 | 13 min | EcoTray falso; celular (peso no rodapé); instalação real? | ✅ 10/11 | | | | |
| T6 | Caixa: abrir, fechar e o cofre | | T5 | 14 min | multi-caixa com 2 operadores | ✅ 10/11 | | | | |
| T7 | Comprar e vender sucata | | T6 | 22 min | balança falsa; modo sem internet; comprovante em PDF | ✅ 10/11 | | | | |
| T8 | Ticket de Pesagem | | T7 | 11 min | dois veículos ao mesmo tempo | ✅ 10/11 | | | | |
| T9 | Pedidos e histórico do caixa | | T8 | 12 min | caixa antigo para reabrir | ✅ 10/11 | | | | |
| T10 | Estoque: saldo, histórico e posição | | T9 | 16 min | 3 meses de histórico; posição em 31/10 | ✅ 10/11 | | | | |
| T13 | Contas a Pagar e Receber | | T10 | 16 min | recorrência, fiado parcelado | ✅ 10/11 | | | | |
| T14 | Bancos, cofre e conciliação bancária | | T13 | 18 min | arquivo OFX fictício casando com o mundo | ✅ 10/11 | | | | |
| T15 | Relatório Financeiro e DRE | | T14 | 17 min | exemplo do pátio (caixa × competência) nos dados | ✅ 10/11 | | | | |
| T21 | Cato, o assistente | | T15 | 8 min | respostas simuladas no formato real do Cato | ✅ 10/11 | | | | |
| T25 | Dashboard, Agenda e rotina | | T21 | 13 min | fecha a Fase 1 | ✅ 10/11 | | | | |
| T16 | Nota Fiscal de mercadoria (NF-e) | notas_fiscais | T15 | 25 min | emissão simulada; regime do exemplo a decidir | ✅ 10/11 | | | | |
| T17 | Transporte, serviço e o contador | notas_fiscais | T16 | 16 min | + frota e NFS-e tomada (pendência 3 da fonte) | ✅ 10/11 | | | | |
| T18 | Ambiental: MTR e CDF | notas_fiscais | T17 | 12 min | órgão ambiental simulado | ✅ 10/11 | | | | |
| T19 | Funcionários e ponto eletrônico | funcionarios | T15 | 16 min | celular (ponto com local e hora) | ✅ 10/11 | | | | |
| T27 | White Label | white_label | T1 | 7 min | aula nova | ✅ 10/11 | | | | |
| T20 | Portal do Cliente e Fornecedor | portal_cliente | T4 | 12 min | página pública do parceiro | ✅ 10/11 | | | | |
| T22 | Gerencial: matriz e filiais | modulo_gerencial | T15 | 16 min | matriz Taubaté + filial Pindamonhangaba | ✅ 10/11 | | | | |
| T12 | Coletas e Logística | coletas | T4 | 15 min | Rastreamento e Rotas ficam de fora ("Em breve") | ✅ 10/11 | | | | |
| T11 | Produção | producao | T10 | 20 min | ficha técnica (ex.: latinha vira fardo) | ✅ 10/11 | | | | |
| T26 | CRM/Kanban | crm_kanban | T4 | 16 min | aula nova; conferir se as automações estão na versão publicada | ✅ 10/11 | | | | |

Soma da fonte: ~6 h 30. Pela experiência da Domiflix, a fala costuma fechar abaixo do alvo.

## Observações sobre a fonte (para o Kaik corrigir lá, se quiser)
- "Ordem sugerida de gravação" lista o T25 duas vezes.
- "Pendências antes de gravar" pula do 9 para o 11.
- As aberturas, recaps e próximos têm travessão; nos roteiros ele sai.
- "Mostre o erro de propósito" choca com a regra da Domiflix de não encenar a falha (decisão pendente em PRODUCAO.md).
