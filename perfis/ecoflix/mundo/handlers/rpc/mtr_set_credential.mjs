// mtr_set_credential (useMtr.tsx: "Salvar acesso" do Configuração do MTR, T18 cap03): grava o acesso da empresa ao órgão ambiental
// (um por empresa e sistema). A senha vai para o cofre no banco de verdade; aqui nada dela é guardado (só um id de cofre fictício),
// e o teste anterior é zerado: o quadro volta a "Acesso salvo, teste pendente" até o "Testar acesso salvo".
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (a, { db, companyId, RpcError }) => {
  const cid = a.p_company_id || companyId;
  const cpf = String(a.p_cpf || '').replace(/\D/g, '');
  if (!a.p_sistema) throw new RpcError('Sistema ambiental não informado');
  if (!cpf) throw new RpcError('Informe o CPF da pessoa usuária');
  const campos = {
    usuario_cpf: cpf, cod_unidade_gerador: a.p_cod_unidade == null ? null : Number(a.p_cod_unidade), ambiente: a.p_ambiente || 'producao',
    cnpj_unidade: a.p_cnpj_unidade || null, senha_secret_id: `cofre-fictício-${cid}`, last_validated_at: null, last_validation_status: null,
    last_validation_message: null, updated_at: nowIso(),
  };
  const atual = db.first('mtr_credentials', (r) => r.company_id === cid && r.sistema === a.p_sistema);
  if (atual) {
    db.update('mtr_credentials', { id: atual.id }, campos);
    return atual.id;
  }
  return db.insert('mtr_credentials', { company_id: cid, sistema: a.p_sistema, created_at: nowIso(), ...campos }).id;
};
