// "Fator humano": trajetoria do mouse, ritmo de digitacao e rolagem suave. Tudo deterministico por semente,
// para regravar o mesmo roteiro e obter o mesmo comportamento.

/** Gerador pseudo-aleatorio (mulberry32) a partir de um texto. */
export function makeRng(seedText = 'domiflix') {
  let h = 1779033703 ^ seedText.length;
  for (let i = 0; i < seedText.length; i++) {
    h = Math.imul(h ^ seedText.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  let a = (h ^ (h >>> 16)) >>> 0;
  const next = () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  next.range = (lo, hi) => lo + (hi - lo) * next();
  next.normal = () => {
    // Box-Muller
    const u = Math.max(next(), 1e-9);
    const v = next();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  next.pick = (arr) => arr[Math.floor(next() * arr.length)];
  return next;
}

export const sleep = (ms) => new Promise((r) => setTimeout(r, Math.max(0, ms)));
export const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

/** Perfil de "minimum jerk": parte devagar, acelera, desacelera e chega suave (0..1 -> 0..1). */
export const minJerk = (t) => {
  const x = clamp(t, 0, 1);
  return x * x * x * (10 - 15 * x + 6 * x * x);
};

/**
 * Duracao (s) de um deslocamento do ponteiro. Curto ~0,3 s; grande 0,5 a 0,9 s.
 * `pace` > 1 deixa tudo mais lento (didatico), < 1 mais rapido.
 */
export function moveDuration(dist, rng, pace = 1) {
  const base = clamp(0.26 + 0.00068 * dist, 0.26, 0.9);
  const jitter = 1 + rng.range(-0.08, 0.08);
  return Math.max(0.18, base * jitter * pace);
}

/**
 * Trajetoria do ponteiro de A para B: curva de Bezier cubica com leve arco (lado e curvatura sorteados) e
 * velocidade em minimum-jerk. Devolve `at(t)` (t em segundos desde o inicio) e a duracao total.
 */
export function planMove(from, to, rng, { pace = 1 } = {}) {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  const dist = Math.hypot(dx, dy);
  const T = moveDuration(dist, rng, pace);
  if (dist < 1.5) return { duration: 0.001, dist, at: () => ({ x: to.x, y: to.y }) };
  const nx = -dy / dist;
  const ny = dx / dist;
  const arc = clamp(dist * rng.range(0.025, 0.09), 3, 70) * (rng() < 0.5 ? -1 : 1);
  const p1 = { x: from.x + dx * 0.28 + nx * arc, y: from.y + dy * 0.28 + ny * arc };
  const p2 = { x: from.x + dx * 0.72 + nx * arc * 0.55, y: from.y + dy * 0.72 + ny * arc * 0.55 };
  // levemente assimetrico: freia um pouco mais devagar do que acelera (como a mao)
  const skew = rng.range(0.9, 1.0);
  const at = (t) => {
    const u = minJerk(Math.pow(clamp(t / T, 0, 1), skew));
    const v = 1 - u;
    return {
      x: v * v * v * from.x + 3 * v * v * u * p1.x + 3 * v * u * u * p2.x + u * u * u * to.x,
      y: v * v * v * from.y + 3 * v * v * u * p1.y + 3 * v * u * u * p2.y + u * u * u * to.y,
    };
  };
  return { duration: T, dist, at };
}

/** Atrasos (ms) entre teclas: ritmo medio por `cps` (caracteres/s), com variacao e pausas depois de espaco/pontuacao. */
export function typingDelays(text, rng, { cps = 11 } = {}) {
  const base = 1000 / cps;
  return [...text].map((ch, i) => {
    let d = base * Math.exp(rng.normal() * 0.3 - 0.045);
    if (ch === ' ') d += rng.range(10, 70);
    if (/[.,;:!?]/.test(ch)) d += rng.range(60, 180);
    if (i > 0 && /[A-ZÁÉÍÓÚÂÊÔÃÕÇ]/.test(ch)) d += rng.range(20, 70);
    if (rng() < 0.04) d += rng.range(120, 320); // hesitacao ocasional
    return Math.round(clamp(d, base * 0.45, base * 4.5));
  });
}
