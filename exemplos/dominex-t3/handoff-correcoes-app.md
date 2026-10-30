# Handoff · Correções no app achadas no inventário do T3 (Clientes, Fornecedores e Equipamentos)

**Para:** o Claude que trabalha no repositório do Dominex (CEO → Tech Lead → Devs, como manda o CLAUDE.md do repo).
**De:** a sessão que está produzindo o tutorial T3 da Domiflix (30/10/2026).
**Base:** leitura do código na versão `1.37.56` (`src/config/version.ts`). Nada foi executado: são achados de leitura.
Os números de linha são dessa versão e podem ter andado; confira antes de mexer. O que está marcado "(confirmar)"
eu deduzi do código e vale reproduzir antes de corrigir.

## Como tocar

1. Tech Lead lê os 7 itens da Prioridade 1, confirma cada um no código atual e escreve o plano em `docs/planos/`.
2. CEO resume para o Kaik e pede aprovação (regra do repo). Itens independentes podem ir em paralelo (máx. 2 Devs).
3. Modelo: os itens 1 a 7 são de UI e formulário, no padrão (Sonnet). O item 2 mexe em formato de dado gravado:
   o Tech Lead decide se é só exibição ou se mexe no banco.
4. Release com changelog nas duas fontes (`VERSION_NOTES` e `changelog_entries`), como sempre. Texto cliente-only.
5. A Prioridade 2 é lista para triagem com o PM: não precisa entrar no mesmo release.

## Prioridade 1 (o cliente final vê ou perde dado)

### 1. WhatsApp do cliente desliga sozinho enquanto se digita o celular

- **Onde:** `src/components/customers/CustomerFormDialog.tsx:492-510` (o `setValue` que desliga está na linha 503);
  padrão em `EMPTY_FORM` (`:85-92`); regra ao salvar em `:285-286`.
- **Hoje:** cada tecla no Celular, enquanto o número tem menos de 10 dígitos, desliga o interruptor
  "Receber mensagens pelo WhatsApp". Quem digita o número tecla a tecla chega ao fim com o interruptor liberado,
  porém **desligado**. Resultado: cliente novo sem os avisos de OS, cobrança e vencimento sem ninguém perceber.
  Colar o número inteiro mantém ligado, então o comportamento depende de como a pessoa digita.
- **Esperado:** enquanto o celular é inválido, o interruptor fica só desabilitado (sem trocar o valor). Ao ficar
  válido, volta ao valor que a pessoa escolheu (padrão ligado). Se a pessoa desligou à mão, continua desligado.
  A regra de salvar desligado quando o celular é inválido (`:285-286`) continua.
- **Aceite:** digitar um celular válido tecla a tecla → interruptor ligado. Desligar à mão e editar o número →
  continua desligado. Apagar o celular e salvar → gravado desligado.

### 2. Cliente do formulário de captação: origem "public_form" crua e documento/telefone sem máscara

- **Onde:** gravação em `submit_lead_capture_form`
  (`supabase/migrations/20261015233000_lead_capture_insert_dinamico_respeita_default.sql:100-336`, chamado por
  `supabase/functions/lead-capture-submit/index.ts`); exibição da Origem em `src/pages/CustomerDetail.tsx:823-839`.
- **Hoje:** o cliente nasce com `origin = 'public_form'` e a ficha mostra esse texto cru, sem ícone (a origem não
  existe no catálogo). Documento, telefone, celular e CEP chegam só com dígitos, enquanto o cadastro feito dentro
  do app grava com máscara. Ao editar e salvar, o formato muda. A busca do computador compara o texto gravado, então
  o mesmo cliente é achado por "12345678" num caso e por "12.345.678" no outro.
- **Esperado:** a Origem aparece como "Formulário de captação" (rótulo traduzido, com ícone). Documento, telefone,
  celular e CEP aparecem formatados na ficha e na lista. Decisão do Tech Lead: formatar na exibição ou padronizar
  o formato gravado (cuidado com NFS-e, cobrança e busca, que leem esses campos).
- **Aceite:** um cliente criado pelo link público mostra "Formulário de captação" na Origem e documento e telefone
  formatados na ficha e na lista.

### 3. Equipamento: mensagens cruas "customer_required" e "name_required"

- **Onde:** `src/components/customers/EquipmentFormDialog.tsx:33-34`.
- **Hoje:** clicar em "Criar" com "Cliente *" ou "Nome *" vazio mostra o texto cru `customer_required` /
  `name_required` embaixo do campo.
- **Esperado:** mensagem traduzida nos idiomas do app, por exemplo "Selecione o cliente" e
  "Informe o nome do equipamento".
- **Aceite:** "Criar" com os dois vazios mostra as duas frases traduzidas.

### 4. Campo personalizado Sim/Não aparece "Sim" quando o valor é "Não"

- **Onde:** `src/pages/EquipmentDetail.tsx:639` (testa só se o campo tem valor; o valor gravado é `sim` ou `nao`).
  Conferir também a "Visão geral" do equipamento no portal (`src/pages/CustomerPortal.tsx`) e a etiqueta.
- **Esperado:** `sim` → "Sim", `nao` → "Não".
- **Aceite:** equipamento com o campo em "Não" mostra "Não" na ficha e no portal.

### 5. Datas um dia antes na ficha do equipamento (fuso) (confirmar)

