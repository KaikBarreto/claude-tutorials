# Roteiro T18 · Ambiental: MTR e CDF

- **Título:** Ambiental: MTR e CDF
- **Antes:** Transporte, serviço e o contador (T17)
- **Próximo:** Funcionários e ponto eletrônico (T19)
- **Vinhetas (áreas):** AMBIENTAL · CONFIGURAÇÃO · MTR · CDF · NOTA FISCAL · RESUMO (todo capítulo menos o 0)
- **Duração estimada:** ~10,5 min de vídeo (1.403 palavras de fala, ~9,0 min a 2,6 palavras/s, mais a vinheta de abertura, 10
  vinhetas de capítulo, as esperas do órgão simulado e a cartela; alvo da fonte ~12 min)
- Coluna Fala = texto da narração na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela =
  o que o robô faz e onde a câmera foca, rótulos entre aspas como no código 1.59.154 (`T18/inventario.md`; "SIGOR" é o nome curto que o
  app mostra para SP). Logado como Rafael Nogueira (MASTER), desktop. Mundo e sementes: `T18/plano.md`. FAKE_NOW 10/11/2026 09:30 nos
  capítulos 0 a 5 (junção: depois das notas do T16 e do T17) e 10:40 do 6 em diante. Nenhum acesso real ao órgão ambiental: o SIGOR é simulado no backend falso.
- Marcas: `[BACKEND: ...]` o que o backend falso ainda não tem; `[ZOOM: ...]` zoom suave que dura a frase inteira (sem zoom em cima de
  zoom); `[ILUSTRAÇÃO: ...]` desenho por código no estilo da marca, nunca tela inventada nem documento oficial desenhado.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Ambiental: MTR e CDF". | (sem fala) |
| Dashboard do EcoSistema, logado como Rafael Nogueira. [ILUSTRAÇÃO: o dia: entra "Recicla Vale Metais · terça, 10 de novembro" e dois cartões, um por frase: um caminhão 3/4 com chaparia rumo à "Aços Quiririm"; a "Auto Peças Vale Forte" esperando o "certificado de outubro".] | Oi! Neste tutorial a gente vai cuidar da parte que mantém a licença da Recicla Vale Metais de pé: o manifesto de cada carga de resíduo e o certificado do destino. |
| (ilustração: os dois cartões acendem, um em cada frase) | Hoje sai uma carga de chaparia pra Aços Quiririm. E a Auto Peças Vale Forte espera o certificado das sucatas que mandou em outubro. |
| A ilustração sai; a câmera vai ao menu lateral, clica em "Fiscal & Ambiental" e em "Ambiental (MTR/CDF)": tela "Ambiental". | Tudo isso fica no menu Fiscal & Ambiental, em Ambiental. |
| Cartão discreto: "Módulo Notas Fiscais". | O Ambiental faz parte do módulo de Notas Fiscais, então depende do plano contratado. |
| Cartão discreto: "Antes: Transporte, serviço e o contador". | Se você ainda não viu o tutorial de transporte, serviço e o contador, dá uma olhada antes. [pause] Primeiro, o que é cada um. |

### cap01 · O que é MTR e CDF (vinheta: AMBIENTAL)

