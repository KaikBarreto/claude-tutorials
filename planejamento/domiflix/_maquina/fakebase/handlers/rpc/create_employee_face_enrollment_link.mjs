// RPC create_employee_face_enrollment_link(p_employee_id) → jsonb { token, expires_at } · hooks/useFaceBiometrics.ts:40 (T15, cap. 9)
// O token (64 caracteres hexadecimais) vai no link de ativação /ativar-ponto/<token> (vale 24 h). No banco real é aleatório; aqui sai de um
// hash do NOME do funcionário (`tokenDoNome`), de modo que o capítulo do celular abre o mesmo link que o capítulo do computador copiou, sem
// precisar guardar o token entre as gravações. A edge `face-enrollment` (ação `context`) reconhece o funcionário pelo mesmo hash.
import crypto from 'node:crypto';
import { RpcError } from '../../http/rest.mjs';
import { now } from '../../core/util.mjs';

export const tokenDoNome = (nome) => crypto.createHash('sha256').update('t15-ativacao:' + nome).digest('hex');

export default async function createEmployeeFaceEnrollmentLink(a, { db }) {
  const emp = db.first('employees', { id: a.p_employee_id });
  if (!emp) throw new RpcError('Funcionário não encontrado', '22023');
  if (emp.ponto_enabled !== true) throw new RpcError('Ponto eletrônico não está ativo para este funcionário', '22023');
  return { token: tokenDoNome(emp.name), expires_at: new Date(now().getTime() + 24 * 3600 * 1000).toISOString() };
}
