// Trigger trg_set_invite_code_expiry (20260405225817): grupo novo sem validade ganha a do código de convite = agora + 30 dias (T22: "Válido até
// 10/12/2026"); e created_at = agora (DEFAULT now()).
export default {
  beforeInsert(row, { nowIso }) {
    const agora = new Date(nowIso()).getTime();
    if (!row.created_at) row.created_at = new Date(agora).toISOString();
    if (!row.invite_code_expires_at) row.invite_code_expires_at = new Date(agora + 30 * 86400000).toISOString();
  },
};
