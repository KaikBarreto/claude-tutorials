# Briefing do roteiro · trilha EcoFlix (uma aula: do código ao texto da voz)

Repositório da skill: `/home/claude/claude-tutorials` (os caminhos abaixo são relativos a ele).
Objetivo: deixar a aula **pronta para gerar a voz e gravar**, sem etapa de aprovação (como na Domiflix: o Kaik ajusta
depois se precisar). Uma pasta por aula: `planejamento/ecoflix/Tnn/` (dois dígitos: T03, T16). Só escreva na pasta da
sua aula. Não faça commit. Não edite `MUNDO_FICTICIO.md`, `PERFIL.md`, `TRILHA.md` nem arquivo de outra aula: o que
precisar mudar neles vai no relatório.

## Ler antes (nesta ordem, só o necessário)
1. `perfis/ecoflix/PERFIL.md` (vale inteiro; o que ele não muda é o da Domiflix, `perfis/domiflix/PERFIL.md`).
2. A fonte da sua aula: `python3 -I planejamento/ecoflix/trecho_aula.py Tn`, e o molde: `... trecho_aula.py molde`.
   Não leia a fonte inteira (60 mil tokens).
3. `planejamento/ecoflix/MUNDO_FICTICIO.md` e a linha da sua aula em `planejamento/ecoflix/TRILHA.md`.
4. Formato (copie a forma, não o conteúdo): `planejamento/domiflix/T21/` (`inventario.md`, `plano.md`, `roteiro.md`,
   `narracao/tts_textos.py`, `narracao/config_narracao.json`) e `exemplos/dominex-t3/estilo_narracao.md`.
5. O código do app na versão gravada (1.59.154, só leitura): `/home/claude/ecoflix/app-src-1.59.154/` (`src/` e
   `supabase/functions/`). Ache a tela pela rota ou pelo menu e leia só os componentes dela. Rótulo na fala e na coluna
   Tela = o texto exato do código.

## Entregar (em `planejamento/ecoflix/Tnn/`)
1. `inventario.md` (enxuto): cada tela da aula com rota, componente (`arquivo:linha`), os rótulos usados (botões,
   abas, campos, avisos, toasts, mensagens de erro citadas) e as chamadas ao backend (tabela, RPC, edge function) que
   a tela faz. Só o que a aula usa.
2. `plano.md`: capítulos (os da fonte, na ordem), o que se mostra em cada um, o estado de partida, e as seções
   **"Mundo: o que esta aula precisa"** (dados além do `MUNDO_FICTICIO.md`, com valores) e **"Gravação"** (rotas, RPCs,
   edge functions e integrações a simular; celular, página pública ou outro usuário, se houver; ilustrações, se houver).
