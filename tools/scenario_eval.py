#!/usr/bin/env python3
"""Reproduce 39 read-only source-formula scenarios for the reviewed workbooks.

This uses a purpose-limited interpreter, not native Excel. Expected outcomes
include documented defects. Overrides stay in memory; workbooks are never saved.
Requires the optional dependencies in requirements-test.txt.
"""
from pathlib import Path
import argparse,json,sys
from excel_eval import Evaluator,to_excel,datetime

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--workbook-dir',type=Path,default=Path(__file__).resolve().parents[1]/'workbooks')
parser.add_argument('--output',type=Path,help='Write the complete JSON result to this path.')
args=parser.parse_args()
FILES=['LLM_Agent_Security_Assessment_v0_6_8_r4.xlsx','SOC-Autonomy-Map-v1.4.3.xlsx']

reports=[]
def record(e,name,changes,reads,expected=None):
 e.reset(changes);r={s+'!'+a:e.cell(s,a) for s,a in reads}
 ok=all(r[k]==v for k,v in (expected or {}).items())
 reports.append({'name':name,'results':r,'expected':expected,'pass':ok})
 print(name,json.dumps(r),ok)
 return r

e=Evaluator(args.workbook_dir/FILES[0])
reads=[('Dashboard','B3'),('Dashboard','B7'),('Dashboard','B10'),('Dashboard','B11'),('Dashboard','B12'),('Dashboard','B13'),('Dashboard','B21'),('Dashboard','B26')]
record(e,'LLM blank template',{},reads,{'Dashboard!B21':'INCOMPLETE','Dashboard!B7':68})
scoping={3:'Synthetic audit fixture',4:'Test reviewer',5:to_excel(datetime.datetime(2026,10,22)),6:'1.0',9:'External SaaS / API',10:'Production',11:'No',12:'No',13:'Yes',14:'Internal (limited group)',15:'No',16:'No',17:'No',18:'No',19:'No',20:'None (chat or single completions)',21:'No',22:'No',23:'No',24:'No',25:'Cloud or SaaS tenant',26:'Assist (informs a human)',27:'No'}
base={('Scoping','C'+str(r)):v for r,v in scoping.items()}
base.update({('Assessment Matrix',c+str(r)):'Yes' if c=='K' else 'Synthetic evidence reference' for r in range(2,70) for c in ['K','O']})
record(e,'LLM fully answered with evidence',base,reads,{'Dashboard!B21':'APPROVABLE'})
def test(name,delta,expect,extra=[]):return record(e,name,{**base,**delta},reads+extra,expect)
test('LLM production Blocker Partial',{('Assessment Matrix','K3'):'Partial'},{'Dashboard!B21':'BLOCKED'})
test('LLM pilot Blocker Partial',{('Assessment Matrix','K3'):'Partial',('Scoping','C10'):'Pilot / PoC'},{'Dashboard!B21':'CONDITIONAL APPROVAL'})
test('LLM blocker No remains blocked when status Remediated',{('Assessment Matrix','K3'):'No',('Assessment Matrix','S3'):'Remediated'},{'Dashboard!B21':'BLOCKED'})
test('LLM documented exemption stays conditional',{('Assessment Matrix','K3'):'No',('Assessment Matrix','S3'):'Accepted Risk',('Assessment Matrix','X3'):'Synthetic approval',('Assessment Matrix','Y3'):'Risk owner',('Assessment Matrix','Z3'):46317},{'Dashboard!B21':'CONDITIONAL APPROVAL','Dashboard!B13':1})
test('LLM missing exemption metadata holds decision',{('Assessment Matrix','K3'):'No',('Assessment Matrix','S3'):'Accepted Risk'},{'Dashboard!B21':'INCOMPLETE'})
test('LLM blocker de-scope needs review',{('Assessment Matrix','J3'):'No',('Assessment Matrix','T3'):'Synthetic reason'},{'Dashboard!B21':'INCOMPLETE'})
test('LLM missing evidence is conditional',{('Assessment Matrix','O3'):None},{'Dashboard!B21':'CONDITIONAL APPROVAL'})
test('LLM unanswered control is incomplete',{('Assessment Matrix','K3'):None},{'Dashboard!B21':'INCOMPLETE'})
test('LLM invalid response is incomplete',{('Assessment Matrix','K3'):'Yess'},{'Dashboard!B21':'INCOMPLETE'})
test('LLM invalid likelihood is incomplete',{('Assessment Matrix','G3'):0},{'Dashboard!B21':'INCOMPLETE'})
test('LLM invalid scoping is incomplete',{('Scoping','C20'):'unknown'},{'Dashboard!B21':'INCOMPLETE'})
test('LLM missing policy setting is incomplete',{('Lookups','B21'):None},{'Dashboard!B21':'INCOMPLETE'})
test('LLM inverted readiness thresholds are incomplete',{('Lookups','B21'):0.9},{'Dashboard!B21':'INCOMPLETE'})
test('LLM capability keeps tools local memory and MCP controls applicable',{('Scoping','C19'):'Yes',('Scoping','C22'):'Yes',('Scoping','C23'):'Yes',('Scoping','C27'):'Yes'},{'Assessment Matrix!I60':'Yes','Assessment Matrix!I61':'Yes','Assessment Matrix!I63':'Yes','Assessment Matrix!I67':'Yes'},[('Assessment Matrix','I60'),('Assessment Matrix','I61'),('Assessment Matrix','I63'),('Assessment Matrix','I67')])
mcp={('Scoping','C27'):'Yes',('MCP Server Checklist','I2'):'Yes',('MCP Server Checklist','I3'):'Yes',('MCP Server Checklist','E3'):'Local stdio',('MCP Server Checklist','G3'):'Local process',('MCP Server Checklist','C4'):'N/A',('MCP Server Checklist','E4'):'No',('MCP Server Checklist','G4'):'No',('MCP Client Checklist','I2'):'No',('MCP Client Checklist','D35'):'Only server is assessed in this synthetic fixture'}
mcp.update({('MCP Server Checklist',c+str(r)):'Compliant' if c=='E' else 'Synthetic evidence' for r in range(6,22) for c in ['E','F']})
test('LLM required MCP server complete',mcp,{'Dashboard!B21':'APPROVABLE','MCP Server Checklist!D25':'GO'},[('MCP Server Checklist','D25')])
test('LLM invalid calendar protocol date',{**mcp,('MCP Server Checklist','C3'):'2026-02-30'},{'Dashboard!B21':'INCOMPLETE'})
test('LLM MCP mandatory failure blocks',{**mcp,('MCP Server Checklist','E6'):'Non-compliant'},{'Dashboard!B21':'BLOCKED'},[('MCP Server Checklist','D23'),('MCP Server Checklist','D25')])
test('LLM MCP failure plus missing context',{**mcp,('MCP Server Checklist','E6'):'Non-compliant',('MCP Server Checklist','G3'):None},{'Dashboard!B21':'INCOMPLETE'},[('MCP Server Checklist','D23'),('MCP Server Checklist','D25')])
test('LLM S19 no with required checklist holds decision',{('MCP Server Checklist','I2'):'Yes'},{'Dashboard!B21':'INCOMPLETE'})

