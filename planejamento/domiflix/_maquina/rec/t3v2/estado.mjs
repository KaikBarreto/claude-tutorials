#!/usr/bin/env node
// Imprime o que o robô deixou nas tabelas de etiquetas, campos e vínculos do Supabase falso (FAKE_URL), em nomes legíveis.
const FAKE = process.env.FAKE_URL || 'http://127.0.0.1:54323';
const get = async (t) => (await fetch(`${FAKE}/__dev/state?table=${encodeURIComponent(t)}`)).json().catch(() => []);
const [labels, cla, sla, ela, fcfg, ecfg, cust, sup, eq, cats, origins, forms] = await Promise.all(['party_labels', 'customer_label_assignments', 'supplier_label_assignments', 'equipment_label_assignments', 'party_field_config', 'equipment_field_config', 'customers', 'suppliers', 'equipment', 'equipment_categories', 'customer_origins', 'lead_capture_forms'].map(get));
const L = new Map((labels || []).map((l) => [l.id, l]));
const nome = (m, id, k = 'name') => (m.get(id) || {})[k] || id;
const C = new Map((cust || []).map((c) => [c.id, c])), S = new Map((sup || []).map((c) => [c.id, c])), E = new Map((eq || []).map((c) => [c.id, c]));
console.log('etiquetas:', (labels || []).map((l) => `${l.name} [${l.scope}] ${l.color} ativo=${l.is_active} portal=${l.show_in_portal}`).join(' | ') || '(nenhuma)');
console.log('clientes x etiquetas:', (cla || []).map((a) => `${nome(C, a.customer_id)} <- ${nome(L, a.label_id)} (pos ${a.position})`).join(' | ') || '(nenhum)');
console.log('fornecedores x etiquetas:', (sla || []).map((a) => `${nome(S, a.supplier_id)} <- ${nome(L, a.label_id)} (pos ${a.position})`).join(' | ') || '(nenhum)');
console.log('equipamentos x etiquetas:', (ela || []).map((a) => `${nome(E, a.equipment_id)} <- ${nome(L, a.label_id)} (pos ${a.position})`).join(' | ') || '(nenhum)');
console.log('campos de cliente/fornecedor:', (fcfg || []).map((f) => `${f.entity_type}:${f.label} (${f.field_type}) vis=${f.is_visible} obrig=${f.is_required} portal=${f.is_visible_in_portal}`).join(' | ') || '(nenhum)');
console.log('campos de equipamento (novos):', (ecfg || []).filter((f) => /^custom_/.test(f.field_key || '')).map((f) => `${f.label} (${f.field_type}) obrig=${f.is_required} portal=${f.is_visible_in_portal}`).join(' | ') || '(nenhum)');
console.log('custom_fields do Colégio:', JSON.stringify((cust || []).filter((c) => /Colégio/.test(c.name)).map((c) => c.custom_fields)));
console.log('origens:', (origins || []).map((o) => o.name).join(', '));
console.log('categorias:', (cats || []).map((o) => o.name).join(', '));
console.log('formulários:', (forms || []).map((o) => `${o.title} (${o.short_code})`).join(', '));
console.log('equipamentos (novos):', (eq || []).filter((e) => /garantia|Sala dos professores|Recepção/i.test(e.name || '')).map((e) => `${e.name} id=${e.identifier || ''} custom=${JSON.stringify(e.custom_fields || {})}`).join(' | '));
