# T27 · andamento da aplicação no 1.60.22 (21/11)

**Feito:** `tts_textos.py` (9 caps, 1.126 palavras; 6.061 caracteres de fala com títulos; antes 798 palavras), `config_narracao.json` (+ "á-quatro" -> A4), `roteiro.md` (reescrito), `plano.md`, `inventario.md` (seção 8 + correção do interruptor),
`preparar_aula.sh T27` (9 estimados), `rec/t27/gerar.py` (9 caps; VERSAO lê `app/dist/.versao-app`; 1600x900; método `upload`), `t27_corpo.sh` e `t27_lote.sh` (novos; gravam em `/dev/shm/t27_ens`), `cenas/ilustracoes.json` (11 entradas, `clima` + `v3: pendente`).
Capítulo novo: **6 "Desligar e voltar atrás"**; Equipe vira 7 e Recapitulando 8. Sementes: nenhuma nova (`inicio`, `apos-cap03`, `apos-cap04` valem; o cap06 termina igual a `apos-cap04`). Nenhum handler novo; nada pedido ao mundo base.
Trechos novos: cap01 L3 (módulo), cap02 L6 (ícone padrão), cap03 L8-L9 (menu escuro, "Seguir o tema" só apontado), cap04 L4 (código com "#"), cap05 L3, L5, L7, L8, cap08 L5. A dica de desligar saiu do cap05.

**Correção da cobertura:** o interruptor NÃO trava com o White Label ligado e sem logo (`CompanySettings.tsx:1145` só desabilita sem logo E desligado). A fala do cap06 não diz que trava; mostra o cartão ainda "White Label Ativo" e o aviso âmbar. Também não diz "seis caracteres" (o código só confere o "#").

**Ensaios (2 lotes):** rápido 0 falho, 0 SEM ALVO, pageIssues vazio nos 9 caps. Completo (voz ESTIMADA, só referência) caps 1 a 8, 0 falho: maxLate cap01 0,21; cap02 0,18; cap03 0,83 (L8; hover encurtado depois, SEM reensaio); cap04 0,05; cap05 0,00; cap06 1,61 (marca L7; hovers do aviso e do interruptor encurtados depois, SEM reensaio); cap07 0,00; cap08 0,08. Cap00 só rápido (sem mudança). Refazer âncoras com a voz real.
PDF do comprovante devolvido (cap05; pedido #1758, compra, sem ticket, térmico, sem rodapé do EcoSistema): `rec/t27/t27-cap05.comprovante.pdf` (via `python3 -I rec/t27/t27_pdf.py --ens`).

**Comandos:** subir fake: `cd /home/claude/ecoflix && FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54327 bash rec/run.sh fake` (porta 54327; o corpo sobe sozinho; instância derrubada no fim).
Lote em segundo plano (`TUT_SENHA` aleatória é gerada dentro do corpo): `cd /home/claude/ecoflix && bash rec/t27/t27_lote.sh 06:c 03:c > /dev/shm/t27_lote3.log 2>&1` (`NN:r` rápido, `NN:c` completo). `FAKE_NOW` fixo 2026-11-10T08:30:00-03:00. Derrubar: `FAKE_PORT=54327 bash rec/run.sh down`.
Falta: reensaio completo de 06 e 03 (hovers encurtados); `cenas/tempos/` ficou com os estimados antigos (regenerar com a voz).

**Lido na tela:** cap06 "White Label desativado.", cartão "White Label Desativado"; `--primary` volta a `0 0% 10%` (preto padrão) e religado `213 70% 40%` em ~450 ms; Cor Primária "#1F5FAD" guardada; confirmação "Remover logo da empresa?" ("O logo personalizado será removido..."); "Nenhum logo enviado" + aviso âmbar; "Logo atualizado com sucesso!". Cap05: pedido #1758, Fornecedor Aparecida Ramos, Alumínio latinha 26 kg R$ 161,20, Papelão 60 kg R$ 33,00, Total R$ 194,20, Operador(a): Marcos (nada falado).

**Frases só com ilustração (sem tela real):** cap05 L3 (tabela de preços, ticket, fechamento: cartões), L5 (QR com logo: o pedido do robô não tem foto), L7 (comprovante do Portal), L8 (rosto no ponto e Logo para Nota Fiscal); cap06 L7 (documentos seguem sem rodapé); cap03 L8 (logo escuro some: o logo do mundo é a versão clara); cap01 L3 (gaveta que não aparece: a tela só mostra a gaveta presente).
**Achados para o MELHORIAS:** (1) com White Label ligado e logo removido o cartão diz "Seu logo está sendo exibido no lugar do logo EcoSistema" e o selo "Ativo" (falso naquele estado); (2) "Nome Exibido no Sistema" segue sem uso; (3) cor sem "#" é salva com "salvas!" e nada muda, sem validação; (4) o "Seguir o tema" fica em Aparência, fora do White Label, e o logo escuro some no menu padrão; (5) a cobertura de 20/11 errou sobre o interruptor travado (corrigido acima).

## 21/11 16:56 · reensaio da coordenação
- Completos: cap06 0 falho, maxLate 0,70; cap03 0 falho, 0,07. Instância 54327 derrubada. **T27 pronta para a voz.**

## 28/11 · fechamento
- Aula final 7:21,5 (441,5 s), 1080p, -16,3 LUFS, pico -3,6 dBTP; legendas 160. Prévia 720p 27,6 MiB em `entrega_previa/`. Aula: `t27/edit/out/T27/aula_final.mp4`. Gravação final: 9 caps, 0 falho, maxLate <= 0,78 (cap01 0,78; cap06 0,74).
- Regravados: cap06 (respiros 1,38 s em T=16,64; 1,20 em 27,82; 1,52 em 47,68, `rec/t27/t27_respiros.py`; maxLate 1,27 -> 0,74) e cap07 (o balão do WhatsApp com nome e foto de gente de verdade aparecia 15 s depois do login da Juliana: `support_widget_last_dismissed` no `storage` do `gerar.py`). `ANIM_FIX` no `setup` do `gerar.py` (depois dos gotos).
- Scripts: `rec/t27/t27_final.sh`, `t27_respiros.py`; edição em `t27/edit/` (`t27_specs.py`, `caps/extra.json`, `fechar_t27.sh`, `montar_t27.sh`, `render_ilus_v3.sh`, `t27_parada.py`).
- Zooms (6, em `caps/extra.json`): cap02 ícone; cap03 interruptor e ícone recolhido; cap04 código #1F5FAD e barrinha do menu; cap06 interruptor. Sem destaques e sem acelerações (nenhum respiro >= 3 s).
- Ilustrações v3 (5, todas encaixadas; as demais entradas do ilustracoes.json seguem tiradas): ilu01_muda (maior piscada 9 quadros, 1,0% da tela, em 26,07 s: câmera/cartões, como combinado), ilu03, ilu05_documentos (papel real do #1758), ilu05_portal_ponto, ilu06. 0 piscadas nas outras 4.
- Conferência: folha de 3 s inteira olhada; varredura a 1 q/s: só 1 quadro quase branco (275 s, entrada dos cartões da ilustração de Documentos), nenhuma >= 3 s. Câmera: 3 instantes com alvo na borda (100% visível). Texto sem plano ou preço.
- Disco no fim: / 2,8 GB livres, /dev/shm 6,4 GB livres. Instância 54327 derrubada; `out/capNN`, `proj` e `video_sem_audio` apagados.