comparator={**base,**{('Model Comparator','G'+str(r)):'Yes' for r in range(10,78)}}
cmp_reads=[('Model Comparator','G5'),('Model Comparator','G6'),('Model Comparator','G7'),('Model Comparator','G8'),('Model Comparator','AB8')]
record(e,'Comparator complete candidate',comparator,cmp_reads,{'Model Comparator!G7':'Suitable'})
excluded={**comparator,('Model Comparator','G11'):'N/A',('Model Comparator','K11'):'Synthetic scope exclusion'}
record(e,'Comparator proposed exclusion needs review',excluded,cmp_reads,{'Model Comparator!G7':'PENDING REVIEW'})
snapshot=e.cell('Model Comparator','S8')
approved={**excluded,('Model Comparator','K8'):'Approved',('Model Comparator','P8'):'Test reviewer',('Model Comparator','Q8'):46317,('Model Comparator','R8'):snapshot}
record(e,'Comparator approved current exclusion set',approved,cmp_reads,{'Model Comparator!G7':'Suitable'})
record(e,'Comparator changed exclusion requires new review',{**approved,('Model Comparator','K11'):'Changed reason'},cmp_reads,{'Model Comparator!G7':'PENDING REVIEW'})
record(e,'Comparator formula snapshot is rejected',{**approved,('Model Comparator','R8'):'=S8'},cmp_reads,{'Model Comparator!G7':'PENDING REVIEW'})
record(e,'Comparator rejected exclusion is incomplete',{**approved,('Model Comparator','K8'):'Rejected'},cmp_reads,{'Model Comparator!G7':'INCOMPLETE - re-answer rejected exclusions'})
record(e,'Comparator shared invalid policy is provisional',{**comparator,('Lookups','B29'):None},cmp_reads,{'Model Comparator!G7':'PROVISIONAL - invalid scope/config'})
record(e,'Comparator operational evidence does not change sourcing',{**comparator,('Assessment Matrix','O3'):'=1/0'},cmp_reads,{'Model Comparator!G7':'Suitable'})

