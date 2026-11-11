// VIEW collection_equipment_positions · 20261008210000_collection_equipment_types_icon_color.sql
// Posição derivada do razão (collection_equipment_movements, sem as anuladas): regime "fungivel" = saldo por (tipo, lugar), com o "desde"
// contado a partir da última vez que o saldo zerou (só saldo ≠ 0); regime "identificavel" = uma linha por unidade, com o destino da última
// movimentação (lugar_kind nulo = "Sem movimentação"; "externo" = quantidade 0).
const ord = (a, b) => String(a.moved_at).localeCompare(String(b.moved_at)) || String(a.created_at).localeCompare(String(b.created_at)) || String(a.id).localeCompare(String(b.id));

export default function collectionEquipmentPositions(store) {
  const tipos = new Map(store.rows('collection_equipment_types').map((t) => [t.id, t]));
  const movs = store.rows('collection_equipment_movements').filter((m) => !m.voided);
  const grupos = new Map();
  for (const m of movs.filter((x) => !x.container_id)) {
    const lados = [];
    if (m.origem_kind !== 'externo') lados.push([m.origem_kind, m.origem_partner_type ?? null, m.origem_partner_id ?? null, -Number(m.quantidade)]);
    if (m.destino_kind !== 'externo') lados.push([m.destino_kind, m.destino_partner_type ?? null, m.destino_partner_id ?? null, Number(m.quantidade)]);
    for (const [kind, ptype, pid, qtd] of lados) {
      const k = JSON.stringify([m.company_id, m.equipment_type_id, kind, ptype, pid]);
      if (!grupos.has(k)) grupos.set(k, { company_id: m.company_id, equipment_type_id: m.equipment_type_id, kind, ptype, pid, rows: [] });
      grupos.get(k).rows.push({ ...m, qtd });
    }
  }
  const out = [];
  for (const g of grupos.values()) {
    g.rows.sort(ord);
    let saldo = 0;
    let zero = -1;
    g.rows.forEach((r, i) => {
      saldo += r.qtd;
      if (saldo <= 0) zero = i;
    });
    if (saldo === 0) continue;
    const t = tipos.get(g.equipment_type_id);
    if (!t) continue;
    const depois = g.rows.slice(zero + 1);
    out.push({
      company_id: g.company_id, regime: 'fungivel', equipment_type_id: t.id, equipment_type_nome: t.nome, identificavel: t.identificavel, tipo_ativo: t.ativo,
      container_id: null, container_identificacao: null, condicao: null, container_ativo: null,
      lugar_kind: g.kind, lugar_partner_type: g.ptype, lugar_partner_id: g.pid, quantidade: saldo,
      desde: depois.length ? depois[0].moved_at : null, equipment_type_icon: t.icon, equipment_type_color: t.color,
    });
  }
  const ultimo = new Map();
  for (const m of movs.filter((x) => x.container_id).sort(ord)) ultimo.set(m.container_id, m);
  for (const c of store.rows('collection_containers')) {
    const u = ultimo.get(c.id);
    const t = tipos.get(c.equipment_type_id) || {};
    out.push({
      company_id: c.company_id, regime: 'identificavel', equipment_type_id: t.id ?? null, equipment_type_nome: t.nome ?? null,
      identificavel: t.identificavel ?? null, tipo_ativo: t.ativo ?? null, container_id: c.id, container_identificacao: c.identificacao,
      condicao: c.condicao, container_ativo: c.ativo, lugar_kind: u ? u.destino_kind : null, lugar_partner_type: u ? u.destino_partner_type ?? null : null,
      lugar_partner_id: u ? u.destino_partner_id ?? null : null, quantidade: !u || u.destino_kind === 'externo' ? 0 : 1, desde: u ? u.moved_at : null,
      equipment_type_icon: t.icon ?? null, equipment_type_color: t.color ?? null,
    });
  }
  return out;
}
