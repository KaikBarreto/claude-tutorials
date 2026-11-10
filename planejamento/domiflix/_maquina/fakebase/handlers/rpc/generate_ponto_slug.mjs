// RPC generate_ponto_slug(p_employee_id) → text · 20260916140000_guarda_posse_ponto_reassign_e_fecha_rpcs_mortas.sql:135-235 (T15, cap. 9)
// O slug do link pessoal do ponto: nome sem acento, minúsculo, hifenizado + "-" + 8 letras/números. Gerado UMA vez e permanente
// (chamar de novo devolve o mesmo). No banco real o código é aleatório; aqui sai de um hash do nome, para a gravação sempre
// escrever o mesmo endereço (o capítulo do celular abre o link pelo mesmo código).
import crypto from 'node:crypto';
import { RpcError } from '../../http/rest.mjs';

const ALFA = 'abcdefghjkmnpqrstuvwxyz23456789';

export function slugDoNome(nome) {
  const base = String(nome || 'funcionario').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  const h = crypto.createHash('sha1').update('t15-ponto:' + nome).digest();
  let cod = '';
  for (let i = 0; i < 8; i++) cod += ALFA[h[i] % ALFA.length];
  return `${base}-${cod}`;
}

export default async function generatePontoSlug(a, { db }) {
  const emp = db.first('employees', { id: a.p_employee_id });
  if (!emp) throw new RpcError('Funcionário não encontrado', '22023');
  if (emp.ponto_slug) return emp.ponto_slug;
  const slug = slugDoNome(emp.name);
  db.update('employees', { id: emp.id }, { ponto_slug: slug });
  return slug;
}
