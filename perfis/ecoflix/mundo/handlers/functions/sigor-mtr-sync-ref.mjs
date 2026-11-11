// Edge sigor-mtr-sync-ref (T18 cap03; supabase/functions/sigor-mtr-sync-ref), SIGOR simulado: "Testar acesso salvo" (action
// test-credential), "Sincronizar dados do SIGOR" (padrão: grava as seis listas oficiais em mtr_ref_*) e as classes permitidas para
// o resíduo escolhido (classes-for-residue). Nenhum acesso real ao órgão ambiental.
import { nowIso } from '../../../fakebase/core/util.mjs';
import { REF, classesDoResiduo } from '../../lib/mtr_sigor.mjs';

export default (body, { db, FunctionError }) => {
  const { companyId, sistema, action = 'sync', residueCode } = body || {};
  if (!companyId || !sistema) throw new FunctionError('companyId e sistema são obrigatórios.', 400, { success: false });
  const nome = db.first('mtr_sistemas', { sistema }) ? 'SIGOR' : 'sistema ambiental';

  if (action === 'test-credential') {
    const cred = db.first('mtr_credentials', (r) => r.company_id === companyId && r.sistema === sistema);
    if (!cred) throw new FunctionError(`Configure o acesso ao ${nome} antes de testar.`, 400, { success: false });
    const message = `Acesso ao ${nome} aceito. A emissão ainda depende de a unidade possuir perfil Gerador no portal.`;
    const validatedAt = nowIso();
    db.update('mtr_credentials', { id: cred.id }, { last_validated_at: validatedAt, last_validation_status: 'success', last_validation_message: message });
    return { success: true, action, validatedAt, validationScope: 'authentication', message };
  }

  if (action === 'classes-for-residue') {
    const cod = String(residueCode || '').trim();
    if (!cod) throw new FunctionError('Informe o resíduo para consultar as classes.', 400, { success: false });
    return { success: true, action, supported: true, source: 'provider', classes: classesDoResiduo(cod) };
  }

  if (action !== 'sync') throw new FunctionError('Ação de sincronização inválida.', 400, { success: false });
  const cred = db.first('mtr_credentials', (r) => r.company_id === companyId && r.sistema === sistema);
  if (!cred) throw new FunctionError(`Configure o acesso ao ${nome} antes de sincronizar.`, 400, { success: false });
  const counts = {};
  for (const [tabela, linhas] of Object.entries(REF)) {
    db.remove(tabela, (r) => r.sistema === sistema);
    for (const [codigo, descricao] of linhas) db.insert(tabela, { sistema, codigo, descricao });
    counts[tabela] = linhas.length;
  }
  return { success: true, sistema, counts };
};
