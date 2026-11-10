# Briefing das ilustrações · trilha EcoFlix (as cenas de conceito de uma ou mais aulas)

Repositório da skill: `/home/claude/claude-tutorials` (caminhos relativos a ele). Os roteiros das 26 aulas estão prontos
em `planejamento/ecoflix/Tnn/`: o `roteiro.md` marca cada cena com `[ILUSTRAÇÃO: ...]` e o `narracao/tts_textos.py` tem o
texto exato da voz (`CAPS[n]`, uma linha da fala por linha da tabela). A voz ainda não existe (vem por último): as cenas
ficam presas às palavras com `W(linha, 'palavra')` e se ajustam sozinhas quando o `capNN.json` de verdade chegar.
**Tarefa**: montar todas as cenas `[ILUSTRAÇÃO]` das suas aulas no kit da EcoFlix, conferir em quadros e deixar prontas
para o render da edição. Sem aprovação no meio: termine e relate.

## Ler antes (só isto)
1. `docs/09-aula-ilustrada.md`: "Cenas", "Conferir antes do render" e "Ilustração de conceito no meio do capítulo (kit
   EcoFlix)".
2. `perfis/ecoflix/cenas/cenas_ecoflix.html`: utilitários (`vis`, `conta`, `traco`, `arco`, `contorno`, `posTitulo`,
   `titulo`, `ic`, `kg`, `brl`, `caminhao`...) e os dois exemplos (`CAPS[1]` "Tara e peso líquido", `CAPS[2]` "Caixa ×
   competência"). Se a sua aula tem um desses conceitos, use o mesmo desenho.
3. `perfis/ecoflix/PERFIL.md`: marca e regras da fala.
4. Das suas aulas: `roteiro.md` (as marcações e a fala ao lado), `narracao/tts_textos.py`, e o `inventario.md` quando a
   cena cita rótulo do app; `planejamento/ecoflix/MUNDO_FICTICIO.md` para nomes e números do mundo.

## Entregar, por aula (em `planejamento/ecoflix/Tnn/cenas/`)
1. `cenas.html`: cópia do kit com os `CAPS[n]` da aula (os dois exemplos saem, menos o que você reaproveitar). Várias
   cenas do mesmo capítulo ficam no mesmo `CAPS[n]`, cada uma na sua janela de tempo.
2. `tempos/capNN.json` (tempos estimados de cada capítulo com cena):
   `python3 ferramentas/edit/cenas/tempos_estimados.py planejamento/ecoflix/Tnn/cenas/tempos/capNN.json --tts planejamento/ecoflix/Tnn/narracao/tts_textos.py --cap N`
   O `W()` procura a grafia da legenda (já com as trocas: "QR", não "quê-érre"); número por extenso vira palavras soltas.
3. `ilustracoes.json`: uma entrada por cena, na ordem da aula:
   `{"cap": 3, "id": "ilu03_chave", "de": [2, "link", 1], "ate": [4, "fechada", 1], "cauda": 0.6, "resumo": "o link é uma chave"}`
   `de` = [linha, palavra, ocorrência] em cujo início a cena começa (a janela abre 0,3 s antes); `ate` = a palavra em cujo
   fim a cena pode sair; a janela fecha `cauda` segundos depois. A cena usa exatamente essas âncoras: é com elas que a
   edição calcula o `at`, o `dur` e o `repouso` do `specs.json`.

## Como a cena deve ser (PERFIL e Domiflix, sem exceção)
- **Uma ideia por cena**, fácil de entender para quem não é técnico: a cena mostra, a fala explica. Texto curto (título
  até 5 palavras; chips de 1 a 3 palavras). Nada de parágrafo na tela.
- **Nunca desenhe tela do app** nem invente tela, função, botão ou número. Desenho genérico (caminhão, balança, pátio,
  documento, celular sem marca), sem logo nem marca de terceiros. Rótulo do app só igual ao `inventario.md`; nome e
  número só os do mundo e da fala (formato brasileiro com `kg()` e `brl()`).
- **Presa à fala**: o título já está na tela no primeiro quadro da janela (`posTitulo`: grande no centro, sobe quando o
  desenho entra); cada elemento entra na palavra que o nomeia. Movimento suave (entradas de 0,4 a 0,6 s), nada piscando,
  nada saltando. **Cartão nunca vazio** (`docs/09`, regra 6) e nada sai antes do fim da janela.
- Texto medido: nada cortado nem a menos de 12 px da borda do cartão ou do elemento. Contraste: verde de texto `#2E7D57`,
  âmbar `#8A5A00` para o segundo conceito; o acento `#50D088` só em preenchimento, barra e contorno.
- Sem travessão em texto da cena; sem "Passo 1/5" nem contador de etapas.
- A marcação do roteiro é o ponto de partida, não contrato: se ela pedir algo que contradiz o app ou o mundo, ou que não
  cabe com clareza, simplifique e diga no relatório. **Não altere `roteiro.md` nem `tts_textos.py`**: se a fala precisar
  mudar para a cena funcionar, proponha no relatório (linha e texto novo).

## Conferir (obrigatório antes de dar a aula por pronta)
Quadros JPEG, **sempre sob a trava** (a máquina tem 2 CPUs e a gravação do robô disputa a mesma CPU), todos os instantes
de um capítulo numa chamada só, em `/dev/shm/ilu/Tnn/` (fora do git):
```bash
mkdir -p /dev/shm/ilu/Tnn && cd /dev/shm/ilu/Tnn && flock /home/claude/ecoflix/.heavy.lock \
  node /home/claude/claude-tutorials/ferramentas/edit/cenas/render_cenas.cjs N <caminho>/tempos/capNN.json capNN \
  --html <caminho>/cenas.html --stills t1,t2,...
```
Instantes: o primeiro quadro da janela, o meio e o fim de cada linha de fala coberta e o último quadro. Monte uma folha
de contato (PIL) e olhe tudo: texto cortado, sobreposição, elemento que não entrou, cartão vazio, contraste, aviso
"palavra não achada" no console. Corrija e confira de novo. Não renderize MP4 (sai na edição).
No fim de cada aula: uma folha de contato com todas as cenas em `/home/claude/ecoflix/previa_ilustracoes/Tnn.jpg`
(JPEG até 1,5 MB, para o coordenador) e apague `/dev/shm/ilu/Tnn`.

## Limites
- Só escreva em `planejamento/ecoflix/Tnn/cenas/` das suas aulas e em `/home/claude/ecoflix/previa_ilustracoes/`. Não
  mexa em `perfis/`, `ferramentas/`, outras aulas, `MUNDO_FICTICIO.md`, `PRODUCAO.md`, `MELHORIAS_ECOSISTEMA.md` nem no
  repositório do app (só leitura). Faltou utilitário no kit: escreva na cena da aula e conte no relatório.
- Não faça commit (o coordenador faz). Scripts auxiliares no seu scratch, com o prefixo da aula; nunca rode script de
  outro agente. Nada de `pkill`/`killall`, `git stash`, `reset` ou `clean`; `rm` só com caminho absoluto literal.
- Salve cedo e com frequência (um reinício da máquina mata o agente, mas o disco fica).

## Relatório final (até 200 palavras)
Por aula: quantas cenas e em que capítulos; o que simplificou ou deixou de fora e por quê; mudança de fala proposta
(linha e texto); achado do app ou do mundo para o coordenador; utilitário que faltou no kit.
