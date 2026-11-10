#!/usr/bin/env bash
# Roda o teste de APP_ORIGIN duas vezes (ligada e desligada) numa trava só. Saída em rec/t12/_teste_origem.log
set -u
export TUT_HOME=/home/claude/domiflix
cd "$TUT_HOME"
export FAKE_URL=http://127.0.0.1:54327 FAKE_NOW=2026-11-10T10:00:00-03:00
{
  echo "=== COM APP_ORIGIN=https://www.dominex.app  ($(date +%H:%M:%S))"
  APP_ORIGIN=https://www.dominex.app node rec/t12/app_origin_teste.mjs / /clientes /equipamentos 2>&1
  echo
  echo "=== SEM APP_ORIGIN (linha de base)  ($(date +%H:%M:%S))"
  node rec/t12/app_origin_teste.mjs / /clientes /equipamentos 2>&1
  echo "=== fim ($(date +%H:%M:%S))"
} > rec/t12/_teste_origem.log
