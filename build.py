"""Build the static homepage and one page per paper from research.json."""
from pathlib import Path
import json, html, hashlib
from urllib.parse import quote

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'research.json').read_text())
STYLE_VERSION=hashlib.sha256((ROOT/'assets/style.css').read_bytes()).hexdigest()[:10]
esc=lambda x:html.escape(str(x),quote=True)
# Conference papers first (newest meeting first), then journals by JIF.
data['papers'].sort(key=lambda p:(p.get('publication_type')=='conference',p.get('conference_date',''),p.get('impact_factor',0)),reverse=True)

def external_link(url, label):
 return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'

def linked_profile(text):
 links=data['profile']['links']
 names={'Beijing University of Chemical Technology':links['undergraduate_university'],
        'Zhejiang University':links['university'],
        'Control Science and Engineering':links['department']}
 text=esc(text)
 for name,url in names.items():text=text.replace(name,external_link(url,name))
 return text

def venue(p):
 label,*suffix=p['venue'].split(' · ',1)
 title=external_link(p['venue_url'],label) if p.get('venue_url') else esc(label)
 return title+(' · '+esc(suffix[0]) if suffix else '')

def title_target(p):
 return p.get('doi') or p.get('paper') or 'projects/'+p['id']+'/'

def star_badge(p):
 return f'<a class="repo-badge" href="https://github.com/Joss0623/{p["repo"]}" target="_blank" rel="noopener noreferrer" aria-label="{esc(p["name"])} GitHub repository and stars"><img src="https://img.shields.io/github/stars/Joss0623/{p["repo"]}?style=social&amp;label=Stars" alt="{esc(p["name"])} GitHub stars" loading="lazy" height="20"></a>'

