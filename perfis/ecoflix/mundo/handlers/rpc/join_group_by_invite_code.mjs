// RPC join_group_by_invite_code (20260405225817), chamada pela FILIAL (Configurações > Empresa > Filial > Vincular): a empresa do usuário entra
// no grupo do código (maiúsculas, sem espaços). Recusa empresa já vinculada a outro grupo, código inválido ou vencido, o próprio grupo e o
// limite de filiais; quem já foi membro (status removed) volta a ativo com a data de agora (é a "volta pelo código" da dica do cap09).
import { empresaDoUsuario } from '../../lib/grupo.mjs';
import { agoraMs } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError, db } = ctx;
  const cid = empresaDoUsuario(store, ctx.userId);
  if (!cid) throw new RpcError('Empresa não encontrada');
  const membros = store.rows('company_group_members');
  if (membros.some((m) => m.company_id === cid && m.status === 'active')) {
    throw new RpcError('Sua empresa já está vinculada a um grupo. Saia do grupo atual antes de entrar em outro.');
  }
  const codigo = String(a._invite_code || '').trim().toUpperCase();
  const g = store.rows('company_groups').find((x) => x.invite_code === codigo);
  if (!g) throw new RpcError('Código de convite inválido');
  const agora = agoraMs();
  if (g.invite_code_expires_at && new Date(g.invite_code_expires_at).getTime() < agora) {
    throw new RpcError('Código de convite expirado. Solicite um novo código ao administrador do grupo.');
  }
  if (g.owner_company_id === cid) throw new RpcError('Você não pode se juntar ao seu próprio grupo');
  const ativos = membros.filter((m) => m.group_id === g.id && m.status === 'active').length;
  if (ativos >= Number(g.max_members ?? 10)) throw new RpcError(`Este grupo atingiu o limite máximo de ${g.max_members} filiais.`);
  const antigo = membros.find((m) => m.group_id === g.id && m.company_id === cid);
  const iso = new Date(agora).toISOString();
  if (antigo) {
    antigo.status = 'active';
    antigo.joined_at = iso;
    store.table('company_group_members').touch();
  } else {
    db.insert('company_group_members', { group_id: g.id, company_id: cid, joined_at: iso, status: 'active' });
  }
  return null;
};
