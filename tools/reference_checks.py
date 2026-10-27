#!/usr/bin/env python3
"""Independent checks of the shipped examples, using only Python's standard library.

This reads XLSX cached values and applies a separate reference model. It does not
recalculate Excel formulas, change a workbook or certify native Excel behavior.
Run: python reference_checks.py --workbook-dir /path/to/workbooks
"""
import argparse,json,math,re,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
R='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

def read_xlsx(path):
 sheets={};formula_count=0;errors=[]
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None,'ZIP checksum failure'
  shared=[]
  if 'xl/sharedStrings.xml' in z.namelist():shared=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  rel={e.get('Id'):e.get('Target') for e in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  for s in ET.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',NS):
   target=rel[s.get(R+'id')];target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
   cells={}
   for c in ET.fromstring(z.read(target)).findall('s:sheetData/s:row/s:c',NS):
    val=c.find('s:v',NS);v=val.text if val is not None else None;t=c.get('t')
    if t=='s' and v is not None:v=shared[int(v)]
    elif t=='inlineStr':v=''.join(c.find('s:is',NS).itertext())
    elif t=='b':v=v=='1'
    elif v is not None and t not in ['str','e']:
     try:v=float(v)
     except ValueError:pass
    if c.find('s:f',NS) is not None:formula_count+=1
    if t=='e':errors.append(s.get('name')+'!'+c.get('r')+':'+str(v))
    cells[c.get('r')]=v
   sheets[s.get('name')]=cells
 return sheets,formula_count,errors

def soc_release(policy,current,adjustment,read_only,gate_passed,choice=None,approved=False,guardrail=False):
 """Reference for target and release. Inputs are already classified and valid."""
 target=policy if choice is None else choice
 confidence=4 if read_only or adjustment==0 else max(1,policy+adjustment)
 authorized=policy if target>policy and not approved else target
 staged=(4 if gate_passed else current) if read_only else current+(1 if gate_passed else 0)
 return target,min(authorized,confidence,staged,3 if guardrail and not read_only else 4),confidence

def main(directory):
 report={'method':'Independent reference calculations over XLSX cached values; no native recalculation','checks':[],'known_issues':[]}
 def check(name,actual,expected):
  ok=math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-10) if isinstance(actual,(int,float)) and isinstance(expected,(int,float)) else actual==expected
  report['checks'].append({'check':name,'pass':ok,'actual':actual,'expected':expected})
  if not ok:raise AssertionError(f'{name}: {actual!r} != {expected!r}')
 soc_path=directory/'SOC-Autonomy-Map-v1.4.3.xlsx'
 soc,soc_formulas,soc_errors=read_xlsx(soc_path)
 check('SOC cached formula errors',soc_errors,[])
 rv=[soc['Scales']['B'+str(i)] for i in range(24,28)]
 blasts=[soc['Scales']['B'+str(i)] for i in range(31,34)]
 levels=[soc['Scales']['B'+str(i)] for i in range(6,11)]
 appetites=[soc['Policy'][col+'4'] for col in 'CDE']
 policy={(r,b,a):soc['Policy'][col+str(5+i*3+j)] for i,r in enumerate(rv) for j,b in enumerate(blasts) for a,col in zip(appetites,'CDE')}
 adjustments={soc['Scales']['B'+str(i)]:soc['Scales']['C'+str(i)] for i in range(39,42)}
 ucs={soc['Use cases'].get('A'+str(i)):{'name':soc['Use cases'].get('B'+str(i)),'appetite':soc['Use cases'].get('D'+str(i)) or soc['Autonomy map']['C4']} for i in range(5,35)}
 gates={soc['Readiness gate'].get('A'+str(i)):[soc['Readiness gate'].get(col+str(i)) for col in 'CDEFGH'] for i in range(7,37)}
 released=[];row_checks=0
 for row in range(6,186):
  get=lambda col:soc['Register'].get(col+str(row))
  uid=get('A')
  if uid not in ucs or not ucs[uid]['name']:continue
  risk=policy[(get('F'),get('G'),ucs[uid]['appetite'])]
  read_only=get('F')==rv[0];ans=gates[uid];gate=all(x=='Yes' for x in ans)
  setting=soc['Readiness gate'].get('C4')
  if read_only and setting=='Signal + cost':gate=ans[0]=='Yes' and ans[4]=='Yes'
  if read_only and setting=='Signal + cost + resilience':gate=ans[0]=='Yes' and ans[4]=='Yes' and ans[5]=='Yes'
  choice=levels.index(get('M')) if get('M') in levels else None
  target,release,ceiling=soc_release(risk,get('R'),adjustments[get('H')],read_only,gate,choice,get('N')=='Yes',get('F')==rv[3] or get('G')==blasts[2])
  critical=min(target,policy[(get('F'),blasts[2],ucs[uid]['appetite'])])
  for col,want in [('J',levels[int(risk)]),('L',ceiling),('O',target),('Q',critical),('T',release)]:
   check(f'SOC Register!{col}{row}',get(col),want);row_checks+=1
  released.append(release)
 check('SOC released autonomous share',soc['Autonomy map']['E5'],sum(x==4 for x in released)/len(released))
 check('SOC released human-approved share',soc['Autonomy map']['G5'],sum(x==3 for x in released)/len(released))
 check('SOC released human-decides share',soc['Autonomy map']['I5'],sum(x<3 for x in released)/len(released))
 check('SOC boundary: high blast approved exception remains L3',soc_release(3,4,0,False,True,4,True,True)[1],3)
 check('SOC boundary: low confidence limits L4 policy to L2',soc_release(4,2,-2,False,True)[1],2)
 check('SOC boundary: gate failure holds current',soc_release(4,2,0,False,False)[1],2)
 check('SOC boundary: passed read-only releases fully',soc_release(4,2,-2,True,True)[1],4)
 high=soc_release(4,2,-2,False,True)[1];low=soc_release(4,2,0,False,True)[1]
 report['known_issues'].append({'id':'SOC-01','issue':'Config validation does not enforce High >= Medium >= Low adjustments','probe_adjustments':[-2,-1,0],'current_configuration_check_would_accept':True,'high_confidence_release':high,'low_confidence_release':low})
 llm,llm_formulas,llm_errors=read_xlsx(directory/'LLM_Agent_Security_Assessment_v0_6_8_r4.xlsx')
 check('LLM cached formula errors',llm_errors,[])
 controls=[i for i in range(2,70) if llm['Assessment Matrix'].get('A'+str(i))]
 check('LLM control count',llm['Dashboard']['B6'],len(controls))
 check('LLM blank template recommendation',llm['Dashboard']['B21'],'INCOMPLETE')
 exposure=sum(llm['Assessment Matrix']['F'+str(i)]*llm['Assessment Matrix']['G'+str(i)]*llm['Assessment Matrix']['H'+str(i)] for i in controls if llm['Assessment Matrix']['I'+str(i)]=='Yes')
 check('LLM blank template open exposure',llm['Dashboard']['B15'],exposure)
 blocker_count=sum(llm['Model Comparator'].get('C'+str(i))=='Blocker' and llm['Model Comparator'].get('E'+str(i))=='Yes' for i in range(10,78))
 for col in 'GHIJ':
  cached=llm['Model Comparator'].get(col+'6')
  if cached!=blocker_count:report['known_issues'].append({'id':'LLM-01','cell':'Model Comparator!'+col+'6','cached':cached,'independently_calculated':blocker_count,'issue':'Stale blocker count; full recalculation required'})
  cached_na=llm['Model Comparator'].get(col+'8')
  if cached_na!=0:report['known_issues'].append({'id':'LLM-01','cell':'Model Comparator!'+col+'8','cached':cached_na,'independently_calculated':0,'issue':'Stale exclusion count in blank template'})
 report['summary']={'SOC_formula_count':soc_formulas,'SOC_active_rows':len(released),'SOC_row_output_reconciliations':row_checks,'LLM_formula_count':llm_formulas,'checks_passed':len(report['checks']),'known_issue_observations':len(report['known_issues'])}
 print(json.dumps(report,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workbook-dir',type=Path,default=Path(__file__).resolve().parents[1]/'workbooks');args=p.parse_args();main(args.workbook_dir)
