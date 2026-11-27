// Cupom de impressora térmica saindo da fenda: papel de bobina com as linhas impressas (barras, sem texto) ou o texto de
// teste. Pivô no centro da BASE (o que sai por último), face para +z.
// uso: const c = cupom(imp, imp.userData.fenda, { w: .22, h: .34 }); c.userData.sai(p);   // p de 0 a 1: o papel sobe da fenda
// o: w, h (m), tipo ('generico' | 'teste' | 'branco'), quando (texto da data no teste), dobra (quanto curva ao sair, .3).
// A impressora.js e a registradora.js já trazem o seu. Para o cupom solto (voar, ir à mão), use sai(1) e mexa no grupo.
import { mat, malha, grupo, pintura, THREE } from '../motor.js';
export function cupom(pai, pos = [0, 0, 0], o = {}) {
  const w = o.w ?? .22, h = o.h ?? .34, g = grupo(pai, pos), W = 440, H = Math.round(W * h / w), k = W / 58;
  const m = pintura(W, H, (x) => { x.fillStyle = '#FBFBF7'; x.fillRect(0, 0, W, H); if (o.tipo === 'branco') return;
    const bar = (mx, my, mw, mh, c) => { x.fillStyle = c; x.beginPath(); x.roundRect(mx * k, my * k, mw * k, mh * k, Math.min(mh * k / 2, 8)); x.fill(); };
    if (o.tipo === 'teste') { x.fillStyle = '#17191A'; x.textAlign = 'center'; x.font = `700 ${4.2 * k}px M, Montserrat, sans-serif`; x.fillText('Teste de Impressão', W / 2, 14 * k);
      x.font = `500 ${2.7 * k}px M, Montserrat, sans-serif`; x.fillText('Se você vê isso, está funcionando!', W / 2, 21 * k); x.fillText(o.quando ?? '', W / 2, 27 * k); return; }
    bar(14, 5, 30, 3, '#475467'); bar(19, 10, 20, 1.9, '#98A2B3'); const n = Math.max(2, Math.floor((H / k - 48) / 6.2));
    for (let i = 0; i < n; i++) { const y = 18 + i * 6.2; bar(4.5, y, 20 + (i % 2) * 6, 2.1, '#98A2B3'); bar(41.5, y, 12, 2.1, '#475467'); }
    const y = 20 + n * 6.2; x.strokeStyle = '#D0D5DD'; x.lineWidth = 3; x.setLineDash([14, 10]); x.beginPath(); x.moveTo(4.5 * k, y * k); x.lineTo(53.5 * k, y * k); x.stroke(); x.setLineDash([]);
    bar(4.5, y + 4, 16, 2.8, '#475467'); bar(35.5, y + 3.6, 18, 3.4, '#2FB271'); bar(17, y + 14, 24, 1.9, '#98A2B3'); }, { emi: .55, ds: true });
  const geo = new THREE.PlaneGeometry(w, h); geo.translate(0, h / 2, 0); const papel = malha(geo, m, [0, 0, 0], g);
  g.userData = { w, h, papel, sai(p) { p = Math.min(1, Math.max(0, p)); papel.visible = p > .002; papel.scale.y = Math.max(p, 1e-4); m.uniforms.uUV.value.set(0, 1 - p, 1, p); g.rotation.x = (o.dobra ?? .3) * p; } };
  g.userData.sai(1); return g;
}
