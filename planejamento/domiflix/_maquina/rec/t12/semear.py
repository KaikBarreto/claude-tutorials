#!/usr/bin/env python3
"""T12 · monta as sementes do mundo do Portal do Cliente e do Portal do Contrato.

Gera rec/fakebase/seeds-extra/t12/{inicio,apos-cap03,apos-cap07,apos-cap08,apos-cap11}.json e rec/t12/cadeia.json.

O T10 e o T11 ainda não foram gravados: `inicio` reconstrói o FIM DO T11 (o estado inicial do T12, ver T12/roteiro.md) em cima da
cadeia do T5 (t3/apos-cap10, t1/apos-cap13, t4/inicio, t4/apos-cap14, t5/inicio, t5/apos-cap05):
  - OS #16 (Colégio, T5) vira Concluída (T7); OS #17 = a OS do orçamento #9 da Pousada Brisa do Mar (T9), agendada, R$ 1.000,00;
  - RT Ricardo Tavares Albuquerque; contrato comum do Colégio (OS #18 a #21, a cada 3 meses desde 15/12/2026, Hi-Wall da sala dos
    professores); contrato PMOC do Hotel Mirante do Mar (OS #22 a #33, mensal desde 01/12/2026, três ambientes, quatro máquinas),
    "Portal Público" ligado, portal_sections {} (as oito seções "Sem senha"), documentos versão 1 + TRT individual NÃO liberados.
  - Valores explícitos no contrato (portal_is_public true, portal_sections {}, token de 32 hex e código curto): ninguém criou o
    hooks/contracts.mjs ainda; quando o T11 criar, estas linhas continuam valendo.
As sementes de capítulo são CUMULATIVAS sobre `inicio` (cada apos-capNN traz tudo o que mudou desde o início):
  apos-cap03  chamado do hotel (OS #34, Pendente, origem portal, Cassete do restaurante)
  apos-cap07  + "Cobranças" Oculto no Portal do Contrato do hotel
  apos-cap08  + documentos do PMOC liberados no portal
  apos-cap11  = apos-cap08 (o capítulo 11 só revê); é o estado de partida do T13.
Uso: python3 rec/t12/semear.py   (de qualquer pasta; TUT_HOME opcional)"""
import json
import os

HOME = os.environ.get("TUT_HOME") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SAIDA = os.path.join(HOME, "rec", "fakebase", "seeds-extra", "t12")
CADEIA = os.path.join(HOME, "rec", "t12", "cadeia.json")

EMP = "9c307966-79f1-567c-ac4d-d5fd3c1a2f40"          # Glacial Cold Brasil
CAMILA = "d40f5787-1779-501f-900c-ddb2b90a36e5"
RAFAEL = "34c36c63-0890-5e89-8963-7c77b7996908"
BRUNO = "9b6bb38f-1ec8-5efc-86d8-4cc1a41af29d"
HOTEL = "cbed8554-3919-5fa8-b9c6-5d13ef24cf37"        # Hotel Mirante do Mar (base)
COLEGIO = "63ecba84-bfb8-4646-85d1-73774a3f4be1"      # Colégio Monte Verde (T3)
POUSADA = "325e6e13-2fcd-5a02-85d4-ebf56f8764d2"      # Pousada Brisa do Mar (base)
EQ_POUSADA = "f8f3b47b-825c-55f4-b385-f3d3ea7d5cb0"   # Hi-Wall 9.000 BTUs - Suíte 1
HIWALL = "d0f4c4b5-7a28-40ff-895f-6bdf7252c748"       # Hi-Wall 18.000 BTUs - Sala dos professores (T3)
LOBBY = "702fe3a4-c022-541e-a2d1-7a1706e3d55b"        # Cassete 36.000 BTUs - Lobby
REST = "9539608c-f4be-5fb9-a443-e350e659b4cc"         # Cassete 36.000 BTUs - Restaurante do hotel
RECEP = "08a6906e-93b7-5633-ae39-e45b753e9672"        # Hi-Wall 12.000 BTUs - Recepção
SALAO = "685a9331-e393-5e5a-ae40-f1f35eccf696"        # Piso-Teto 48.000 BTUs - Salão de eventos
ST_MP = "49db63cb-1737-415d-b795-187297148790"        # Manutenção Preventiva
ST_HIG = "10113e22-97c6-46e6-bcc5-f411f62f6935"       # Higienização de Split
FT_MP = "d5a900b6-960f-438e-973c-9844ececa223"        # Manutenção preventiva de split
OS16 = "2c9dc476-c5ca-412f-90fe-6c38a67f125e"