| Tela | Fala |
| --- | --- |
| Tela "Ambiental"; a câmera passa pelas sub-abas "MTR" e "CDF" e pelo título "Manifesto de Transporte de Resíduos (MTR)". [BACKEND: semente `inicio`, sem acesso ao SIGOR, sem MTR e sem CDF] | Aqui em Ambiental ficam as duas abas: MTR e CDF. Em português claro, é assim. |
| [ILUSTRAÇÃO: a cadeia do resíduo: três estações numa estrada, uma por trecho da frase: "Gerador" (uma oficina genérica), "Transportador" (um caminhão), "Destinador" (um pátio de reciclagem).] | Gerador é quem produz o resíduo. Transportador é quem leva. E destinador é quem recebe e dá o destino, como reciclar. |
| (ilustração: uma folha "MTR" sai do gerador e viaja junto com a carga até o destinador) | O MTR, o manifesto de transporte de resíduos, acompanha a carga do gerador até o destino. |
| (ilustração: do destinador volta ao gerador uma folha "CDF", com um visto) | E o CDF, o certificado de destinação final, é o destinador confirmando que recebeu e deu o destino. |
| (ilustração: o desenho ganha nomes, em duas faixas: em cima "Recicla Vale" (gerador) → "Aços Quiririm" (destinador), com o MTR; embaixo "Auto Peças Vale Forte" (gerador) → "Recicla Vale" (destinador), com o CDF voltando) | A Recicla Vale faz os dois papéis. Quando manda chaparia pra Aços Quiririm, ela é a geradora e emite o MTR. Quando a Auto Peças Vale Forte manda sucata pra cá, ela é a destinadora e emite o CDF. |
| [ILUSTRAÇÃO: a ordem no tempo: uma linha de outubro com três folhas "MTR" nos dias das cargas; em cada uma, "recebido e baixa"; no fim do mês, as três se juntam num "CDF" do período.] | Uma dica: a ordem no tempo é sempre essa. Primeiro sai o MTR, junto com a carga. Depois que o destinador recebe e dá baixa, sai o CDF, que cobre um período e junta os MTR desse período. Um não substitui o outro. |

### cap02 · Licença e fiscalização (vinheta: AMBIENTAL)

| Tela | Fala |
| --- | --- |
| Aba "MTR", sub-aba "Manifestos": "Manifestos de Transporte de Resíduos" e "Nenhum MTR emitido ainda.". [ILUSTRAÇÃO: a pasta "Licença de operação · Recicla Vale Metais" e, ao lado, um cartão genérico "Órgão ambiental do estado", sem brasão.] | Por que isso importa? Quem trabalha com resíduo trabalha com licença ambiental. |
| (ilustração: cada carga vira um "MTR" e cada destino um "CDF"; os dois entram na pasta da licença; uma prancheta genérica de fiscalização pede "MTR e CDF do período") | E é pelo MTR e pelo CDF que a empresa mostra pra onde foi cada carga. Numa fiscalização, os dois costumam ser pedidos juntos. |
| A ilustração sai; cartão "Dica: quem define é o órgão ambiental e a licença". | Uma dica: e se perguntarem se a sua empresa é obrigada a emitir? A resposta honesta é que quem define é o órgão ambiental do estado e a licença da empresa. O sistema entrega a ferramenta, e a interpretação da norma fica com eles. |

### cap03 · Acesso e resíduos (vinheta: CONFIGURAÇÃO)

