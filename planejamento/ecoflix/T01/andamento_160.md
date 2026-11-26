# T01 · andamento da aplicação do 1.60.18

Atualizado em 20/11. Base: app 1.60.18, tela 1600x900.

## Feito
- Fala (`narracao/tts_textos.py`) e `roteiro.md` reescritos pela cobertura: 16 capítulos (novos: cap10 "O comprovante do seu jeito" e cap11 "Ticket, idioma e guia"; antigos 10-13 viraram 12-15). 2.351 -> 3.348 palavras (~21,5 min de fala). Verificado por script: roteiro e fala com as mesmas linhas.
- `plano.md`, `inventario.md` (seção "Revisão 1.60.18") e `cenas/ilustracoes.json` (2 novas, 4 reancoradas, todas `v3: pendente`).
- Robô `rec/t01/gerar.py` com os 16 capítulos; `python3 -I rec/t01/gerar.py` sem aviso (só um `L10` do cap14 de 0,01 s).
- Sementes: `inicio` (condição À vista padrão, 2º endereço desligado, idioma pt-BR); `apos-cap12` substitui `apos-cap10` (gerada pelo `--seed` do cap12).
- Lote de ensaio lançado (rápido de 00 a 15, depois completos de 03 04 09 10 11 12 13 14).

## Estado do ensaio (20/11 18:50)
- O app de gravação virou **1.60.22** durante o trabalho; o robô fixava 1.60.18 e o aviso "Sistema atualizado" cobria as abas. `VERSAO = '1.60.22'` em `rec/t01/gerar.py` (corrigido).
- Lote 1 (abortado, versão errada) e lote 2 (ordem 09-15, 05, 06, 08, 00...; parou no prazo de 2 h).
- Rápido OK com o 1.60.22 (0 passo falho): caps 05, 06, 08, 09, 10, 11, 12, 13, 14, 15. Folhas vistas: 10 e 12 (corretas).
- Rápido com o 1.60.22 ainda por fazer: 00, 01, 02, 03, 04, 07 (passaram no lote 1 com o aviso de versão na tela; conteúdo não mudou, mas refazer para a folha limpa).
- **Lote 3 (último) rodando em segundo plano**: rápido de 00 01 02 03 04 07 e depois completos de 14 10 03 12 09 11 13 04. Log: `/dev/shm/t01_lote_c.log`. Termina no prazo de 2 h (~20:50) ou antes; a fila está cheia (cada capítulo leva 7 a 20 min).
- Atraso a corrigir: cap14 (rápido, `prever`): acumula 1-2 s de atraso em L4 a L10. Já encurtei o `Aceito em` (2,4 -> 1,0 s) e adiantei o clique em Ver Contrato; o completo do cap14 no lote 3 confere. Se ainda passar de 1 s, encurtar os hovers da lista do Zerar Sistema (L8) e o `Serão mantidos` (L10).
- cap10: o `confere_ausente` olhava "Quem assina" e achava a descrição ("Escolha quem assinar"); passou a olhar "Só o cliente/fornecedor". Conferir no rápido do cap10 (não foi refeito).
- Bolha do assistente ("Qual número de operação você quer entender agora? Abrir Cato") aparece embaixo à direita nas folhas dos caps 10 e 12; é do app, não do robô; avisar a edição (esconder no corte).

## Como conferir o lote
- Log: `/dev/shm/t01_lote_c.log` (linhas `RES capNN`, `CADEIA FIM`, `LOTE FIM`); o lote 2 está em `/dev/shm/t01_lote.log`.
- Por capítulo: `rec/t01/_ens/capNN.resumo.txt`, `.prever.txt`, `.log`; completos em `rec/t01/capNN.resumo.txt`; folhas em `/dev/shm/t01_rec/_ens/*.contact.jpg`.
- Instância do mundo falso: porta 54301 (`FAKE_NOW=2026-11-10T08:30:00-03:00`).

## Derrubar (quando o lote acabar, ou para abortar)
```
cd /home/claude/ecoflix && pgrep -af t01_lote_160_c   # pega o pid do bash e mate com kill <pid>
FAKE_PORT=54301 bash rec/run.sh down
```
Depois apagar MP4/jpg de ensaio: `/dev/shm/t01_rec` (disco apertado).

## Falta
- Resultado do lote 3 e correção do que falhar (sem lote 4: o limite de 3 foi usado).
- Voz ElevenLabs e gravação final (rodar `preparar_aula.sh T01` depois da voz).
- Decisões do Kaik: À vista como única condição na partida (o app real semeia 6); selo "MASTER"; senha do ambiente com 5 requisitos.