# relógio do mundo (FAKE_NOW = 2026-11-10T10:00:00-03:00 = 13:00Z); o fim do T11 aconteceu nesta mesma manhã
T = lambda hhmmss: f"2026-11-10T{hhmmss}.000Z"
NOW = T("13:00:00")

TOKEN_HOTEL = "3f9a1c7e5b2d4a60c8e1f7b94d2a6c05"      # token de 32 hex FICTÍCIO do QR impresso do hotel
CODIGO_HOTEL = "k7m2q9x4wb3d"                         # código curto (base32 sem ambíguos, 12) do link amigável do hotel
TOKEN_COLEGIO = "a64e0b19d7c3258f1be6094a7d3c5e82"
CODIGO_COLEGIO = "p4n8vh6ctz2e"

COMENTARIO = ("T12 · fim do T11 reconstruído (T10/T11 ainda sem gravação) · cadeia: t3/apos-cap10, t1/apos-cap13, t4/inicio, "
              "t4/apos-cap14, t5/inicio, t5/apos-cap05, t12/inicio")


def soma_meses(ano, mes, n):
    t = ano * 12 + (mes - 1) + n
    return t // 12, t % 12 + 1


def datas(ano, mes, dia, passo_meses, qtd):
    out = []
    for i in range(qtd):
        a, m = soma_meses(ano, mes, i * passo_meses)
        out.append(f"{a:04d}-{m:02d}-{dia:02d}")
    return out


def visita(n_os, contrato, cliente, equipamento, descricao, data, criada, tecnico):
    return {
        "id": f"@id:t12.os.{n_os}", "order_number": n_os, "company_id": EMP, "entry_type": "os", "origin": "contract",
        "status": "agendada", "os_type": "manutencao_preventiva", "customer_id": cliente, "equipment_id": equipamento,
        "contract_id": contrato, "service_type_id": ST_MP, "form_template_id": FT_MP, "technician_id": tecnico,
        "created_by": CAMILA, "description": descricao, "scheduled_date": data, "scheduled_time": "08:00:00",
        "require_tech_signature": True, "generate_nps_survey": True, "duration_minutes": 120,
        "created_at": criada, "updated_at": criada,
    }


# Tabelas que as telas deste tutorial (Dashboard, Ordens de Serviço, Clientes, Contratos, portais) consultam e que ficam VAZIAS de propósito
# (nada do T12 depende delas: o Financeiro e o Estoque só entram nas aulas T8/T9/T13). Lista vazia marca a tabela como "com seed" e
# mantém o /__dev/unknowns limpo; o que aparecer nele a mais é falha de verdade (RPC, função ou tabela que a tela precisa).
VAZIAS = ["tenant_tasks", "financial_transactions", "leads", "crm_stages", "crm_pipelines", "pricing_settings", "pmoc_activity_catalog",
          "cost_centers", "financial_accounts", "financial_categories", "tenant_charges", "os_sla_config", "os_required_fields", "os_photos",
          "inventory", "inventory_stock_levels", "stocks", "service_order_materials", "contract_health_status", "tenant_subscriptions",
          "contract_plan_activities", "service_order_activities", "contract_attachments", "pmoc_contract_documents_custom",
          "company_pmoc_document_templates"]