| Tela | Fala |
| --- | --- |
| Passa o mouse no "Novo MTR", que está desligado: aparece a dica "Configure o acesso ao SIGOR primeiro". | Antes do primeiro MTR, um passo de configuração. Repara que o Novo MTR ainda está desligado. |
| A dica some; cartão "Dica: estado da empresa e acesso ao sistema ambiental". | Uma dica: antes de qualquer emissão, precisam estar prontos o estado da empresa, nas Configurações Fiscais, e o acesso ao sistema ambiental do estado, que a gente configura agora. |
| Clica na sub-aba "Configurações": "Configuração do MTR", "Sistema:" com o nome do SIGOR e o aviso "Configure o acesso ao SIGOR para emitir MTR.". [ZOOM: "Sistema:"] [BACKEND: `mtr_uf_sistema` SP → `sigor_sp` e `mtr_sistemas` ativo] | Em Configurações, o sistema já vem pelo estado da empresa. A Recicla Vale é de São Paulo, então é o SIGOR. |
| Digita "274.913.508-79" em "CPF da pessoa usuária do SIGOR *" e uma senha fictícia em "Senha do SIGOR *" (só pontinhos). [ZOOM: "CPF da pessoa usuária do SIGOR *"] | No SIGOR, o acesso é o do próprio usuário: o CPF da pessoa cadastrada no portal e a mesma senha que ela usa pra entrar. Aqui, o do Rafael. |
| Digita "203918" em "Código da unidade geradora *"; "Ambiente" fica em "Produção". | O código da unidade geradora é o número que aparece no portal, ao lado do nome da empresa. |
| Clica em "Salvar acesso": toast "Acesso ao SIGOR salvo"; clica em "Testar acesso salvo": toast "Acesso ao SIGOR validado" e o quadro "Acesso validado". [BACKEND: RPC `mtr_set_credential`; `sigor-mtr-sync-ref` testa → validado] | Salvar acesso. E Testar acesso salvo: pronto, validado. |
| No cartão "Dados do SIGOR", clica em "Sincronizar dados do SIGOR": toast "Dados do SIGOR sincronizados". [BACKEND: `sigor-mtr-sync-ref` devolve as listas do órgão] | Agora, Sincronizar dados do SIGOR. Ele traz as listas oficiais de resíduo, classe, unidade e tratamento, e com elas o Novo MTR libera. |
| Aparece o cartão "Resíduos salvos"; clica em "Novo resíduo"; digita "Sucata de ferro" em "Nome do resíduo *". | Também aparecem os Resíduos salvos. A Recicla Vale manda muita sucata de ferro, então eu salvo esse resíduo uma vez só. |
| Em "Código IBAMA *", clica em "Buscar código IBAMA...", digita "ferrosos" e escolhe o de metais ferrosos; em "Classe *" (lista filtrada pelo resíduo), escolhe a da licença; "Estado físico *" → "Sólido"; "Acondicionamento *" → o de granel; "Tratamento *" → "Reciclagem". [BACKEND: classes permitidas para o resíduo] | Código do IBAMA, classe, estado físico, acondicionamento e tratamento vêm das listas do órgão. Quem confirma cada um é quem cuida da licença da empresa. |
| Em "Unidade *", escolhe "TON - Tonelada". [ZOOM: "Unidade *" com "TON - Tonelada"] | Repara que a unidade aparece do jeito que o órgão escreve, com a sigla na frente. Aqui, tonelada. |
| Clica em "Salvar resíduo": toast "Resíduo salvo"; a lista mostra "Sucata de ferro". | Salvar resíduo. Na hora do MTR, é só escolher. |
| Menu "Materiais" › "Estoque": marca "Ferro pesado", "Ferro misto" e "Chaparia"; na barra de ações, "Definir resíduo do MTR": diálogo "Definir resíduo do MTR dos selecionados"; em "Resíduo do MTR", "Sucata de ferro"; clica em "Definir resíduo em 3": toast "Resíduo do MTR definido em 3 material(is)". | Por último, em Materiais, eu ligo os três ferros a esse resíduo. Assim o MTR consegue puxar a carga direto da nota fiscal. |

