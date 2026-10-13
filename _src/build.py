"""Build every IDIU screen as SVG (light and dark), write prototype.html, optionally render PNG previews.

    python build.py            # every screen + prototype.html
    python build.py --png      # also PNG previews via headless Chrome, into _previews/
    python build.py w11 w30    # only matching screens (does not rewrite prototype.html)
"""
from __future__ import annotations

import importlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import shell  # noqa: E402
import theme  # noqa: E402
from data import PEOPLE, SESSIONS, SUPPLIER_ACCOUNTS, SUPPLIER_SESSIONS, menu_for  # noqa: E402

MODULES = ["public", "home", "procurement", "suppliers", "budgets", "setup", "admin"]
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def screen_key(fn):
    """w07b_review -> w07b; a person's own screen carries an explicit key (w01-ruth)."""
    return getattr(fn, "key", None) or fn.__name__.split("_")[0]


def _order(fn):
    """The public site (w80–w83) first, then sign in (w00) and everything behind it, by number."""
    key = screen_key(fn)
    n = int(key[1:3])
    return (0 if n >= 80 else 1, n, key[3:])


def slug(title: str) -> str:
    t = title.lower().replace("&", "and").replace("'", "").replace("→", "to")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


PROTO = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>IDIU Procurement Management System · Mockup</title>
<meta name="description" content="Clickable mockup of the IDIU Procurement Management System: budgets, supplier prequalification, requisitions, RFQs, evaluation, LPOs, delivery and close-out, with maker-checker approvals. Illustrative data.">
<meta name="theme-color" content="#1A683F">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" type="image/png" sizes="64x64" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="IDIU Procurement mockup">
<meta property="og:title" content="IDIU Procurement Management System: clickable mockup">
<meta property="og:description" content="From budget to closed procurement file: requisitions, RFQs, committee evaluation, LPOs, delivery and payment reference, with maker-checker approvals and a full audit trail. Illustrative data.">
<meta property="og:url" content="https://idiu-pms.vercel.app/prototype.html">
<meta property="og:image" content="https://idiu-pms.vercel.app/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://idiu-pms.vercel.app/og-image.jpg">
<style>
  :root { --bg:#0D1712; --bar:#13241B; --ink:#E8F0EB; --muted:#9FB3A8; --accent:#D9F0B8; --btn:#1D3328; --btnline:#2C4A3A; }
  html, body { margin:0; height:100%; background:var(--bg); color:var(--ink); font:14px "Segoe UI", system-ui, sans-serif; overflow:hidden; }
  body.fs #stage { inset:0; }
  body.fs #bar { transform:translateY(100%); transition:transform .25s; }
  body.fs.peek #bar { transform:none; }
  #stage { position:absolute; inset:0 0 46px 0; display:flex; align-items:center; justify-content:center; }
  #frame { position:relative; box-shadow:0 10px 40px rgba(0,0,0,.35); }
  #frame img { display:block; width:100%; height:100%; user-select:none; -webkit-user-drag:none; transition:opacity .15s; }
  #frame #chrome { position:absolute; inset:0; pointer-events:none; display:none; transition:none; }
  #who { color:var(--ink); font-size:12.5px; background:var(--btn); border:1px solid var(--btnline); border-radius:8px; padding:5px 10px; }
  #who:empty { display:none; }
  #frame.loading img { opacity:.25; }
  #msg { position:absolute; inset:0; display:none; align-items:center; justify-content:center; text-align:center; color:#fff; background:rgba(13,23,18,.85); font-size:15px; padding:20px; }
  #frame.failed #msg { display:flex; }
  .hot { position:absolute; cursor:pointer; border-radius:8px; }
  .flash .hot, .show .hot { background:rgba(217,240,184,.22); outline:2px solid rgba(160,214,96,.95); }
  .flash .hot { transition:background .6s, outline-color .6s; }
  #bar { position:absolute; left:0; right:0; bottom:0; height:46px; background:var(--bar); display:flex; align-items:center; gap:10px; padding:0 14px; }
  #bar button, #bar select { background:var(--btn); color:var(--ink); border:1px solid var(--btnline); border-radius:8px; height:32px; padding:0 11px; font:inherit; cursor:pointer; }
  #bar select { max-width:380px; }
  #bar .sp { flex:1; }
  #bar button.on { background:var(--accent); color:#13241B; border-color:var(--accent); font-weight:600; }
  #bar > * { white-space:nowrap; flex-shrink:0; }
  #bar .hint { color:var(--muted); font-size:12.5px; overflow:hidden; text-overflow:ellipsis; flex-shrink:1; min-width:0; }
  #ready { color:var(--muted); font-size:12.5px; }
  #bar .pill { color:#13241B; background:var(--accent); border-radius:10px; padding:2px 9px; font-weight:600; font-size:12px; }
  @media (max-width:1500px) { #bar .hint { display:none; } }
  #rotate { position:absolute; left:50%; bottom:54px; transform:translateX(-50%); background:var(--btn); color:var(--ink); font-size:12.5px; padding:6px 12px; border-radius:999px; display:none; white-space:nowrap; }
  body.small.portrait #rotate { display:block; }
  @media (max-width:760px) {
    #bar { gap:6px; padding:0 8px; }
    #bar .pill, #bar #ready, #bar .sp, #bar .long { display:none; }
    #bar select { flex:1 1 auto; min-width:0; max-width:none; }
    #bar button { padding:0 9px; }
  }
</style></head><body>
<div id="stage"><div id="frame"><img id="img" alt=""><img id="chrome" alt=""><div id="msg">This screen could not load. Check the internet connection, then press → or pick it again.</div></div></div>
<div id="rotate">Turn your phone sideways to see the screens larger</div>
<div id="bar">
  <button id="prev" title="Previous (←)">&#8592;</button>
  <select id="pick"></select>
  <button id="next" title="Next (→)">&#8594;</button>
  <button id="web" title="The web system, from its front door (public Home)">Web dashboard</button>
  <button id="fs" title="Full screen (F) · Esc to exit">&#x26F6;<span class="long"> Full screen</span></button>
  <span id="who" title="Who is signed in: the sidebar and menus stay theirs until you switch (click the name)"></span>
  <span id="ready"></span><span class="sp"></span>
  <span class="hint">← → keys · H hotspots · F full screen (bar: mouse to the bottom edge) · D dark mode · Esc exit</span>
  <span class="pill">Illustrative data</span>
</div>
<script>
const SCREENS = __DATA__;
// Who is signed in decides the sidebar on every screen, as in the real app (SDS: AuthContext + AppSidebar).
const CHROME = __CHROME__, PERM = __PERM__, NAMES = __NAMES__, ROLE = __ROLE__, SB = __SB__, IDENT = __IDENT__;
let session = null;
const order = SCREENS.map(s => s.key);
const byKey = Object.fromEntries(SCREENS.map(s => [s.key, s]));
// public: the site anyone can read · auth: sign in, forgot password, register · staff: the console · supplier: the portal
const AREA_LABEL = { public: 'Public site · not signed in', auth: 'Not signed in' };
let theme = 'light';
try { theme = localStorage.getItem('idiu-theme') || 'light'; } catch (e) {}
const srcOf = s => theme === 'dark' ? s.src.replace(/^(web|chrome)\//, '$1-dark/') : s.src;
const CHROMES = Object.values(CHROME).flatMap(c => Object.values(c));
// Download every screen up front so the walkthrough keeps working if the connection drops.
const CACHE = {}; let loaded = 0;
function preload() {
  loaded = 0;
  const all = SCREENS.length + CHROMES.length;
  [...SCREENS, ...CHROMES].forEach(s => {
    const im = new Image();
    im.onload = () => { loaded++; document.getElementById('ready').textContent =
      loaded === all ? '✓ Offline-ready' : `Loading ${loaded}/${all}…`; };
    im.src = srcOf(s); CACHE[theme + s.src] = im;
  });
}
preload();
const img = document.getElementById('img'), frame = document.getElementById('frame'), pick = document.getElementById('pick');
let cur = null, showAll = location.search.includes('show');
SCREENS.forEach(s => { const o = document.createElement('option'); o.value = s.key; o.textContent = s.title; pick.appendChild(o); });
function fit() {
  if (!cur) return;
  const s = byKey[cur], st = document.getElementById('stage');
  const small = innerWidth <= 760;
  document.body.classList.toggle('small', small);
  document.body.classList.toggle('portrait', innerHeight > innerWidth);
  const pad = small ? 0 : 16;
  const k = Math.min((st.clientWidth - pad) / s.w, (st.clientHeight - pad) / s.h, 1);
  frame.style.width = (s.w * k) + 'px'; frame.style.height = (s.h * k) + 'px';
}
const hist = [];   // screens visited, so back arrows return to where you came from
function back(fallback) { const prev = hist.pop(); go(prev && byKey[prev] ? prev : fallback, true, false); }
// One door: the public site and sign in have nobody signed in. An account's own screen (a dashboard, a decision, any
// supplier portal page) signs that account in; a shared console screen keeps whoever is signed in, if their role may
// open it. Who signed in decides the dashboard (Alpha: investor → portal, staff → console).
function settle(s) {
  if (s.owner) { session = s.owner; return; }
  if (!s.console) { session = null; return; }
  if (!session || !PERM[session].includes(s.label)) session = s.viewer;
}
// Inside a session, a link may open only what that account may open: never another person's or company's own
// screen, never a menu their role lacks. Signing out (public site, sign in) is always allowed.
// A record can have the signed-in person's own copy (w21c-samuel: the application, with their decision): open that.
const resolve = k => session && byKey[k + '-' + session] ? k + '-' + session : k;
function allowed(dest) {
  const d = byKey[resolve(dest)];
  if (!d) return false;
  if (!session) return true;
  if (d.owner) return d.owner === session;
  if (d.write && !d.write.includes(ROLE[session])) return false;   // a form their role may not fill in
  if (d.console) return PERM[session].includes(d.label);
  return true;
}
const chromeEl = document.getElementById('chrome');
function go(key, push = true, record = true) {
  if (!byKey[key]) key = 'w80';
  key = resolve(key);
  if (record && cur && cur !== key) { hist.push(cur); if (hist.length > 60) hist.shift(); }
  cur = key; const s = byKey[key];
  frame.className = showAll ? 'show' : '';
  settle(s);
  const ch = s.console && session && session !== s.viewer ? (CHROME[session] || {})[s.label] : null;
  chromeEl.style.display = ch ? 'block' : 'none';
  // under a dialog the person's sidebar is dimmed with the page; a drawer covers the top-bar identity
  chromeEl.style.filter = s.modal ? 'brightness(.62)' : '';
  chromeEl.style.clipPath = s.modal === 'drawer' ? `inset(0 ${100 - SB / s.w * 100}% 0 0)` : '';
  if (ch) chromeEl.src = (CACHE[theme + ch.src] || {}).src || srcOf(ch);
  document.getElementById('who').textContent = session ? 'Signed in: ' + NAMES[session] : (AREA_LABEL[s.area] || '');
  const cached = CACHE[theme + s.src];
  if (cached && cached.complete && cached.naturalWidth) { img.src = cached.src; }
  else {
    frame.classList.add('loading');
    img.onload = () => frame.classList.remove('loading', 'failed');
    img.onerror = () => { frame.classList.remove('loading'); frame.classList.add('failed'); };
    img.src = srcOf(s);
  }
  frame.querySelectorAll('.hot').forEach(h => h.remove());
  // under a session's own sidebar, the screen's sidebar and identity hotspots give way to the session's
  const under = ([x, y, w, h]) => x < SB || (x >= IDENT[0] - 1 && y < IDENT[1] + IDENT[3]);
  const links = ch && !s.modal ? s.links.filter(l => !under(l)).concat(ch.links) : s.links;
  links.forEach(([x, y, w, h, t]) => {
    const isBack = t.startsWith('!back:'), isTab = t.startsWith('!tab:');
    const dest = isTab ? t.slice(5) : t;
    if (t !== '!theme' && !isBack && !byKey[dest]) return;
    if (t !== '!theme' && !isBack && !allowed(dest)) return;
    const a = document.createElement('div'); a.className = 'hot';
    a.title = t === '!theme' ? 'Light / dark mode' : (isBack ? 'Back' : byKey[resolve(dest)].title);
    Object.assign(a.style, { left: x / s.w * 100 + '%', top: y / s.h * 100 + '%', width: w / s.w * 100 + '%', height: h / s.h * 100 + '%' });
    a.onclick = e => { e.stopPropagation(); if (t === '!theme') toggleTheme(); else if (isBack) back(t.slice(6));
      else if (isTab) go(dest, true, false); else go(t); };
    frame.appendChild(a);
  });
  pick.value = key; fit();

  if (push) history.replaceState(null, '', '#' + key);
}
frame.addEventListener('click', () => { frame.classList.add('flash'); setTimeout(() => frame.classList.remove('flash'), 700); });
function step(d) { const i = order.indexOf(cur); go(order[(i + d + order.length) % order.length]); }
document.getElementById('prev').onclick = () => step(-1);
document.getElementById('next').onclick = () => step(1);
document.getElementById('web').onclick = () => go('w80');
pick.onchange = () => go(pick.value);
addEventListener('keydown', e => {
  if (e.target.tagName === 'SELECT') return;
  const k = e.key.toLowerCase();
  if (e.key === 'ArrowRight') step(1); else if (e.key === 'ArrowLeft') step(-1);
  else if (k === 'h') { showAll = !showAll; frame.classList.toggle('show', showAll); }
  else if (k === 'd') toggleTheme();
  else if (k === 'f') toggleFs();
});
// the moon button in the console's top bar switches light / dark (D does the same for presenters)
function toggleTheme() {
  theme = theme === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('idiu-theme', theme); } catch (e) {}
  preload(); go(cur, false);
}
const fsBtn = document.getElementById('fs');
function toggleFs() { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
fsBtn.onclick = toggleFs;
document.addEventListener('fullscreenchange', () => {
  const on = !!document.fullscreenElement;
  document.body.classList.toggle('fs', on);
  fsBtn.innerHTML = on ? '&#x2715; Exit full screen' : '&#x26F6;<span class="long"> Full screen</span>';
  setTimeout(fit, 50);
});
// in full screen the bar hides. It comes back only when the mouse touches the very bottom edge, and stays while the
// mouse is on it, so links near the bottom of a screen (the public footer) stay clickable.
addEventListener('mousemove', e => {
  if (e.clientY >= innerHeight - 3) document.body.classList.add('peek');
  else if (e.clientY < innerHeight - 52) document.body.classList.remove('peek');
});
addEventListener('resize', fit);
// a link to another screen (pasted, or typed in the address bar) opens it without reloading the page
addEventListener('hashchange', () => { const k = location.hash.slice(1); if (k && k !== cur) go(k, false); });
go(location.hash.slice(1) || 'w80', false);   // no hash: the public Home
</script></body></html>
"""


def screens():
    fns = []
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                continue
            raise
        fns += mod.SCREENS
    return sorted(fns, key=_order)


def write_prototype(built, chromes):
    data = [{"key": key, "title": title, "src": f"web/{name}.svg", "w": w, "h": h, "links": links,
             "label": meta["label"], "viewer": meta["viewer"], "owner": meta["owner"], "area": meta["area"],
             "modal": meta["modal"], "write": meta["write"],
             "console": meta["area"] == "staff"}
            for name, w, h, path, key, title, links, meta in built]
    names = {p: f"{PEOPLE[p][0]} · {PEOPLE[p][2]}" for p in SESSIONS}
    names |= {p: f"{a[0]} · {a[2]}" for p, a in SUPPLIER_ACCOUNTS.items()}
    page = (PROTO.replace("__DATA__", json.dumps(data)).replace("__CHROME__", json.dumps(chromes))
            .replace("__PERM__", json.dumps({p: menu_for(p) for p in SESSIONS} | {p: [] for p in SUPPLIER_SESSIONS})).replace("__NAMES__", json.dumps(names))
            .replace("__ROLE__", json.dumps({p: PEOPLE[p][2] for p in SESSIONS} | {p: "Supplier" for p in SUPPLIER_SESSIONS}))
            .replace("__SB__", str(shell.SB)).replace("__IDENT__", json.dumps(list(shell.IDENT))))
    with open(os.path.join(OUT, "prototype.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("prototype.html", len(data), "screens,", sum(len(d["links"]) for d in data), "hotspots,",
          sum(len(c) for c in chromes.values()), "session sidebars")


def build_chromes():
    """Each person's sidebar and identity, once per menu entry they can open (light and dark)."""
    chromes = {}
    for d in ("chrome", "chrome-dark"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for p in SESSIONS:
        chromes[p] = {}
        for label in menu_for(p):
            s = shell.chrome(p, label)
            name = f"{p}--{slug(label)}"
            svg = s.svg()
            with open(os.path.join(OUT, "chrome", name + ".svg"), "w", encoding="utf-8") as f:
                f.write(svg)
            with open(os.path.join(OUT, "chrome-dark", name + ".svg"), "w", encoding="utf-8") as f:
                f.write(theme.dark_svg(svg))
            chromes[p][label] = {"src": f"chrome/{name}.svg", "links": s.links}
    return chromes


def main():
    png = "--png" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    built = []
    for d in ("web", "web-dark"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for fn in screens():
        key = screen_key(fn)
        if only and not any(o == key or o in fn.__name__ for o in only):
            continue
        s = fn()
        name = slug(s.title)
        path = os.path.join(OUT, "web", name + ".svg")
        svg = s.svg()
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        with open(os.path.join(OUT, "web-dark", name + ".svg"), "w", encoding="utf-8") as f:
            f.write(theme.dark_svg(svg))
        built.append((name, s.w, s.h, path, key, s.title, s.links, s.meta))
        print(f"{key:5} web/{name}.svg  {os.path.getsize(path) // 1024} KB")
    if not only:
        chromes = build_chromes()
        write_prototype(built, chromes)
        # a renamed screen leaves its old file behind; a full build removes whatever it did not write
        keep = {"web": {n for n, *_ in built}, "chrome": {c["src"][7:-4] for cs in chromes.values() for c in cs.values()}}
        for folder, names in keep.items():
            for d in (folder, folder + "-dark"):
                for fn in os.listdir(os.path.join(OUT, d)):
                    if fn.endswith(".svg") and fn[:-4] not in names:
                        os.remove(os.path.join(OUT, d, fn))
                        print("removed stale", d + "/" + fn)
    if png:
        prev = os.path.join(OUT, "_previews")
        os.makedirs(prev, exist_ok=True)
        for name, w, h, path, key, *_ in built:
            renders = [(path, "")]
            if "--dark" in sys.argv:   # python build.py --png --dark: also the dark versions
                renders.append((os.path.join(OUT, "web-dark", name + ".svg"), "-dark"))
            for src, tag in renders:
                out = os.path.join(prev, f"{key}{tag}-{name}.png")
                subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                                f"--window-size={w},{h}", f"--screenshot={out}", "file:///" + src.replace("\\", "/")],
                               capture_output=True, timeout=60)
                print("png", out)


if __name__ == "__main__":
    main()
