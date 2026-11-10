# Inventário · T16 · Nota Fiscal de mercadoria (NF-e)

> EM ANDAMENTO (salvo cedo por segurança; a máquina reiniciou na primeira tentativa).
> Código da versão gravada `APP_VERSION = "1.59.154"` (`src/config/version.ts:16`), cópia somente leitura em
> `/home/claude/ecoflix/app-src-1.59.154/`. Caminhos relativos a `src/`, exceto `supabase/...`.

## 1. Onde fica
- Menu lateral "Fiscal & Ambiental" → "Notas Fiscais (NF-e)" → `/fiscal-ambiental/nfe/entrada` (`config/routes.ts:428-445`).
  Outros itens do submenu (fora desta aula): "SPED Fiscal" (selo "BETA"), "Notas de Serviço (NFS-e)", "Transporte (MDF-e)",
  "Ambiental (MTR/CDF)", "Estoque Fiscal".
- Sub-abas da tela NF-e (`config/fiscalAmbientalTabs.ts:75-81`; rótulos `pages/NotasFiscais.tsx:176-179`): "Entrada",
  "Saída", "Notas Recebidas", "Inutilizadas".
- Permissão `screen_notas_fiscais`; ações `action_emit_nfe`, `action_manifest_inbound`, `action_export_contabil`
  (`config/routes.ts:248-253`). Módulo `notas_fiscais` (🔒).

## 2. Configuração Fiscal (`/fiscal-ambiental/configuracao/:secao`, `pages/ConfiguracaoFiscal.tsx`)
- Botão "Configurações Fiscais" no cabeçalho da tela NF-e (`pages/NotasFiscais.tsx:1832-1843`) → página "Configuração
  Fiscal", descrição "Tudo que a SEFAZ precisa saber antes da primeira nota." (`ConfiguracaoFiscal.tsx:1192-1201`).
- Trilho (`:924-980`): grupo "Emissão": "Certificado", "Empresa"; "Regras fiscais": "Impostos (padrão)" (sublabel "usado
  quando nenhum cenário se aplica"), "Cenários"; "Documentos": "Numeração", "Transportadora", "Serviços".
  Sem certificado, Empresa/Impostos/Numeração/Transportadora ficam apagados com "precisa do certificado digital"; quem
  entra por link vê "Esta seção só abre depois do certificado digital" / "É o certificado que assina a nota. Sem ele,
  nada do que for preenchido aqui chega na SEFAZ." e "Ir para o certificado" (`:985-1000`).
- Rodapé (`:1087-1096`, `:1239-1282`): "Esta seção salva sozinha, item a item" (Certificado, Cenários, Numeração,
  Transportadora, Serviços) ou "Alterações não salvas" / "Sem alterações pendentes" + "Descartar alterações" e
  **"Salvar configuração"** ("Salvando..." / "Cadastrando...") em Empresa e Impostos.
- Salvar (`handleSave`, `:696-909`): grava `company_fiscal_config` e chama a edge `plugnotas-register-company`
  (toast "Empresa cadastrada no sistema de NF-e!"); edge `ibge-cities` se faltar o código IBGE.

### 2.1 Certificado (`components/notas-fiscais/CertificadoSection.tsx`)
- "Passo 1 de 3: Configure primeiro o certificado digital." (`:309`); "Certificado Digital A1" / "Necessário para assinar
  e transmitir notas fiscais" (`:321-323`).
- Sem certificado: "Certificado não configurado" (`:391`); "Arquivo do Certificado (.pfx ou .p12)", botão "Selecionar
  arquivo"; "Senha do Certificado" (placeholder "Digite a senha do certificado"; ajuda "Use a senha do próprio
  certificado digital, não a senha da empresa."); **"Validar Certificado"** ("Validando...") (`:394-457`).
- Sucesso: toast "Certificado validado com sucesso!" (`:279-285`); "Certificado validado!" + "Configure os dados da
  empresa" (ou "Empresa habilitada para NF-e" depois do cadastro) (`:342-348`); chip de validade "Válido até dd/mm/aaaa"
  (`CertificateValidityChip.tsx:38-40`); "Próximo: Configurar Empresa"; "Substituir Certificado" (`:353-360`).
- Validade implausível (> 400 dias): "Certificado enviado, mas a validade não confere" / "Pode ser recusado pela SEFAZ.
  Confirme com sua contabilidade se este é o certificado A1 vigente." (`:332-340`); chip "Validade não confere · confira
  com a contabilidade" (`CertificateValidityChip.tsx:46-50`).
- Backend: edge `plugnotas-upload-certificate`; edge `plugnotas-certificate-info` (`hooks/useCertificateInfo.tsx:48`);
  RPC `certificate_vault_status` e (só rollback) `certificate_upload_store_self`.

### 2.2 Empresa (`components/notas-fiscais/EmpresaSection.tsx`)
- "Passo 2 de 3: Preencha os dados da empresa para NF-e." (`:264`); "Dados da Empresa" (+ "Importar dados" quando vazio);
  "Razão Social *", "Nome Fantasia", "CNPJ *", "Telefone", "E-mail", "Inscrição Estadual", "Inscrição Municipal"
  ("Necessária para emitir NFS-e") (`:270-324`); "Endereço Fiscal" (endereço do cadastro + "Editar em Configurações ›
  Empresa") (`:331-381`); "Responsável técnico (CSRT)"; "Logo para Nota Fiscal".

### 2.3 Impostos (padrão) (`components/notas-fiscais/ImpostosTab.tsx`)
- "Passo 3 de 3: Selecione o regime tributário. Os campos serão ajustados automaticamente." (`:310`); "Regime Tributário *"
  / "Este campo controla todos os cálculos de impostos e campos visíveis"; opções "Simples Nacional", "Simples Nacional —
  excesso de sublimite", "Lucro Presumido", **"Lucro Real"** (`:317-338`). Lucro Real mostra o quadro "Lucro Real:" com
  "PIS: 1,65% | COFINS: 7,60% (Regime Não Cumulativo)", "ICMS destacado conforme CST", "Gera direito a crédito de
  PIS/COFINS", "Possibilidade de apuração de IPI" (`:375-385`) e preenche PIS 1,65, COFINS 7,6, CST 01, não cumulativo
  (`:252-257`).
- Blocos com CST (regime normal): "Contribuinte de ICMS", "Alíquota do ICMS interno, sem o FCP (%)", "Alíquota do FCP,
  que soma por cima do ICMS (%)"; "ICMS" ("CST Entrada", "CST Saída"); "PIS / COFINS"; "IPI ..."; **"CFOPs Padrão"**
  ("CFOP Entrada Interna", "CFOP Entrada Interestadual", "CFOP Saída Interna", "CFOP Saída Interestadual", "CFOP Saída
  Indústria", "CFOP Saída Exportação") (`:984-1060`); "Informações Complementares Padrão"; "Reservado ao Fisco
  (padrão)"; "Código de Benefício Fiscal (cBenef)"; **"Reforma Tributária (IBS/CBS)"** ("Calcular IBS e CBS
  automaticamente", "CST-IBS/CBS", "cClassTrib") (`:1197-1300`).
- **Achado**: `IbsCbsReformaBanner.tsx` (o aviso "Reforma Tributária: IBS/CBS na NF-e" com as datas 03/08/2026 e
  04/01/2027) **não é renderizado em nenhuma tela** da 1.59.154 (nenhum import). A fonte diz "O aviso fica fixo no topo
  da tela": vale o código, a aula não mostra esse aviso.
