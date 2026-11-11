// Contas do módulo de Coletas (T12), espelho das funções do banco do EcoSistema 1.59.154 (supabase/migrations):
// change_collection_order_status + sync_collection_order_equipment_movements (20261008150000, 20261008140000),
// register_collection_equipment_movement (20261008140000), build_collection_order_snapshot (20260924130000).
import { agoraMs } from './eco.mjs';

export const STATUS_LABEL = { solicitada: 'Solicitada', agendada: 'Agendada', a_caminho: 'A caminho', coletada: 'Concluída', cancelada: 'Cancelada' };
export const JANELA_LABEL = { manha: 'Manhã', tarde: 'Tarde', dia_todo: 'Dia todo' };
export const PROXIMOS = { solicitada: ['agendada', 'cancelada'], agendada: ['a_caminho', 'cancelada'], a_caminho: ['coletada', 'cancelada'] };
export const agoraIso = () => new Date(agoraMs()).toISOString();
const vazio = (v) => (v === null || v === undefined || String(v).trim() === '' ? null : String(v).trim());

/** nome do parceiro (fornecedor ou cliente) pelo id */
export function nomeParceiro(store, tipo, id) {
  if (!id) return null;
  const r = store.rows(tipo === 'customer' ? 'customers' : 'suppliers').find((x) => x.id === id);
  return r ? r.name || r.razao_social || null : null;
}

/** uma linha do razão de equipamentos (_collection_equipment_insert_line, sem as checagens de cadeia) */
export function inserirMovimento(db, store, l) {
  const pt = (k) => (l[`${k}_kind`] === 'partner' ? l[`${k}_partner_type`] : null);
  const pid = (k) => (l[`${k}_kind`] === 'partner' ? l[`${k}_partner_id`] : null);
  const agora = agoraIso();
  return db.insert('collection_equipment_movements', {
    company_id: l.company_id, equipment_type_id: l.equipment_type_id, container_id: l.container_id || null,
    quantidade: Number(l.quantidade ?? 1) || 1,
    origem_kind: l.origem_kind, origem_partner_type: pt('origem'), origem_partner_id: pid('origem'),
    origem_partner_nome: nomeParceiro(store, pt('origem'), pid('origem')),
    destino_kind: l.destino_kind, destino_partner_type: pt('destino'), destino_partner_id: pid('destino'),
    destino_partner_nome: nomeParceiro(store, pt('destino'), pid('destino')),
    moved_at: l.moved_at || agora, collection_order_id: l.collection_order_id || null, observacao: vazio(l.observacao),
    created_by: l.created_by || null, created_at: agora, updated_at: agora, voided: false, edit_history: [],
  });
}

/** sync_collection_order_equipment_movements: as linhas "entreguei/recolhi" da ordem concluída viram movimentações (moved_at = conclusão) */
export function sincronizarEquipamentos(db, store, ordem, linhas, uid) {
  const antigas = store.rows('collection_equipment_movements').filter((m) => m.collection_order_id === ordem.id && !m.voided);
  const agora = agoraIso();
  for (const m of antigas) Object.assign(m, { voided: true, voided_at: agora, voided_by: uid || null, voided_reason: 'Ordem reconcluída' });
  if (antigas.length) store.table('collection_equipment_movements').touch();
  const ids = [];
  if (ordem.status === 'coletada' && Array.isArray(linhas)) {
    for (const l of linhas) {
      const ent = l.direcao === 'entregue';
      const r = inserirMovimento(db, store, {
        company_id: ordem.company_id, equipment_type_id: l.equipment_type_id, container_id: l.container_id, quantidade: l.quantidade,
        origem_kind: ent ? 'base' : 'partner', origem_partner_type: ordem.partner_type, origem_partner_id: ordem.partner_id,
        destino_kind: ent ? 'partner' : 'base', destino_partner_type: ordem.partner_type, destino_partner_id: ordem.partner_id,
        moved_at: ordem.completed_at || agora, collection_order_id: ordem.id, created_by: uid,
      });
      ids.push(r.id);
    }
  }
  return { inseridas: ids.length, anuladas: antigas.length, movement_ids: ids };
}

