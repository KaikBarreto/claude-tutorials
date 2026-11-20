"""T02 · refaz "ilustracoes" e "repouso" de cada capítulo no caps/specs.json a partir de out/ilus/janelas.json (o resto do specs fica).
Caixa = a janela do palco para gravação 16:9 (1600x900 -> 1763x992 em (78, 44))."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(H, 'out/ilus/janelas.json')))
p = os.path.join(H, 'caps/specs.json'); S = json.load(open(p))
for k, v in S.items():
    if isinstance(v, dict): v.pop('ilustracoes', None); v.pop('repouso', None)
for i, w in sorted(J.items(), key=lambda x: (x[1]['cap'], x[1]['at'])):
    v = S[f"{w['cap']:02d}"]
    v.setdefault('ilustracoes', []).append({"at": w['at'], "dur": w['dur'], "src": os.path.join(H, 'out/ilus', i + '.mp4'), "box": [78, 44, 1763, 992],
                                            "scale_in": 0.0, "radius": 16, "shadow": False, "loop": False})
    v.setdefault('repouso', []).append([w['at'], round(w['at'] + w['dur'], 2)])
json.dump(S, open(p, 'w'), ensure_ascii=False, indent=1)
print({k: len(v.get('ilustracoes', [])) for k, v in S.items() if isinstance(v, dict) and v.get('ilustracoes')})
