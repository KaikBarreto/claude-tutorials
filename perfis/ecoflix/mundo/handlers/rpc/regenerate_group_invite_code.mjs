// RPC regenerate_group_invite_code (20260405225817): só a dona do grupo; código novo e validade de mais 30 dias a partir de agora.
import { exigeDono } from '../../lib/grupo.mjs';
import { agoraMs } from '../../lib/eco.mjs';
import gerar from './generate_group_invite_code.mjs';
export default (a, ctx) => {
  const g = exigeDono(ctx, a._group_id);
  g.invite_code = gerar({}, ctx);
  g.invite_code_expires_at = new Date(agoraMs() + 30 * 86400000).toISOString();
  ctx.store.table('company_groups').touch();
  return g.invite_code;
};
