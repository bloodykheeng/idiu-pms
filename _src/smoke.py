"""Click through the built mockup in a real browser (Playwright + Chromium), the way IDIU will use it.

    python smoke.py            # exits 1 on any failure

Serves the repo over HTTP (as Vercel does) and checks:
  load     every screen's light and dark SVG loads in the viewer (the "✓ Offline-ready" preload)
  hotspots every screen shows exactly the hotspots whose targets exist
  door     no hash opens the public Home (w80)
  walks    the public site → register → application; Home → Sign in → each person's and each supplier's walkthrough,
           clicking the real hotspots; every click must land on the expected screen, the signed-in account (and
           their sidebar) must never change, and signing out returns to Home
  dark     the D key and the moon button switch to the dark screens and back
  errors   no JavaScript errors on the page
Run build.py first; check.py covers the structure, this covers what a person actually clicks.
"""
from __future__ import annotations

import functools
import http.server
import os
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

# Each walk: one person's demo path, clicked through real hotspots. The person must stay signed in throughout:
# the viewer's session never changes on a click, only by signing in again (PLAN.md §5, sessions).
WALKS = [
    ("Public site → register", None, ["w80", "w83", "w81", "w82", "w00b", "w00", "w70", "w70b", "w70c", "w70d", "w80"]),
    ("System Admin", "ivan", ["w80", "w00", "w01-ivan", "w60", "w60c", "w60", "w60b", "w60", "w50", "w50b", "w50", "w51",
                              "w51b", "w51", "w10", "w10c", "w10", "w11", "w11b", "w14b", "w63", "w63b", "w63", "w80"]),
    ("Country Director", "samuel", ["w80", "w00", "w01-samuel", "w02b", "w02", "w13c", "w02", "w31b", "w02", "w21b",
                                    "w02", "w01-samuel", "w10", "w11", "w20", "w21", "w21c-samuel", "w21", "w30", "w31",
                                    "w31d-samuel", "w31"]),
    ("Setup lists", "ivan", ["w80", "w00", "w01-ivan", "w50", "w52", "w52b", "w52", "w53", "w53b", "w53", "w55",
                             "w55b", "w55", "w56", "w56b", "w56", "w57", "w57b", "w57", "w58", "w58b", "w58"]),
    ("Head of Department", "daniel", ["w80", "w00", "w01-daniel", "w03b", "w03", "w01-daniel", "w41"]),
    ("Procurement Officer", "joseph", ["w80", "w00", "w01-joseph", "w12b", "w12", "w12c", "w13d", "w14b", "w15d",
                                       "w15c", "w11c", "w11", "w01-joseph", "w21", "w21c", "w21"]),
    ("Finance Officer", "ruth", ["w80", "w00", "w01-ruth", "w30c", "w30d", "w30", "w30e", "w30", "w30b", "w11", "w30b",
                                 "w31c", "w31", "w31d", "w31", "w02-ruth"]),
    ("Requester", "grace", ["w80", "w00", "w01-grace", "w10b", "w10", "w10c", "w10", "w11", "w01-grace", "w80"]),
    ("Committee member", "esther", ["w80", "w00", "w01-esther", "w13b", "w13-esther", "w13d"]),
    ("Stores", "peter", ["w80", "w00", "w01-peter", "w15b", "w15", "w15d", "w14"]),
    ("Auditor", "agnes", ["w80", "w00", "w01-agnes", "w11c", "w11", "w30b", "w63", "w63b", "w63"]),
    ("Supplier", "busoga", ["w80", "w00", "w71", "w72", "w73", "w74", "w74b", "w75", "w76", "w77", "w77b", "w77",
                            "w71", "w80"]),
    ("Applicant", "mpumudde", ["w80", "w00", "w70d", "w80"]),
]


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(_Quiet, directory=OUT)
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/prototype.html"