e=Evaluator(args.workbook_dir/FILES[1]);reads=[('Register','J7'),('Register','L7'),('Register','O7'),('Register','P7'),('Register','Q7'),('Register','S7'),('Register','T7'),('Register','U7')]
record(e,'SOC baseline',{},reads,{'Register!T7':3})
record(e,'SOC missing action', {('Register','E7'):None},reads,{'Register!O7':'','Register!T7':'','Register!P7':'Incomplete assessment'})
record(e,'SOC missing current level', {('Register','R7'):None},reads,{'Register!O7':'','Register!T7':'','Register!P7':'Incomplete assessment'})
record(e,'SOC low confidence caps release', {('Register','H7'):'Low'},reads,{'Register!L7':2,'Register!T7':2})
record(e,'SOC invalid policy fails closed', {('Policy','C5'):None},reads+[('Policy','B24')],{'Register!J7':'Config error','Register!T7':''})
record(e,'SOC high blast guardrail caps approved exception',{('Register','G8'):'High',('Register','M8'):'L4 Autonomous',('Register','N8'):'Yes',('Register','R8'):4},[('Register','O8'),('Register','T8'),('Register','U8')],{'Register!O8':4,'Register!T8':3})
record(e,'SOC unknown read-only confidence bypasses confidence cap',{('Register','H6'):'unknown'},[('Register','L6'),('Register','T6'),('Register','P6')],{'Register!L6':4,'Register!T6':4})
record(e,'SOC nonmonotonic confidence high',{('Scales','C39'):-2,('Scales','C40'):-1,('Scales','C41'):0,('Register','H7'):'High'},reads+[('Scales','C43')],{'Scales!C43':'OK','Register!T7':2})
record(e,'SOC nonmonotonic confidence low',{('Scales','C39'):-2,('Scales','C40'):-1,('Scales','C41'):0,('Register','H7'):'Low'},reads+[('Scales','C43')],{'Scales!C43':'OK','Register!T7':3})
record(e,'SOC read-only relaxed gate',{('Readiness gate','C4'):'Signal + cost'},[('Register','T30'),('Register','T60'),('Register','T66'),('Register','T72'),('Register','T96')],{'Register!T30':4,'Register!T60':4,'Register!T66':4,'Register!T72':4,'Register!T96':4})
if args.output:
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(reports,indent=2)+'\n',encoding='utf-8')
passed=sum(x['pass'] for x in reports)
print('TOTAL',len(reports),'MATCHED EXPECTATIONS',passed)
print('Expected outcomes include documented defects; this is not native Excel acceptance.')
sys.exit(0 if passed==len(reports) else 1)