### cap04 · Emitir o MTR da carga (vinheta: MTR)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Ambiental (MTR/CDF)" › "MTR" › "Manifestos"; clica em "Novo MTR", agora ligado: "Novo MTR", etapa "Transporte e destino". [BACKEND: semente `apos-cap03` com a NF-e da chaparia de hoje] | Hora de emitir. Hoje sai pra Aços Quiririm uma carga de chaparia de três mil e seiscentos quilos. Novo MTR. |
| Em "Transportador *", clica em "Selecione o transportador" e em "Cadastrar novo transportador"; digita "Recicla Vale Metais Ltda" em "Razão social *", o CNPJ da Recicla Vale em "CNPJ *" e "203918" em "Código da unidade no SIGOR *"; clica em "Salvar e usar": toast "Parceiro salvo". | O transportador é a própria Recicla Vale, com o caminhão dela. Como é o primeiro MTR, eu cadastro com a razão social, o CNPJ e o código da unidade no SIGOR. |
| Em "Destinador *", "Cadastrar novo destinador": "Aços Quiririm Ltda", o CNPJ da Aços Quiririm e "187402"; "Salvar e usar". [ZOOM: "CNPJ *" do destinador] | O destinador é a Aços Quiririm, que vai reciclar o ferro. O código da unidade dela vem do cadastro dela no SIGOR. |
| Em "Motorista", digita "Jair" e escolhe "Jair Lopes"; em "Veículo / placa", "GHT7B19"; "Data de expedição *" já com 10/11/2026. | Motorista e placa vêm da mesma frota do manifesto de transporte: o Jair, no caminhão três quartos. E a expedição é hoje. |
| Clica em "Avançar": etapa "Resíduos"; clica em "Puxar da nota fiscal": diálogo "Puxar da nota fiscal"; digita "Quiririm" em "Buscar por número, parceiro ou chave...", marca a NF-e de hoje e clica em "Conferir (1)". | Avançar. Nos resíduos, em vez de digitar, eu puxo da nota fiscal da carga. Busco a Aços Quiririm, marco a nota de hoje e clico em Conferir. |
| A prévia: "1 nota escolhida", "Resíduos que serão criados": "Sucata de ferro" ("IBAMA ... · 1 item · Chaparia"), "3,6 TON - Tonelada" e "1 item convertido de quilo para tonelada."; embaixo, "Vai pra Observações do Gerador" com a chave. [ZOOM: "3,6 TON - Tonelada" e "1 item convertido de quilo para tonelada."] | A prévia mostra o resíduo salvo e a quantidade já em tonelada: três vírgula seis. E a chave da nota vai pras observações. |
| Clica em "Usar no MTR": a linha de resíduo vem preenchida ("Usar resíduo salvo" "Sucata de ferro", "Quantidade" 3,6, "Unidade" "TON - Tonelada"), com o aviso "Puxado da nota fiscal" e "1 chave acrescentada à observação do manifesto (passo Responsável).". | Usar no MTR. A linha já vem com tudo que estava no resíduo salvo, e com a quantidade da nota. |
| Clica em "Avançar": etapa "Responsável"; digita "Rafael Nogueira" em "Nome do responsável *" e "Sócio-administrador" em "Cargo *"; a "Observação" já tem a chave da NF-e. | Avançar. No responsável, o Rafael, sócio-administrador. E a observação já leva a chave da nota. |
| O "Resumo do MTR" mostra "Tudo pronto para emitir o MTR"; clica em "Emitir MTR" ("Emitindo..."): "MTR emitido", "MTR emitido com sucesso", "Nº do manifesto: 2611000318"; toast "MTR emitido". [ZOOM: "Nº do manifesto: 2611000318"] [BACKEND: `sigor-mtr-emit` → emitido, nº 2611000318, PDF] | Tudo pronto. Emitir MTR. Pronto: o MTR foi emitido no SIGOR, com o número oficial dele. |
| Clica em "Concluir"; a câmera vai ao selo da cota no cabeçalho ("... Documentos"). [ZOOM: selo da cota] | Uma dica: o MTR e o CDF contam na mesma cota mensal das notas fiscais. Perto do fim do mês, confira esse número antes de emitir. |

### cap05 · Acompanhar e baixar o PDF (vinheta: MTR)

| Tela | Fala |
| --- | --- |
| A lista com a linha "2611000318", "Aços Quiririm Ltda", a descrição do IBAMA em "Resíduo", "10/11/2026" e "Emitido". | Com o MTR emitido, ele aparece na lista com o destinador, o resíduo, a data e o status: emitido. |
| Clica em "Ver tentativas": "Histórico de tentativas", "MTR 2611000318", uma tentativa "Autorizada"; clica em "Fechar". | Em Ver tentativas fica cada envio ao órgão. Aqui, um só, autorizado. Se um envio der erro, a linha mostra o botão de tentar de novo. |
| Clica em "Baixar PDF" (o PDF abre em aba nova; a câmera fica no app). [ILUSTRAÇÃO: o PDF com o motorista: uma folha genérica "MTR 2611000318" passa para a mão do motorista, ao lado do caminhão GHT7B19 carregado de chaparia; sem brasão nem marca de órgão.] | Baixar PDF. O PDF do MTR vai com o motorista, junto com a carga. |
| A ilustração sai; zoom no ícone "Usar como modelo" da linha, sem clicar. | E pra próxima carga parecida, o Usar como modelo abre um MTR novo com os mesmos resíduos. |

### cap06 · Cancelar um MTR (vinheta: MTR)

