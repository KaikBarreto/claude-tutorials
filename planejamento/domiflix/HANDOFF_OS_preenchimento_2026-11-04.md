*HANDOFF | Atualização do preenchimento e edição de OS*

A experiência de preenchimento e edição da OS foi revisada. Considere estas mudanças antes de gravar ou atualizar os tutoriais.

*Status atual*

A implementação está pronta e validada localmente, mas ainda não teve commit, push ou deploy. Também existe uma migration pendente de aplicação. Não tratar como disponível em produção até a publicação ser confirmada.

*1. Nova edição da OS durante o preenchimento*

A ação “Editar OS” continua dentro do menu de mais ações e depende da permissão “Editar OS em campo”.

O modal não possui mais uma aba separada para Equipamentos e outra para Checklists avulsos.

Agora existem duas áreas principais:

- Equipamentos e checklists
- Data e horários

*2. Equipamentos e checklists numa única estrutura*

Na primeira área, a pessoa visualiza:

- Equipamentos da OS
- Checklists vinculados dentro de cada equipamento
- Checklists sem equipamento, no mesmo fluxo
- Quantidade de checklists por equipamento
- Indicação dos checklists que já possuem respostas

Equipamentos e checklists podem ser expandidos e recolhidos.

*3. Movimentação por arrastar*

Agora é possível:

- Reordenar equipamentos
- Reordenar checklists
- Arrastar um checklist sem equipamento para dentro de um equipamento
- Mover um checklist entre equipamentos
- Retirar um checklist de um equipamento e deixá-lo sem equipamento

Quando um checklist já possui respostas, elas acompanham o checklist durante a movimentação. A mudança é de vínculo, não uma exclusão seguida de uma nova criação.

O sistema também sinaliza visualmente qual item está sendo arrastado e qual será o destino.

*4. Adição e remoção*

Dentro do mesmo modal é possível:

- Adicionar equipamento
- Criar rapidamente um equipamento
- Selecionar checklists para cada equipamento
- Adicionar checklist sem equipamento
- Remover equipamento
- Remover checklist

Remoções que possam descartar respostas preenchidas exigem confirmação.

*5. Data e horários*

A aba “Data e horários” permite revisar ou remarcar a programação da OS sem sair do preenchimento.

Ela contempla:

- Data
- Horário
- Duração
- Programação em mais de um dia, quando aplicável
- Validação de conflito de agenda

*6. Mudanças visuais no preenchimento da OS*

O início da OS ficou mais limpo e contínuo.

Check-in, cliente, telefone, endereço, contrato, descrição do serviço e observações agora aparecem em um único bloco visual, sem vários cards e bordas.

A hierarquia atual é:

- Metadados, como check-in e rótulos auxiliares, menores e em tom secundário
- Nome do cliente e contrato com maior peso
- “Descrição do serviço” e “Observações” em negrito
- “Checklists” como título principal da área

O bloco do cliente atualmente usa o ícone padrão. A foto do cliente não é exibida nessa área, mesmo quando existir cadastro de foto.

*7. Checklists*

O título geral “Checklists” não repete mais o ícone usado no checklist específico.

Nomes extensos de checklist quebram linha e não devem ser apresentados com reticências.

Cada equipamento continua com seu cabeçalho próprio, mostrando nome, categoria, ambiente, modelo e andamento das respostas.

*8. Cores e estados*

A interface reduziu o uso do verde como cor genérica de ação.

Agora:

- Preto, branco e tons neutros são usados nas ações operacionais
- Verde permanece para sucesso, conclusão e resposta salva
- Laranja permanece para finalização parcial ou atenção
- Estados de arraste não usam fundos pastéis
- Quando existe fundo saturado, texto e ícone são brancos

*9. Rodapé móvel*

O rodapé de ações é preto/cinza escuro e totalmente opaco.

Ele contém:

- Finalizar
- Finalizar parcial
- Menu de mais ações

Um print anterior mostrou esse rodapé transparente, mas era apenas uma falha da prévia isolada. O componente real utiliza fundo escuro opaco.

*10. Comportamento offline*

A edição de equipamentos, checklists e programação continua disponível somente com internet.

Quando estiver offline, a ação “Editar OS” permanece desativada com a indicação “Disponível apenas online”.

*Prints de referência*

Modal Editar OS no celular:
.context/edit-os-mobile.png

Modal Editar OS no computador:
.context/edit-os-desktop.png

Aba Data e horários no celular:
.context/edit-os-schedule-mobile.png

Preenchimento da OS com nova hierarquia:
.context/os-fill-hierarchy-mobile.png

Rodapé móvel opaco corrigido:
.context/os-fill-footer-opaque-mobile-v2.png

*Orientação para o tutorial*

Antes de gravar, confirmar se a branch foi publicada e se a migration foi aplicada no ambiente usado na gravação.

O trecho antigo que diz que “Editar OS abre duas abas, Equipamentos e Checklists avulsos” está desatualizado e deve ser substituído pela estrutura unificada “Equipamentos e checklists”, com movimentação por arrastar.

Também vale demonstrar o principal caso de uso:

1. A OS foi criada com um checklist sem equipamento.
2. O equipamento é cadastrado depois.
3. A pessoa abre “Editar OS”.
4. Arrasta o checklist para dentro do equipamento.
5. Salva a alteração.
6. As respostas já preenchidas permanecem no checklist.