## Resultado final do lote 3 (20/11 20:45)
- Rápido (1.60.22): os 16 capítulos com 0 passo falho, sem SEM ALVO nem erro de página.
- Completos feitos: cap14 (maxLate 0,60 s, 1 atraso >= 0,3) e cap10 (maxLate 0,28 s): dentro de 0,8 s.
- Completos NÃO feitos (prazo): 03, 12, 09, 11, 13, 04. A gravação final com a voz confere esses.
- Instância 54301 derrubada; `/dev/shm/t01_rec` apagado.

## 26/11 · ilustrações v3 prontas; papel para o fechamento
- 7 feitas, 7 tiradas (`cenas/ilustracoes.json`), auditoria 0, piscadas 0. Números das cenas conferidos na fala (Dona Cida 37 kg, R$ 229,40 → R$ 229,00 + R$ 0,40; 190 kg, R$ 142,50 × R$ 150,00; Fundição Bandeira do Vale 30/60/90).
- **No fechamento, mostrar papel real onde a fala cita o comprovante** (hoje nenhum actions.json da T01 traz o PDF do comprovante; o do cap14 é outro): cap00 L0 e cap04 L"O logo, o nome e o CNPJ saem no comprovante" (dá para reusar papel real do mesmo mundo: T27 pedido #1758 com logo, T07 cupom #1760); cap08 L"O comprovante já sai com a cara da Recicla Vale" e cap10 (formato, peso líquido, assinaturas): capturar o PDF depois de salvar, no molde `T04/cenas_v3/pdf12.html` / T21 cap07. Nunca desenhar papel.

## 26/11 (tarde) · fechamento da T01: gravação final, montagem e prévia
- **Aula**: `t01/edit/out/T01/aula_final.mp4` (1920x1080, 30 fps, 21:14,6, 279,5 MiB), legendas `aula_final.srt` e `.vtt` (na mesma pasta e em `legendas/`), `capitulos.json`, conferência e folhas de 3 s em `folhas3s/`. Áudio -16,3 LUFS, pico -3,8 dBTP. Prévia 720p de 27,7 MiB em `$TUT_HOME/entrega_previa/EcoFlix T01 - Sua conta e sua empresa 1.60.22 (previa 720p).mp4`.
- **Voz**: as palavras "fracas" do `proc_1.60.22.log` eram o reconhecedor (siglas, "por cento", "e-mail"); nenhuma palavra errada. Nada de voz nova.
- **Gravação final** (`rec/t01/t01_final.sh`, senha fictícia de 5 requisitos só no ambiente; a 1ª tentativa com senha aleatória não mostrou "Senha forte" no cap01 e foi descartada). Rodada 1: maxLate cap00 0,07, cap01 0,90, cap02 0,41, cap03 0,31, cap04 0,16, cap05 0,42, cap06 1,07, cap07 1,44, cap08 2,71, cap09 0,09, cap10 0,42, cap11 0,18, cap12 0,54, cap13 0,47, cap14 0,70, cap15 0,18. Regravados (rodada 1, os demais ficaram): cap01 (respiro de 1,0 s no vão de 20,1 s) fechou em 0,11; cap07 (digitação do "RV-" adiantada para "faltar", sem respiro) fechou em 0,33; cap06 (respiro de 1,1 s no vão de 87,7 s) fechou em 1,34 e cap08 (respiro de 2,8 s no vão de 14,6 s) fechou em 0,80, os dois por digitação lenta no app (e-mail de contato 4,1 s contra 2,6 s; frase de 68 caracteres em ~6 s). Pelo combinado, sem 2ª rodada: no cap06 o atraso é só da marca L3 (nenhum gesto atrasado), no cap08 é o hover do contador "68/2000" (~18,6 s da gravação).
- **Papel real** (nunca desenhado): o robô `rec/t01/t01_papel.py` abre "Ver comprovante" no mundo da Recicla Vale e guarda o PDF que o app gerou (PNG 300 dpi em `t01/edit/out/comprovantes/`, PDFs e texto em `rec/t01/papel/`). Papel A (pedido #1758: logo, nome, CNPJ 47.318.506/0001-07, telefone, frase) no cap00 L1, cap05 L7 e cap08 (L4 e L5); cap10: T_on/T_off (pedido #1757 com tara de 5 kg via `seeds-extra/t01/papel.json`, só para a captura), S_ambas/S_cli e E_nome. Cena `T01/cenas_v3/comprovante.html`. A cena `ilu05_para_onde_vao` ficou só com a 2ª frase (CNPJ e endereço na nota da assinatura).
- **Zooms** só os do roteiro (`ZOOMS` em `t01_specs.py`); 0 piscadas nas 16 ilustrações; `auditar_camera.py` 0 problema. Sem `acelera` (nenhum silêncio longo pediu).
- Diferenças com o brief: o texto "O logo, o nome e o CNPJ saem no comprovante" está no cap05 (não no cap04, que é "Esqueci minha senha"). No papel do peso líquido o app mostra Bruto 100 e Líquido 95, sem a tara em linha própria.
