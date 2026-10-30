// Parser do parametro `select` do PostgREST.
//   *   a,b   alias:coluna   coluna::tipo   json->chave   json->>chave   coluna.sum()
//   alias:tabela(cols)   tabela!inner(cols)   tabela!fk_ou_coluna(cols)   ...tabela(cols)   tabela(count)
//
// Resultado: lista de itens
//   { kind:'star' }
//   { kind:'field', name, alias, cast, json:[{op,key}], agg }
//   { kind:'embed', name, alias, hints:[...], inner, spread, children:[...] }

/** Quebra `s` em virgulas de nivel zero (ignora parenteses e aspas). */
export function splitTop(s, sep = ',') {
  const out = [];
  let depth = 0;
  let quote = false;
  let cur = '';
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (quote) {
      cur += c;
      if (c === '\\') cur += s[++i] ?? '';
      else if (c === '"') quote = false;
      continue;
    }
    if (c === '"') {
      quote = true;
      cur += c;
    } else if (c === '(' || c === '{' || c === '[') {
      depth++;
      cur += c;
    } else if (c === ')' || c === '}' || c === ']') {
      depth--;
      cur += c;
    } else if (c === sep && depth === 0) {
      out.push(cur);
      cur = '';
    } else cur += c;
  }
  if (cur !== '' || out.length) out.push(cur);
  return out;
}

function unquote(s) {
  const t = s.trim();
  return t.length >= 2 && t[0] === '"' && t[t.length - 1] === '"' ? t.slice(1, -1) : t;
}

/** Separa `alias:resto` (um unico ':' que nao faca parte de '::'). */
function splitAlias(s) {
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (c === '(' || c === '!' || c === '-' || c === '"') break;
    if (c === ':' && s[i + 1] !== ':' && s[i - 1] !== ':') return [s.slice(0, i), s.slice(i + 1)];
  }
  return [null, s];
}

function parseJsonPath(s) {
  // coluna->a->>b  => { col:'coluna', json:[{op:'->',key:'a'},{op:'->>',key:'b'}] }
  const idx = s.indexOf('->');
  if (idx < 0) return { col: s, json: [] };
  const json = [];
  let p = idx;
  while (p < s.length) {
    const op = s.startsWith('->>', p) ? '->>' : '->';
    const start = p + op.length;
    let next = s.indexOf('->', start);
    if (next < 0) next = s.length;
    json.push({ op, key: unquote(s.slice(start, next)) });
    p = next;
  }
  return { col: s.slice(0, idx), json };
}

export function parseSelect(str) {
  if (str === undefined || str === null || str.trim() === '') return [{ kind: 'star' }];
  const items = [];
  for (const rawItem of splitTop(str)) {
    let s = rawItem.trim();
    if (!s) continue;
    if (s === '*') {
      items.push({ kind: 'star' });
      continue;
    }
    let spread = false;
    if (s.startsWith('...')) {
      spread = true;
      s = s.slice(3);
    }
    const paren = (() => {
      let q = false;
      for (let i = 0; i < s.length; i++) {
        if (s[i] === '"') q = !q;
        else if (!q && s[i] === '(') return i;
      }
      return -1;
    })();
    if (paren >= 0 && s.endsWith(')')) {
      const head = s.slice(0, paren);
      const inner = s.slice(paren + 1, -1).trim();
      // Agregados: count(), total:count(), price.sum(), s:price.sum()
      if (inner === '') {
        const [al, rs] = splitAlias(head);
        const am0 = rs.match(/^(?:(.*)\.)?(sum|avg|min|max|count)$/);
        if (am0) {
          items.push({ kind: 'field', name: am0[1] || null, alias: al || am0[2], agg: am0[2], json: [], cast: null });
          continue;
        }
      }
      const [alias, rest] = splitAlias(head);
      const [name, ...hints] = rest.split('!');
      const children = inner === 'count' || inner === 'count()' ? [{ kind: 'field', name: 'count', alias: 'count', agg: 'count', json: [] }] : parseSelect(inner);
      items.push({
        kind: 'embed',
        name: unquote(name),
        alias: alias ? unquote(alias) : null,
        hints,
        inner: hints.includes('inner'),
        spread,
        children,
      });
      continue;
    }
    // campo simples
    const [alias, rest0] = splitAlias(s);
    let rest = rest0;
    let agg = null;
    const am = rest.match(/^(.*)\.(sum|avg|min|max|count)\(\)$/);
    if (am) {
      rest = am[1];
      agg = am[2];
    }
    let cast = null;
    const ci = rest.indexOf('::');
    if (ci >= 0) {
      cast = rest.slice(ci + 2);
      rest = rest.slice(0, ci);
    }
    const { col, json } = parseJsonPath(rest);
    items.push({ kind: 'field', name: unquote(col), alias: alias ? unquote(alias) : null, cast, json, agg });
  }
  return items.length ? items : [{ kind: 'star' }];
}
