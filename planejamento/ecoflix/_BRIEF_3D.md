# Briefing das cenas 3D · trilha EcoFlix (passar para 3D as cenas físicas de uma ou mais aulas)

Repositório da skill: `/home/claude/claude-tutorials` (caminhos relativos a ele). O Kaik aprovou o 3D de argila em 11/11
(piloto: T07 cap06) e pediu as cenas de conceito físico em 3D. Cada cena 2D já existe e está aprovada em estilo; a 3D
**conta a mesma história, com as mesmas âncoras e os mesmos textos**, e a 2D fica de reserva (não apague nada dela).
**Tarefa**: as cenas da sua lista em `planejamento/ecoflix/Tnn/cenas3d/cena3d.html`, conferidas em quadros, com uma
prévia em vídeo por aula. Sem aprovação no meio: termine e relate.

## Ler antes (só isto)
1. `perfis/ecoflix/cenas3d/LEIA.md` (o kit) e `perfis/ecoflix/cenas3d/kit3d.js` (a API; objetos prontos: caminhão,
   balança rodoviária, carroça, caçamba, saco, tambor, monte de sucata, palete, fardo, prensa, latinhas, baterias,
   impressora, computador, chão do pátio...).
2. Os dois exemplos: `planejamento/ecoflix/T07/cenas3d/cena3d.html` e `planejamento/ecoflix/T08/cenas3d/cena3d.html`
   (um `CAPS` por capítulo, rótulos HTML presos ao mundo, câmera com chaves, `W(linha, 'palavra')`).
3. Da aula: `cenas/ilustracoes.json` (a entrada da cena: `de`, `ate`, `cauda`, `resumo`, `mostra`), o `CAPS[n]` da cena
   2D em `cenas/cenas.html`, os tempos estimados `cenas/tempos/capNN.json`, a fala em `narracao/tts_textos.py` e, quando
   a cena cita rótulo do app, o `inventario.md`. Nomes e números: `planejamento/ecoflix/MUNDO_FICTICIO.md`.

## Como a cena 3D deve ser
- Mesma ideia, mesmas palavras de entrada, mesmos textos da 2D (`mostra`): nada de número, nome ou rótulo novo. Título
  na tela desde o primeiro quadro da janela (`titulo` + `posTitulo`), cada objeto entra na palavra que o nomeia, nada sai
  antes do fim da janela, quadro nunca vazio. Movimento de câmera suave, sem zoom brusco (Kaik: "evite zooms bruscos").
- Estilo saturado (selo, chip e quadrado de ícone com fundo cheio e ícone/texto branco), cores da marca do kit, argila
  fosca, sem marca, logo ou tela do app. Desenho genérico; a 3D ganha quando mostra o objeto físico (caminhão, carga,
  pilha, prensa, balança, impressora, cupom); conceito abstrato (lista, regra, fluxo de documento) fica na 2D: se uma cena
  da sua lista não ganhar nada em 3D, deixe na 2D e diga no relatório.
- **Tara**: no Ticket de Pesagem e na compra, Tara é a embalagem (saco, tambor, caçamba); na dupla pesagem o caminhão
  vazio não é tara. No cadastro de veículo das Coletas (T12) o app chama o peso do veículo vazio de "Tara (kg)": ali a
  tara É o caminhão vazio. Siga o rótulo do app de cada módulo.
- Objeto que o kit não tem: crie em `perfis/ecoflix/cenas3d/objetos/<nome>.js` (um arquivo por objeto, módulo ES que
  importa do kit, com um comentário de uso no topo). Antes, olhe a pasta: outro agente pode ter feito o mesmo objeto
  (use o dele). **Nunca edite o `kit3d.js`** nem arquivo de outra aula (outros agentes usam). Diga no relatório o que criou.
- No `ilustracoes.json` da aula, só acrescente `"3d": "cenas3d/cena3d.html"` na entrada da cena feita em 3D.

## Conferir e prévia (nunca na trava pesada: ela é da gravação dos robôs)
Quadros e prévia na **trava leve com prioridade baixa**, em `/dev/shm/ilu3d/Tnn/` (fora do git):
```bash
mkdir -p /dev/shm/ilu3d/Tnn && cd /dev/shm/ilu3d/Tnn && flock /home/claude/ecoflix/.stills.lock nice -n 19 timeout 600 \
  node /home/claude/claude-tutorials/ferramentas/edit/cenas/render_cenas.cjs N <aula>/cenas/tempos/capNN.json capNN \
  --html <aula>/cenas3d/cena3d.html --dsf 1 --stills t1,t2,...
```
Instantes: o primeiro quadro da janela, o meio e o fim de cada linha coberta e o último quadro. Folha de contato (PIL),
olhe tudo (texto cortado, rótulo longe do objeto, objeto atravessando outro, câmera cortando o assunto, quadro vazio,
`ERROS:` e `AVISOS:` no console); corrija e confira de novo.
Prévia da aula: cada cena com `--de <início da janela> --ate <fim da janela> --dsf 1.35`, em trechos de até 13 s (cada
trecho uma chamada na trava leve com `nice -n 19 timeout 900`), juntados com o concat do ffmpeg (`-c copy`), todas as
cenas da aula num arquivo só: `/home/claude/ecoflix/previa_ilustracoes/Tnn_3d.mp4` (até 25 MB) e uma folha com 12
quadros em `/home/claude/ecoflix/previa_ilustracoes/Tnn_3d.jpg`. Arquivo temporário com nome terminado em `.mp4` e
renomeado só depois do ffmpeg sair com 0. Apague `/dev/shm/ilu3d/Tnn` no fim.

## Limites
- Escreva só em `planejamento/ecoflix/Tnn/cenas3d/` e no `ilustracoes.json` das suas aulas, em
  `perfis/ecoflix/cenas3d/objetos/` (arquivos novos) e em `/home/claude/ecoflix/previa_ilustracoes/`. Não mexa em
  `roteiro.md`, `tts_textos.py`, `cenas/cenas.html`, no kit, em `ferramentas/`, outras aulas, `PRODUCAO.md` nem no
  repositório do app (só leitura). Mudança de fala que a cena pediria: proponha no relatório (linha e texto novo).
- Não faça commit (o coordenador faz). Scripts auxiliares no seu scratch; nunca rode script de outro agente. Nada de
  `pkill`/`killall`, `git stash`, `reset` ou `clean`; `rm` só com caminho absoluto literal. Salve cedo e com frequência.

## Relatório final (até 200 palavras)
Por aula: cenas feitas em 3D (capítulo e id), as que ficaram na 2D e por quê, objetos novos criados, achado do app ou do
mundo, mudança de fala proposta e o caminho da prévia.
