"""Build the static homepage and one page per paper from research.json."""
from pathlib import Path
import json, html

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'research.json').read_text())
esc=lambda x:html.escape(str(x),quote=True)

def head(title,depth=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="Simengxu Qiao — temporal representation learning, knowledge-guided forecasting, and multimodal time series at Zhejiang University."><meta name="theme-color" content="#176b81"><link rel="icon" href="{depth}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{depth}assets/style.css"></head><body>'''

def teaser(p,depth=''):
 image=ROOT/'assets'/f'{p["id"]}.png'
 return f'<img src="{depth}assets/{p["id"]}.png" alt="{esc(p["name"])} method overview" loading="lazy">' if image.exists() else f'<span class="monogram">{esc(p["name"])}</span>'

def resource_links(p,project=True):
 links=[]
 if project:links.append(f'<a href="projects/{p["id"]}/">🌐 Project ↗</a>')
 if p.get('paper'):links.append(f'<a href="{esc(p["paper"])}">📄 Paper ↗</a>')
 links.append(f'<a href="https://github.com/Joss0623/{p["repo"]}">{"💻 Code" if p["hasCode"] else "📦 Repository"} ↗</a>')
 return '<div class="links">'+''.join(links)+'</div>'

def status_icon(p):
 return {'Published':'🎉','Accepted':'🎉','Under review':'📝','Manuscript':'📄','In progress':'🔬'}[p['status']]

pubs=[]
for p in data['papers']:
 pubs.append(f'''<article class="pub" data-category="{p['category']}"><a class="teaser" href="projects/{p['id']}/" aria-label="{esc(p['name'])} project">{teaser(p)}</a><div><div class="meta"><span class="status"><span aria-hidden="true">{status_icon(p)}</span> {esc(p['status'])}</span><span>{esc(p['venue'])}</span></div><h3><a href="projects/{p['id']}/">{esc(p['title'])}</a></h3><p class="summary">{esc(p['summary'])}</p>{resource_links(p)}<div class="tags">{' · '.join(map(esc,p['tags']))}</div></div></article>''')
 home='https://joss0623.github.io/'
 page=head(p['title'],'../../')+f'''<header><div class="nav"><a class="wordmark" href="../../">Simengxu Qiao</a><nav><a href="../../#publications">All research</a><a href="https://github.com/Joss0623/{p['repo']}">💻 GitHub ↗</a></nav></div></header><main class="project-shell"><p class="eyebrow">{esc(p['name'])} · Research project</p><h1>{esc(p['title'])}</h1><p class="meta">{esc(p['venue'])}</p><p class="lead">{esc(p['summary'])}</p>'''
 if p.get('paper'):
  paper=p['paper'] if p['paper'].startswith('http') else '../../'+p['paper']
  page+=f'<div class="links"><a href="{esc(paper)}">Read the paper ↗</a><a href="https://github.com/Joss0623/{p["repo"]}">GitHub repository ↗</a></div>'
 else:page+=f'<div class="links"><a href="https://github.com/Joss0623/{p["repo"]}">GitHub repository ↗</a></div>'
 if (ROOT/'assets'/f'{p["id"]}.png').exists():page+=f'<img class="framework" src="../../assets/{p["id"]}.png" alt="{esc(p["name"])} method overview">'
 page+=f'''<section><h2>Research focus</h2><p class="tags">{' · '.join(map(esc,p['tags']))}</p></section><section><h2>Resources</h2><p>The repository contains the available paper and implementation resources for this work. See its README for code entry points, dependencies, and data requirements.</p></section><footer><span>Simengxu Qiao · Zhejiang University</span><a href="../../#publications">Back to publications ↑</a></footer></main></body></html>'''
 out=ROOT/'projects'/p['id'];out.mkdir(parents=True,exist_ok=True);(out/'index.html').write_text(page)

p=data['profile']
index=head('Simengxu Qiao | 乔斯梦旭 — Zhejiang University')+f'''<a class="skip" href="#main">Skip to content</a><header><div class="nav"><a class="wordmark" href="#about">Simengxu Qiao</a><nav aria-label="Main navigation"><a href="#about">About</a><a href="#publications">Research</a><a href="#experience">Experience</a><a href="#education">Education</a></nav></div></header><main id="main" class="shell"><section id="about" class="intro"><aside class="profile-side"><img class="portrait" src="assets/portrait.jpeg" alt="Portrait of Simengxu Qiao" width="180" height="225"><div class="identity"><strong>Zhejiang University</strong>Control Science and Engineering<br>Hangzhou, China</div></aside><div class="bio"><p class="eyebrow">Temporal intelligence · Knowledge-guided forecasting</p><h1>Simengxu Qiao <span>乔斯梦旭</span></h1><p>{esc(p['intro'])}</p><p>{esc(p['interests'])}</p><p class="research-line">Previously, I worked on medical search relevance at Alibaba's Quark team and multi-city supply–demand modeling at DiDi.</p><div class="contact"><a href="mailto:{p['email']}">✉️ Email ↗</a><a href="{p['github']}">💻 GitHub ↗</a><a href="#publications">🔥 Research & projects ↓</a></div></div></section><section class="section" id="publications"><div class="section-heading"><div><h2><span aria-hidden="true">📚</span> Research & publications</h2><p class="section-note">Temporal representations, source composition, and knowledge-guided prediction.</p></div><div class="filters" role="group" aria-label="Filter research"><button data-filter="All" aria-pressed="true">All</button><button data-filter="Temporal" aria-pressed="false">Temporal modeling</button><button data-filter="Multimodal" aria-pressed="false">Multimodal & LLM</button></div></div><span id="filter-status" class="skip" aria-live="polite"></span>{''.join(pubs)}</section><section class="section" id="experience"><div class="section-heading"><h2><span aria-hidden="true">💻</span> Research experience</h2></div><div class="timeline"><article><div class="date">Sep. 2025 — Feb. 2026</div><div><h3>DiDi · Research Algorithm Intern</h3><p>Multi-city supply–demand forecasting, conditional expert routing, and distribution-aware optimization for long-tailed regression.</p></div></article><article><div class="date">Jun. 2024 — Sep. 2024</div><div><h3>Alibaba, Quark · LLM Algorithm Intern</h3><p>Medical cross-language relevance modeling, supervised fine-tuning, and continuous relevance scoring for search.</p></div></article></div></section><section class="section" id="education"><div class="section-heading"><h2><span aria-hidden="true">🎓</span> Education</h2></div><div class="education"><article><h3>Zhejiang University</h3><p>Control Science and Engineering<br>Integrated master's–doctoral program<br>2023 — 2028 (expected)</p></article><article><h3>Beijing University of Chemical Technology</h3><p>B.Eng. in Automation<br>2019 — 2023</p></article></div></section><section class="section"><div class="section-heading"><h2><span aria-hidden="true">🏅</span> Selected honors</h2></div><div class="awards"><span>🏆 National Scholarship · Three awards</span><span>🎖️ Outstanding Graduate of Beijing</span><span>✨ Eight university-level honors during graduate study</span></div></section><footer><span>© 2026 Simengxu Qiao</span><span><a href="https://github.com/Joss0623/Joss0623.github.io">Site source</a> · Last updated November 2026</span></footer></main><script src="assets/site.js"></script></body></html>'''
(ROOT/'index.html').write_text(index)
(ROOT/'.nojekyll').touch()
(ROOT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#176b81"/><text x="32" y="44" text-anchor="middle" fill="white" font-family="Georgia,serif" font-size="40">Q</text></svg>')
print(f'Built homepage and {len(data["papers"])} project pages.')
