// RPC get_employee_face_template_status(p_employee_id) → jsonb · hooks/useFaceBiometrics.ts:25 (T15, cap. 9)
// Biometria facial do funcionário. A aula não faz o cadastro facial ("Continuar sem biometria"), então ninguém está cadastrado.
export default async function getEmployeeFaceTemplateStatus() {
  return { enrolled: false, template_count: 0, model_version: null, created_at: null };
}
