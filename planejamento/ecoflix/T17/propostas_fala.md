# Propostas de fala · T17 Transporte, serviço e o contador

Saem do robô e dos ensaios (EcoSistema 1.59.154 no Supabase falso, voz ESTIMADA). Nada aqui foi aplicado: `roteiro.md` e
`tts_textos.py` ficam para a revisão geral. Linhas numeradas como no roteiro (L1 = 1ª linha da tabela do capítulo).

## Fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 02 | L8 | O manifesto leva o CPF do motorista, então eu completo o CPF, a CNH e a categoria. | O manifesto leva o CPF do motorista, então eu completo o CPF, a CNH, a categoria e a validade. | A tela (roteiro) também preenche "Validade da CNH"; com a fala atual o campo é digitado depois de "categoria" e o "Salvar." da L9 fica sem folga. |
| 07 | L7 | A alíquota do ISS veio da lista do município. Quem confirma esse número é o contador. | Na alíquota do ISS, eu coloco três por cento, o número da lista do município. Quem confirma esse número é o contador. | Na 1.59.154 a alíquota da lista do município não chega ao campo "Alíquota ISS %" da aba Valores (vem 0,00; ver Achados): o robô digita 3. Com a fala atual a tela contradiz "veio da lista". |
| 10 | L5 | Na última aba, o fiscal e o operacional ficam lado a lado. Repara no metal amarelo: seiscentos quilos de diferença. | (depende da junção, ver Achados 4) Se o mundo ficar como está: "Repara no metal amarelo: mil e cem quilos de diferença." e a L6/L7 explicam só os seiscentos da nota de 30/10. | A tela mostra Delta -1.100 kg no metal amarelo em outubro (Mov. Fiscal -1.100, Mov. Operacional 0). |

## Achados do app

1. **Nova NFS-e, alíquota do município (bug).** Ao escolher o código de tributação, a alíquota que a lista do município traz (3,00 % em
   Taubaté) vai para `service.issAliquota` (`nfse/ServicoStep.tsx:117-127`), mas a aba Valores usa o estado `issAliquota` do
   `NovaNfseModal.tsx` (:210), que só é preenchido ao abrir um rascunho ou puxar um serviço salvo (:338-340, :510-512): "Alíquota ISS %"
   fica 0,00 e a prévia diz "ISS 0%". O roteiro (cap07, "com 3 vindo da lista do município") supõe o contrário.
2. **Pré-visualização da NFS-e:** "DATA DE EMISSÃO" mostra a data de competência sem formatar ("2026-11-06").
3. **Lista de MDF-e, coluna "Trajeto":** mostra só origem e destino ("Taubaté/SP → Itamonte/MG"); o trajeto com as UFs do percurso
   (`MdfeTab.tsx:93-97`) só serve para ordenar, a célula usa cidade/UF (`:615`). O RJ do percurso não aparece na linha (a recapitulação
   do cap13 cita "o percurso com o RJ": usar a etapa "Trajeto e carga" do cap04 ou a ilustração do cap03).
4. **Mundo (para a junção): Fiscal × operacional de outubro.** O metal amarelo dá **Delta -1.100 kg**, não -600: Mov. Fiscal -1.100
   (as notas de saída de outubro para a Fundição, 500 kg, mais a 1248 de 600 kg) e Mov. Operacional 0 (500 kg comprados e 500 kg vendidos
   no pátio; as compras de latão de outubro não têm nota de entrada). E 13 dos 15 materiais aparecem com divergência ("Materiais com
   divergência 13", ferro pesado -40.000 kg, chaparia -6.770 kg...), não "só o metal amarelo" (T17/plano.md). Para a fala atual valer, o
   latão comprado em outubro precisaria de nota de entrada (muda os R$ 97.315,00 de entrada falados no cap09/cap11) ou sair de outubro
   no histórico operacional (mexe nos números do T15); senão, a fala muda (tabela acima).
5. **Toast do encerramento do MDF-e:** a função real responde "Encerramento enviado. Aguardando confirmação da SEFAZ — o status é
   atualizado automaticamente." (`_shared/mdfe-event.ts`); o "... A confirmação da SEFAZ aparece em instantes." do inventário é o texto
   de reserva do `useMdfe.tsx`, que só aparece quando a função não manda mensagem. A fala não depende disso.
6. **Frota:** a lista "Veículos da frota" abre com o primeiro da ordem (EZR4C63, Picape) no painel; o robô clica no FKD2E41 em "Os
   caminhões da Recicla Vale..." (o roteiro supõe o painel do FKD2E41 já aberto).
7. **Menu Fiscal & Ambiental:** não mostra "SPED Fiscal" na 1.59.154 com este plano (o inventário cita o item com selo BETA).
8. **Tomador da NFS-e:** o seletor e a nota mostram a razão social "Aços Quiririm Indústria e Comércio Ltda"; a lista de notas, o nome
   "Aços Quiririm Ltda".
9. **Categoria da conta:** o mundo base não tem "Manutenção"; a conta da Balanças Tremembé vai em "Manutenção de máquinas" (a fala não
   diz o nome da categoria).
10. **Menu da NFS-e:** "Baixar PDF" só aparece com `pdf_url` (a função de status real guarda o PDF da prefeitura no Storage); as NFS-e
    12 e 13 da semente não têm PDF, a 14 emitida na aula tem.
