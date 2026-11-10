# Retomadas agendadas · EcoFlix (pedido do Kaik, 10/11 00:29)

> "consegue estruturar de uma forma que você continue fazendo tudo independentemente de acabar meu limite de 5h ou
> semanal? ir voltando a fazer conforme voltar o limite"

Lembretes `send_later` nesta mesma sessão, "EcoFlix: retomar produção (N/20)": de 5 em 5 h até 12/11, depois de 12 em
12 h. Lembrete que chega com o trabalho andando: só conferir e seguir. O 20º agenda uma série nova se ainda faltar.

## O que fazer em cada retomada
1. Estado: `git -C /home/claude/claude-tutorials status --short`; branches `consolidacao-domiflix`, `ecoflix-mundo` e
   `ecoflix-marca` (`git log -1 origin/<branch>`); aulas prontas em `planejamento/ecoflix/Tnn/` (pronta = `inventario.md`,
   `plano.md`, `roteiro.md`, `narracao/tts_textos.py` e `narracao/config_narracao.json`); `df -h /home/claude`; `free -g`.
2. Agentes que pararam no meio (limite, reinício do container) são relançados com o mesmo briefing, dizendo o que já
   existe na pasta. Modelo: opus até o limite do Sonnet voltar (11/11); depois sonnet no trabalho mecânico. Até 20 ao
   mesmo tempo quando o limite está novo (pedido do Kaik); trabalho pesado sempre um por vez
   (`flock /home/claude/ecoflix/.heavy.lock`).
3. App e Supabase falso: se o container reiniciou (/dev/shm vazio), religar com os comandos do relatório do agente
   Mundo (anotados em PRODUCAO.md).
4. Seguir a fila de PRODUCAO.md ("Fila"), anotando cada passo no "Registro".
5. Commit e push do que houver nas pastas das aulas, mesmo em andamento: é a cópia de segurança contra reinício da
   máquina (a mensagem diz "em andamento"). Nunca stash, reset ou clean.
6. Fim de tudo: ZIP das legendas e capítulos, o **report de melhorias do sistema** (`MELHORIAS_ECOSISTEMA.md`),
   avisar o Kaik e apagar com `delete_trigger` os lembretes que sobrarem.

| N | Dispara (UTC) | trigger_id |
|---|---|---|
| 1 | 10/11 05:40 | trig_012LJECQRj5zwWjJSJZ3A8yG |
| 2 | 10/11 10:40 | trig_01E7HQX1hL57nrG3QCVpL2Y4 |
| 3 | 10/11 15:40 | trig_013v94ECRjAmgxv1XwzZjwwX |
| 4 | 10/11 20:40 | trig_01HSoKXeBpSVjuFpkTZdbC3T |
| 5 | 11/11 01:40 | trig_01QnqeL9mKMM7M4DWEKMCHYn |
| 6 | 11/11 06:40 | trig_01BwfAokFrZypguxzvEU1CHZ |
| 7 | 11/11 11:40 | trig_0188ZLp9mJLMLRG5JS22i4vK |
| 8 | 11/11 16:40 | trig_016njxidHyfaggJ1SLBTNBea |
| 9 | 11/11 21:40 | trig_01XN7yFmydJVA4cwfcXh7FPu |
| 10 | 12/11 02:40 | trig_01V1WCamq8sm7huYqYRgVRuz |
| 11 | 12/11 07:40 | trig_018CYAsoSony9yfNg4aVm9XF |
| 12 | 12/11 12:40 | trig_01YXHJ9SfBynELvuKJTXackH |
| 13 | 12/11 17:40 | trig_01VCyXRthzp74bytQMYPGXhE |
| 14 | 12/11 22:40 | trig_016F2AqcbERBdzUNmwN1Ngc6 |
| 15 | 13/11 10:40 | trig_01M9c9neEGQ4Syr163MGiUuc |
| 16 | 13/11 22:40 | trig_01WJB1L7isfcXi6bzjpjXUMY |
| 17 | 14/11 10:40 | trig_01YVDvgnay8t1HNWCsUoLq4U |
| 18 | 14/11 22:40 | trig_01Nd8WEM6SxLecD4R3LPPUfX |
| 19 | 15/11 10:40 | trig_01YEHJSSKZ3KkcCe48jbVtiq |
| 20 | 15/11 22:40 | trig_01Hrqca5GYCfvBqBWa4xCxep |
