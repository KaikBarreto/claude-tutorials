#!/usr/bin/env python3
"""T11 · monta a semente de partida do T11 (Contratos e PMOC), no fim do T10.

Gera rec/fakebase/seeds-extra/t11/inicio.json e rec/t11/cadeia.json. As sementes de capítulo (apos-capNN) NÃO nascem aqui: saem do estado
real do falso depois de cada capítulo (`rec/t11/rodar.sh NN --seed` -> snap.mjs).

Cadeia (a mesma do T10 + o fim do T10; a base do T12 não trazia a Tatiane nem os orçamentos do T9):
  t2/apos-cap10 (Tatiane Ribeiro, cargos e permissões), t3/apos-cap10, t1/apos-cap13, t4/inicio, t4/apos-cap14, t5/inicio, t9/inicio, t9/apos-cap16
  (financeiro padrão, orçamentos, OS #17 do orçamento #9 da Pousada Brisa do Mar, agendada, R$ 1.000,00), t10/apos-cap09 (CRM e Projetos: o PMOC do hotel
  em Negociação) e `t11/inicio`.
`t11/inicio` acrescenta só o que é desta aula:
  - G1 (1.38.19): trilha Domiflix com `is_onboarding: false` por `_patch` (a linha já existe na base; semente com o mesmo id duplicaria; o `t10/inicio` já faz o
    mesmo, o patch repetido é inofensivo);
  - o catálogo global da norma PMOC (`pmoc_activity_catalog`, 151 atividades, reconstruído das migrações do app: catalogo.py);
  - tabelas que as telas deste tutorial consultam e ficam vazias de propósito (nenhum contrato, nenhum RT, nenhum documento): `/__dev/unknowns` limpo.
O T10 (CRM) não muda nada que o T11 mostre (a oportunidade do hotel segue em Negociação e a aula não mexe no CRM)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from catalogo import monta as monta_catalogo  # noqa: E402

HOME = os.environ.get("TUT_HOME") or os.path.abspath(os.path.join(HERE, "..", ".."))
SEEDS = os.path.join(HOME, "rec", "fakebase", "seeds-extra")
SAIDA = os.path.join(SEEDS, "t11")
CADEIA = os.path.join(HERE, "cadeia.json")

EMP = "9c307966-79f1-567c-ac4d-d5fd3c1a2f40"
CAMILA = "d40f5787-1779-501f-900c-ddb2b90a36e5"
RAFAEL = "34c36c63-0890-5e89-8963-7c77b7996908"
BRUNO = "9b6bb38f-1ec8-5efc-86d8-4cc1a41af29d"
HOTEL = "cbed8554-3919-5fa8-b9c6-5d13ef24cf37"
COLEGIO = "63ecba84-bfb8-4646-85d1-73774a3f4be1"
POUSADA = "325e6e13-2fcd-5a02-85d4-ebf56f8764d2"
EQ_POUSADA = "f8f3b47b-825c-55f4-b385-f3d3ea7d5cb0"
HIWALL = "d0f4c4b5-7a28-40ff-895f-6bdf7252c748"
ST_HIG = "10113e22-97c6-46e6-bcc5-f411f62f6935"
OS16 = "2c9dc476-c5ca-412f-90fe-6c38a67f125e"
T = lambda hhmmss: f"2026-11-10T{hhmmss}.000Z"

BASE = ["t2/apos-cap10", "t3/apos-cap10", "t1/apos-cap13", "t4/inicio", "t4/apos-cap14", "t5/inicio", "t9/inicio", "t9/apos-cap16", "t10/apos-cap09"]

# Tabelas que as telas do tutorial consultam e que começam VAZIAS (lista vazia = "tem semente": /__dev/unknowns não acusa)
VAZIAS = ["contracts", "contract_items", "contract_environments", "contract_plan_activities", "contract_attachments", "contract_health_status",
          "pmoc_contract_documents_custom", "company_pmoc_document_templates", "responsible_technicians", "pmoc_documents", "service_order_activities",
          # consultadas pelas telas do contrato (Financeiro do contrato e seletor de categoria) e vazias de propósito
          "tenant_subscriptions", "dre_groups", "contract_activity_execution"]


def monta_inicio():
    s = {"_comentario": "T11 · fim do T10 para a aula Contratos e PMOC · cadeia: " + ", ".join(BASE) + ", t11/inicio"}
    for nome in VAZIAS:
        s[nome] = []
    s["pmoc_activity_catalog"] = [
        {**{k: v for k, v in l.items()}, "created_at": "@now-200d", "updated_at": "@now-200d"} for l in monta_catalogo()[0]]
    s["_patch"] = {"domiflix_learning_paths": [{"match": {"id": "c0000000-0000-4000-8000-000000000001"}, "set": {"is_onboarding": False}}]}
    return s


def grava(nome, dados):
    os.makedirs(SAIDA, exist_ok=True)
    tmp = os.path.join(SAIDA, f".{nome}.json.tmp")
    with open(tmp, "w", encoding="utf8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(SAIDA, f"{nome}.json"))


def main():
    grava("inicio", monta_inicio())
    cad = {"fake_now": "2026-11-10T10:00:00-03:00", "base": BASE, "inicio": BASE + ["t11/inicio"],
           "ids": {"hotel": HOTEL, "colegio": COLEGIO, "hiwall": HIWALL}}
    with open(CADEIA + ".tmp", "w", encoding="utf8") as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    os.replace(CADEIA + ".tmp", CADEIA)
    print("ok: t11/inicio + cadeia.json")


if __name__ == "__main__":
    main()
