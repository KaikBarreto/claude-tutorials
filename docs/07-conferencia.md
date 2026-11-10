# 07 · Conferência antes de entregar

## Narração
- [ ] Cada arquivo bateu com o capítulo certo (semelhança ≥ 0,9 no `proc.py`).
- [ ] Palavras vigiadas ouvidas certas (QR Code, Hi-Wall, BTUs, Waze, nomes de marca, números).
- [ ] Nenhuma palavra engolida (as "sumidas" do ASR conferidas no trecho isolado).
- [ ] Nenhuma fala sobre o que o sistema não faz.

## Gravação
- [ ] 12/12 capítulos sem passo falho, `lateBy` < 0,8 s, `pageIssues` vazio.
- [ ] Versão do app certa no rodapé; empresa fictícia; nada real (documentos, telefones, e-mails `.example`).

## Edição (folha de quadros de cada capítulo + 1:1 nos zooms)
- [ ] `python3 -I auditar_camera.py` com 0 problema em todos os capítulos (alvo de cada clique/tecla no quadro,
      nenhuma âncora no canto); `render_chapter.py` já recusa capítulo com problema.
- [ ] Zoom cai no que a fala aponta; nenhum zoom exagerado (texto cortado); campo digitado nunca cortado na borda.
- [ ] Destaques no botão certo, com o rótulo igual ao da tela.
- [ ] Ilustração entra e sai na fala certa, sem zoom por baixo.
- [ ] Vinhetas de capítulo: título certo, voz lendo o título, whoosh na entrada e na saída.
- [ ] Depois do render (antes da limpeza): `python3 -I lacunas.py` (nenhum trecho > ~20 s sem zoom, destaque ou ilustração),
      `python3 -I confere_render.py` (zoom engolido; aviso sob zoom > 2,6× no celular; no computador `--toast R,G,B` acha o aviso
      da edição por cima do aviso do app: Dominex `--toast 4,150,105`) e a folha de destaques (`folha_destaques_16x9.py`; no 9:16
      do celular, `folha_destaques.py`, com OCR do rótulo).

## Final
- [ ] `ffprobe`: 1920×1080, 30 fps, H.264 yuv420p bt709 TV + AAC 48 kHz estéreo; duração = esperada.
- [ ] Loudness ~−16 LUFS, pico ≤ −1 dBTP; SFX audíveis mas abaixo da voz. Pico acima: `python3 -I pico_aac.py
      out/<AULA>/aula_final.mp4 out/<AULA>/proj/build/mix.wav mix_novo.wav --mux aula_nova.mp4` (−3 dB só no trecho, vídeo
      copiado com MD5 conferido; troque o arquivo à mão e rode o `entregar.py` de novo).
- [ ] Tira de quadros do final: vinheta, 1º quadro, uma vinheta de capítulo, um zoom, a ilustração, a cartela.
- [ ] **Folha de 3 s do vídeo INTEIRO, olhada do começo ao fim** (obrigatória; pega mês errado no calendário, aviso de erro do app,
      tela que a fala não descreve): `flock $TUT_HOME/.heavy.lock nice -n 10 bash folhas3s.sh out/<AULA>/aula_final.mp4
      out/<AULA>/folhas3s` (6×5 = 90 s por folha; o rótulo é o tempo do próprio quadro, `round=up`; no 9:16, 180×320 em 10×3).
      Nas duas proporções quando houver a vertical.
- [ ] Legendas abrem no player, sem sobreposição, no tempo da fala (conferir 3 pontos: início, meio, fim).
- [ ] Entrega: o vídeo completo 1080p + .srt + .vtt com o mesmo nome, enviados direto no chat (187 MB passou).

## Script de entrega
```bash
cd $DOMI/t<n>/edit
flock ../../.heavy.lock python3 -I entregar.py out/<AULA> "<Série> - <Título>"
```
Imprime specs, loudness e pico; gera `out/T<n>/conferencia.jpg` (vinheta, início, cada vinheta de capítulo,
ilustração, cartela); copia o vídeo e as legendas com o nome amigável em `out/T<n>/entrega/`; corta partes nas
vinhetas de capítulo indicadas (`--partes`, só se pedirem), com legendas no relógio de cada parte.
Legenda corrigida depois? `--so-legendas` refaz as legendas da aula e das partes sem reencodar nada.
Padrão: **um vídeo só, completo**. `--unico` (720p ≤ 29 MiB) e `--partes` existem só para um pedido explícito.
`--refazer 3` reencoda só a parte 3 quando um capítulo daquela parte mudou.
O arquivo completo vai direto no chat (em 30/10 passaram 187 MB); se um dia o envio recusar, salve numa pasta do computador da pessoa (sessão vinculada ao computador) ou outro canal que ela indicar.
