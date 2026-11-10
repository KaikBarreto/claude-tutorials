// ../../src-1.38.21/src/lib/disc/questions.ts
function isChoiceItem(i) {
  return "kind" in i && i.kind === "choice";
}
var LIKERT_MIN = 1;
var LIKERT_MAX = 5;
var DISC_ITEMS = [
  // ── D — Dominância ──────────────────────────────────────────────────────
  { id: "d1", factor: "D", reverse: false },
  { id: "d2", factor: "D", reverse: false },
  { id: "d3", factor: "D", reverse: false },
  { id: "d4", factor: "D", reverse: false },
  { id: "d5", factor: "D", reverse: false },
  { id: "d6", factor: "D", reverse: true },
  { id: "d7", factor: "D", reverse: true },
  { id: "d8", factor: "D", reverse: false },
  { id: "d9", factor: "D", reverse: false },
  { id: "d10", factor: "D", reverse: false },
  { id: "d11", factor: "D", reverse: true },
  { id: "d12", factor: "D", reverse: false },
  { id: "d13", factor: "D", reverse: false },
  { id: "d14", factor: "D", reverse: false },
  // ── I — Influência ──────────────────────────────────────────────────────
  { id: "i1", factor: "I", reverse: false },
  { id: "i2", factor: "I", reverse: false },
  { id: "i3", factor: "I", reverse: false },
  { id: "i4", factor: "I", reverse: false },
  { id: "i5", factor: "I", reverse: false },
  { id: "i6", factor: "I", reverse: true },
  { id: "i7", factor: "I", reverse: true },
  { id: "i8", factor: "I", reverse: false },
  { id: "i9", factor: "I", reverse: false },
  { id: "i10", factor: "I", reverse: false },
  { id: "i11", factor: "I", reverse: true },
  { id: "i12", factor: "I", reverse: false },
  { id: "i13", factor: "I", reverse: false },
  { id: "i14", factor: "I", reverse: false },
  // ── S — Estabilidade ────────────────────────────────────────────────────
  { id: "s1", factor: "S", reverse: false },
  { id: "s2", factor: "S", reverse: false },
  { id: "s3", factor: "S", reverse: false },
  { id: "s4", factor: "S", reverse: false },
  { id: "s5", factor: "S", reverse: false },
  { id: "s6", factor: "S", reverse: true },
  { id: "s7", factor: "S", reverse: true },
  { id: "s8", factor: "S", reverse: false },
  { id: "s9", factor: "S", reverse: false },
  { id: "s10", factor: "S", reverse: false },
  { id: "s11", factor: "S", reverse: true },
  { id: "s12", factor: "S", reverse: false },
  { id: "s13", factor: "S", reverse: false },
  { id: "s14", factor: "S", reverse: false },
  // ── C — Conscienciosidade ───────────────────────────────────────────────
  { id: "c1", factor: "C", reverse: false },
  { id: "c2", factor: "C", reverse: false },
  { id: "c3", factor: "C", reverse: false },
  { id: "c4", factor: "C", reverse: false },
  { id: "c5", factor: "C", reverse: false },
  { id: "c6", factor: "C", reverse: true },
  { id: "c7", factor: "C", reverse: true },
  { id: "c8", factor: "C", reverse: false },
  { id: "c9", factor: "C", reverse: false },
  { id: "c10", factor: "C", reverse: false },
  { id: "c11", factor: "C", reverse: true },
  { id: "c12", factor: "C", reverse: false },
  { id: "c13", factor: "C", reverse: false },
  { id: "c14", factor: "C", reverse: false }
];
var DISC_ITEM_IDS = DISC_ITEMS.map((i) => i.id);
var DISC_FACTORS = ["D", "I", "S", "C"];
var DISC_CHOICE_ITEMS = Array.from(
  { length: 20 },
  (_, idx) => ({ id: `ch${idx + 1}`, kind: "choice" })
);
var DISC_CHOICE_ITEM_IDS = DISC_CHOICE_ITEMS.map(
  (i) => i.id
);

