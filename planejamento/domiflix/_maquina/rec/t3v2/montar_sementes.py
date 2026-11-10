#!/usr/bin/env python3
"""T3 v2 (Dominex 1.38.9): monta as sementes encadeadas rec/fakebase/seeds-extra/t3v2/apos-capNN.json.

Cada semente = o estado do T3 original no capítulo equivalente (seeds-extra/t3/apos-capNN.json, gravado na 1.37/1.38.6)
+ o que a v2 acrescenta (etiquetas, vínculos, campo personalizado). A numeração é a da v2 (cap06 Etiquetas e cap07 Campos
personalizados são novos; Formulário de captação passa de 6 para 8, Fornecedores de 7 para 9, e assim por diante).

  v2        parte do T3     acrescenta
  apos-02   apos-02
  apos-03   apos-03
  apos-04   apos-04
  apos-05   apos-05         etiqueta Preferencial (clientes e fornecedores, laranja), sem vínculo  [seed sem câmera]
  apos-06   apos-05         + etiqueta Contrato PMOC (azul); Colégio Monte Verde: Contrato PMOC (posição 0) e Preferencial
  apos-07   apos-05         + campo de cliente Horário de acesso; valor "Depois das 17h ou aos sábados" no colégio
  apos-08   apos-06         (formulário de captação e Luana) + tudo acima
  apos-09   apos-07         (fornecedor Ventura Gás e Tubos) + tudo acima + Ventura: Preferencial
  apos-10   apos-08         (Tensão e categoria Multi Split) + tudo acima + etiqueta de equipamento Em garantia
  apos-11   apos-09         (Hi-Wall e Cassete) + tudo acima + Hi-Wall: Em garantia
  apos-12   apos-10         (anexo e tarefa) + tudo acima
Uso: python3 rec/t3v2/montar_sementes.py   (a partir de $TUT_HOME)"""
import copy
import json
import os
import sys

HOME = os.environ.get("TUT_HOME") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
T3 = os.path.join(HOME, "rec", "fakebase", "seeds-extra", "t3")
SAIDA = os.path.join(HOME, "rec", "fakebase", "seeds-extra", "t3v2")

EMPRESA = "9c307966-79f1-567c-ac4d-d5fd3c1a2f40"        # Glacial Cold Brasil (stableId('company.glacial'))
COLEGIO = "63ecba84-bfb8-4646-85d1-73774a3f4be1"        # Colégio Monte Verde (criado no cap02 do T3)
VENTURA = "ccba3e9f-e533-4b73-9809-71eaa3499d0d"        # Ventura Gás e Tubos (cap07 do T3)
HIWALL = "d0f4c4b5-7a28-40ff-895f-6bdf7252c748"         # Hi-Wall 18.000 BTUs - Sala dos professores (cap09 do T3)
ID_PREF, ID_PMOC, ID_GARANTIA = "@id:t3v2.etiqueta.preferencial", "@id:t3v2.etiqueta.contrato-pmoc", "@id:t3v2.etiqueta.em-garantia"
CHAVE_CAMPO = "custom_1793719200000"                    # chave do campo Horário de acesso (custom_<ms>, como o app gera)
VALOR_CAMPO = "Depois das 17h ou aos sábados"


def etiqueta(id_, nome, cor, escopo, criada):
    return {"id": id_, "company_id": EMPRESA, "name": nome, "color": cor, "is_active": True, "scope": escopo,
            "show_in_portal": False, "created_at": criada, "updated_at": criada}


def vinculo(tabela_fk, cadastro, etiqueta_id, pos, criada):
    return {"company_id": EMPRESA, tabela_fk: cadastro, "label_id": etiqueta_id, "position": pos, "created_by": None,
            "created_at": criada}


def somar(estado, tabela, linha):
    estado.setdefault(tabela, []).append(linha)


def achar(estado, tabela, id_):
    for r in estado.get(tabela, []):
        if r.get("id") == id_:
            return r
    raise SystemExit(f"semente: linha {id_} não achada em {tabela}")


def acrescenta(estado, ate):
    """`ate` = 5 (só Preferencial) ... 12 (tudo): aplica no estado o que a v2 acrescenta até aquele capítulo."""
    if ate >= 5:
        somar(estado, "party_labels", etiqueta(ID_PREF, "Preferencial", "#F97316", "party", "@now-30d"))
    if ate >= 6:
        somar(estado, "party_labels", etiqueta(ID_PMOC, "Contrato PMOC", "#3B82F6", "party", "@now-0m"))
        somar(estado, "customer_label_assignments", vinculo("customer_id", COLEGIO, ID_PMOC, 0, "@now-0m"))
        somar(estado, "customer_label_assignments", vinculo("customer_id", COLEGIO, ID_PREF, 1, "@now-0m"))
        achar(estado, "customers", COLEGIO)["label_id"] = ID_PMOC
    if ate >= 7:
        somar(estado, "party_field_config", {"id": "@id:t3v2.campo.horario-acesso", "company_id": EMPRESA, "entity_type": "customer",
                                             "field_key": CHAVE_CAMPO, "label": "Horário de acesso", "field_type": "text", "options": None,
                                             "is_required": False, "is_visible": True, "is_visible_in_portal": False, "position": 0,
                                             "created_at": "@now-0m", "updated_at": "@now-0m"})
        achar(estado, "customers", COLEGIO)["custom_fields"] = {CHAVE_CAMPO: VALOR_CAMPO}
    if ate >= 9:
        somar(estado, "supplier_label_assignments", vinculo("supplier_id", VENTURA, ID_PREF, 0, "@now-0m"))
        achar(estado, "suppliers", VENTURA)["label_id"] = ID_PREF
    if ate >= 10:
        somar(estado, "party_labels", etiqueta(ID_GARANTIA, "Em garantia", "#22C55E", "equipment", "@now-0m"))
    if ate >= 11:
        somar(estado, "equipment_label_assignments", vinculo("equipment_id", HIWALL, ID_GARANTIA, 0, "@now-0m"))


def grava(nome, estado):
    os.makedirs(SAIDA, exist_ok=True)
    # `_patch` por último: o carregador aplica as linhas novas antes (ordem das chaves)
    out = {k: v for k, v in estado.items() if k != "_patch"}
    if "_patch" in estado:
        out["_patch"] = estado["_patch"]
    p = os.path.join(SAIDA, f"{nome}.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{nome}: " + "  ".join(f"{t}:{len(v)}" if t != "_patch" else "_patch" for t, v in out.items()))


def main():
    # (nome da semente v2, semente do T3 de partida, "acrescenta até")
    plano = [("apos-cap02", "apos-cap02", 4), ("apos-cap03", "apos-cap03", 4), ("apos-cap04", "apos-cap04", 4),
             ("apos-cap05", "apos-cap05", 5), ("apos-cap06", "apos-cap05", 6), ("apos-cap07", "apos-cap05", 7),
             ("apos-cap08", "apos-cap06", 8), ("apos-cap09", "apos-cap07", 9), ("apos-cap10", "apos-cap08", 10),
             ("apos-cap11", "apos-cap09", 11), ("apos-cap12", "apos-cap10", 12)]
    for nome, base, ate in plano:
        estado = copy.deepcopy(json.load(open(os.path.join(T3, base + ".json"), encoding="utf-8")))
        acrescenta(estado, ate)
        grava(nome, estado)


if __name__ == "__main__":
    main()
