import json,sys
cad=json.load(open('/home/claude/domiflix/rec/t9/cadeia.json'))
def mk(name, steps, seed=None):
    json.dump({"seedExtra":seed or cad["inicio"],"steps":steps,"storage":{"dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5":"2031-01-01T00:00:00.000Z"}},open(f'/home/claude/domiflix/rec/t9/_ex2/{name}.json','w'),ensure_ascii=False,indent=1)