// ../../src-1.38.21/src/lib/disc/formSelection.ts
var FORM_LIKERT_PER_FACTOR = 5;
var FORM_CHOICE_ITEMS = 8;
var FORM_TOTAL_ITEMS = DISC_FACTORS.length * FORM_LIKERT_PER_FACTOR + FORM_CHOICE_ITEMS;
function mulberry32(seed) {
  let s = seed >>> 0;
  return function() {
    s += 1831565813;
    let t = Math.imul(s ^ s >>> 15, 1 | s);
    t ^= t + Math.imul(t ^ t >>> 7, 61 | t);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
function hashString(str) {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = (Math.imul(hash, 33) ^ str.charCodeAt(i)) >>> 0;
  }
  return hash >>> 0;
}
function shuffle(arr, rng) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
  return arr;
}
function selectFormItems(seed, likertPerFactor = FORM_LIKERT_PER_FACTOR, choiceCount = FORM_CHOICE_ITEMS) {
  const rng = mulberry32(hashString(seed));
  const likertSelected = [];
  for (const factor of DISC_FACTORS) {
    const factorItems = DISC_ITEMS.filter((item) => item.factor === factor);
    const shuffled = shuffle([...factorItems], rng);
    likertSelected.push(...shuffled.slice(0, likertPerFactor));
  }
  const choiceSelected = shuffle(
    [...DISC_CHOICE_ITEMS],
    rng
  ).slice(0, choiceCount);
  const combined = [...likertSelected, ...choiceSelected];
  return shuffle(combined, rng);
}

// ../../src-1.38.21/src/lib/disc/scoring.ts
function isFactorLetter(v) {
  return v === "D" || v === "I" || v === "S" || v === "C";
}
var SCALE_MID = 50;
var PURE_GAP = 15;
var PURE_SECONDARY_CEILING = 55;
var FACTOR_ANGLE = {
  D: 270,
  // topo
  I: 0,
  // direita
  S: 90,
  // baixo
  C: 180
  // esquerda
};
var DEG2RAD = Math.PI / 180;
function clampScore(value) {
  return Math.min(100, Math.max(0, Math.round(value)));
}
function computeScores(answers) {
  const rawByFactor = { D: 0, I: 0, S: 0, C: 0 };
  const countByFactor = { D: 0, I: 0, S: 0, C: 0 };
  for (const item of DISC_ITEMS) {
    const raw = answers[item.id];
    if (typeof raw !== "number" || Number.isNaN(raw)) continue;
    const clamped = Math.min(LIKERT_MAX, Math.max(LIKERT_MIN, raw));
    const effective = item.reverse ? LIKERT_MIN + LIKERT_MAX - clamped : clamped;
    rawByFactor[item.factor] += effective;
    countByFactor[item.factor] += 1;
  }
  for (const item of DISC_CHOICE_ITEMS) {
    const pick = answers[item.id];
    if (!isFactorLetter(pick)) continue;
    for (const f of DISC_FACTORS) {
      rawByFactor[f] += f === pick ? LIKERT_MAX : LIKERT_MIN;
      countByFactor[f] += 1;
    }
  }
  const scoreForFactor = (f) => {
    const maxRaw = countByFactor[f] * LIKERT_MAX;
    if (maxRaw === 0) return 0;
    return clampScore(100 * rawByFactor[f] / maxRaw);
  };
  return {
    D: scoreForFactor("D"),
    I: scoreForFactor("I"),
    S: scoreForFactor("S"),
    C: scoreForFactor("C")
  };
}
function rankFactors(scores) {
  return [...DISC_FACTORS].sort((a, b) => {
    if (scores[b] !== scores[a]) return scores[b] - scores[a];
    return DISC_FACTORS.indexOf(a) - DISC_FACTORS.indexOf(b);
  });
}
function computeBlendAngle(scores) {
  let x = 0;
  let y = 0;
  for (const factor of DISC_FACTORS) {
    const weight = scores[factor];
    const rad = FACTOR_ANGLE[factor] * DEG2RAD;
    x += weight * Math.cos(rad);
    y += weight * Math.sin(rad);
  }
  if (Math.abs(x) < 1e-9 && Math.abs(y) < 1e-9) return FACTOR_ANGLE.D;
  let deg = Math.atan2(y, x) / DEG2RAD;
  if (deg < 0) deg += 360;
  return Math.round(deg * 100) / 100;
}
function computeIntensity(scores) {
  const total = DISC_FACTORS.reduce(
    (acc, f) => acc + Math.abs(scores[f] - SCALE_MID),
    0
  );
  const avg = total / DISC_FACTORS.length;
  const norm = avg / SCALE_MID;
  return Math.round(Math.min(1, Math.max(0, norm)) * 1e3) / 1e3;
}
function classify(scores) {
  const ranked = rankFactors(scores);
  const primary = ranked[0];
  const secondary = ranked[1];
  const gap = scores[primary] - scores[secondary];
  const isPure = gap >= PURE_GAP && scores[secondary] < PURE_SECONDARY_CEILING;
  const profileCode = isPure ? primary : `${primary}${secondary}`;
  return {
    primary,
    secondary,
    profileCode,
    isPure,
    blendAngle: computeBlendAngle(scores),
    intensity: computeIntensity(scores)
  };
}
function scoreAndClassify(answers) {
  const scores = computeScores(answers);
  return { scores, classification: classify(scores) };
}
export {
  classify,
  isChoiceItem,
  scoreAndClassify,
  selectFormItems
};