3. `roteiro.md`: cabeçalho (título = o da fonte; "Antes: <pré-requisito da fonte>"; "Próximo: <a aula do Próximo da
   fonte>"; áreas das vinhetas; duração estimada) e, por capítulo, `### capMM · <título da vinheta> (vinheta: ÁREA)` +
   tabela **Tela | Fala** (uma linha da tabela = uma linha da fala). cap00 = abertura (sem vinheta); o último =
   "Recapitulando" (com vinheta). Tela: ações exatas do robô e onde a câmera foca, rótulos entre aspas como no código;
   o que o backend falso ainda não tem vai marcado `[BACKEND: ...]`; zoom nos campos críticos (CNPJ, peso, valor,
   alíquota, chave de acesso, número da nota) marcado `[ZOOM: ...]`.
4. `narracao/tts_textos.py`: `CAPS = {0: """linha\nlinha""", ...}` (o texto EXATO para o TTS, uma linha por linha da
   tabela, com a grafia de pronúncia do PERFIL), `TITULOS = {1: "Título.", ...}` (só os capítulos com vinheta) e
   `KICKERS = {1: "Área", ...}`.
5. `narracao/config_narracao.json`: cópia de `perfis/ecoflix/narracao/config_narracao.json` + as trocas da tabela de
   pronúncia que a aula usa + trocas novas (mesmo número de palavras dos dois lados).

## Regras da fala (PERFIL e Domiflix, sem exceção)
- Colega mostrando ao vivo: "a gente", "você", "olha", "repara" (no máximo um a cada 3 ou 4 frases), "pronto". Frases
  curtas, uma ideia por frase. Exemplo concreto antes da regra. Dados do pátio ditos em voz alta (material, peso, valor).
- Abertura "Oi! Neste tutorial a gente vai..." com o problema real, citando a Recicla Vale Metais; o pré-requisito;
  cada capítulo abre com uma transição falada; no fim, "Recapitulando", "No próximo tutorial, ..." e "Até lá!".
- ⚠️ falado com "Uma dica:" na hora certa. 🚫 como informação do que acontece, no positivo. 🔒: dizer que depende do
  plano contratado (preço de plano, nunca).
- **Erro na tela (Kaik, 10/11)**: caminho certo primeiro e a consequência como informação; a mensagem de erro só
  aparece na tela quando reconhecê-la é o ponto (ex.: "Abra o caixa antes de realizar compras"), e a saída vem logo
  em seguida.
- Rótulos ditos exatamente como na tela. **Nenhum travessão** (— ou –), nem nas frases tiradas da fonte. Sem
  superlativo, sem tom de anúncio, sem prometer o que o app não faz, nada do que a fonte deixa de fora ("Em breve",
  telas fora da trilha).
- Fiscal: regime do exemplo **Lucro Real**; a fala mostra os campos e diz que quem define a tributação é o contador;
  não ensina regra tributária.
- Tamanho: o tempo natural da fala (~2,6 palavras/s, ~790 caracteres por minuto); a minutagem da fonte é alvo.
- **Simples (Kaik, 10/11)**: palavras do dia a dia do pátio; termo técnico explicado na primeira vez em que aparece,
  com um exemplo do ferro-velho; uma ideia por frase. Se der para dizer mais curto, diga.

## Ilustrar conceitos (Kaik, 10/11: mais do que na Domiflix)
Sempre que a fala explicar um conceito, e não só uma tela (caixa × competência, saldo a favor e contra, tara e peso
líquido, cofre × caixa, o caminho da nota até a SEFAZ, MTR e CDF, matriz e filial, ficha técnica...), marque na coluna
Tela `[ILUSTRAÇÃO: <conceito>: o que o desenho mostra, em que ordem, com qual frase]`. Ilustração é desenho por código
ou cena HTML no estilo da marca (`docs/09-aula-ilustrada.md`), nunca uma tela inventada do app. Pelo menos uma em
cada capítulo que explica conceito; a abertura também pode ter uma (o problema do pátio).

## Sem erro na gravação (Kaik, 10/11)
- Cada afirmação conferida no código da 1.59.154 (a fonte conferiu ⚠️ e 🚫; se código e fonte discordarem, vale o
  código, e isso vai no relatório). Número na fala só do mundo fictício.
- Zoom nunca brusco: cada `[ZOOM: ...]` dura a frase inteira que fala do campo (≥ 2,5 s), sem zoom em cima de zoom; a
  Tela dá tempo para a ação acontecer antes da fala que a comenta.
- A voz não é gerada agora: os textos passam por uma revisão geral e por um ensaio gravado antes (economia de créditos).

## Gravável
A coluna Tela tem de ser executável pelo robô no app real (1.59.154) com o backend falso: só telas e rótulos que existem
no código, com os dados do mundo fictício. O que não dá para gravar com verdade (tela do Windows, papel saindo da
impressora) fica na fala ou vira `[GRAVAÇÃO REAL: ...]`; nunca tela inventada. Dados novos plausíveis para ferro-velho
em Taubaté, SP; CPF e CNPJ com dígito verificador válido (calcule); e-mails `.example`; nada real.

## Relatório (≤ 150 palavras)
Arquivos; capítulos, palavras e duração estimada; pronúncias novas; resumo dos `[BACKEND: ...]` e do "Mundo: o que esta
aula precisa"; dúvidas que só o Kaik responde.