def main():
    httpd, url = serve()
    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1126})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url)
        screens = page.evaluate("SCREENS")
        by_key = {s["key"]: s for s in screens}
        page.wait_for_function("document.getElementById('ready').textContent.includes('Offline-ready')", timeout=120_000)
        print(f"load      {len(screens)} light screens preloaded")

        # every screen, opened fresh (signed in as that screen's own person): the image loads, and it shows exactly
        # the hotspots whose targets exist and that this person may open
        perm = page.evaluate("PERM")

        role = page.evaluate("ROLE")

        def resolve(dest, person):   # the person's own copy of a record (w21c-samuel), as the viewer opens it
            return f"{dest}-{person}" if person and f"{dest}-{person}" in by_key else dest

        def allowed(person, dest):   # the viewer's allowed(): never another account's own screen, nor a form not theirs
            d = by_key[resolve(dest, person)]
            if not person:
                return True
            if d["owner"]:
                return d["owner"] == person
            if d["write"] and role[person] not in d["write"]:
                return False
            if d["console"]:
                return d["label"] in perm[person]
            return True

        def signed_in(s, person):    # who the viewer has signed in on screen s, walking as person
            return s["owner"] or (person if s["console"] else None)

        home_of = {"agnes": "w01-agnes", "samuel": "w01-samuel", "daniel": "w01-daniel"}

        # no hash: the public Home
        page.goto(url)
        if page.evaluate("cur") != "w80":
            failures.append(f"door: no hash opened {page.evaluate('cur')}, expected w80 (public Home)")
        print("door      no hash opens the public Home")

        for s in screens:
            page.evaluate("session = null")
            page.goto(f"{url}#{s['key']}")
            page.wait_for_function("document.getElementById('img').complete && document.getElementById('img').naturalWidth > 0")
            person = s["owner"] or (s["viewer"] if s["console"] else None)
            want = 0
            for *_, t in s["links"]:
                dest = t[5:] if t.startswith("!tab:") else t
                if t == "!theme" or t.startswith("!back:") or (dest in by_key and allowed(person, dest)):
                    want += 1
            got = page.locator(".hot").count()
            if got != want:
                failures.append(f"{s['key']}: {got} hotspots on screen, expected {want}")
        print(f"hotspots  {len(screens)} screens checked")

        # walks: click the hotspot that opens the next screen; the signed-in person must never change
        for name, person, path in WALKS:
            page.goto(f"{url}#{path[0]}")
            for cur, nxt in zip(path, path[1:]):
                title = by_key[nxt]["title"]
                hot = page.locator(f'.hot[title="{title}"]')
                if hot.count() == 0:
                    failures.append(f"walk {name}: no hotspot on {cur} opens {nxt} ({title})")
                    break
                hot.last.click()   # the topmost one, as a real mouse would hit it
                got = page.evaluate("location.hash.slice(1)")
                if got != nxt:
                    failures.append(f"walk {name}: clicking towards {nxt} on {cur} landed on {got}")
                    break
                who = page.evaluate("session")
                want = signed_in(by_key[nxt], person)
                if who != want:
                    failures.append(f"walk {name}: on {nxt} the signed-in person is {who}, expected {want}")
                    break
                s = by_key[nxt]
                if s["console"] and s["viewer"] != person:
                    src = page.evaluate("document.getElementById('chrome').style.display === 'block' && document.getElementById('chrome').src")
                    if not src or f"/{person}--" not in src:
                        failures.append(f"walk {name}: on {nxt} the sidebar is not {person}'s ({src})")
                        break
            else:
                print(f"walk      {name}: {' → '.join(path)}")

        # forms: the Auditor fills in nothing, and budgets are Finance's to prepare
        for person, screen, form in [("agnes", "w60", "w60c"), ("agnes", "w10", "w10c"), ("agnes", "w30", "w30e"),
                                     ("samuel", "w30", "w30e"), ("daniel", "w10", "w10c")]:
            page.goto(f"{url}#{home_of[person]}")
            page.evaluate(f"go('{screen}')")
            n = page.locator(f'.hot[title="{by_key[form]["title"]}"]').count()
            if (n > 0) != (form == "w10c" and person == "daniel"):
                failures.append(f"forms: signed in as {person}, {screen} shows {n} hotspot(s) to {form}")
        print("forms     Auditor reads only; New budget only for Finance and the System Admin")
        # under a dialog: the person's sidebar is dimmed and nothing under the backdrop is clickable
        page.goto(f"{url}#w01-ruth")
        page.evaluate("go('w50'); go('w50b')")
        left = page.evaluate("[...document.querySelectorAll('.hot')].filter(h => parseFloat(h.style.left) < SB / 19.2).length")
        dim = page.evaluate("document.getElementById('chrome').style.filter")
        if left or "brightness" not in dim or page.evaluate("session") != "ruth":
            failures.append(f"modal: on w50b as ruth, {left} sidebar hotspot(s), chrome filter '{dim}'")
        print("modal     under a dialog the sidebar is dimmed and not clickable")

        # full screen: hovering the public footer's links must not raise the bar over them; the very bottom edge does
        page.goto(f"{url}#w80")
        page.evaluate("document.body.classList.add('fs')")
        page.mouse.move(1500, page.viewport_size["height"] - 40)
        over = page.evaluate("document.body.classList.contains('peek')")
        page.mouse.move(1500, page.viewport_size["height"] - 1)
        edge = page.evaluate("document.body.classList.contains('peek')")
        if over or not edge:
            failures.append(f"full screen: bar raised over the footer {over}, at the bottom edge {edge}")
        page.evaluate("document.body.classList.remove('fs', 'peek')")
        print("fullscr   footer links stay clickable; the bar comes up at the bottom edge")

        # dark mode: D key, then the moon button in the console's top bar
        page.goto(f"{url}#w01-joseph")
        page.keyboard.press("d")
        page.wait_for_function("document.getElementById('ready').textContent.includes('Offline-ready')", timeout=120_000)
        src = page.evaluate("document.getElementById('img').src")
        if "/web-dark/" not in src:
            failures.append(f"dark: D key did not switch to the dark screen ({src})")
        page.locator('.hot[title="Light / dark mode"]').first.click()
        if "/web-dark/" in page.evaluate("document.getElementById('img').src"):
            failures.append("dark: the moon button did not switch back to light")
        print("dark      all dark screens preloaded; D key and moon button switch")
        browser.close()
    httpd.shutdown()

    if errors:
        failures += [f"page error: {e}" for e in errors]
    if failures:
        print(f"\n{len(failures)} failure(s):")
        for f in failures:
            print("  ✗", f)
        sys.exit(1)
    print("✓ smoke test passed")


if __name__ == "__main__":
    main()