def monta_inicio():
    s = {"_comentario": COMENTARIO}
    for nome in VAZIAS:
        s[nome] = []

    # --- G1 (1.38.19): trilha Domiflix sem tela escura de introdução nem faixa de lembrete. A linha já existe na base
    # (seeds/gen-03-domiflix.json, is_onboarding true): semente com o mesmo id DUPLICA, então vai por _patch.
    patch_trilha = [{"match": {"id": "c0000000-0000-4000-8000-000000000001"}, "set": {"is_onboarding": False}}]

    # --- T7: OS #16 do Colégio concluída esta manhã (antes do relógio de 10:00)
    patch_os = [{"match": {"id": OS16}, "set": {
        "status": "concluida", "check_in_by": RAFAEL, "check_in_time": T("12:02:00"), "check_out_by": RAFAEL,
        "check_out_time": T("12:48:00"), "started_at": T("12:02:00"), "completed_at": T("12:49:00"), "updated_at": T("12:49:00"),
        "diagnosis": "Filtros sujos e dreno com pouca vazão.", "solution": "Limpeza dos filtros e do dreno; equipamento testado."}}]

    # --- T9: OS #17 = orçamento #9 da Pousada Brisa do Mar convertido (agendada, R$ 1.000,00)
    os17 = {
        "id": "@id:t12.os.17", "order_number": 17, "company_id": EMP, "entry_type": "os", "origin": "manual", "status": "agendada",
        "os_type": "manutencao_preventiva", "customer_id": POUSADA, "equipment_id": EQ_POUSADA, "service_type_id": ST_HIG,
        "technician_id": "10b0daa2-5924-5a9c-9510-93101d7b1a07", "created_by": CAMILA,
        "description": "Higienização dos splits da pousada e carga de gás", "scheduled_date": "2026-11-17", "scheduled_time": "09:00:00",
        "duration_minutes": 240, "total_value": 1000.0, "labor_value": 890.0, "parts_value": 150.0,
        "generate_nps_survey": True, "created_at": T("11:00:00"), "updated_at": T("11:00:00"),
    }
    oss = [os17]

    # --- T11: responsável técnico
    s["responsible_technicians"] = [{
        "id": "@id:t12.rt.ricardo", "company_id": EMP, "full_name": "Ricardo Tavares Albuquerque", "cft_crea": "CREA-RJ 9000012345",
        "modality": "Engenheiro Mecânico", "registry_number": "ART 9000001234/2026", "email": "ricardo.tavares@glacialcold.example",
        "phone": "(21) 3000-1009", "is_active": True, "created_by": CAMILA, "created_at": T("11:30:00"), "updated_at": T("11:30:00")}]

    # --- T11: contrato comum do Colégio (4 OS, #18 a #21)
    colegio = {
        "id": "@id:t12.contrato.colegio", "company_id": EMP, "customer_id": COLEGIO, "name": "Manutenção preventiva trimestral - Colégio Monte Verde",
        "status": "active", "is_pmoc": False, "frequency_type": "months", "frequency_value": 3, "horizon_months": 12,
        "start_date": "2026-12-15", "next_pmoc_generation_date": None, "technician_id": RAFAEL, "service_type_id": ST_MP,
        "form_template_id": FT_MP, "portal_is_public": True, "portal_sections": {}, "portal_documents_released": False,
        "public_pmoc_token": TOKEN_COLEGIO, "public_short_code": CODIGO_COLEGIO, "created_by": CAMILA,
        "created_at": T("12:10:00"), "updated_at": T("12:10:00"),
    }
    # --- T11: contrato PMOC do Hotel Mirante do Mar (12 OS, #22 a #33)
    hotel = {
        "id": "@id:t12.contrato.hotel", "company_id": EMP, "customer_id": HOTEL, "name": "PMOC - Hotel Mirante do Mar",
        "status": "active", "is_pmoc": True, "frequency_type": "months", "frequency_value": 1, "horizon_months": 12,
        "start_date": "2026-12-01", "next_pmoc_generation_date": "2027-01-01", "responsible_technician_id": "@id:t12.rt.ricardo",
        "technician_id": RAFAEL, "service_type_id": ST_MP, "unidade_nome": "Hotel Mirante do Mar - São Francisco",
        "unidade_endereco": "Avenida Quintino Bocaiúva", "unidade_numero": "770", "unidade_bairro": "São Francisco",
        "unidade_cidade": "Niterói", "unidade_uf": "RJ", "unidade_cep": "24360-000",
        "pmoc_legal_compliance_text": "Conforme Lei Federal 13.589/2018", "portal_is_public": True, "portal_sections": {},
        "portal_documents_released": False, "public_pmoc_token": TOKEN_HOTEL, "public_short_code": CODIGO_HOTEL,
        "created_by": CAMILA, "created_at": T("12:30:00"), "updated_at": T("12:30:00"),
    }
    s["contracts"] = [colegio, hotel]

    # ambientes e itens
    amb = [("lobby", "Lobby e recepção", "Recepção de hotel", 180, 4, 40, 4), ("rest", "Restaurante", "Restaurante do hotel", 220, 10, 80, 3),
           ("salao", "Salão de eventos", "Salão de eventos", 300, 2, 150, 4)]
    s["contract_environments"] = [{
        "id": f"@id:t12.amb.{k}", "company_id": EMP, "contract_id": "@id:t12.contrato.hotel", "identificacao": nome, "tipo_atividade": tipo,
        "area_climatizada_m2": area, "ocupantes_fixos": fixos, "ocupantes_flutuantes": flut, "carga_termica_tr": tr, "sort_order": i,
        "created_at": T("12:30:00"), "updated_at": T("12:30:00")} for i, (k, nome, tipo, area, fixos, flut, tr) in enumerate(amb)]
    itens_h = [("lobby", LOBBY, "Cassete 36.000 BTUs - Lobby"), ("lobby", RECEP, "Hi-Wall 12.000 BTUs - Recepção"),
               ("rest", REST, "Cassete 36.000 BTUs - Restaurante do hotel"), ("salao", SALAO, "Piso-Teto 48.000 BTUs - Salão de eventos")]
    s["contract_items"] = [{
        "id": f"@id:t12.item.hotel.{i}", "contract_id": "@id:t12.contrato.hotel", "environment_id": f"@id:t12.amb.{a}", "equipment_id": e,
        "item_name": nome, "pmoc_scope": "full", "pmoc_start_visit": 1, "first_os_excluded_questions": [], "form_template_ids": [],
        "sort_order": i, "created_at": T("12:30:00")} for i, (a, e, nome) in enumerate(itens_h)]
    s["contract_items"].append({
        "id": "@id:t12.item.colegio.0", "contract_id": "@id:t12.contrato.colegio", "equipment_id": HIWALL, "form_template_id": FT_MP,
        "item_name": "Hi-Wall 18.000 BTUs - Sala dos professores", "pmoc_scope": "full", "pmoc_start_visit": 1,
        "first_os_excluded_questions": [], "form_template_ids": [], "sort_order": 0, "created_at": T("12:10:00")})

    # visitas: #18 a #21 (colégio, a cada 3 meses) e #22 a #33 (hotel, mensal); criadas em sequência, o número crescente
    assignees, soe, sst = [], [], []
    nome_c = colegio["name"]
    for i, d in enumerate(datas(2026, 12, 15, 3, 4)):
        n = 18 + i
        oss.append(visita(n, "@id:t12.contrato.colegio", COLEGIO, HIWALL, f"{nome_c} — Ocorrência {i + 1}", d, T(f"12:10:{10 + i:02d}"), RAFAEL))
        assignees.append({"id": f"@id:t12.assg.{n}.a", "service_order_id": f"@id:t12.os.{n}", "user_id": RAFAEL, "created_at": T("12:10:00")})
        soe.append({"id": f"@id:t12.soe.{n}", "service_order_id": f"@id:t12.os.{n}", "equipment_id": HIWALL, "form_template_id": FT_MP,
                    "created_at": T("12:10:00")})
    for i, d in enumerate(datas(2026, 12, 1, 1, 12)):
        n = 22 + i
        oss.append(visita(n, "@id:t12.contrato.hotel", HOTEL, None, f"{hotel['name']} — Visita {i + 1}", d, T(f"12:30:{10 + i:02d}"), RAFAEL))
        for k, u in enumerate((RAFAEL, BRUNO)):
            assignees.append({"id": f"@id:t12.assg.{n}.{k}", "service_order_id": f"@id:t12.os.{n}", "user_id": u, "created_at": T("12:30:00")})
    for o in oss:
        sst.append({"service_order_id": o["id"], "service_type_id": o["service_type_id"], "company_id": EMP, "position": 0,
                    "created_at": o["created_at"]})
    s["service_orders"] = oss
    s["service_order_assignees"] = assignees
    s["service_order_equipment"] = soe
    s["service_order_service_types"] = sst

    # documentos que nascem sozinhos (versão 1, assinados) + TRT individual (versão 2 do termo), nada liberado no portal
    def doc(chave, tipo, versao, valido_ate, notas):
        return {"id": f"@id:t12.doc.{chave}", "company_id": EMP, "contract_id": "@id:t12.contrato.hotel", "doc_type": tipo, "version": versao,
                "content_hash": f"t12-{chave}", "pdf_storage_path": f"{EMP}/{'hotel'}/{tipo}-v{versao}.pdf", "generated_at": T("12:35:00"),
                "generated_by": CAMILA, "notes": notas, "valid_until": valido_ate}
    s["pmoc_documents"] = [
        doc("dossie", "dossie_pmoc", 1, None, "signature:signed"),
        doc("cronograma", "cronograma_anual", 1, None, None),
        doc("termo1", "termo_rt", 1, "2027-11-10", "signature:signed"),
        doc("certificado", "certificado", 1, "2027-11-10", "signature:signed"),
        {**doc("termo2", "termo_rt", 2, "2027-11-10", "signature:signed"), "generated_at": T("12:50:00")},
    ]
    s["_patch"] = {"service_orders": patch_os, "domiflix_learning_paths": patch_trilha}
    return s


