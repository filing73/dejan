# Generiše roster/index.html iz podataka ispod. Pokreni: python3 roster/build.py
import re
L='Lejla'
WEEKS=[
 ('31/08 – 06/09', ['2026-08-31','2026-09-01','2026-09-02','2026-09-03','2026-09-04','2026-09-05','2026-09-06'], [
  (L,      ['06:15-14:30','06:15-14:30','06:15-14:30','14:30-22:30','','','06:15-14:30']),
  ('Sanja',['','14:15-22:00|reception','08:00-14:00','15:30-22:00','09:30-12:30|mgmt meeting','14:30-22:15','']),
  ('Mia',  ['14:15-22:00','','14:15-22:15','06:15-14:30','06:15-14:30','14:15-22:15','']),
  ('Farooq',['22:00-06:30','22:00-06:30','','','14:15-22:15','06:15-14:30','14:15-22:15']),
  ('Alex', ['','','22:15-06:30','22:15-06:30','22:30-06:30','22:15-06:30','22:15-06:30']),
 ]),
 ('07/09 – 13/09', ['2026-09-07','2026-09-08','2026-09-09','2026-09-10','2026-09-11','2026-09-12','2026-09-13'], [
  (L,      ['','06:15-14:30','06:15-14:30','06:15-14:30','06:15-14:30','','14:15-22:15']),
  ('Sanja',['08:15-14:15','','14:15-22:15|reception','10:00-18:00','09:30-18:30|mgmt mtg & reception','08:15-14:15','09:30-15:30']),
  ('Mia',  ['14:15-22:15','14:15-22:00','','13:30-22:00','14:15-22:15','14:15-22:15','']),
  ('Farooq',['06:15-14:30','22:00-06:30','22:00-06:30','','','06:15-14:30','06:15-14:30']),
  ('Alex', ['22:15-06:30','','','22:15-06:30','22:30-06:30','22:15-06:30','22:15-06:30']),
 ]),
 ('14/09 – 20/09', ['2026-09-14','2026-09-15','2026-09-16','2026-09-17','2026-09-18','2026-09-19','2026-09-20'], [
  (L,      ['06:15-14:30','14:15-22:15|ISPRAVKA: štampano 06:30','06:15-14:30','','14:15-22:15','06:15-14:30','14:15-22:15']),
  ('Sanja',['','08:15-12:15|reception support','14:15-22:15|reception','14:30-22:15','09:00-13:00|mgmt mtg & reception','','06:30-14:15|reception']),
  ('Mia',  ['14:15-22:15','06:30-14:30','','07:00-15:00','06:15-14:30','14:15-22:15','']),
  ('Night shift',['','22:15-06:30','22:15-07:00','','','','']),
  ('Alex', ['22:15-06:30','','','22:15-06:30','22:30-06:30','22:15-06:30','22:15-06:30']),
 ]),
]
# pančovano (stvarno vreme sa kartice) po datumu: 'YYYY-MM-DD': 'HH:MM-HH:MM'
PUNCH={}

DN=['Pon','Uto','Sre','Čet','Pet','Sub','Ned']
COL={'Sanja':'c1','Mia':'c2','Farooq':'c3','Night shift':'c3','Alex':'c4'}
def mins(s):
    a,b=s.split('-'); h1,m1=map(int,a.split(':')); h2,m2=map(int,b.split(':'))
    d=(h2*60+m2)-(h1*60+m1); return d+1440 if d<0 else d
def fmt(m): return f'{m//60}:{m%60:02d}'
def dm(iso): y,mo,d=iso.split('-'); return f'{int(d):02d}/{mo}'

rows=[]; sep_total=0; sep_days=0; aug=0; punch_total=0; punch_n=0
for title,dates,people in WEEKS:
    th=''.join(f'<th data-d="{d}">{DN[i]}<small>{dm(d)}</small></th>' for i,d in enumerate(dates))
    body=''
    for name,shifts in people:
        tot=0; cells=''
        for d,s in zip(dates,shifts):
            if not s: cells+='<td class="off">slobodno</td>'; continue
            t,_,note=s.partition('|'); m=mins(t); tot+=m
            fix='<span class="fix">ISPRAVKA</span>' if note.startswith('ISPRAVKA') else ''
            note=note.replace('ISPRAVKA: ','')
            cells+=f'<td class="shift">{t.replace("-"," – ")}{fix}{"<span class=note>"+note+"</span>" if note else ""}</td>'
            if name==L:
                if d.startswith('2026-09'): sep_total+=m; sep_days+=1
                else: aug+=m
        if name==L:
            body+=f'<tr class="lejla"><td class="name">{name}</td>{cells}<td class="hrs total">{fmt(tot)}</td></tr>'
            pc=''; pt=0
            for d,s in zip(dates,shifts):
                p=PUNCH.get(d)
                if p: m=mins(p); pt+=m; punch_total+=m; punch_n+=1; pc+=f'<td>{p.replace("-"," – ")}</td>'
                else: pc+='<td class="off">—</td>' if s else '<td class="off"></td>'
            body+=f'<tr class="punch"><td class="name">pančovano</td>{pc}<td class="hrs">{fmt(pt) if pt else "—"} / {fmt(tot)}</td></tr>'
        else:
            body+=f'<tr class="p {COL[name]}"><td class="name">{name}</td>{cells}<td class="hrs">{fmt(tot)}</td></tr>'
    rows.append(f'<h2>{title}</h2><div class="scroll"><table><thead><tr><th></th>{th}<th>Ukupno</th></tr></thead><tbody>{body}</tbody></table></div>')

lejla_next=[(d,s.split('|')[0]) for _,dates,people in WEEKS for d,s in zip(dates,people[0][1]) if s]
import json
html=open('/home/user/dejan/roster/template.html').read()
html=html.replace('{{TABLES}}','\n'.join(rows)).replace('{{SEP_H}}',fmt(sep_total)).replace('{{SEP_D}}',str(sep_days)).replace('{{AUG}}',fmt(aug)).replace('{{PUNCH}}',fmt(punch_total) if punch_n else '—').replace('{{NEXT}}',json.dumps(lejla_next))
open('/home/user/dejan/roster/index.html','w').write(html)
print('ok', fmt(sep_total), sep_days, fmt(aug))
