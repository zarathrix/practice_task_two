import sys, pandas as pd
d = pd.read_csv(sys.argv[1], encoding='utf-8-sig')
d = d.sort_values(['ProcessInstanceId', 'EventIndex'])
g = d.groupby('ProcessInstanceId')
routes = g.ActivityName.apply(' > '.join)
v = routes.value_counts().reset_index()
v.columns = ['Route', 'NumberOfCases']
v['Share'] = (v.NumberOfCases / len(routes)).round(4)
v.insert(0, 'Variant', [f'V{i+1}' for i in range(len(v))])
v.to_csv('variants.csv', index=False, encoding='utf-8')
d['next'] = g.ActivityName.shift(-1)
t = d.dropna(subset=['next'])[['ActivityName', 'next']].drop_duplicates()
t.columns = ['SourceActivity', 'TargetActivity']
t.to_csv('student_transitions.csv', index=False, encoding='utf-8')
print(d.dropna(subset=['next']).groupby(['ActivityName', 'next']).size())
print(d.groupby(['ActivityName', 'Result'], dropna=False).size())
a = g.Amount.first()
extra = g.ActivityName.apply(lambda s: 'Дополнительное согласование' in set(s))
done = g.ActivityName.last() == 'Заявка выполнена'
print('точность порога 150000:', ((a[done] >= 150000) == extra[done]).mean())
print('max без доп:', a[done & ~extra].max(), 'min с доп:', a[done & extra].min())
