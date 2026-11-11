// RPC generate_group_invite_code (20260308090641): 'GRP-' + 6 caracteres de um md5 em maiúsculas (só 0-9 e A-F), sem repetir código de outro
// grupo. No mundo da T22 o sorteio é fixo (GRP-7C4E9A, o "código de convite" do cap02), para a gravação sair sempre igual.
const CODIGOS = ['GRP-7C4E9A', 'GRP-3F81B2', 'GRP-A94D07', 'GRP-5E2C6B'];
export default (a, { store }) => CODIGOS.find((c) => !store.rows('company_groups').some((g) => g.invite_code === c)) || 'GRP-0D4A11';
