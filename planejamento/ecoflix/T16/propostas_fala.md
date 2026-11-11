# T16 · Propostas de fala (robô e ensaio de 11/11)

O que a fala precisa mudar para bater com a tela do EcoSistema 1.59.154 (ou caber no gesto). O `gerar.py` da aula
(`$TUT_HOME/rec/t16/gerar.py`) já aceita as duas versões das linhas abaixo: com a voz nova, é só rodar o gerador de novo.
Não editei `roteiro.md` nem `tts_textos.py`.

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 02 | L2 | Na esquerda ficam as seções, em três grupos: emissão, regras fiscais e documentos. | Em cima ficam as seções, na ordem em que se preenche: do certificado até os serviços. | Na 1.59.154 a Configuração Fiscal mostra as seções como abas no alto da página (`ConfiguracaoFiscal.tsx:1208-1213`, `desktopVariant="underline"`), sem trilho à esquerda e sem os rótulos de grupo. |
| 02 | L3 | Repara que Empresa, Impostos, Numeração e Transportadora estão apagados, com o aviso precisa do certificado digital. | Repara que Empresa, Impostos, Numeração e Transportadora estão apagadas: elas só abrem depois do certificado digital. | As abas travadas aparecem só acinzentadas; "precisa do certificado digital" é dica nativa do navegador (`title`, `SettingsSidebarLayout.tsx:179`), que não aparece na gravação. |

## Achados do app

- **Configuração Fiscal sem trilho**: o inventário (seção 2) descreve um trilho à esquerda com os grupos "Emissão", "Regras
  fiscais" e "Documentos" e o sublabel "precisa do certificado digital" embaixo de cada seção travada. No código gravado
  (`pages/ConfiguracaoFiscal.tsx:1208-1213`) a página usa `SettingsSidebarLayout` com `desktopVariant="underline"`: abas no alto
  (`#tab-btn-certificado` ... `#tab-btn-servicos`), sem grupos; o motivo da trava só existe como `title` (dica do mouse do
  navegador). Na tela: "Certificado · Empresa · Impostos (padrão) · Cenários · Numeração · Transportadora · Serviços".
- **Lista vazia**: o texto é "Nenhuma nota fiscal encontrada" (não "Nenhuma nota fiscal de entrada encontrada").
- **Inscrição Estadual digitada no cap04**: a do mundo base B (688.123.456.117, a da configuração fiscal da matriz), e não
  688.047.314.106 do `plano.md`, para a cadeia T16 → T17 → T18 chegar ao mesmo estado de B. A fala não diz o número.