| Tela | Fala |
| --- | --- |
| Corte para as 10:40: a lista com o "2611000325" no topo (Aços Quiririm Ltda, "10/11/2026", "Emitido"). [BACKEND: semente `apos-cap05` com o MTR da tarde emitido às 09:40] | Mais tarde, a Recicla Vale emitiu pelo modelo o MTR da carga de ferro misto da tarde. Só que a Aços Quiririm pediu pra deixar essa carga pra semana que vem. |
| Zoom no ícone "Cancelar MTR" da linha "2611000325". | Essa carga não vai sair hoje, então o MTR é cancelado. O botão de cancelar aparece no MTR emitido. |
| Clica em "Cancelar MTR": diálogo "Cancelar MTR 2611000325", com "O cancelamento será enviado ao sistema ambiental e é irreversível. Deseja continuar?". [ZOOM: o texto do diálogo] | O cancelamento vai pro sistema ambiental e não tem volta. Por isso, confira se é o MTR certo. |
| Clica em "Cancelar MTR" no diálogo: toast "MTR cancelado"; o selo da linha vira "Cancelado". [BACKEND: `sigor-mtr-cancel` → cancelado] | Cancelar MTR. Pronto, cancelado. Quando a carga sair, sai um MTR novo. |
| A câmera vai ao selo da cota no cabeçalho. [ZOOM: selo da cota] | Uma dica: o MTR cancelado continua contando na cota do mês. Por isso, cancele só o que não vai mesmo sair. |

### cap07 · O certificado do destino (vinheta: CDF)

| Tela | Fala |
| --- | --- |
| Clica na sub-aba "CDF": "Certificado de Destinação Final (CDF)", "Certificados de Destinação Final", "Nenhum CDF emitido ainda." e "Novo CDF"; a câmera não para nos cartões de cima. | Agora, o outro lado. Aqui no CDF, a Recicla Vale é a destinadora. |
| [ILUSTRAÇÃO: as cargas de outubro: três caminhões da "Auto Peças Vale Forte" chegam à "Recicla Vale" em 06/10, 16/10 e 27/10, cada um com um "MTR"; em cada chegada, um visto "recebido e baixa no SIGOR".] | Em outubro, a Auto Peças Vale Forte mandou três cargas de sucata pra cá, cada uma com o MTR dela. A Recicla Vale recebeu e deu baixa no SIGOR. |
| (ilustração: no fim do mês, os três MTR se juntam num "CDF · outubro", que volta para a Auto Peças) | Agora sai um CDF só, que cobre outubro e junta os três. |
| A ilustração sai; clica em "Novo CDF": "Novo CDF", passo "Período"; escolhe 01/10/2026 em "Data inicial *" e 31/10/2026 em "Data final *". | Novo CDF. No período, outubro inteiro. |
| Clica em "Avançar": "DESTINADOR", com "O destinador é a sua empresa (quem recebeu o resíduo). Os dados vêm do seu acesso ao SIGOR/SINIR."; "CNPJ do destinador *" já preenchido; digita "Rafael Nogueira" em "Nome do responsável *". [ZOOM: "CNPJ do destinador *"] | O destinador é a sua empresa, quem recebeu o resíduo. O CNPJ já vem preenchido, e o responsável é o Rafael. |
| Clica em "Avançar": "GERADOR (opcional)"; digita o CNPJ da Auto Peças Vale Forte em "CNPJ do gerador" e "184527" em "Unidade no SIGOR". | No gerador, a Auto Peças Vale Forte, com o CNPJ e a unidade dela no SIGOR. |
| Clica em "Avançar": "MTRs INCLUÍDOS"; digita "2610001542", "2610001877" e "2610002203", um por linha, em "Números dos MTRs"; embaixo, "3 MTR(s) informado(s) (duplicados removidos).". | E os números dos três MTR que vieram com as cargas. |
| Clica em "Avançar": passo "Confirmar"; zoom no aviso "Atenção: os MTRs informados precisam já ter sido recebidos no SIGOR. Se ainda não deu baixa no recebimento, faça isso no portal do órgão antes de emitir o CDF.". [ZOOM: o aviso] | Repara no aviso: o CDF só junta MTR que já foi recebido. Se faltar dar baixa em algum, isso é feito no portal do órgão, antes do CDF. |
| A câmera desce até "A emissão do CDF é definitiva e não pode ser cancelada pelo sistema. Confira os dados antes de confirmar." e o resumo ("Período:", "Destinador:", "Gerador:", "MTRs:"). | E a emissão do CDF é definitiva. O resumo aqui embaixo ajuda a conferir tudo antes. |
| Clica em "Emitir CDF" ("Emitindo..."): "CDF emitido", "Nº do certificado: 2611000041", "Baixar PDF" e "Concluir"; toast "CDF emitido". [ZOOM: "Nº do certificado: 2611000041"] [BACKEND: `sigor-cdf-emit` → emitido, nº 2611000041, PDF] | Emitir CDF. Pronto, o certificado foi emitido, com o número dele. |
| Clica em "Concluir": a lista com o CDF ("Nº CDF" 2611000041, o período de outubro, "Gerador" Auto Peças Vale Forte, "Status" "Emitido"). | Na lista, cada CDF mostra o período, o gerador e o status. Se um der erro, o menu de ações mostra o erro e deixa tentar de novo. |