/** build_collection_order_snapshot: o corpo do "Relatório de Coleta N" */
export function relatorio(store, o) {
  const co = store.rows('companies').find((c) => c.id === o.company_id) || {};
  const prefixo = (store.rows('collection_settings').find((s) => s.company_id === o.company_id) || {}).order_number_prefix || '';
  const parc = o.partner_id ? store.rows(o.partner_type === 'customer' ? 'customers' : 'suppliers').find((x) => x.id === o.partner_id) : null;
  const tipos = new Map(store.rows('collection_equipment_types').map((t) => [t.id, t]));
  const conts = new Map(store.rows('collection_containers').map((c) => [c.id, c]));
  const cidadeUf = [vazio(o.cidade), vazio(o.uf)].filter(Boolean).join('/');
  const rua = [vazio(o.logradouro), vazio(o.numero_end)].filter(Boolean).join(', ');
  const completo = [rua, vazio(o.bairro), cidadeUf, vazio(o.cep)].filter(Boolean).join(', ') || null;
  const equip = store.rows('collection_equipment_movements')
    .filter((m) => m.collection_order_id === o.id && !m.voided)
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)) || String(a.id).localeCompare(String(b.id)))
    .map((m) => {
      const t = tipos.get(m.equipment_type_id) || {};
      const dir = m.destino_kind === 'partner' ? 'entregue' : m.origem_kind === 'partner' ? 'recolhido' : 'movimentado';
      return {
        direcao: dir, direcao_label: { entregue: 'Entregue no local', recolhido: 'Recolhido do local', movimentado: 'Movimentado' }[dir],
        tipo_nome: vazio(t.nome) || 'Equipamento', identificavel: !!t.identificavel,
        identificacao: m.container_id ? vazio((conts.get(m.container_id) || {}).identificacao) : null,
        quantidade: Number(m.quantidade), movido_em: m.moved_at, observacao: vazio(m.observacao),
      };
    });
  return {
    versao: 1, gerado_em: agoraIso(),
    empresa: { nome: co.name || null, cnpj: vazio(co.cnpj), telefone: vazio(co.phone), email: vazio(co.email), endereco: vazio(co.address),
      endereco_2: vazio(co.address_2), logo_url: vazio(co.logo_url) },
    ordem: { id: o.id, numero: o.numero, numero_formatado: `${prefixo}${o.numero}`, status: o.status, status_label: 'Concluída', origem: o.origem,
      criada_em: o.created_at, concluida_em: o.completed_at },
    parceiro: { tipo: o.partner_type, tipo_label: o.partner_type === 'customer' ? 'Cliente' : 'Fornecedor',
      nome: vazio(o.partner_nome) || (parc ? parc.name : null), documento: parc ? vazio(parc.cpf_cnpj) : null },
    endereco: { logradouro: vazio(o.logradouro), numero: vazio(o.numero_end), bairro: vazio(o.bairro), cidade: vazio(o.cidade), uf: vazio(o.uf),
      cep: vazio(o.cep), completo },
    agendamento: { data: o.scheduled_date || null, janela: vazio(o.scheduled_window), janela_label: JANELA_LABEL[o.scheduled_window] || null },
    coleta: { motorista: vazio(o.driver_name), veiculo_placa: vazio(o.vehicle_plate), material_estimado: vazio(o.material_estimado),
      observacoes: vazio(o.observacoes) },
    equipamentos: equip, valores: null, checklist: null, assinaturas: { motorista: null, responsavel: null }, foto_urls: [],
  };
}

/** has_module(empresa, código) pelo company_modules */
export function temModulo(store, companyId, codigo) {
  return store.rows('company_modules').some((m) => m.company_id === companyId && (m.module_code || m.code) === codigo && m.is_active !== false && m.active !== false);
}

/** dono do portal (fornecedor ou cliente com o token; resolvePortalParty sem o lado vinculado com senha) */
export function parteDoPortal(store, token) {
  if (!token) return null;
  let tipo = 'customer';
  let row = store.rows('customers').find((c) => c.portal_token === token);
  if (!row) {
    row = store.rows('suppliers').find((s) => s.portal_token === token);
    tipo = 'supplier';
  }
  if (!row) return null;
  const linkedId = tipo === 'customer' ? row.linked_supplier_id : row.linked_customer_id;
  const outro = linkedId ? store.rows(tipo === 'customer' ? 'suppliers' : 'customers').find((x) => x.id === linkedId && x.company_id === row.company_id) : null;
  const customerId = tipo === 'customer' ? row.id : outro ? outro.id : null;
  const supplierId = tipo === 'supplier' ? row.id : outro ? outro.id : null;
  const on = (k) => (row.portal_config || {})[k] !== false && (!outro || (outro.portal_config || {})[k] !== false);
  const cfg = {};
  for (const k of ['historico', 'resumo', 'grafico', 'valores', 'fotos', 'saldo', 'notas', 'relatorio', 'relatorio_valores', 'coletas', 'solicitar_coleta']) cfg[k] = on(k);
  cfg.precos = (row.portal_config || {}).precos === true && (!outro || (outro.portal_config || {}).precos !== false);
  cfg.locked = {};
  return { row, tipo, outro, isDual: !!outro, customerId, supplierId, ids: [customerId, supplierId].filter(Boolean), companyId: row.company_id, cfg,
    senha: !!row.portal_password_enabled || !!(outro && outro.portal_password_enabled) };
}
