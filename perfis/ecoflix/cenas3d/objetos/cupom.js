// cupom(pai, p, o): cupom de impressora térmica saindo da fenda (papel de bobina com texto impresso numa textura), pivô no
// centro da BASE do papel (o que sai por último), face para +z. A largura do papel e a do desenho são independentes: com
// desenho > papel o lado direito fica de fora, e userData.fantasma é o pedaço que se perdeu (âmbar, tracejado, ao lado).
// o: papel (mm, 58), desenho (mm, 80), alt (mm, 40 | 64), esc (m por mm; padrão .22/58, a fenda da impressora do kit),
//    tipo ('teste' | 'generico'), quando (texto da data e hora do teste), cor (tinta).
// userData: larg, alt (m, local), tinta (a malha do texto: tinta.visible = false deixa o papel em branco), fantasma (grupo; escondido até aparecer), corte (barra âmbar na borda do papel),
//    sai(p) (0 a 1: o papel sobe da fenda; precisa do plano de corte em Y do mundo: corteEm(yMundo)).
// Uso (T05): const c = cupom(imp, [0, .196, .068], { papel: 58, desenho: 80, quando: QUANDO }); c.userData.corteEm(mundo(imp,[0,.196,0])[1]);
import { THREE, RD, grupo, poe, rbox, M, COR, lerp } from '../kit3d.js';

const K = 10;   // px por mm na textura
const FONTE = '500 {px}px M, Montserrat, sans-serif';
function desenha(ctx, o, x0, W, H, ghost) {   // desenha o layout de largura o.desenho (mm), a partir do mm x0, num canvas de W px
  const cor = ghost ? '#C8A55F' : (o.cor ?? '#111'), forte = ghost ? '#D9BC7E' : '#475467', claro = ghost ? '#E3CE9E' : '#98A2B3', D = o.desenho;
  const mm = v => (v - x0) * K, bar = (x, y, w, h, c) => { ctx.fillStyle = c; ctx.beginPath(); ctx.roundRect(mm(x), y * K, w * K, h * K, Math.min(h * K / 2, 8)); ctx.fill(); };
  if (o.tipo === 'teste') {
    const L = (y, pt, txt) => { ctx.font = FONTE.replace('{px}', (pt * .3528 * K).toFixed(1)); ctx.fillStyle = cor; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillText(txt, mm(D / 2), y * K); };
    L(15, 12, 'Teste de Impressão'); L(22, 8, 'Se você vê isso, está funcionando!'); L(28, 8, o.quando ?? '');
  } else {
    const p = D * .07;
    bar(D / 2 - D * .26, 3.9, D * .52, 2.9, forte); bar(D / 2 - D * .18, 8.6, D * .36, 1.8, claro);
    for (let i = 0; i < 4; i++) { const y = 16.1 + i * 6.1; bar(p, y, D * (.34 + (i % 2) * .1), 2, claro); bar(D - p - D * .2, y, D * .2, 2, forte); }
    ctx.strokeStyle = '#D0D5DD'; ctx.lineWidth = 3; ctx.setLineDash([14, 10]); ctx.beginPath(); ctx.moveTo(mm(p), 41.4 * K); ctx.lineTo(mm(D - p), 41.4 * K); ctx.stroke(); ctx.setLineDash([]);
    bar(p, 45.4, D * .28, 2.7, forte); bar(D - p - D * .3, 45, D * .3, 3.2, '#344054'); bar(D / 2 - D * .22, 58, D * .44, 1.8, claro);
  }
}
function textura(c) { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; }

export function cupom(pai, p = [0, 0, 0], o = {}) {
  o = { papel: 58, desenho: 80, alt: o.tipo === 'generico' ? 64 : 40, esc: .22 / 58, tipo: 'teste', ...o };
  const g = grupo(pai, p), e = o.esc, w = o.papel * e, h = o.alt * e, u = g.userData, planos = [];
  const mat = m => { m.clippingPlanes = [u.plano = u.plano || new THREE.Plane(new THREE.Vector3(0, 1, 0), 0)]; planos.push(m); return m; };
  const cv = document.createElement('canvas'); cv.width = o.papel * K; cv.height = o.alt * K; desenha(cv.getContext('2d'), o, 0, cv.width, cv.height, false);
  poe(rbox(w, h, .004, .002, 1), mat(M(COR.papel).clone()), g, [0, h / 2, 0]);
  const tx = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat(new THREE.MeshStandardMaterial({ map: textura(cv), transparent: true, roughness: .9, metalness: 0 })));
  tx.position.set(0, h / 2, .0026); g.add(tx);
  const corte = poe(rbox(.012, h + .02, .012, .004, 1), mat(M(COR.ambar).clone()), g, [w / 2, h / 2, .002]); corte.visible = false; u.corte = corte;
  if (o.desenho > o.papel) {
    const fw = (o.desenho - o.papel) * e, gf = grupo(g, [w / 2 + fw / 2, h / 2, .001]), c2 = document.createElement('canvas'); c2.width = (o.desenho - o.papel) * K; c2.height = o.alt * K;
    const x = c2.getContext('2d'); x.fillStyle = 'rgba(255,245,223,.8)'; x.fillRect(0, 0, c2.width, c2.height);
    desenha(x, o, o.papel, c2.width, c2.height, true);
    x.strokeStyle = '#E0B45C'; x.lineWidth = 6; x.setLineDash([22, 14]); x.strokeRect(0, 3, c2.width - 3, c2.height - 6);
    const fm = mat(new THREE.MeshStandardMaterial({ map: textura(c2), transparent: true, roughness: .9, metalness: 0 })); gf.add(new THREE.Mesh(new THREE.PlaneGeometry(fw, h), fm));
    gf.visible = false; u.fantasma = gf;
  }
  u.tinta = tx; u.larg = w; u.alt = h; u.esc = e; u.y0 = p[1];
  RD.localClippingEnabled = true;
  u.corteEm = y => { u.plano.constant = -y; };
  u.sai = q => { g.visible = q > .002; g.position.y = u.y0 - (1 - q) * h * 1.02; };
  u.sai(0); return g;
}
