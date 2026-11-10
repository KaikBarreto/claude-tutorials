

CAPS = {str(n): globals()[f'cap{n:02d}'] for n in range(13) if f'cap{n:02d}' in globals()}
if 'cap09b' in globals():
    CAPS['9b'] = globals()['cap09b']

if __name__ == '__main__':
    quais = [a.lstrip('0') or '0' for a in sys.argv[1:]] or sorted(CAPS, key=lambda k: (int(k.rstrip('b')), k))
    for n in quais:
        c = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
        last = -1
        for stp in d['steps']:   # o `at` precisa ser crescente
            if 'at' in stp:
                if stp['at'] < last:
                    print(f'  aviso {c.nome}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(HERE, f'{c.nome}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'{c.nome}: {len(d["steps"])} passos, narração {c.dur:.1f} s -> {os.path.relpath(path, HERE)}')