- **Onde:** `src/pages/EquipmentDetail.tsx:634-635,641`: `new Date('aaaa-mm-dd')` é lido como UTC e, no fuso do
  Brasil, vira o dia anterior. Afeta Data de Instalação, Garantia até e campos de data personalizados. Outras telas
  já usam `parseIsoDate`.
- **Esperado:** usar `parseIsoDate` (ou o helper equivalente do app) nesses três pontos; conferir portal e etiqueta.
- **Aceite:** instalação gravada em 10/03/2025 aparece 10/03/2025 num navegador em `America/Sao_Paulo`.

### 6. Editar equipamento pela ficha recarrega a página inteira; excluir pela ficha engole o erro

- **Onde:** `src/pages/EquipmentDetail.tsx:1192-1204` (editar: `reload` sem aviso) e `:1217-1226` (excluir: ignora
  erro, não avisa e não atualiza a lista em memória).
- **Hoje:** depois de editar, a tela pisca e recarrega tudo, sem toast. Ao excluir um equipamento que o banco recusa
  (por exemplo, com contrato), a pessoa volta para a lista, o equipamento continua lá e nada explica o porquê.
- **Esperado:** editar atualiza por invalidação da consulta (React Query) e mostra "Equipamento atualizado!", como já
  acontece em `src/components/customers/EquipmentPanel.tsx:201-214`. Excluir mostra o erro traduzido
  (`src/utils/errorMessages.ts`) e só sai da ficha se der certo, atualizando a lista.
- **Aceite:** editar pela ficha não recarrega a página e mostra o aviso. Excluir um equipamento com contrato mostra o
  motivo e mantém a ficha aberta.

### 7. Busca das listas no computador diferencia acento e não acha documento sem máscara

- **Onde:** `src/components/ui/ListDetailLayout.tsx:164-176` (vale para Clientes, Fornecedores e Equipamentos).
  O celular já tem a busca tolerante em `src/lib/utils.ts:14-69` (usada em `src/pages/Customers.tsx:274-285`).
- **Hoje:** "antonio" não acha "Antônio"; "12345678" não acha "12.345.678/0001-90".
- **Esperado:** a mesma busca tolerante do celular no computador (ignora acento, espaço sobrando e ordem das
  palavras; busca só por dígitos quando o texto é numérico).
- **Aceite:** "antonio" acha "Antônio"; "marcos braga" acha "Marcos Antônio Braga"; "12345678" acha o CNPJ com
  máscara; vale nas três telas.

## Prioridade 2 (triagem com o PM)

- **Permissão nas fichas:** "Editar" e "Excluir" do cabeçalho da ficha do cliente e da ficha do equipamento aparecem
  para quem não tem permissão (só a lista confere). `src/pages/CustomerDetail.tsx` (cabeçalho, `:670-802`) e
  `src/pages/EquipmentDetail.tsx` (`:391-480`).
- **"Novo Contato" fecha ao clicar fora** e perde o que foi digitado (os outros formulários não fecham).
  `src/components/customers/ContactFormDialog.tsx:100-125`.
- **Apagar não limpa na edição:** esvaziar Telefone, Email corporativo ou Cargo de um contato, a Data de Nascimento
  do cliente ou o último valor personalizado de um equipamento e salvar não remove o valor antigo (o campo vazio
  é omitido do envio). `ContactFormDialog.tsx`, `CustomerFormDialog.tsx` (`:245-330`),
  `EquipmentFormDialog.tsx:240-242`. Também não há botão para remover a foto do cliente.
- **Excluir sem confirmação:** origem de cliente (`src/components/customers/CustomerOriginManagerDialog.tsx:114`) e
  tarefa do equipamento. Excluir documento do cliente usa o `window.confirm` do navegador
  (`src/components/customers/CustomerDocumentsTab.tsx:146`), diferente dos outros diálogos.
- **Etiqueta do equipamento:** "Imprimir" não faz nada e não avisa quando o navegador bloqueia a nova janela
  (`EquipmentDetail.tsx:304-346`); tamanho com vírgula ("5,5") vira 5; a pré-visualização não mostra os rótulos
  que a impressão mostra.
- **Ficha do equipamento com rótulos fixos:** ignora o nome configurado dos campos padrão em "Configurar Campos"
  ("Capacidade/Especificação" aparece como "Descrição"; renomear "Marca" não muda a ficha nem a etiqueta).
  `EquipmentDetail.tsx:629-635`.
- **Lista de opções já existente:** "Adicionar opção" não acrescenta caixa e apagar o texto remove a opção na hora
  (confirmar). `src/components/customers/EquipmentFieldConfigDialog.tsx:419-422`.
- **Dois avisos de erro seguidos** (só o segundo aparece) ao falhar o cadastro de cliente (`CustomerFormDialog.tsx:325-326`)
  e de equipamento (`EquipmentFormDialog.tsx:251-258`).
- **Fornecedor:** o botão "Salvar" pula a validação de e-mail; no celular o vazio diz `Toque em "Novo Fornecedor"`,
  mas o botão se chama "Fornecedor". `src/components/inventory/SupplierFormDialog.tsx`, `SuppliersTab.tsx`.
- **Decisão de produto (PM):** CPF e CNPJ não são validados no cadastro de cliente, no cliente rápido nem no
  fornecedor; hoje só a cobrança barra documento inválido (`src/lib/documentValidation.ts`). Vale validar no
  cadastro?

## O que não mexer

- O tutorial T3 já contorna todos esses pontos; nada aqui bloqueia a gravação.
- Nenhum item pede mudança de layout ou de fluxo além do descrito.
