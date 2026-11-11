// SIGOR simulado (T18 · Ambiental: MTR e CDF): as listas oficiais que o "Sincronizar dados do SIGOR" traz, as classes permitidas por
// resíduo e as regras de numeração dos documentos emitidos. Nada sai para fora: o órgão ambiental (SIGOR/CETESB-SP) é inventado aqui.
// Códigos e descrições plausíveis, não oficiais (a fala manda conferir na lista do órgão). Unidades no formato do órgão: "SIGLA - Nome".
export const SISTEMA = 'sigor_sp';

export const REF = {
  mtr_ref_residuos: [
    ['15 01 01', 'Embalagens de papel e cartão'],
    ['15 01 02', 'Embalagens de plástico'],
    ['15 01 04', 'Embalagens de metal'],
    ['16 06 01', 'Baterias de chumbo'],
    ['17 04 01', 'Cobre, bronze, latão'],
    ['17 04 02', 'Alumínio'],
    ['17 04 05', 'Ferro e aço'],
    ['17 04 07', 'Mistura de metais'],
    ['19 12 02', 'Metais ferrosos'],
    ['19 12 03', 'Metais não ferrosos'],
    ['19 12 04', 'Plástico e borracha'],
    ['20 01 01', 'Papel e cartão'],
    ['20 01 02', 'Vidro'],
    ['20 01 39', 'Plásticos'],
  ],
  mtr_ref_classe: [[1, 'Classe I - Perigoso'], [2, 'Classe II A - Não inerte'], [3, 'Classe II B - Inerte']],
  mtr_ref_estado_fisico: [[1, 'Sólido'], [2, 'Líquido'], [3, 'Gasoso'], [4, 'Pastoso']],
  mtr_ref_acondicionamento: [[1, 'Tambor'], [2, 'Bombona'], [3, 'Caixa'], [4, 'Caçamba'], [5, 'Granel'], [6, 'Big bag'], [7, 'Saco'], [8, 'Contêiner']],
  mtr_ref_tratamento: [[1, 'Reciclagem'], [2, 'Reutilização'], [3, 'Reprocessamento'], [4, 'Aterro industrial'], [5, 'Incineração'], [6, 'Coprocessamento'], [7, 'Compostagem']],
  mtr_ref_unidade: [[1, 'TON - Tonelada'], [2, 'KG - Quilograma'], [3, 'UN - Unidade'], [4, 'Lt - Litro'], [5, 'M³ - M³']],
};

/** Classes que a licença permite para o resíduo (resposta do "classes-for-residue"): metais, só as não perigosas. */
export function classesDoResiduo(codigo) {
  const cod = String(codigo || '').trim();
  const todas = REF.mtr_ref_classe.map(([c, d]) => ({ codigo: c, descricao: d }));
  return /^(17 04|19 12 0[23])/.test(cod) ? todas.filter((c) => c.codigo !== 1) : todas;
}

/** MTR de outubro da Auto Peças Vale Forte, já recebidos e baixados no portal (o CDF só junta MTR recebido). */
export const MTR_RECEBIDOS = ['2610001542', '2610001877', '2610002203'];

/** Próximo número livre do órgão, a partir do primeiro da aula (MTR 2611000318; CDF 2611000041). */
export function proximoNumero(usados, primeiro) {
  const set = new Set((usados || []).filter(Boolean).map(String));
  let n = BigInt(primeiro);
  while (set.has(String(n))) n += 1n;
  return String(n);
}