### cap08 · Baixar e guardar (vinheta: CDF)

| Tela | Fala |
| --- | --- |
| Abre "Ações" na linha do CDF e clica em "Baixar PDF" (o PDF abre em aba nova; a câmera fica no app). | Com o certificado emitido, o PDF sai pelo menu de ações: Baixar PDF. |
| [ILUSTRAÇÃO: onde guardar: o PDF genérico "CDF · outubro · Auto Peças Vale Forte" sai do computador e entra numa pasta "Licença de operação · Recicla Vale Metais", fora do sistema; ao lado, uma pilha "MTR de outubro".] | Uma dica: o CDF é documento de fiscalização. Guarde o PDF fora do sistema, na pasta da licença, e deixe os MTR do mesmo período por perto. |
| (ilustração: um selo "fiscalização" aponta para a pasta e a pilha juntas) | Na fiscalização, os dois costumam ser pedidos juntos. |

### cap09 · A nota da mesma carga (vinheta: NOTA FISCAL)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Notas Fiscais (NF-e)" › "Saída": a NF-e de hoje da Aços Quiririm Ltda, R$ 3.528,00, "Autorizada". | E como tudo isso conversa com a nota fiscal? A carga de chaparia de hoje tem a nota de venda dela, aqui em Notas Fiscais. |
| [ILUSTRAÇÃO: a mesma carga em três faixas: no centro, o caminhão GHT7B19 com chaparia; faixa "NF-e: a venda · SEFAZ · em Notas Fiscais"; faixa "MTR: o transporte do resíduo · SIGOR · em Ambiental"; faixa "CDF: o destino · depois, pelo destinador".] | São três documentos da mesma carga, cada um com o seu papel. A nota fiscal é a venda, e vai pra SEFAZ. O MTR é o transporte do resíduo, e vai pro órgão ambiental. |
| (ilustração: a faixa do CDF acende mais adiante na linha do tempo) | E o CDF vem depois, do destinador, confirmando o destino. |
| (ilustração: uma seta fina da faixa NF-e para a faixa MTR, com "itens e chave") | Eles são independentes: cada um é emitido na sua tela. O que o MTR aproveita da nota é o que a gente viu: os itens, pelo Puxar da nota fiscal, e a chave, na observação. |
| A ilustração sai; Ambiental › "MTR": a linha do "2611000318". | Assim você digita menos, e a nota e o MTR da mesma carga ficam ligados pela chave. |

### cap10 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: "Acesso validado", "Resíduo salvo" e "Resíduo do MTR definido em 3 material(is)". | Pronto! Recapitulando: a gente configurou o acesso ao SIGOR, sincronizou as listas do órgão, salvou a sucata de ferro como resíduo e ligou os materiais a ele. |
| (montagem: "MTR emitido" com o nº 2611000318, o "Histórico de tentativas" e o 2611000325 "Cancelado") | Emitiu o MTR da carga de chaparia puxando da nota fiscal, acompanhou, baixou o PDF e cancelou o MTR da carga que ficou pra depois. |
| (montagem: "CDF emitido" com o nº 2611000041 e a pasta da licença) | E emitiu o CDF de outubro da Auto Peças Vale Forte, com o PDF guardado junto da licença. |
| Cartão "Próximo: Funcionários e ponto eletrônico". | No próximo tutorial, a gente coloca a equipe do pátio dentro do sistema. Até lá! |
