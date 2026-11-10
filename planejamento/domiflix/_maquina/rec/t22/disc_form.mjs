#!/usr/bin/env node
// T22 · disc_form.mjs <código> [perfil]  ->  JSON com as 28 perguntas do link (id, tipo, fator) e a resposta fixa de cada uma, mais os escores e o
// perfil que essas respostas produzem. Perfil-alvo do Rafael: Estabilidade em primeiro, Conformidade em segundo ("SC").
// Regerar o bundle:  app/node_modules/.bin/esbuild rec/t22/disc_form.entry.ts --bundle --platform=node --format=esm --outfile=rec/t22/.disc_form.mjs
import { selectFormItems, scoreAndClassify, isChoiceItem } from './.disc_form.mjs';

const code = process.argv[2];
// ordem das 4 opções de uma pergunta de alternativa na tela (components/employees/disc/DiscChoiceSelect.tsx: djb2 + mulberry32 + Fisher-Yates, semente `${code}|${id}`)
const mulberry32 = (seed) => { let s = seed >>> 0; return () => { s += 0x6d2b79f5; let t = Math.imul(s ^ (s >>> 15), 1 | s); t ^= t + Math.imul(t ^ (t >>> 7), 61 | t); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
const hashString = (str) => { let h = 5381; for (let i = 0; i < str.length; i++) h = (Math.imul(h, 33) ^ str.charCodeAt(i)) >>> 0; return h >>> 0; };
const ordemOpcoes = (seed) => { const a = ['D', 'I', 'S', 'C']; const rng = mulberry32(hashString(seed)); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rng() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const ALVO = { S: 5, C: 4, I: 2, D: 1 };            // quanto a pessoa "é" cada fator (1 a 5)
const itens = selectFormItems(code);
const respostas = {}, passos = [];
let ci = 0;
for (const it of itens) {
  if (isChoiceItem(it)) {
    const letra = ['S', 'C', 'S', 'C'][ci++ % 4];    // alternativas: Estabilidade, Conformidade, Estabilidade, Conformidade...
    respostas[it.id] = letra;
    passos.push({ id: it.id, tipo: 'alternativa', fator: null, resposta: letra, posicao: ordemOpcoes(`${code}|${it.id}`).indexOf(letra) });
  } else {
    const alvo = ALVO[it.factor];
    const v = it.reverse ? 6 - alvo : alvo;           // item invertido: quem tem o fator alto discorda
    respostas[it.id] = v;
    passos.push({ id: it.id, tipo: 'escala', fator: it.factor, reverse: it.reverse, resposta: v });
  }
}
const { scores, classification } = scoreAndClassify(respostas);
console.log(JSON.stringify({ code, total: itens.length, passos, scores, perfil: classification }, null, 1));
