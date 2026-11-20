// registrar_consulta_cnpj_ie(...): grava no cache global `cnpj_registros_estaduais` o resultado da consulta de inscrição estadual feita pela
// lupa do CNPJ (utils/consultaIeCache.ts:127-170; migration da 1.59.157). O app ignora o retorno. No mundo falso não guarda nada: a próxima
// lupa consulta de novo o `publica.cnpj.ws` simulado, e a aula repete o mesmo CNPJ com o mesmo resultado (T4 cap. 3, 4, 5 e 6).
export default () => null;
