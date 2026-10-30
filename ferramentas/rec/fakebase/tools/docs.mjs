// Documentos sinteticos com digito verificador CORRETO (o app valida CPF/CNPJ no cliente e nas edges).
//
// CNPJ: base de 8 digitos iniciada em 9 (faixa que a Receita ainda nao emitiu) + filial 0001 -> passa no
//       algoritmo e, na pratica, nao pertence a nenhuma empresa real.
// CPF:  nao existe faixa reservada; usamos os CPFs "de exemplo" publicos (111.444.777-35, 529.982.247-25)
//       e, para o resto, numeros gerados pelo algoritmo (podem coincidir com pessoa real por acaso).
export const digits = (s) => String(s).replace(/\D/g, '');

function cpfDigit(nums) {
  let sum = 0;
  for (let i = 0; i < nums.length; i++) sum += nums[i] * (nums.length + 1 - i);
  const d = 11 - (sum % 11);
  return d > 9 ? 0 : d;
}

export function cpf(base9) {
  const nums = digits(base9).padStart(9, '0').slice(0, 9).split('').map(Number);
  const d1 = cpfDigit(nums);
  const d2 = cpfDigit([...nums, d1]);
  return `${nums.slice(0, 3).join('')}.${nums.slice(3, 6).join('')}.${nums.slice(6, 9).join('')}-${d1}${d2}`;
}

function cnpjDigit(nums, weights) {
  const sum = nums.reduce((a, n, i) => a + n * weights[i], 0);
  const m = sum % 11;
  return m < 2 ? 0 : 11 - m;
}

export function cnpj(base8, branch = '0001') {
  const nums = (digits(base8).padStart(8, '0').slice(0, 8) + digits(branch).padStart(4, '0')).split('').map(Number);
  const d1 = cnpjDigit(nums, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
  const d2 = cnpjDigit([...nums, d1], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
  const s = nums.join('') + d1 + d2;
  return `${s.slice(0, 2)}.${s.slice(2, 5)}.${s.slice(5, 8)}/${s.slice(8, 12)}-${s.slice(12)}`;
}

// Copia fiel de app/src/lib/documentValidation.ts para checar o que geramos.
export function validateCPF(value) {
  const c = digits(value);
  if (c.length !== 11 || /^(\d)\1{10}$/.test(c)) return false;
  let sum = 0;
  for (let i = 0; i < 9; i++) sum += parseInt(c[i], 10) * (10 - i);
  let d = 11 - (sum % 11);
  if (d > 9) d = 0;
  if (d !== parseInt(c[9], 10)) return false;
  sum = 0;
  for (let i = 0; i < 10; i++) sum += parseInt(c[i], 10) * (11 - i);
  d = 11 - (sum % 11);
  if (d > 9) d = 0;
  return d === parseInt(c[10], 10);
}

export function validateCNPJ(value) {
  const c = digits(value);
  if (c.length !== 14 || /^(\d)\1{13}$/.test(c)) return false;
  const nums = c.split('').map(Number);
  const d1 = cnpjDigit(nums.slice(0, 12), [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
  const d2 = cnpjDigit(nums.slice(0, 13), [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
  return d1 === nums[12] && d2 === nums[13];
}

if (process.argv[1] && process.argv[1].endsWith('docs.mjs')) {
  const arg = process.argv[2];
  if (!arg) console.log('uso: node docs.mjs <base 9 digitos p/ CPF | base 8 digitos p/ CNPJ>');
  else if (digits(arg).length <= 9) console.log(cpf(arg));
  else console.log(cnpj(arg));
}
