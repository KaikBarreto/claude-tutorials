// Edge time-photo-url (miniatura da selfie no Registro de Ponto, components/funcionarios/ponto/SelfieThumb.tsx; T19 cap10), como a
// função da 1.59.154 (supabase/functions/time-photo-url/index.ts): recebe { record_id } e devolve { signed_url } da foto no bucket
// time-photos (60 s). O endereço é o do próprio Supabase falso (o robô desvia o do build para a instância da aula).
export default (body, { store, req, FunctionError }) => {
  const id = body?.record_id;
  if (!id) throw new FunctionError('record_id é obrigatório', 400);
  const r = store.rows('time_records').find((x) => x.id === id);
  if (!r) throw new FunctionError('Registro não encontrado', 404);
  if (!r.photo_path) throw new FunctionError('Registro sem foto', 404);
  const host = req?.headers?.host || `127.0.0.1:${process.env.FAKE_PORT || 54321}`;
  return { signed_url: `http://${host}/storage/v1/object/sign/time-photos/${r.photo_path.split('/').map(encodeURIComponent).join('/')}?token=t19` };
};