def head(title,depth=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="Simengxu Qiao — temporal representation learning, knowledge-guided forecasting, and multimodal time series at Zhejiang University."><meta name="theme-color" content="#176b81"><link rel="icon" href="{depth}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{depth}assets/style.css?v={STYLE_VERSION}"></head><body>'''

def figure_path(p):
 return next((f'assets/{p["id"]}.{ext}' for ext in ('png','svg') if (ROOT/'assets'/f'{p["id"]}.{ext}').exists()),None)

def teaser(p,depth=''):
 image=figure_path(p)
 return f'<img src="{depth}{image}" alt="{esc(p["name"])} model architecture" loading="lazy">' if image else f'<span class="monogram">{esc(p["name"])}</span>'

def resource_links(p,project=True):
 links=[]
 if project:links.append(f'<a href="projects/{p["id"]}/">🌐 Project ↗</a>')
 if p.get('paper'):links.append(f'<a href="{esc(p["paper"])}">📄 Paper ↗</a>')
 if p.get('doi') and p['doi']!=p.get('paper'):links.append(external_link(p['doi'],'🔗 Publisher / DOI ↗'))
 if p.get('citation'):links.append(f'<a href="{esc(p["citation"])}" download>📋 BibTeX</a>')
 if p.get('discussion'):links.append(external_link(p['discussion'],'💬 OpenReview ↗'))
 if p.get('code_url'):links.append(external_link(p['code_url'],'💻 Code ↗'))
 links.append(f'<a href="https://github.com/Joss0623/{p["repo"]}">{"💻 Code" if p["hasCode"] else "📦 Repository"} ↗</a>')
 if p['hasCode']:links.append(star_badge(p))
 return '<div class="links">'+''.join(links)+'</div>'

def status_icon(p):
 return {'Published':'🎉','Accepted':'🎉','Under review':'📝','Manuscript':'📄','In progress':'🔬'}[p['status']]

pubs=[]
for p in data['papers']:
 pubs.append(f'''<article class="pub" data-category="{p['category']}"><a class="teaser" href="projects/{p['id']}/" aria-label="{esc(p['name'])} project">{teaser(p)}</a><div><div class="meta"><span class="status"><span aria-hidden="true">{status_icon(p)}</span> {esc(p['status'])}</span><span>{venue(p)}</span></div><h3><a href="{esc(title_target(p))}">{esc(p['title'])}</a></h3><p class="summary">{esc(p['summary'])}</p>{resource_links(p)}<div class="tags">{' · '.join(map(esc,p['tags']))}</div></div></article>''')
 home='https://joss0623.github.io/'
 page=head(p['title'],'../../')+f'''<header><div class="nav"><a class="wordmark" href="../../">Simengxu Qiao</a><nav><a href="../../#publications">All research</a><a href="https://github.com/Joss0623/{p['repo']}">💻 GitHub ↗</a></nav></div></header><main class="project-shell"><p class="eyebrow">{esc(p['name'])} · Research project</p><h1>{esc(p['title'])}</h1><p class="meta">{venue(p)}</p><p class="lead">{esc(p['summary'])}</p>'''
 if p.get('paper'):
  paper=p['paper'] if p['paper'].startswith('http') else '../../'+p['paper']
  page+=f'<div class="links"><a href="{esc(paper)}">Read the paper ↗</a><a href="https://github.com/Joss0623/{p["repo"]}">GitHub repository ↗</a></div>'
 else:page+=f'<div class="links"><a href="https://github.com/Joss0623/{p["repo"]}">GitHub repository ↗</a></div>'
 extra=[]
 if p.get('discussion'):extra.append(external_link(p['discussion'],'💬 OpenReview ↗'))
 if p.get('code_url'):extra.append(external_link(p['code_url'],'💻 Code ↗'))
 if p.get('doi') and p['doi']!=p.get('paper'):extra.append(external_link(p['doi'],'🔗 Publisher / DOI ↗'))
 if p.get('citation'):extra.append(f'<a href="../../{esc(p["citation"])}" download>📋 Download BibTeX</a>')
 if p['hasCode']:extra.append(star_badge(p))
 if extra:page+='<div class="links">'+''.join(extra)+'</div>'
 if figure_path(p):
  page+=f'<a href="../../{figure_path(p)}" aria-label="Open full-size model architecture"><img class="framework" src="../../{figure_path(p)}" alt="{esc(p["name"])} model architecture"></a>'
  if p.get("figure_note"):page+=f'<p class="figure-note">{esc(p["figure_note"])}</p>'
 page+=f'''<section><h2>Research focus</h2><p class="tags">{' · '.join(map(esc,p['tags']))}</p></section><section><h2>Resources</h2><p>The repository contains the available paper and implementation resources for this work. See its <a href="https://github.com/Joss0623/{p['repo']}#readme">README</a> for code entry points, dependencies, and data requirements.</p></section><footer><span>Simengxu Qiao · {external_link(data['profile']['links']['university'],'Zhejiang University')}</span><a href="../../#publications">Back to publications ↑</a></footer></main></body></html>'''
 out=ROOT/'projects'/p['id'];out.mkdir(parents=True,exist_ok=True);(out/'index.html').write_text(page)

p=data['profile']
index=head('Simengxu Qiao | 乔斯梦旭 — Zhejiang University')+f'''<a class="skip" href="#main">Skip to content</a><header><div class="nav"><a class="wordmark" href="#about">Simengxu Qiao</a><nav aria-label="Main navigation"><a href="#about">About</a><a href="#publications">Research</a><a href="#experience">Experience</a><a href="#education">Education</a></nav></div></header><main id="main" class="shell"><section id="about" class="intro"><aside class="profile-side"><img class="portrait" src="assets/portrait.jpeg" alt="Portrait of Simengxu Qiao" width="180" height="225"><div class="identity"><strong>{external_link(p['links']['university'],'Zhejiang University')}</strong>{external_link(p['links']['department'],'Control Science and Engineering')}<br>Hangzhou, China</div></aside><div class="bio"><p class="eyebrow">Temporal intelligence · Knowledge-guided forecasting</p><h1>Simengxu Qiao <span>乔斯梦旭</span></h1><p>{linked_profile(p['intro'])}</p><p>{esc(p['interests'])}</p><p class="research-line">Previously, I worked on medical search relevance at {external_link(p['links']['alibaba'],'Alibaba')}'s {external_link(p['links']['qwen'],'Qwen')} team and multi-city supply–demand modeling at {external_link(p['links']['didi'],'DiDi')}.</p><div class="contact"><a href="mailto:{p['email']}">✉️ Email ↗</a><a href="{p['github']}">💻 GitHub ↗</a><a href="{p['orcid']}">🟢 ORCID ↗</a><a href="#publications">🔥 Research & projects ↓</a></div></div></section><section class="section" id="publications"><div class="section-heading"><div><h2><span aria-hidden="true">📚</span> Research & publications</h2><p class="section-note">Temporal representations, source composition, and knowledge-guided prediction.</p></div><div class="filters" role="group" aria-label="Filter research"><button data-filter="All" aria-pressed="true">All</button><button data-filter="Temporal" aria-pressed="false">Temporal modeling</button><button data-filter="Multimodal" aria-pressed="false">Multimodal & LLM</button></div></div><span id="filter-status" class="skip" aria-live="polite"></span>{''.join(pubs)}</section><section class="section" id="experience"><div class="section-heading"><h2><span aria-hidden="true">💻</span> Research experience</h2></div><div class="timeline"><article><div class="date">Sep. 2025 — Feb. 2026</div><div><h3>{external_link(p['links']['didi'],'DiDi')} · Research Algorithm Intern</h3><p>Multi-city supply–demand forecasting, conditional expert routing, and distribution-aware optimization for long-tailed regression.</p></div></article><article><div class="date">Jun. 2024 — Sep. 2024</div><div><h3>{external_link(p['links']['alibaba'],'Alibaba')}, {external_link(p['links']['qwen'],'Qwen')} · LLM Algorithm Intern</h3><p>Medical cross-language relevance modeling, supervised fine-tuning, and continuous relevance scoring for search.</p></div></article></div></section><section class="section" id="education"><div class="section-heading"><h2><span aria-hidden="true">🎓</span> Education</h2></div><div class="education"><article><h3>{external_link(p['links']['university'],'Zhejiang University')}</h3><p>{external_link(p['links']['department'],'Control Science and Engineering')}<br>Integrated master's–doctoral program<br>2023 — 2028 (expected)</p></article><article><h3>{external_link(p['links']['undergraduate_university'],'Beijing University of Chemical Technology')}</h3><p>B.Eng. in Automation<br>2019 — 2023</p></article></div></section><section class="section"><div class="section-heading"><h2><span aria-hidden="true">🏅</span> Selected honors</h2></div><div class="awards"><span>🏆 National Scholarship · Three awards</span><span>🎖️ Outstanding Graduate of Beijing</span><span>✨ Eight university-level honors during graduate study</span></div></section><footer><span>© 2026 Simengxu Qiao</span><span><a href="https://github.com/Joss0623/Joss0623.github.io">Site source</a> · Last updated November 2026</span></footer></main><script src="assets/site.js"></script></body></html>'''
(ROOT/'index.html').write_text(index)
(ROOT/'.nojekyll').touch()
(ROOT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#176b81"/><text x="32" y="44" text-anchor="middle" fill="white" font-family="Georgia,serif" font-size="40">Q</text></svg>')
print(f'Built homepage and {len(data["papers"])} project pages.')