def chamado_hotel():
    """OS #34 aberta pelo cliente no capítulo 3 (o handler create_customer_portal_ticket cria a mesma linha)."""
    return {"id": "@id:t12.os.34", "order_number": 34, "company_id": EMP, "entry_type": "os", "origin": "portal", "status": "pendente",
            "os_type": "manutencao_corretiva", "customer_id": HOTEL, "equipment_id": REST,
            "description": "O ar do restaurante está pingando água perto da janela.", "created_at": NOW, "updated_at": NOW}


def acumula(base, extra):
    out = json.loads(json.dumps(base))
    for k, v in extra.items():
        if k == "_patch":
            for t, itens in v.items():
                out.setdefault("_patch", {}).setdefault(t, []).extend(itens)
        else:
            out.setdefault(k, []).extend(v)
    return out


def grava(nome, dados):
    os.makedirs(SAIDA, exist_ok=True)
    tmp = os.path.join(SAIDA, f".{nome}.json.tmp")
    with open(tmp, "w", encoding="utf8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(SAIDA, f"{nome}.json"))


def main():
    grava("inicio", monta_inicio())
    c03 = {"_comentario": "T12 · apos-cap03: chamado do hotel (OS #34)", "service_orders": [chamado_hotel()]}
    c07 = acumula(c03, {"_patch": {"contracts": [{"match": {"id": "@id:t12.contrato.hotel"},
                                                   "set": {"portal_sections": {"cobrancas": "hidden"}, "updated_at": NOW}}]}})
    c07["_comentario"] = "T12 · apos-cap07: + Cobranças Oculto no Portal do Contrato do hotel"
    c08 = acumula(c07, {"_patch": {"contracts": [{"match": {"id": "@id:t12.contrato.hotel"},
                                                   "set": {"portal_documents_released": True, "updated_at": NOW}}]}})
    c08["_comentario"] = "T12 · apos-cap08: + documentos do PMOC liberados no portal (= estado final, partida do T13)"
    grava("apos-cap03", c03)
    grava("apos-cap07", c07)
    grava("apos-cap08", c08)
    c11 = json.loads(json.dumps(c08))
    c11["_comentario"] = "T12 · apos-cap11: igual ao apos-cap08 (o capítulo 11 só revê); partida do T13"
    grava("apos-cap11", c11)
    base = ["t3/apos-cap10", "t1/apos-cap13", "t4/inicio", "t4/apos-cap14", "t5/inicio", "t5/apos-cap05"]
    with open(CADEIA + ".tmp", "w", encoding="utf8") as f:
        json.dump({"base": base, "inicio": base + ["t12/inicio"],
                   "apos": {"3": "t12/apos-cap03", "7": "t12/apos-cap07", "8": "t12/apos-cap08", "11": "t12/apos-cap11"},
                   "hotel": {"portal_token": "562a7dbb648d5653872808a111187f64", "cliente": HOTEL, "codigo_contrato": CODIGO_HOTEL,
                             "token_contrato": TOKEN_HOTEL},
                   "colegio": {"portal_token": "b1942560a8109dd96fb42b9f2f5b2cb6", "cliente": COLEGIO, "hiwall": HIWALL,
                               "codigo_contrato": CODIGO_COLEGIO}}, f, ensure_ascii=False, indent=1)
    os.replace(CADEIA + ".tmp", CADEIA)
    print("ok:", ", ".join(sorted(x for x in os.listdir(SAIDA) if x.endswith(".json"))))


if __name__ == "__main__":
    main()
