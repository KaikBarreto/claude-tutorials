# Propostas de fala · T17 Transporte, serviço e o contador

**18/11 (aplicação do 1.60.10): tudo o que estava aqui foi aplicado** no `roteiro.md` e no `narracao/tts_textos.py`.
- cap02 L8: a fala agora cita a validade da CNH ("...o CPF, a CNH, a categoria e a validade.").
- cap08 (era 07) L8: "Na alíquota do ISS, eu coloco três por cento, o número da lista do município. ..." (o bug continua no 1.60.10).
- cap16 (era 10): a fala assume a tela, Delta de 1.100 kg no metal amarelo (600 da nota de 30/10 + 500 de compra sem nota).

## Achados do app (situação no 1.60.10)
1. **Nova NFS-e, alíquota do município (bug, continua):** a alíquota da lista do município não chega a "Alíquota ISS %" da aba
   Valores (`NovaNfseModal.tsx`, estado `issAliquota` separado de `service.issAliquota`). O robô digita 3.
2. **MDF-e, toast com jargão interno (novo):** "MDF-e #1 enviado ao motor fiscal próprio" (`NovoMdfeModal.tsx:1013`).
3. **"Sincronizar Numeração" (novo):** o texto ainda fala em "serviço fiscal", mas o botão só grava a série e o número.
4. **CIOT (novo):** o balão "Como gerar o CIOT?" cita a marca de um parceiro (a aula não abre o balão).
5. **Lista de MDF-e, coluna "Trajeto":** mostra só origem e destino; as UFs do percurso não aparecem na linha (continua).
6. **Corrigido no 1.60.10:** a pré-visualização da NFS-e agora mostra a série e o número previsto (era "a definir").
7. Os demais achados de 11/11 (data de emissão sem formatar na pré-visualização, razão social × nome do tomador, "Baixar PDF" só
   com `pdf_url`) ficam para conferir na folha de contato do ensaio do cap08.
