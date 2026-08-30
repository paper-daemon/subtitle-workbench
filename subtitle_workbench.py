#!/usr/bin/env python3
import argparse, html, json, re
from pathlib import Path

TIME_RE=re.compile(r'(\d{2}):(\d{2}):(\d{2})[,.](\d{3})')

def ms(text):
    m=TIME_RE.fullmatch(text.strip())
    if not m: raise ValueError(f'bad timestamp: {text}')
    h,mn,s,z=map(int,m.groups())
    if mn > 59 or s > 59:
        raise ValueError(f'bad timestamp: {text}')
    return ((h*60+mn)*60+s)*1000+z

def fmt(value):
    value=max(0,int(value)); z=value%1000; value//=1000
    s=value%60; value//=60; mn=value%60; h=value//60
    return f'{h:02d}:{mn:02d}:{s:02d},{z:03d}'

def parse_srt(path):
    text=Path(path).read_text(encoding='utf-8-sig').replace('\r\n','\n')
    blocks=re.split(r'\n\s*\n',text.strip()) if text.strip() else []
    cues=[]
    for b in blocks:
        lines=b.splitlines(); idx=0
        if lines and lines[0].strip().isdigit(): idx=1
        if idx>=len(lines) or '-->' not in lines[idx]:
            label=lines[0] if lines else '<empty>'
            raise ValueError(f'bad cue block: missing timing line near {label}')
        a,btime=[x.strip() for x in lines[idx].split('-->',1)]
        cues.append({'start':ms(a),'end':ms(btime),'text':'\n'.join(lines[idx+1:]).strip()})
    return cues
def analyze(cues):
    findings=[]
    for i,c in enumerate(cues):
        if c['end']<=c['start']:
            findings.append({'kind':'bad-duration','cue':i+1,'detail':f"{c['start']}→{c['end']}"})
        if i:
            prev=cues[i-1]
            if c['start']<prev['end']:
                findings.append({'kind':'overlap','cue':i+1,'detail':f"{prev['end']-c['start']} ms"})
            gap=c['start']-prev['end']
            if gap>5000:
                findings.append({'kind':'long-gap','cue':i+1,'detail':f'{gap} ms'})
        if len(c['text'])>84:
            findings.append({'kind':'long-text','cue':i+1,'detail':f"{len(c['text'])} chars"})
    return {'cues':len(cues),'duration_ms':max([c['end'] for c in cues] or [0]),'findings':findings}

def shifted(cues,offset):
    return [{'start':max(0,c['start']+offset),'end':max(0,c['end']+offset),'text':c['text']} for c in cues]

def write_srt(path,cues):
    parts=[]
    for i,c in enumerate(cues,1):
        parts.append(f"{i}\n{fmt(c['start'])} --> {fmt(c['end'])}\n{c['text']}\n")
    Path(path).write_text('\n'.join(parts),encoding='utf-8')

def render(report):
    rows=''.join(f"<tr><td>{f['cue']}</td><td>{html.escape(f['kind'])}</td><td>{html.escape(f['detail'])}</td></tr>" for f in report['findings'])
    return f'''<!doctype html><meta charset="utf-8"><title>Subtitle Workbench</title><style>body{{font:15px system-ui;max-width:900px;margin:auto;padding:40px;background:#f3eee5}}table{{width:100%;border-collapse:collapse;background:#fffaf2}}td,th{{padding:9px;border-bottom:1px solid #ddd;text-align:left}}</style><h1>Subtitle Workbench</h1><p>{report['cues']} cues · {len(report['findings'])} findings · {report['duration_ms']/1000:.1f}s</p><table><tr><th>cue</th><th>kind</th><th>detail</th></tr>{rows}</table>'''
def main():
    ap=argparse.ArgumentParser(description='Inspect, normalize and time-shift SRT subtitles.')
    ap.add_argument('input'); ap.add_argument('--output',default='cleaned.srt')
    ap.add_argument('--shift-ms',type=int,default=0); ap.add_argument('--html',default='subtitle-report.html'); ap.add_argument('--json')
    a=ap.parse_args()
    try:
        cues=parse_srt(a.input)
    except ValueError as e:
        ap.error(str(e))
    out=shifted(cues,a.shift_ms)
    report=analyze(out)
    write_srt(a.output,out); Path(a.html).write_text(render(report),encoding='utf-8')
    if a.json: Path(a.json).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"cues={report['cues']} findings={len(report['findings'])} shift_ms={a.shift_ms} output={a.output}")

if __name__=='__main__':
    main()
