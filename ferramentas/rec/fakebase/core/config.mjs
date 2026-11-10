// Configuracao do mundo falso. Tudo pode ser trocado por variavel de ambiente.
import { stableId } from './util.mjs';
import { mundo } from './mundo.mjs';

// Identidade do mundo de uma série (FAKE_MUNDO/mundo.json, chave "config"); sem ela, o mundo da Dominex.
const M = mundo.config || {};

export const config = {
  host: process.env.FAKE_HOST || '127.0.0.1',
  port: Number(process.env.FAKE_PORT || 54321),
  // A unica empresa (tenant) do mundo falso e a usuaria logada.
  companyId: stableId(M.empresa || 'company.glacial'),
  userId: stableId(M.usuario || 'user.camila'),
  userEmail: process.env.FAKE_USER_EMAIL || M.email || 'camila.duarte@glacialcold.example',
  userName: M.nome || 'Camila Duarte',
  // Qualquer senha serve no login falso; esta e a "oficial" so para documentar.
  userPassword: process.env.FAKE_USER_PASSWORD || 'dominex123',
  jwtSecret: 'domiflix-fake-jwt-secret-nao-e-segredo',
  // Limite de linhas por requisicao (Supabase usa 1000 por padrao).
  maxRows: Number(process.env.FAKE_MAX_ROWS || 1000),
};

export const SERVER_ORIGIN = `http://${config.host}:${config.port}`;
