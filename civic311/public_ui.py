"""Static public UI shell for Civic311 v0.1.1."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing Civic311 sample page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Civic311 Resident Service Request Support</title>
<style>
  :root { --ink:#17202a; --muted:#5c6470; --blue:#214f7a; --green:#2f654c; --gold:#d8ad48; --line:#ccd5df; }
  * { box-sizing: border-box; }
  html, body { max-width:100%; overflow-x:hidden; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:linear-gradient(135deg,#eef8ff,#fff8ed); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:999px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:100%; max-width:1120px; margin:0 auto; padding-left:16px; padding-right:16px; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.18em; font-weight:800; font-size:.78rem; }
  h1 { max-width:980px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.2rem,7vw,5.4rem); line-height:1.02; letter-spacing:-.04em; overflow-wrap:break-word; word-break:break-word; }
  .lede { max-width:840px; font-size:clamp(1.1rem,2.4vw,1.45rem); line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:999px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,minmax(0,1fr)); gap:18px; min-width:0; }
  .card { grid-column:span 6; min-width:0; max-width:100%; padding:24px; border:1px solid var(--line); border-radius:28px; background:rgba(255,255,255,.92); box-shadow:0 18px 40px rgba(35,43,50,.10); }
  .card.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; letter-spacing:-.03em; }
  h2 { margin:0 0 14px; font-size:clamp(1.8rem,4vw,3rem); }
  p, li { line-height:1.65; overflow-wrap:anywhere; }
  textarea, button { width:100%; max-width:100%; min-width:0; border:1px solid #b9c6cc; border-radius:16px; padding:.85rem 1rem; font:inherit; }
  textarea { background:#f7f8fb; color:var(--ink); }
  button { width:fit-content; min-width:190px; border:0; background:var(--blue); color:white; font-weight:900; cursor:default; }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:18px; background:white; }
  .warning { border-left-color:#b2603f; background:#fff8f4; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) { header{padding-top:34px}h1{font-size:clamp(1.95rem,10vw,2.55rem)}.lede{font-size:1.02rem}.card{grid-column:span 12;padding:20px;border-radius:22px}button{width:100%;white-space:normal} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / Civic311 public sample</p>
  <h1>Resident requests routed without black-box dispatch.</h1>
  <p class="lede">Civic311 demonstrates service-request intake support: request stubs, deterministic triage, duplicate-candidate review, department routing checklists, and Open311-compatible export artifacts without creating official work orders.</p>
  <p><span class="badge">v0.1.1 resident service request foundation</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="card large">
      <p class="kicker">Sample service request</p>
      <h2 id="lookup-title">Pothole near the library</h2>
      <textarea aria-label="Sample request notes" rows="4">Resident reports a pothole near the library entrance. Confirm category, location, duplicate requests, accessibility impacts, and department ownership.</textarea>
      <button type="button">Draft sample intake file</button>
      <div class="result" role="status" aria-live="polite">
        <h3>Staff review packet</h3>
        <ul><li>Confirm location, category, urgency, and contact preference.</li><li>Check duplicate candidates before assignment.</li><li>Prepare resident acknowledgment and Open311-compatible export artifact.</li></ul>
      </div>
    </article>
    <article class="card"><p class="kicker">Triage</p><h2>Department hints</h2><div class="result"><p>Civic311 suggests a routing bucket; staff confirm ownership before assignment.</p></div></article>
    <article class="card"><p class="kicker">Duplicates</p><h2>Review, don't suppress</h2><div class="result"><p>Duplicate candidates are surfaced for staff review; requests are never merged automatically.</p></div></article>
    <article class="card"><p class="kicker">Export</p><h2>Open311-ready</h2><div class="result"><p>Exports preserve standard field names for a future official 311 or work-order handoff.</p></div></article>
    <article class="card large"><p class="kicker">Boundary</p><h2>No official dispatch</h2><div class="result warning"><p>Civic311 does not create official work orders, dispatch crews, handle emergencies, provide legal advice, call live LLMs, write back to 311 systems, or replace the system of record.</p></div></article>
  </section>
</main>
<footer><p>Civic311 is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
</body>
</html>
"""
