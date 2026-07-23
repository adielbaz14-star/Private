# -*- coding: utf-8 -*-
"""בניית קובץ מוצר יחיד (HTML) מקבצי ה-md של קורס ה-CRM."""
import re, os, markdown

BASE = '/home/user/Private/crm-course'
OUT = '/home/user/Private/dist/crm-zoho-course.html'

FILES = [
    ('README.md', 'intro'),
    ('00-syllabus.md', 'mod0'),
    ('01-understanding-business.md', 'mod1'),
    ('02-discovery-meeting.md', 'mod2'),
    ('03-zoho-basics.md', 'mod3'),
    ('04-building-the-system.md', 'mod4'),
    ('05-data-import.md', 'mod5'),
    ('06-daily-operations.md', 'mod6'),
    ('07-quotes-and-signatures.md', 'mod7'),
    ('08-dashboards-and-delivery.md', 'mod8'),
    ('09-selling-and-implementation.md', 'mod9'),
    ('10-ongoing-and-growth.md', 'mod10'),
    ('templates/discovery-questions.md', 'tpl-questions'),
    ('templates/spec-template.md', 'tpl-spec'),
    ('templates/delivery-checklist.md', 'tpl-checklist'),
    ('templates/pricing-proposal.md', 'tpl-pricing'),
]

# מיפוי קובץ -> עוגן, לכל צורות הכתיבה של הקישורים
anchor_map = {}
for path, anchor in FILES:
    name = os.path.basename(path)
    for variant in (name, path, f'../{name}', f'templates/{name}'):
        anchor_map[variant] = anchor

def preprocess(text, fname):
    # הסרת שורות ניווט הקודם/הבא/חזרה
    lines = []
    for line in text.split('\n'):
        s = line.strip()
        if s.startswith('**הקודם:**') or s.startswith('**הבא:**') or s.startswith('**חזרה:**'):
            continue
        lines.append(line)
    text = '\n'.join(lines)
    # הסרת קו מפריד שנשאר בסוף
    text = re.sub(r'\n---\s*$', '\n', text.strip()) + '\n'
    # המרת קישורי md לעוגנים פנימיים
    def repl(m):
        label, target = m.group(1), m.group(2)
        path = target.split('#')[0]
        if path in anchor_map:
            return f'[{label}](#{anchor_map[path]})'
        if target.startswith('#'):  # עוגן פנימי בעמוד — משאירים כטקסט
            return label
        return m.group(0)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl, text)
    # צ'קבוקסים
    text = text.replace('- [ ]', '- ☐')
    return text

md = markdown.Markdown(extensions=['tables', 'fenced_code', 'sane_lists'])
sections = []
toc_entries = []
for path, anchor in FILES:
    raw = open(os.path.join(BASE, path), encoding='utf-8').read()
    title = raw.split('\n', 1)[0].lstrip('# ').strip()
    toc_entries.append((anchor, title))
    html = md.reset().convert(preprocess(raw, path))
    sections.append(f'<section class="module" id="{anchor}">\n{html}\n</section>')

toc_html = '\n'.join(
    f'<li><a href="#{a}">{t}</a></li>' for a, t in toc_entries[1:]
)

CSS = '''
@page { size: A4; margin: 18mm 15mm; }
* { box-sizing: border-box; }
body { direction: rtl; font-family: "Noto Sans Hebrew","Noto Sans",sans-serif;
  color: #1f2937; line-height: 1.65; margin: 0; font-size: 11.5pt; }
.cover { min-height: 95vh; display: flex; flex-direction: column; justify-content: center;
  align-items: center; text-align: center; page-break-after: always;
  background: linear-gradient(160deg,#0f3d5c 0%,#14532d 100%); color:#fff;
  padding: 40px; border-radius: 0; }
.cover h1 { font-size: 30pt; margin: 0 0 12px; color: #fff; border-bottom: none; }
.cover .sub { font-size: 15pt; opacity: .92; max-width: 34em; }
.cover .badge { margin-top: 28px; background: rgba(255,255,255,.15);
  padding: 10px 22px; border-radius: 999px; font-size: 11pt; }
.toc { page-break-after: always; padding: 24px 8px; }
.toc h2 { color: #0f3d5c; border-bottom: 3px solid #0f3d5c; padding-bottom: 8px; }
.toc ol { padding-right: 22px; } .toc li { margin: 7px 0; }
.toc a { color: #1f2937; text-decoration: none; }
.module { page-break-before: always; padding: 0 4px; }
.module:first-of-type { page-break-before: avoid; }
h1 { color: #0f3d5c; font-size: 19pt; border-bottom: 3px solid #0f3d5c; padding-bottom: 8px; }
h2 { color: #14532d; font-size: 14.5pt; margin-top: 1.5em; }
h3 { color: #0f3d5c; font-size: 12.5pt; }
table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 10.5pt; }
th { background: #0f3d5c; color: #fff; padding: 7px 10px; text-align: right; }
td { border: 1px solid #d1d5db; padding: 6px 10px; vertical-align: top; }
tr:nth-child(even) td { background: #f3f6f9; }
code, pre { font-family: "Noto Sans Mono",monospace; background: #f3f4f6; border-radius: 4px; }
code { padding: 1px 5px; font-size: 10pt; }
pre { direction: ltr; text-align: right; padding: 12px 14px; overflow-x: auto;
  border: 1px solid #e5e7eb; font-size: 9.5pt; line-height: 1.5; }
blockquote { border-right: 4px solid #14532d; background: #f0f7f1; margin: 14px 0;
  padding: 10px 16px; border-radius: 0 6px 6px 0; }
a { color: #0f3d5c; }
li { margin: 3px 0; }
hr { border: none; border-top: 1px solid #d1d5db; margin: 22px 0; }
'''

html = f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<title>בונים מערכות CRM לעסקים — עם Zoho</title>
<style>{CSS}</style>
</head>
<body>
<div class="cover">
  <h1>בונים מערכות CRM לעסקים</h1>
  <div class="sub">קורס מעשי למתחילים: מאפיון ומציאת הכאב של בעל העסק, דרך בניית המערכת ב-Zoho CRM, ועד מכירה, הטמעה ושירותי המשך</div>
  <div class="badge">11 מודולים · 4 נספחי עבודה · מותאם למתחילים ללא רקע טכני</div>
</div>
<div class="toc">
  <h2>תוכן העניינים</h2>
  <ol>{toc_html}</ol>
</div>
{chr(10).join(sections)}
</body>
</html>'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)
print('written', OUT, len(html), 'bytes')
