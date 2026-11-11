// Trigger de mdfe_manifests (T17 cap04): o app grava `mdfe_number: 0` e "a trigger reserva o número de forma atômica e substitui
// estes placeholders" (NovoMdfeModal.tsx). O número é o maior entre o `last_mdfe_number` da configuração fiscal e os manifestos
// da série, mais 1 (a Recicla Vale começa no 1); a configuração passa a guardar o último usado. Também liga o manifesto à
// configuração fiscal padrão da empresa quando o app não manda.
export default {
  beforeInsert(row, { store, nowIso }) {
    const cfgs = store.rows('company_fiscal_config').filter((c) => c.company_id === row.company_id);
    const cfg = cfgs.find((c) => c.id === row.fiscal_config_id) || cfgs.find((c) => c.is_default) || cfgs[0] || null;
    if (cfg && !row.fiscal_config_id) row.fiscal_config_id = cfg.id;
    if (!Number(row.mdfe_number)) {
      const serie = Number(row.serie) || 1;
      const usados = store.rows('mdfe_manifests').filter((m) => m.company_id === row.company_id && (Number(m.serie) || 1) === serie).map((m) => Number(m.mdfe_number) || 0);
      row.mdfe_number = Math.max(Number(cfg?.last_mdfe_number) || 0, 0, ...usados) + 1;
      row.number_reserved_at = nowIso();
      if (cfg) {
        cfg.last_mdfe_number = row.mdfe_number;
        cfg.updated_at = nowIso();
        store.table('company_fiscal_config').touch();
      }
    }
  },
};
