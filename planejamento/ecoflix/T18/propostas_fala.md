# T18 · propostas de fala (robô)

Base: ensaios rápidos do robô com a voz ESTIMADA. O tempo fino só se confere na gravação final com a voz de verdade.
Não editei `roteiro.md` nem `tts_textos.py`.

## O que a fala deve mudar

| Cap. | Linha | Texto atual | Texto novo | Motivo |
| --- | --- | --- | --- | --- |
| 1 | L1 | (a voz começa em "Gerador é quem produz...") | Acrescentar a primeira linha do roteiro: "Aqui em Ambiental ficam as duas abas: MTR e CDF. Em português claro, é assim." | A voz de 5 linhas não tem a linha 1 do roteiro; sem ela a tela das abas fica sem fala (o robô só deixa o cursor em repouso). |
| 3 | L9 | "Código do IBAMA, classe, estado físico, acondicionamento e tratamento vêm das listas do órgão. Quem confirma cada um é quem cuida da licença da empresa." | manter o texto e pôr uma pausa de ~3 s depois de "tratamento" | Cinco escolhas em ~6 s de fala; o robô fecha as cinco só por volta de "Quem confirma" (atraso previsto até 2,3 s). |
| 3 | L12 | "Por último, em Materiais, eu ligo os três ferros a esse resíduo. ..." | manter e pôr pausa de ~4 s no fim da linha | Menu, três marcas, ação em massa, escolha do resíduo e confirmar são ~9 gestos em ~10 s. |
| 4 | L2 e L3 | cadastro dos dois parceiros em ~13 s e ~9 s | pausa de ~2 s no fim de cada uma (ou "[pause]") | Três campos digitados e "Salvar e usar" por parceiro; o modelo de custo prevê atraso de 1,4 a 2,5 s em L3. |
| 7 | L4 | "Novo CDF. No período, outubro inteiro." | acrescentar pausa de ~2 s no fim | Abrir o calendário duas vezes, voltar o mês e escolher os dias 1 e 31 não cabe em 3,6 s. |
| 3 | L6 | "Salvar acesso. E Testar acesso salvo: pronto, validado." | sem mudança no texto | O app mostra no cartão "Acesso aceito ... depende do perfil Gerador" (não o toast "Acesso ao SIGOR validado" do roteiro); a fala continua certa. |

## Achados do app (1.59.154)

- O selo "Acesso validado" do roteiro é, na tela, o cartão verde "Acesso ao SIGOR aceito. A emissão ainda depende de a unidade possuir perfil Gerador no portal." (mensagem real da edge). Texto do roteiro precisa seguir isso.
- "Sistema:" mostra "SIGOR-MTR / CETESB-SP" (nome do banco), não só "SIGOR".
- O formulário "Novo resíduo" é um cartão dentro de Configurações, não uma janela; o campo "Classe" só libera depois do código IBAMA.
- Em Materiais, a barra de ações em massa é fixa no rodapé e o botão "Definir resíduo do MTR" fica ATRÁS do botão flutuante do Cato (clique de verdade abre o Cato, e na primeira visita aparece o aviso "Antes da primeira conversa com o Cato"). O robô clica por eval.
- O MTR e o CDF não têm passo "Resumo": o resumo do MTR fica no painel lateral e o último passo ("Responsável" / "Confirmar") já traz "Emitir".
- Coluna "Gerador" do CDF mostra o CNPJ formatado, não o nome da Auto Peças Vale Forte (o roteiro diz o nome).
- "Baixar PDF" abre aba nova; o robô não grava essa aba.
- "Novo MTR" desligado mostra a dica "Configure o acesso ao SIGOR primeiro" (confere).
