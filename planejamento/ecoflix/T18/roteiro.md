# Roteiro T18 · Ambiental: MTR e CDF

Roteiro para a voz e a gravação no app 1.60.22, tela 1600x900, menu lateral aberto. A fala (coluna Fala) é a de `narracao/tts_textos.py`, na grafia da legenda (MTR, CDF, PDF, SIGOR; a pronúncia do TTS fica no tts). A coluna Tela resume o que o robô faz, com os rótulos copiados do código 1.60.22 (`inventario.md`); o passo a passo exato está nas docstrings e nas marcas de `rec/t18/gerar.py`. Mundo, números e sementes: `plano.md`. Cobertura aplicada: `cobertura_160.md`.

- **Título:** Ambiental: MTR e CDF
- **Antes:** Transporte, serviço e o contador (T17)
- **Próximo:** Funcionários e ponto eletrônico (T19)
- **Capítulos:** 14 (0 a 13). Novos em 21/11: 6 (modelo), 8 (quando o envio não passa), 11 (quando o certificado não sai). Renumerados: Cancelar 6→7, CDF 7→9, Baixar 8→10, Nota 9→12, Recapitulando 10→13.
- **FAKE_NOW:** `2026-11-10T09:30:00-03:00` nos capítulos 0 a 6 e `2026-11-10T10:40:00-03:00` do 7 ao 13 (o MTR da tarde, 2611000325, sai no cap06 pelo modelo e é cancelado no cap07).
- **Fala:** 2311 palavras (antes 1.403). Sem travessão; número por extenso; valores calculados só depois de vistos na tela no ensaio. Nenhum acesso real ao órgão: o SIGOR é simulado no backend falso.
- Não anunciar: nota de teste (homologação) e modelo novo da DANFE. PDF do MTR (cap05) e do CDF (cap10, e Gerar PDF no cap11) são capturados pelo robô para a ilustração (`"tipo": "comprovante"`).
- Marcas: `[ILUSTRAÇÃO: ...]` desenho por código no estilo da marca, nunca tela inventada nem documento oficial desenhado (as ilustrações estão em `cenas/ilustracoes.json`).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Ambiental: MTR e CDF". | (sem fala) |
| Abertura: ilustração sobre o Dashboard; depois o menu Fiscal & Ambiental > Ambiental (MTR/CDF). [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Oi! Neste tutorial a gente vai cuidar da parte que mantém a licença da Recicla Vale Metais de pé: o manifesto de cada carga de resíduo e o certificado do destino. |
| (segue a tela da linha anterior; ver `gerar.py`) | Hoje sai uma carga de chaparia pra Aços Quiririm. E a Auto Peças Vale Forte espera o certificado das sucatas que mandou em outubro. |
| (segue a tela da linha anterior; ver `gerar.py`) | Tudo isso fica no menu Fiscal & Ambiental, em Ambiental. |
| (segue a tela da linha anterior; ver `gerar.py`) | O Ambiental faz parte do módulo de Notas Fiscais, então depende do plano contratado. |
| (segue a tela da linha anterior; ver `gerar.py`) | Se você ainda não viu o tutorial de transporte, serviço e o contador, dá uma olhada antes. Primeiro, o que é cada um. |

### cap01 · O que é MTR e CDF (vinheta: AMBIENTAL)

| Tela | Fala |
| --- | --- |
| O que é MTR e CDF: a linha 1 passa o mouse nas abas MTR e CDF; o resto é ilustração (cursor em repouso). [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Aqui em Ambiental ficam as duas abas: MTR e CDF. Em português claro, é assim. |
| (segue a tela da linha anterior; ver `gerar.py`) | Gerador é quem produz o resíduo. Transportador é quem leva. E destinador é quem recebe e dá o destino, como reciclar. |
| (segue a tela da linha anterior; ver `gerar.py`) | O MTR, o manifesto de transporte de resíduos, acompanha a carga do gerador até o destino. |
| (segue a tela da linha anterior; ver `gerar.py`) | E o CDF, o certificado de destinação final, é o destinador confirmando que recebeu e deu o destino. |
| (segue a tela da linha anterior; ver `gerar.py`) | A Recicla Vale faz os dois papéis. Quando manda chaparia pra Aços Quiririm, ela é a geradora e emite o MTR. Quando a Auto Peças Vale Forte manda sucata pra cá, ela é a destinadora e emite o CDF. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: a ordem no tempo é sempre essa. Primeiro sai o MTR, junto com a carga. Depois que o destinador recebe e dá baixa, sai o CDF, que cobre um período e junta os MTR desse período. Um não substitui o outro. |

### cap02 · Licença e fiscalização (vinheta: AMBIENTAL)

| Tela | Fala |
| --- | --- |
| Licença e fiscalização: Manifestos vazio na tela; as ilustrações cobrem a fala. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Por que isso importa? Quem trabalha com resíduo trabalha com licença ambiental. |
| (segue a tela da linha anterior; ver `gerar.py`) | E é pelo MTR e pelo CDF que a empresa mostra pra onde foi cada carga. Numa fiscalização, os dois costumam ser pedidos juntos. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: e se perguntarem se a sua empresa é obrigada a emitir? A resposta honesta é que quem define é o órgão ambiental do estado e a licença da empresa. O sistema entrega a ferramenta, e a interpretação da norma fica com eles. |

### cap03 · Acesso e resíduos (vinheta: CONFIGURAÇÃO)

| Tela | Fala |
| --- | --- |
| Acesso ao SIGOR (CPF, senha, unidade, ambiente), salvar, testar, trocar a senha, sincronizar, resíduo "Sucata de ferro" (editar/excluir) e os três ferros em Materiais (a lista traz "Nenhum"). [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Antes do primeiro MTR, um passo de configuração. Repara que o Novo MTR ainda está desligado. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: antes de qualquer emissão, precisam estar prontos o estado da empresa, nas Configurações Fiscais, e o acesso ao sistema ambiental do estado, que a gente configura agora. |
| (segue a tela da linha anterior; ver `gerar.py`) | Em Configurações, o sistema já vem pelo estado da empresa. A Recicla Vale é de São Paulo, então é o SIGOR. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: em outro estado, a tela é a mesma, e o sistema também vem pelo estado da empresa. Nos estados que usam o sistema federal, no lugar do CPF e da senha entra o token de integração, que a gente gera no portal. |
| (segue a tela da linha anterior; ver `gerar.py`) | No SIGOR, o acesso é o do próprio usuário: o CPF da pessoa cadastrada no portal e a mesma senha que ela usa pra entrar. Aqui, o do Rafael. |
| (segue a tela da linha anterior; ver `gerar.py`) | O código da unidade geradora é o número que aparece no portal, ao lado do nome da empresa. |
| (segue a tela da linha anterior; ver `gerar.py`) | O ambiente fica em Produção. A opção Homologação é só pra teste. |
| (segue a tela da linha anterior; ver `gerar.py`) | Salvar acesso. Repara que o quadro avisa: acesso salvo, teste pendente. Então eu clico em Testar acesso salvo. Pronto: acesso validado, com a resposta do órgão e a data do último teste. |
| (segue a tela da linha anterior; ver `gerar.py`) | Se a senha do portal mudar, é só digitar a nova aqui, salvar e testar de novo. E se você esquecer a senha, a dica logo abaixo manda usar o Esqueci minha senha, na tela de login do portal. |
| (segue a tela da linha anterior; ver `gerar.py`) | Agora, Sincronizar dados do SIGOR. Ele traz as listas oficiais de resíduo, classe, unidade e tratamento, e com elas o Novo MTR libera. Se o órgão mudar uma lista, é só sincronizar de novo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Também aparecem os Resíduos salvos. A Recicla Vale manda muita sucata de ferro, então eu salvo esse resíduo uma vez só. |
| (segue a tela da linha anterior; ver `gerar.py`) | Código do IBAMA, classe, estado físico, acondicionamento e tratamento vêm das listas do órgão. Quem confirma cada um é quem cuida da licença da empresa. |
| (segue a tela da linha anterior; ver `gerar.py`) | Repara que a unidade aparece do jeito que o órgão escreve, com a sigla na frente. Aqui, tonelada. Se um dia o resíduo for líquido, em litro ou metro cúbico, o campo Densidade passa a ser obrigatório. |
| (segue a tela da linha anterior; ver `gerar.py`) | Salvar resíduo. Na hora do MTR, é só escolher. |
| (segue a tela da linha anterior; ver `gerar.py`) | Cada resíduo salvo pode ser editado ou excluído por aqui. Excluir não mexe nos manifestos que já saíram. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: emitir e cancelar MTR e CDF é uma permissão própria, a de documentos ambientais. Quem não tem continua vendo as listas e baixando o PDF, mas o botão de novo fica desligado. |
| (segue a tela da linha anterior; ver `gerar.py`) | Por último, em Materiais, eu marco os três ferros e ligo todos a esse resíduo. Na lista também tem a opção Nenhum, que tira a ligação, mas aqui eu escolho a sucata de ferro. Assim o MTR consegue puxar a carga direto da nota fiscal. |

### cap04 · Emitir o MTR da carga (vinheta: MTR)

| Tela | Fala |
| --- | --- |
| Novo MTR (tela cheia): parceiros cadastrados na hora (a lupa do CNPJ no destinador), Jair + GHT7B19, data, Puxar da nota fiscal (uma nota, depois duas: o cobre fica de fora), Desfazer, responsável, Emitir, cota. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Hora de emitir. Hoje sai pra Aços Quiririm uma carga de chaparia de três mil e seiscentos quilos. Novo MTR. |
| (segue a tela da linha anterior; ver `gerar.py`) | Ele abre em tela cheia, em três etapas: transporte e destino, resíduos e responsável. Aqui do lado, o resumo vai se preenchendo e avisa quantas etapas ainda faltam. |
| (segue a tela da linha anterior; ver `gerar.py`) | O transportador é a própria Recicla Vale, com o caminhão dela. Como é o primeiro MTR, eu cadastro com a razão social, o CNPJ e o código da unidade no SIGOR. |
| (segue a tela da linha anterior; ver `gerar.py`) | O destinador é a Aços Quiririm, que vai reciclar o ferro. Aqui eu só digito o CNPJ e clico na lupa: a razão social vem sozinha. O código da unidade dela vem do cadastro dela no SIGOR. |
| (segue a tela da linha anterior; ver `gerar.py`) | Motorista e placa vêm da mesma frota do manifesto de transporte: o Jair, no caminhão três quartos. Se o motorista ou a placa forem novos, o botão de mais, ao lado do campo, cadastra na hora. |
| (segue a tela da linha anterior; ver `gerar.py`) | A expedição é hoje. Dá pra marcar um dia à frente, mas não pra trás. |
| (segue a tela da linha anterior; ver `gerar.py`) | Avançar. Nos resíduos, em vez de digitar, eu puxo da nota fiscal da carga. Busco a Aços Quiririm, marco a nota de hoje e clico em Conferir. |
| (segue a tela da linha anterior; ver `gerar.py`) | A prévia mostra o resíduo salvo e a quantidade já em tonelada: três vírgula seis. E a chave da nota vai pras observações. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: dá pra marcar mais de uma nota, e o sistema soma tudo por resíduo. Se um material da nota não estiver ligado a um resíduo salvo, como o cobre desta outra nota, ele fica de fora, e a prévia avisa. |
| (segue a tela da linha anterior; ver `gerar.py`) | Usar no MTR. A linha já vem com tudo que estava no resíduo salvo, e com a quantidade da nota. Se marcar a nota errada, o botão Desfazer tira tudo o que veio dela. |
| (segue a tela da linha anterior; ver `gerar.py`) | Avançar. No responsável, o Rafael, sócio-administrador. E a observação já leva a chave da nota. |
| (segue a tela da linha anterior; ver `gerar.py`) | Tudo pronto. Emitir MTR. Pronto: o MTR foi emitido no SIGOR, com o número oficial dele. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: o MTR e o CDF contam na mesma cota mensal das notas fiscais. Passando o mouse aqui no selo, aparece o seu nível, quantos documentos o mês permite e quantos você já emitiu. Perto do fim do mês, confira antes de emitir. |

### cap05 · Acompanhar e baixar o PDF (vinheta: MTR)

| Tela | Fala |
| --- | --- |
| Lista com o 2611000318, Ver tentativas, Baixar PDF (aba nova; o robô devolve o PDF) e o ícone Usar como modelo (sem clicar). [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Com o MTR emitido, ele aparece na lista com o destinador, o resíduo, a data e o status: emitido. |
| (segue a tela da linha anterior; ver `gerar.py`) | Em Ver tentativas fica cada envio ao órgão, com a resposta dele. Aqui, um só, autorizado. |
| (segue a tela da linha anterior; ver `gerar.py`) | Baixar PDF. Ele baixa o manifesto que o órgão devolveu, pra ir com o motorista, junto com a carga. |
| (segue a tela da linha anterior; ver `gerar.py`) | A lista guarda o histórico de todos os manifestos, cada um com o PDF dele. E pra próxima carga parecida, repara no ícone de Usar como modelo. |

### cap06 · O próximo manifesto mais rápido (vinheta: MTR)

| Tela | Fala |
| --- | --- |
| Usar como modelo: o 2611000318 vira o Novo MTR da carga da tarde (quantidade 3,2; Adicionar resíduo e resíduo salvo; Resíduo perigoso aberto e fechado; observação apagada); emite o 2611000325. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | À tarde sai outra carga pra Aços Quiririm, agora de ferro misto. Em vez de começar do zero, eu clico em Usar como modelo. Transportador, destinador, motorista e placa já vêm preenchidos, e a data é a de hoje. |
| (segue a tela da linha anterior; ver `gerar.py`) | Avançar. Nos resíduos, vem a mesma sucata de ferro. Eu só troco a quantidade: três vírgula dois toneladas. |
| (segue a tela da linha anterior; ver `gerar.py`) | Se a carga levar mais de um tipo de resíduo, o Adicionar resíduo cria outra linha, e cada linha pode partir de um resíduo salvo, mesmo sem nota fiscal. Pra esta carga uma linha basta, então eu tiro a segunda. |
| (segue a tela da linha anterior; ver `gerar.py`) | Pra resíduo perigoso no transporte, como bateria, os dados da ONU entram aqui, em Resíduo perigoso. Sucata de ferro não é o caso, então fica fechado. Cada resíduo ainda tem um campo de observação, que também é opcional. |
| (segue a tela da linha anterior; ver `gerar.py`) | Avançar. No responsável, já vem o Rafael. Uma dica: o modelo copia também a observação, com a chave da nota da carga anterior. Eu apago, porque esta carga tem outra nota. |
| (segue a tela da linha anterior; ver `gerar.py`) | Tudo pronto. Emitir MTR. Pronto, o segundo manifesto do dia, em poucos cliques. |

### cap07 · Cancelar um MTR (vinheta: MTR)

| Tela | Fala |
| --- | --- |
| Corte 10:40: o MTR da tarde (2611000325) é cancelado; selo da cota. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Mais tarde, a Aços Quiririm pediu pra deixar essa carga de ferro misto pra semana que vem. |
| (segue a tela da linha anterior; ver `gerar.py`) | Essa carga não vai sair hoje, então o MTR é cancelado. O botão de cancelar aparece no MTR emitido. |
| (segue a tela da linha anterior; ver `gerar.py`) | O cancelamento vai pro sistema ambiental e não tem volta. Por isso, confira se é o MTR certo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Cancelar MTR. Pronto, cancelado. Quando a carga sair, sai um MTR novo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: o MTR cancelado continua contando na cota do mês. Por isso, cancele só o que não vai mesmo sair. |

### cap08 · Quando o envio não passa (vinheta: MTR)

| Tela | Fala |
| --- | --- |
| Quando o envio não passa: a lista com os cinco status; Ver tentativas do Erro; Corrigir e Tentar novamente (voltar); Confirmar no órgão. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Nem todo envio passa de primeira. Olha a lista inteira: além do emitido e do cancelado, tem um com Erro, um com Confirmar no órgão e um Rascunho, que é o manifesto salvo, mas ainda não enviado. |
| (segue a tela da linha anterior; ver `gerar.py`) | No erro, o Ver tentativas mostra o que o órgão respondeu. |
| (segue a tela da linha anterior; ver `gerar.py`) | Daí são dois caminhos. Corrigir e tentar novamente abre o mesmo manifesto, pra arrumar o campo que o órgão recusou. E Tentar novamente reenvia do jeito que está. Como a data de expedição já passou, o sistema troca pra hoje. |
| (segue a tela da linha anterior; ver `gerar.py`) | Já o Confirmar no órgão quer dizer que o envio pode ter chegado lá, mas a resposta não voltou. Por isso a linha só tem o Ver tentativas: o sistema não deixa reenviar nem copiar esse manifesto. |
| (segue a tela da linha anterior; ver `gerar.py`) | Antes de qualquer coisa, confira no portal do órgão se o manifesto foi criado. Assim a mesma carga não sai com dois manifestos. |

### cap09 · O certificado do destino (vinheta: CDF)

| Tela | Fala |
| --- | --- |
| CDF: Novo CDF de outubro (01/10 a 31/10) para a Auto Peças Vale Forte, três MTR (lista opcional), Emitir; nº 2611000041; a lista. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Agora, o outro lado. Aqui no CDF, a Recicla Vale é a destinadora. |
| (segue a tela da linha anterior; ver `gerar.py`) | Em outubro, a Auto Peças Vale Forte mandou três cargas de sucata pra cá, cada uma com o MTR dela. A Recicla Vale recebeu e deu baixa no SIGOR. |
| (segue a tela da linha anterior; ver `gerar.py`) | Agora sai um CDF só, que cobre outubro e junta os três. |
| (segue a tela da linha anterior; ver `gerar.py`) | Novo CDF. Ele também abre em tela cheia, com as cinco etapas em cima: dá pra clicar em qualquer uma pra voltar e conferir. No período, outubro inteiro. |
| (segue a tela da linha anterior; ver `gerar.py`) | O destinador é a sua empresa, quem recebeu o resíduo. O CNPJ já vem preenchido, a unidade dela no SIGOR aparece logo abaixo, e o responsável é o Rafael. |
| (segue a tela da linha anterior; ver `gerar.py`) | No gerador, a Auto Peças Vale Forte, com o CNPJ e a unidade dela no SIGOR. |
| (segue a tela da linha anterior; ver `gerar.py`) | Como o gerador já está informado, a lista de MTR aqui é opcional: sem ela, o certificado sai pelo gerador e pelo período. Mas eu informo os números dos três MTR que vieram com as cargas. |
| (segue a tela da linha anterior; ver `gerar.py`) | Repara no aviso: o CDF só junta MTR que já foi recebido. Se faltar dar baixa em algum, isso é feito no portal do órgão, antes do CDF. Aqui também tem a observação, que consta no certificado. |
| (segue a tela da linha anterior; ver `gerar.py`) | E a emissão do CDF é definitiva. O resumo aqui embaixo ajuda a conferir tudo antes. |
| (segue a tela da linha anterior; ver `gerar.py`) | Emitir CDF. Pronto, o certificado foi emitido, com o número dele. |
| (segue a tela da linha anterior; ver `gerar.py`) | Na lista, cada CDF mostra o período, o CNPJ do gerador e o status. O menu de ações tem o que dá pra fazer com cada certificado. |

### cap10 · Baixar e guardar (vinheta: CDF)

| Tela | Fala |
| --- | --- |
| Ações > Baixar PDF na linha do CDF 2611000041 (aba nova; o PDF é do órgão e não aparece no vídeo) | Com o certificado emitido, o PDF sai pelo menu de ações: Baixar PDF, pra salvar fora do sistema. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: o CDF é documento de fiscalização. Guarde o PDF fora do sistema, na pasta da licença, e deixe os MTR do mesmo período por perto. |
| (segue a tela da linha anterior; ver `gerar.py`) | Na fiscalização, os dois costumam ser pedidos juntos. |

### cap11 · Quando o certificado não sai (vinheta: CDF)

| Tela | Fala |
| --- | --- |
| Quando o certificado não sai: a lista com Erro, Rascunho e emitido sem PDF; Ver erro, Tentar novamente, Excluir rascunho, Gerar PDF. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | O CDF também pode parar no caminho. Aqui tem um com erro, um rascunho e um emitido que ficou sem o PDF. |
| (segue a tela da linha anterior; ver `gerar.py`) | Em Ver erro aparece o motivo. Este é o mais comum: um dos manifestos ainda não teve a baixa do recebimento no portal. |
| (segue a tela da linha anterior; ver `gerar.py`) | Depois de dar a baixa lá no portal, é só clicar em Tentar novamente. Pronto, emitido, já com número. |
| (segue a tela da linha anterior; ver `gerar.py`) | O rascunho é um certificado que não chegou a ser enviado. Ele pode ser excluído, porque ainda não existe no órgão. |
| (segue a tela da linha anterior; ver `gerar.py`) | E quando um certificado fica emitido sem o PDF, o menu de ações mostra Gerar PDF, que busca o arquivo de novo. |

### cap12 · A nota da mesma carga (vinheta: NOTA FISCAL)

| Tela | Fala |
| --- | --- |
| Notas Fiscais > Saída: a NF-e 1257 da chaparia; depois a lista MTR; ilustração dos três documentos. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | E como tudo isso conversa com a nota fiscal? A carga de chaparia de hoje tem a nota de venda dela, aqui em Notas Fiscais. |
| (segue a tela da linha anterior; ver `gerar.py`) | São três documentos da mesma carga, cada um com o seu papel. A nota fiscal é a venda, e vai pra SEFAZ. O MTR é o transporte do resíduo, e vai pro órgão ambiental. |
| (segue a tela da linha anterior; ver `gerar.py`) | E o CDF vem depois, do destinador, confirmando o destino. |
| (segue a tela da linha anterior; ver `gerar.py`) | Eles são independentes: cada um é emitido na sua tela. O que o MTR aproveita da nota é o que a gente viu: os itens, pelo Puxar da nota fiscal, e a chave, na observação. |
| (segue a tela da linha anterior; ver `gerar.py`) | Assim você digita menos, e a nota e o MTR da mesma carga ficam ligados pela chave. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Recapitulando: montagem das gravações dos capítulos 3 a 11 por cima; a tela fica parada em Ambiental > MTR. [ILUSTRAÇÃO onde a tela não mostra: ver `cenas/ilustracoes.json`] | Pronto! Recapitulando: a gente configurou o acesso ao SIGOR, sincronizou as listas do órgão, salvou a sucata de ferro como resíduo e ligou os materiais a ele. |
| (segue a tela da linha anterior; ver `gerar.py`) | Emitiu o MTR da carga de chaparia puxando da nota fiscal, acompanhou, baixou o PDF, usou esse manifesto como modelo pra carga seguinte e cancelou o que ficou pra depois. |
| (segue a tela da linha anterior; ver `gerar.py`) | Viu também o que fazer quando um envio dá erro ou fica pra confirmar no órgão. |
| (segue a tela da linha anterior; ver `gerar.py`) | E emitiu o CDF de outubro da Auto Peças Vale Forte, guardou o PDF junto da licença e viu como resolver um certificado com erro, rascunho ou sem PDF. |
| (segue a tela da linha anterior; ver `gerar.py`) | No próximo tutorial, a gente coloca a equipe do pátio dentro do sistema. Até lá! |
