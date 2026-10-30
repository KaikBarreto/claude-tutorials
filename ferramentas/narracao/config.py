"""Configuração da narração de cada tutorial: <pasta do tutorial>/narracao/config_narracao.json (ao lado destes scripts).
{
  "idioma": "pt_BR",                       # num2words: como o ASR escreve números por extenso para casar com o texto
  "trocas": [["quê-érre côde", "QR Code"]], # grafia usada na fala (TTS) -> grafia da legenda (mesmo nº de palavras)
  "unidades": {"V": "volts"},              # sufixo que o ASR cola no número ("380V") -> palavra falada
  "numeros": [["dezoito mil btus", "18.000 BTUs"]],  # sequência falada (minúsculas, sem pontuação) -> legenda
  "asr_fix": {"<id do take>": {"1800": "18000"}}     # correção pontual do que o ASR ouviu num take
}
Sem o arquivo: português do Brasil, sem trocas nem correções."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PADRAO = {"idioma": "pt_BR", "trocas": [], "unidades": {}, "numeros": [], "asr_fix": {}}


def carregar():
    p = os.environ.get("NARRACAO_CONFIG") or os.path.join(HERE, "config_narracao.json")
    cfg = dict(PADRAO)
    if os.path.exists(p):
        cfg.update(json.load(open(p, encoding="utf-8")))
    cfg["trocas"] = [tuple(x) for x in cfg["trocas"]]
    cfg["numeros"] = [tuple(x) for x in cfg["numeros"]]
    return cfg


CFG = carregar()
