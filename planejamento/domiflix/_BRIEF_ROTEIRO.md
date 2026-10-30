# Briefing do roteiro · trilha Domiflix (molde T3; vale para todos os tutoriais com tela)

Objetivo: deixar o tutorial **pronto para gerar a voz e gravar**, sem etapa de aprovação (Kaik, 30/10 22:44: "faça
todos... se precisar depois eu ajusto detalhes"). Decisões abertas seguem `PRODUCAO.md` → "padrão adotado".

## Ler antes
`perfis/domiflix/PERFIL.md` · `docs/01-padrao.md` · `docs/02-roteiro.md` · `docs/03-narracao.md` ·
`exemplos/dominex-t3/roteiro.md` (o molde) · `exemplos/dominex-t3/estilo_narracao.md` ·
`exemplos/dominex-t3/narracao/tts_textos.py` e `config_narracao.json` · `planejamento/domiflix/{TRILHA,PRODUCAO,MUNDO_FICTICIO}.md` ·
`Tnn/inventario.md` e `Tnn/plano.md` (e o `plano.md` da aula anterior na ordem de exibição, para a continuidade).

## Entregar (em `planejamento/domiflix/Tnn/`)
1. `roteiro.md`: cabeçalho (título final, áreas das vinhetas, "Antes: <aula anterior>", "Próximo: <próxima>",
   duração estimada) e, por capítulo, `### capMM · <título da vinheta> (vinheta: ÁREA)` + tabela **Tela | Fala**.
   cap00 = abertura (sem vinheta); último = "Recapitulando" (com vinheta, como no T3). Uma linha da tabela = uma linha
   da fala. Tela: ações exatas do robô e onde a câmera foca, com os rótulos entre aspas como na tela (do inventário);
   o que precisar de backend que o falso ainda não tem vai marcado `[BACKEND: ...]`.
2. `narracao/tts_textos.py`: `CAPS = {0: """linha\nlinha""", 1: ...}` (texto EXATO enviado ao TTS, uma linha por
   linha da tabela, grafia de pronúncia aplicada), `TITULOS = {1: "Título.", ...}` (só os capítulos com vinheta) e
   `KICKERS = {1: "Área", ...}`.
3. `narracao/config_narracao.json`: cópia de `perfis/domiflix/narracao/config_narracao.json` + as trocas/números novos.

## Regras da fala (as do T3, sem exceção)
- Colega mostrando o sistema ao vivo: "a gente", "você", "olha", "repara" (no máximo um a cada 3 ou 4 frases),
  "pronto". Frases curtas, uma ideia por frase. Exemplo concreto antes da regra. Dica prática quando houver.
- **Só possibilidades**: nunca narrar o que o sistema não faz ou dificuldade. Cuidados (⚠️): primeiro o caminho
  certo, depois a consequência numa frase, como informação; nunca encenar a falha.
- Rótulos da interface ditos exatamente como na tela. **Nenhum travessão** (— ou –) no texto. Sem superlativo, sem tom
  de anúncio, sem prometer o que o app não faz. Sem preço de plano da Dominex.
- Abertura: o que vai ser feito + por quê + "se você ainda não viu <aula anterior>, dá uma olhada antes".
  Cada capítulo começa com uma transição falada. Fim: recapitulação curta + "no próximo tutorial, ...".
- Pronúncia (texto do TTS): siglas e números como a voz deve ler (tabela em `docs/02-roteiro.md` e no
  `config_narracao.json` do perfil: QR Code, BTUs, Hi-Wall...). Toda troca nova vai para `trocas`/`numeros`.
- Tamanho: o tempo natural da fala (~2,6 palavras/s na Fernanda); o T3 teve 12 capítulos e ~1.770 palavras.

## Gravável
A coluna Tela tem de ser executável pelo robô no app real com o backend falso: só telas e rótulos que existem
(inventário com `arquivo:linha`), dados do mundo fictício (`MUNDO_FICTICIO.md` + estado final da aula anterior).
Dados novos: plausíveis para climatização em Niterói/RJ; CPF/CNPJ com dígito verificador válido (calcule);
e-mails `.example`; nada real.

## Relatório (≤ 150 palavras)
Arquivos, palavras por capítulo e duração estimada, pronúncias novas, lista resumida de `[BACKEND: ...]`.
