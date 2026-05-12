#!/usr/bin/env python3
"""Build the final single-file HTML study app from econ_data.json."""
import json
from pathlib import Path

DATA = json.load(open('/Users/chaitanyasingh/workspace/econ_data.json'))
OUT = Path('/Users/chaitanyasingh/workspace/econ_study_app.html')

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Econ Study Lab · Krugman AP® · IEO Prep</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #fafaf6;
    --panel: #ffffff;
    --line: #e5e3dc;
    --line-soft: #efece4;
    --ink: #0f172a;
    --ink-soft: #475569;
    --ink-mute: #94a3b8;
    --micro: #2563eb;
    --micro-bg: #eff6ff;
    --micro-line: #c7dbff;
    --macro: #c2410c;
    --macro-bg: #fff5ec;
    --macro-line: #ffd9b3;
    --finlit: #047857;
    --finlit-bg: #ecfdf5;
    --finlit-line: #b7e8c8;
    --warn: #b45309;
    --warn-bg: #fffbeb;
    --green: #15803d;
    --red: #b91c1c;
    --shadow: 0 1px 2px rgba(15,23,42,.04), 0 4px 18px rgba(15,23,42,.06);
    --radius: 14px;
    --radius-sm: 9px;
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0; background: var(--bg);
    color: var(--ink);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-size: 14.5px;
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
  }
  .mono { font-family: 'JetBrains Mono', ui-monospace, Menlo, monospace; }

  /* ── Top bar ─────────────────────────────────────────────────── */
  header.top {
    position: sticky; top: 0; z-index: 30;
    background: rgba(250,250,246,.92);
    backdrop-filter: saturate(160%) blur(8px);
    border-bottom: 1px solid var(--line);
  }
  .top-row { max-width: 1380px; margin: 0 auto; padding: 14px 28px; display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
  .brand { font-weight: 800; font-size: 18px; letter-spacing: -0.01em; }
  .brand .dot { display: inline-block; width: 9px; height: 9px; background: linear-gradient(135deg,#2563eb,#c2410c); border-radius: 50%; margin-right: 8px; vertical-align: middle; }
  .sub { color: var(--ink-soft); font-size: 12.5px; }
  .spacer { flex: 1; }
  .search { display: flex; align-items: center; gap: 8px; background: white; border: 1px solid var(--line); border-radius: 999px; padding: 6px 12px; min-width: 280px; }
  .search input { border: 0; outline: 0; background: transparent; font-family: inherit; font-size: 13.5px; flex: 1; color: var(--ink); }
  .search svg { width: 14px; height: 14px; color: var(--ink-mute); }

  /* ── Category & tab chips ────────────────────────────────────── */
  .chips { display: flex; gap: 8px; flex-wrap: wrap; }
  .chip {
    border: 1px solid var(--line); background: white; padding: 6px 12px;
    border-radius: 999px; font-size: 12.5px; font-weight: 600;
    color: var(--ink-soft); cursor: pointer; transition: all .12s ease;
    user-select: none;
  }
  .chip:hover { border-color: var(--ink); color: var(--ink); }
  .chip.active { background: var(--ink); color: white; border-color: var(--ink); }
  .chip.micro.active { background: var(--micro); border-color: var(--micro); }
  .chip.macro.active { background: var(--macro); border-color: var(--macro); }
  .chip.finlit.active { background: var(--finlit); border-color: var(--finlit); }

  .tabs { max-width: 1380px; margin: 0 auto; padding: 0 28px 12px; display: flex; gap: 4px; }
  .tab {
    padding: 10px 16px; cursor: pointer; font-weight: 600; font-size: 13.5px;
    color: var(--ink-soft); border-bottom: 2px solid transparent; transition: all .12s;
  }
  .tab:hover { color: var(--ink); }
  .tab.active { color: var(--ink); border-bottom-color: var(--ink); }
  .tab .count { font-size: 11px; color: var(--ink-mute); margin-left: 4px; font-weight: 500; }

  /* ── Main ────────────────────────────────────────────────────── */
  main { max-width: 1380px; margin: 0 auto; padding: 24px 28px 80px; }
  .summary-bar { display: flex; gap: 14px; align-items: baseline; margin-bottom: 18px; flex-wrap: wrap; }
  .summary-bar h2 { margin: 0; font-size: 20px; letter-spacing: -0.01em; }
  .summary-bar .sublabel { color: var(--ink-soft); font-size: 13px; }

  /* Card grid */
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 14px; }
  .card {
    background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius);
    padding: 16px 16px 14px; box-shadow: var(--shadow);
    display: flex; flex-direction: column; gap: 8px;
    transition: transform .12s ease, box-shadow .12s ease;
  }
  .card:hover { transform: translateY(-1px); box-shadow: 0 2px 6px rgba(15,23,42,.05), 0 12px 28px rgba(15,23,42,.08); }
  .card h3 { margin: 0; font-size: 15px; line-height: 1.35; letter-spacing: -0.005em; }
  .card .meta { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
  .tag {
    font-size: 10.5px; font-weight: 700; letter-spacing: 0.03em;
    padding: 2px 7px; border-radius: 5px; text-transform: uppercase;
  }
  .tag.micro { background: var(--micro-bg); color: var(--micro); }
  .tag.macro { background: var(--macro-bg); color: var(--macro); }
  .tag.finlit { background: var(--finlit-bg); color: var(--finlit); }
  .tag.page { background: #f1f5f9; color: var(--ink-soft); }
  .tag.diff-easy { background: #ecfdf5; color: #047857; }
  .tag.diff-medium { background: #eff6ff; color: #1d4ed8; }
  .tag.diff-hard { background: #fef3c7; color: #92400e; }
  .tag.diff-olympiad { background: #fce7f3; color: #be185d; }
  .tag.type-conceptual { background: #f1f5f9; color: var(--ink-soft); }
  .tag.type-numerical { background: #eef2ff; color: #4338ca; }

  .field { font-size: 13.5px; }
  .field .lbl {
    display: inline-block; min-width: 64px; color: var(--ink-mute);
    font-weight: 700; font-size: 10.5px; letter-spacing: 0.05em; text-transform: uppercase;
    margin-right: 6px; vertical-align: top;
  }
  .field .val { color: var(--ink); }
  .field .val .em { font-weight: 700; color: var(--ink); }

  .card .mnemonic {
    border-left: 3px solid var(--warn); background: var(--warn-bg);
    padding: 8px 10px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 13px; color: #78350f;
  }
  .card .mnemonic strong { color: var(--warn); }
  .card .related { font-size: 12px; color: var(--ink-soft); }
  .card .equation {
    background: #0f172a; color: #f8fafc; padding: 10px 12px; border-radius: var(--radius-sm);
    font-family: 'JetBrains Mono', monospace; font-size: 13px; overflow-x: auto;
  }
  .card .example { background: #f8fafc; border: 1px solid var(--line-soft); border-radius: var(--radius-sm); padding: 8px 10px; font-size: 12.5px; }
  .card .example strong { color: var(--ink-soft); font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.05em; }

  /* ── Formula card (extra polish) ─────────────────────────────── */
  .formula-card {
    background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius);
    padding: 18px 18px 16px; box-shadow: var(--shadow);
    display: flex; flex-direction: column; gap: 12px;
    transition: transform .12s ease, box-shadow .12s ease;
    position: relative; overflow: hidden;
  }
  .formula-card:hover { transform: translateY(-1px); box-shadow: 0 2px 6px rgba(15,23,42,.05), 0 12px 28px rgba(15,23,42,.08); }
  .formula-card::before {
    content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
    background: linear-gradient(180deg, var(--micro), var(--macro));
    opacity: 0.85;
  }
  .formula-card.cat-micro::before { background: var(--micro); }
  .formula-card.cat-macro::before { background: var(--macro); }
  .formula-card.cat-finlit::before { background: var(--finlit); }
  .formula-card .fhead { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .formula-card .fhead h3 {
    margin: 0; font-size: 15.5px; line-height: 1.3; letter-spacing: -0.005em;
    font-weight: 700;
  }
  .formula-card .eqn {
    background: linear-gradient(180deg, #fefcf6, #faf7ec);
    border: 1px solid #efe6cc;
    border-radius: 12px;
    padding: 18px 18px;
    text-align: center;
    position: relative;
  }
  .formula-card .eqn .eqn-label {
    position: absolute; top: 7px; left: 12px;
    font-size: 9.5px; letter-spacing: 0.08em; text-transform: uppercase;
    color: #b69148; font-weight: 700;
  }
  .formula-card .eqn .eqn-body {
    font-family: 'Cambria Math', 'STIX Two Math', 'Cambria', Georgia, serif;
    font-size: 17px; line-height: 1.7; color: #1a1305;
    word-break: break-word; padding-top: 4px;
  }
  .formula-card .eqn .eqn-body .v { font-style: italic; }      /* variables */
  .formula-card .eqn .eqn-body .op { color: #c2410c; font-weight: 600; padding: 0 2px; }   /* operators */
  .formula-card .eqn .eqn-body .num { color: #1d4ed8; font-weight: 600; }                    /* numbers */
  .formula-card .eqn .eqn-body .eq { color: #047857; font-weight: 700; padding: 0 6px; }     /* equals */
  .formula-card .vars-grid {
    display: grid; grid-template-columns: 1fr; gap: 4px;
    font-size: 13px; color: var(--ink-soft);
  }
  .formula-card .var-item {
    display: flex; gap: 8px; padding: 3px 0;
  }
  .formula-card .var-item .sym {
    font-family: 'Cambria Math', Georgia, serif; font-style: italic; font-weight: 600;
    color: var(--ink); min-width: 38px; font-size: 14px;
  }
  .formula-card .notes {
    font-size: 12.5px; color: var(--ink-soft); border-top: 1px dashed var(--line-soft);
    padding-top: 9px;
  }
  .formula-card .notes strong {
    font-size: 9.5px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--ink-mute); font-weight: 700; display: block; margin-bottom: 3px;
  }
  .formula-card .ex {
    background: #f0f7ff; border: 1px solid #cfe2ff; border-radius: 10px;
    padding: 11px 13px; font-size: 12.8px; line-height: 1.55; color: #0c2d6b;
  }
  .formula-card .ex .ex-label {
    display: inline-block; font-size: 9.5px; font-weight: 800; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--micro); margin-bottom: 4px;
  }
  .formula-card .ex .answer-pill {
    display: inline-block; background: #1d4ed8; color: white;
    padding: 1px 8px; border-radius: 4px; font-weight: 700;
    font-family: 'Cambria Math', Georgia, serif;
  }

  /* ── Quiz ────────────────────────────────────────────────────── */
  .quiz-config {
    background: white; border: 1px solid var(--line); border-radius: var(--radius);
    padding: 22px 24px; box-shadow: var(--shadow); max-width: 760px;
  }
  .quiz-config h2 { margin: 0 0 4px; font-size: 22px; letter-spacing: -0.01em; }
  .quiz-config p.lede { margin: 0 0 22px; color: var(--ink-soft); }
  .config-row { margin-bottom: 16px; }
  .config-row .label { font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: var(--ink-soft); text-transform: uppercase; margin-bottom: 7px; }
  .opt-group { display: flex; gap: 6px; flex-wrap: wrap; }
  .opt {
    padding: 8px 14px; border: 1px solid var(--line); border-radius: 9px;
    background: white; cursor: pointer; font-weight: 600; font-size: 13px;
    color: var(--ink-soft); transition: all .12s;
  }
  .opt:hover { border-color: var(--ink); color: var(--ink); }
  .opt.active { background: var(--ink); color: white; border-color: var(--ink); }
  .opt-group.cats .opt.active[data-val=MICRO] { background: var(--micro); border-color: var(--micro); }
  .opt-group.cats .opt.active[data-val=MACRO] { background: var(--macro); border-color: var(--macro); }
  .opt-group.cats .opt.active[data-val=FIN-LIT] { background: var(--finlit); border-color: var(--finlit); }
  .start-btn {
    margin-top: 8px; padding: 12px 22px;
    background: var(--ink); color: white; border: 0;
    border-radius: 10px; font-weight: 700; font-size: 14px; cursor: pointer;
    font-family: inherit; transition: transform .1s;
  }
  .start-btn:hover { transform: translateY(-1px); }
  .start-btn:disabled { background: var(--ink-mute); cursor: not-allowed; transform: none; }

  /* Quiz runner */
  .quiz-stage { display: grid; grid-template-columns: 1fr 280px; gap: 22px; align-items: start; }
  @media (max-width: 880px) { .quiz-stage { grid-template-columns: 1fr; } }
  .qcard {
    background: white; border: 1px solid var(--line); border-radius: var(--radius);
    padding: 22px 24px 24px; box-shadow: var(--shadow); min-height: 320px;
  }
  .q-topic { font-size: 14px; color: var(--ink-soft); font-weight: 600; margin-bottom: 4px; }
  .q-text {
    font-size: 16px; line-height: 1.55; color: var(--ink); margin: 8px 0 18px;
  }
  .choices { display: grid; gap: 9px; }
  .choice-btn {
    text-align: left; padding: 12px 14px 12px 12px; background: white;
    border: 1.5px solid var(--line); border-radius: 11px; cursor: pointer;
    font-family: inherit; font-size: 14px; line-height: 1.45; color: var(--ink);
    display: flex; gap: 12px; align-items: flex-start;
    transition: border-color .1s, background .1s, transform .05s;
    width: 100%;
  }
  .choice-btn:hover:not(:disabled) { border-color: var(--ink); background: #f6f7f9; }
  .choice-btn:active:not(:disabled) { transform: scale(0.995); background: #eef0f3; }
  .choice-btn:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }
  .choice-btn * { pointer-events: none; }  /* clicks on inner spans bubble to button */
  .choice-btn .letter {
    font-weight: 700; color: var(--ink-mute); min-width: 22px;
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; background: #f1f5f9; border-radius: 6px;
    font-size: 12.5px;
  }
  .choice-btn.correct { border-color: var(--green); background: #ecfdf5; color: #064e3b; }
  .choice-btn.correct .letter { color: white; background: var(--green); }
  .choice-btn.wrong { border-color: var(--red); background: #fef2f2; color: #7f1d1d; }
  .choice-btn.wrong .letter { color: white; background: var(--red); }
  .choice-btn:disabled { cursor: default; }
  .free-input {
    width: 100%; padding: 11px 14px; border: 1.5px solid var(--line); border-radius: 11px;
    font-family: inherit; font-size: 14px; color: var(--ink);
  }
  .free-input:focus { outline: 0; border-color: var(--ink); }
  .free-submit {
    margin-top: 10px; padding: 10px 18px; background: var(--ink); color: white;
    border: 0; border-radius: 9px; font-weight: 700; font-size: 13px; cursor: pointer;
    font-family: inherit;
  }
  .explain {
    margin-top: 16px; border-left: 3px solid var(--ink); background: #f8fafc;
    padding: 12px 14px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 13.5px; line-height: 1.55;
  }
  .explain.right { border-left-color: var(--green); background: #ecfdf5; }
  .explain.wrong { border-left-color: var(--red); background: #fef2f2; }
  .explain .verdict { font-weight: 800; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; margin-bottom: 4px; }
  .explain .verdict.right { color: var(--green); }
  .explain .verdict.wrong { color: var(--red); }
  .quiz-actions { display: flex; gap: 8px; margin-top: 14px; justify-content: space-between; align-items: center; }
  .pill-btn {
    padding: 9px 16px; background: var(--ink); color: white; border: 0; border-radius: 9px;
    font-weight: 700; font-size: 13px; cursor: pointer; font-family: inherit;
  }
  .pill-btn.ghost { background: white; color: var(--ink-soft); border: 1px solid var(--line); }
  .pill-btn.ghost:hover { color: var(--ink); border-color: var(--ink); }

  .qsidebar {
    background: white; border: 1px solid var(--line); border-radius: var(--radius);
    padding: 18px 18px; box-shadow: var(--shadow); position: sticky; top: 130px;
  }
  .qsidebar h4 { margin: 0 0 12px; font-size: 13px; color: var(--ink-soft); text-transform: uppercase; letter-spacing: 0.04em; }
  .progress { height: 8px; background: var(--line-soft); border-radius: 4px; overflow: hidden; margin-bottom: 14px; }
  .progress > div { height: 100%; background: linear-gradient(90deg, var(--micro), var(--macro)); transition: width .3s; }
  .stat-row { display: flex; justify-content: space-between; padding: 7px 0; border-top: 1px solid var(--line-soft); font-size: 13px; }
  .stat-row:first-of-type { border-top: 0; }
  .stat-row .val { font-weight: 700; }
  .stat-row .val.green { color: var(--green); }
  .stat-row .val.red { color: var(--red); }

  /* Results */
  .results {
    background: white; border: 1px solid var(--line); border-radius: var(--radius);
    padding: 26px 28px; box-shadow: var(--shadow); max-width: 720px;
  }
  .results h2 { margin: 0 0 4px; font-size: 24px; }
  .big-score { font-size: 60px; font-weight: 800; letter-spacing: -0.02em; }
  .big-score .denom { color: var(--ink-mute); font-size: 32px; font-weight: 600; }
  .breakdown { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0; }
  .bdcell { background: #f8fafc; border: 1px solid var(--line-soft); border-radius: 9px; padding: 12px 14px; }
  .bdcell .lbl { font-size: 10.5px; color: var(--ink-soft); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; }
  .bdcell .v { font-size: 22px; font-weight: 700; margin-top: 2px; }

  /* Synthesis */
  .synth-list { display: grid; gap: 10px; }
  .synth-card {
    background: white; border: 1px solid var(--line); border-radius: var(--radius);
    padding: 14px 18px; display: flex; gap: 14px; align-items: flex-start; box-shadow: var(--shadow);
  }
  .synth-card .num { color: var(--ink-mute); font-family: 'JetBrains Mono', monospace; font-size: 12px; margin-top: 3px; }
  .synth-card p { margin: 0; font-size: 14px; line-height: 1.55; }

  /* Map */
  .map-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
  @media (max-width: 760px) { .map-grid { grid-template-columns: 1fr; } }
  .chunk-card {
    background: white; border: 1px solid var(--line); border-radius: var(--radius);
    padding: 14px 18px; box-shadow: var(--shadow);
  }
  .chunk-card h4 { margin: 0 0 4px; font-size: 14px; }
  .chunk-card .pages { color: var(--ink-soft); font-size: 12px; font-family: 'JetBrains Mono', monospace; }
  .chunk-card ul { margin: 8px 0 0; padding-left: 20px; font-size: 13px; color: var(--ink-soft); }
  .chunk-card ul li { margin-bottom: 2px; }

  /* Empty state */
  .empty { text-align: center; padding: 60px 20px; color: var(--ink-mute); font-size: 14px; }
  .empty strong { color: var(--ink-soft); display: block; margin-bottom: 4px; }
  .hidden { display: none !important; }
</style>
</head>
<body>
<header class="top">
  <div class="top-row">
    <div>
      <div class="brand"><span class="dot"></span>Econ Study Lab</div>
      <div class="sub">Krugman's <em>Economics for AP®</em> · 2e · IEO Prep · 942 pp condensed</div>
    </div>
    <div class="spacer"></div>
    <div class="chips" id="catChips">
      <div class="chip active" data-cat="ALL">All</div>
      <div class="chip micro" data-cat="MICRO">Microeconomics</div>
      <div class="chip macro" data-cat="MACRO">Macroeconomics</div>
      <div class="chip finlit" data-cat="FIN-LIT">Financial Literacy</div>
    </div>
    <label class="search">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.5-4.5"/></svg>
      <input id="searchBox" placeholder="Search concepts, figures, formulas…" />
    </label>
  </div>
  <div class="tabs" id="tabs">
    <div class="tab active" data-tab="concepts">Concepts <span class="count" id="cnt-concepts"></span></div>
    <div class="tab" data-tab="figures">Figures <span class="count" id="cnt-figures"></span></div>
    <div class="tab" data-tab="formulas">Formulas <span class="count" id="cnt-formulas"></span></div>
    <div class="tab" data-tab="quiz">Quiz <span class="count" id="cnt-quiz"></span></div>
    <div class="tab" data-tab="synthesis">High-Yield <span class="count" id="cnt-synth"></span></div>
    <div class="tab" data-tab="map">Book Map</div>
  </div>
</header>

<main>
  <section id="view-concepts"></section>
  <section id="view-figures" class="hidden"></section>
  <section id="view-formulas" class="hidden"></section>
  <section id="view-quiz" class="hidden"></section>
  <section id="view-synthesis" class="hidden"></section>
  <section id="view-map" class="hidden"></section>
</main>

<script id="econ-data" type="application/json">__DATA__</script>
<script>
(function(){
  const DATA = JSON.parse(document.getElementById('econ-data').textContent);
  let state = {
    tab: 'concepts',
    category: 'ALL',     // ALL | MICRO | MACRO | FIN-LIT
    search: '',
    quiz: null,          // active quiz state object
  };

  // ── Counts in tab bar ───────────────────────────────────────────
  function setCounts() {
    document.getElementById('cnt-concepts').textContent = DATA.concepts.length;
    document.getElementById('cnt-figures').textContent = DATA.figures.length;
    document.getElementById('cnt-formulas').textContent = DATA.formulas.length;
    document.getElementById('cnt-quiz').textContent = DATA.questions.length;
    document.getElementById('cnt-synth').textContent = DATA.synthesis.length;
  }

  // ── Category helpers ────────────────────────────────────────────
  const CAT_CLASS = { 'MICRO': 'micro', 'MACRO': 'macro', 'FIN-LIT': 'finlit' };
  const CAT_LABEL = { 'MICRO': 'Micro', 'MACRO': 'Macro', 'FIN-LIT': 'Fin Lit' };
  function passesCategory(item) {
    if (state.category === 'ALL') return true;
    return item.category === state.category;
  }
  function passesSearch(item, fields) {
    if (!state.search) return true;
    const q = state.search.toLowerCase();
    return fields.some(f => (f || '').toLowerCase().includes(q));
  }
  function tagFor(cat) {
    const cls = CAT_CLASS[cat] || '';
    const lbl = CAT_LABEL[cat] || cat;
    return `<span class="tag ${cls}">${lbl}</span>`;
  }
  function chunkPageRange(chunk) {
    const c = DATA.chunks.find(x => x.chunk === chunk);
    if (!c) return '';
    const ranges = [[1,95],[96,190],[191,285],[286,380],[381,475],[476,570],[571,665],[666,760],[761,855],[856,942]];
    const [a,b] = ranges[chunk-1] || [0,0];
    return `pp. ${a}–${b}`;
  }
  function esc(s){return (s||'').replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}

  // ── Render: Concepts ────────────────────────────────────────────
  function renderConcepts() {
    const items = DATA.concepts.filter(c => passesCategory(c) && passesSearch(c, [c.name,c.definition,c.mnemonic,c.related,c.why]));
    const root = document.getElementById('view-concepts');
    root.innerHTML = `
      <div class="summary-bar">
        <h2>Key Concepts</h2>
        <span class="sublabel">${items.length} of ${DATA.concepts.length} · each with a mnemonic hook</span>
      </div>
      ${items.length === 0 ? `<div class="empty"><strong>No matches.</strong>Try clearing search or switching category.</div>` :
        `<div class="grid">${items.map(c => `
          <article class="card">
            <div class="meta">${tagFor(c.category)} <span class="tag page">chunk ${c.chunk}</span></div>
            <h3>${esc(c.name)}</h3>
            <div class="field"><span class="lbl">Def</span><span class="val">${esc(c.definition)}</span></div>
            ${c.why ? `<div class="field"><span class="lbl">Why</span><span class="val">${esc(c.why)}</span></div>` : ''}
            ${c.mnemonic ? `<div class="mnemonic"><strong>Mnemonic ·</strong> ${esc(c.mnemonic)}</div>` : ''}
            ${c.related ? `<div class="related"><em>Related:</em> ${esc(c.related)}</div>` : ''}
          </article>`).join('')}
        </div>`}`;
  }

  // ── Render: Figures ─────────────────────────────────────────────
  function renderFigures() {
    const items = DATA.figures.filter(f => passesCategory(f) && passesSearch(f, [f.name,f.what_shows,f.axes,f.shifts,f.memorize]));
    const root = document.getElementById('view-figures');
    root.innerHTML = `
      <div class="summary-bar">
        <h2>Important Figures</h2>
        <span class="sublabel">${items.length} of ${DATA.figures.length} · open the PDF to the cited page to see the graphic</span>
      </div>
      ${items.length === 0 ? `<div class="empty"><strong>No matches.</strong></div>` :
        `<div class="grid">${items.map(f => `
          <article class="card">
            <div class="meta">${tagFor(f.category)} ${f.page ? `<span class="tag page">p. ${esc(f.page)}</span>` : ''} <span class="tag page">chunk ${f.chunk}</span></div>
            <h3>${esc(f.name)}</h3>
            ${f.what_shows ? `<div class="field"><span class="lbl">Shows</span><span class="val">${esc(f.what_shows)}</span></div>` : ''}
            ${f.axes ? `<div class="field"><span class="lbl">Axes</span><span class="val">${esc(f.axes)}</span></div>` : ''}
            ${f.shifts ? `<div class="field"><span class="lbl">Shape</span><span class="val">${esc(f.shifts)}</span></div>` : ''}
            ${f.memorize ? `<div class="mnemonic"><strong>Memorize ·</strong> ${esc(f.memorize)}</div>` : ''}
          </article>`).join('')}
        </div>`}`;
  }

  // Equation prettifier — highlight =, operators, numbers, and split multi-equation lines
  function prettifyEquation(raw) {
    if (!raw) return '';
    // Split into separate equations on '. ' / '; ' (preserve readability)
    let lines = raw.split(/(?:\.\s+|;\s+|\s+OR\s+|\s+or\s+)(?=[A-Za-z\(])/);
    // Filter out trailing punctuation-only fragments
    lines = lines.map(l => l.trim().replace(/\.$/, '')).filter(Boolean);
    return lines.map(line => {
      let h = esc(line);
      // Highlight equality signs (don't touch >=, <=, ≠)
      h = h.replace(/(\s)(=)(\s)/g, '$1<span class="eq">$2</span>$3');
      // Highlight operators × ÷ + − - (between spaces)
      h = h.replace(/(\s)([+×÷±])(\s)/g, '$1<span class="op">$2</span>$3');
      h = h.replace(/(\s)(-)(\s)/g, '$1<span class="op">$2</span>$3');
      h = h.replace(/(\s)(\/)(\s)/g, '$1<span class="op">$2</span>$3');
      // Highlight numbers (standalone, including decimals & percents)
      h = h.replace(/\b(\d+(?:\.\d+)?%?)\b/g, '<span class="num">$1</span>');
      return `<div>${h}</div>`;
    }).join('');
  }

  // Variables splitter — parse "X is foo; Y is bar" or comma-separated into list items
  function prettifyVariables(raw) {
    if (!raw) return '';
    // Split by sentence boundaries / semicolons
    let parts = raw.split(/[;.]\s+(?=[A-Za-z%Δπ∆])/);
    parts = parts.map(p => p.trim().replace(/\.$/, '')).filter(Boolean);
    // For each part try to identify a leading variable symbol up to '=', ':' or ' is '/' = '
    const items = parts.map(p => {
      const m = p.match(/^([A-Za-zπΔΘΣµ%][A-Za-z_0-9πΔΘΣµ()\-]*?)\s*(?:=|:|\s+is\s+|\s+represents\s+|\s+denotes\s+|\s+stands for\s+|\s+,)\s*(.+)$/);
      if (m) {
        return `<div class="var-item"><span class="sym">${esc(m[1])}</span><span>${esc(m[2])}</span></div>`;
      }
      return `<div class="var-item"><span class="sym">·</span><span>${esc(p)}</span></div>`;
    });
    return items.join('');
  }

  // Example prettifier — emphasize numeric answer if present
  function prettifyExample(raw) {
    if (!raw) return '';
    let h = esc(raw);
    // Bold the final numeric answer if a pattern like "= 6.25%" or "= $60" appears
    h = h.replace(/(=\s*\$?[-+]?[\d,]+(?:\.\d+)?\s*[%a-zA-Z]*\.?)$/, '<span class="answer-pill">$1</span>');
    return h;
  }

  // ── Render: Formulas ────────────────────────────────────────────
  function renderFormulas() {
    const items = DATA.formulas.filter(f => passesCategory(f) && passesSearch(f, [f.name,f.equation,f.variables,f.example]));
    const root = document.getElementById('view-formulas');
    root.innerHTML = `
      <div class="summary-bar">
        <h2>Important Formulas</h2>
        <span class="sublabel">${items.length} of ${DATA.formulas.length} · each with a worked numeric example</span>
      </div>
      ${items.length === 0 ? `<div class="empty"><strong>No matches.</strong></div>` :
        `<div class="grid">${items.map(f => {
          const catCls = 'cat-' + (CAT_CLASS[f.category] || 'micro');
          return `
          <article class="formula-card ${catCls}">
            <div class="fhead">
              ${tagFor(f.category)}
              <span class="tag page">chunk ${f.chunk}</span>
              <h3 style="width:100%;margin-top:4px">${esc(f.name)}</h3>
            </div>
            <div class="eqn">
              <span class="eqn-label">Formula</span>
              <div class="eqn-body">${prettifyEquation(f.equation)}</div>
            </div>
            ${f.variables ? `
              <div>
                <strong style="font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-mute);font-weight:700;display:block;margin-bottom:5px">Variables</strong>
                <div class="vars-grid">${prettifyVariables(f.variables)}</div>
              </div>` : ''}
            ${f.units ? `<div class="notes"><strong>Sign / units</strong>${esc(f.units)}</div>` : ''}
            ${f.example ? `<div class="ex"><span class="ex-label">▸ Worked example</span><br>${prettifyExample(f.example)}</div>` : ''}
          </article>`;
        }).join('')}
        </div>`}`;
  }

  // ── Render: Synthesis ───────────────────────────────────────────
  function renderSynthesis() {
    const items = DATA.synthesis.filter(s => {
      // Synthesis items have category by chunk; we'll just respect search.
      return passesSearch(s, [s.text]);
    });
    const root = document.getElementById('view-synthesis');
    root.innerHTML = `
      <div class="summary-bar">
        <h2>High-Yield Synthesis</h2>
        <span class="sublabel">The top takeaways from every section — your night-before-exam crib sheet.</span>
      </div>
      <div class="synth-list">
        ${items.map((s,i) => `
          <div class="synth-card">
            <div class="num">${String(i+1).padStart(2,'0')}</div>
            <p><strong style="font-size:11px;letter-spacing:.05em;color:#94a3b8;text-transform:uppercase;">Chunk ${s.chunk} · ${chunkPageRange(s.chunk)}</strong><br>${esc(s.text)}</p>
          </div>`).join('')}
      </div>`;
  }

  // ── Render: Book Map ────────────────────────────────────────────
  function renderMap() {
    const root = document.getElementById('view-map');
    root.innerHTML = `
      <div class="summary-bar">
        <h2>Book Map</h2>
        <span class="sublabel">All 10 chunks → modules covered. Use this to plan study sessions.</span>
      </div>
      <div class="map-grid">
        ${DATA.chunks.map(c => `
          <div class="chunk-card">
            <h4>Chunk ${c.chunk} · ${tagFor(c.default_category)}</h4>
            <div class="pages">${chunkPageRange(c.chunk)}</div>
            <ul>${c.modules.map(m => `<li>${esc(m)}</li>`).join('')}</ul>
          </div>`).join('')}
      </div>`;
  }

  // ── Render: Quiz ────────────────────────────────────────────────
  function renderQuiz() {
    const root = document.getElementById('view-quiz');
    if (!state.quiz) {
      // Pre-quiz config
      root.innerHTML = `
        <div class="quiz-config">
          <h2>Custom Quiz</h2>
          <p class="lede">Test yourself with trick-trap MCQs and numerical problems pulled from the entire 942-page book. Pick your difficulty curve and go.</p>

          <div class="config-row">
            <div class="label">Category</div>
            <div class="opt-group cats" data-key="qcat">
              <div class="opt active" data-val="ALL">All</div>
              <div class="opt" data-val="MICRO">Micro</div>
              <div class="opt" data-val="MACRO">Macro</div>
              <div class="opt" data-val="FIN-LIT">Fin Lit</div>
            </div>
          </div>

          <div class="config-row">
            <div class="label">Difficulty</div>
            <div class="opt-group" data-key="qdiff">
              <div class="opt active" data-val="MIX">All levels</div>
              <div class="opt" data-val="EASY">Easy</div>
              <div class="opt" data-val="MEDIUM">Medium</div>
              <div class="opt" data-val="HARD">Hard</div>
              <div class="opt" data-val="OLYMPIAD">Olympiad</div>
              <div class="opt" data-val="RAMP">Adaptive ramp ↑</div>
            </div>
          </div>

          <div class="config-row">
            <div class="label">Type</div>
            <div class="opt-group" data-key="qtype">
              <div class="opt active" data-val="ALL">Both</div>
              <div class="opt" data-val="CONCEPTUAL">Conceptual only</div>
              <div class="opt" data-val="NUMERICAL">Numerical only</div>
            </div>
          </div>

          <div class="config-row">
            <div class="label">Length</div>
            <div class="opt-group" data-key="qlen">
              <div class="opt" data-val="10">10 Qs</div>
              <div class="opt active" data-val="20">20 Qs</div>
              <div class="opt" data-val="50">50 Qs</div>
              <div class="opt" data-val="ALL">All available</div>
            </div>
          </div>

          <button class="start-btn" id="startQuiz">Start quiz →</button>
        </div>`;

      // Attach option click handlers
      root.querySelectorAll('.opt-group').forEach(grp => {
        grp.querySelectorAll('.opt').forEach(opt => {
          opt.addEventListener('click', () => {
            grp.querySelectorAll('.opt').forEach(o => o.classList.remove('active'));
            opt.classList.add('active');
          });
        });
      });
      root.querySelector('#startQuiz').addEventListener('click', startQuiz);
      return;
    }

    // Active quiz
    const q = state.quiz;
    if (q.finished) {
      const pct = Math.round(100 * q.correct / q.questions.length);
      const byCat = {};
      const byDiff = {};
      q.history.forEach(h => {
        byCat[h.category] = byCat[h.category] || {c:0,t:0};
        byCat[h.category].t++; if (h.right) byCat[h.category].c++;
        byDiff[h.difficulty] = byDiff[h.difficulty] || {c:0,t:0};
        byDiff[h.difficulty].t++; if (h.right) byDiff[h.difficulty].c++;
      });
      root.innerHTML = `
        <div class="results">
          <h2>Quiz complete</h2>
          <div class="big-score">${q.correct}<span class="denom"> / ${q.questions.length}</span></div>
          <div class="sublabel" style="margin-bottom:18px;font-size:14px;color:var(--ink-soft)">${pct}% correct · longest streak ${q.maxStreak}</div>
          <div class="breakdown">
            ${['EASY','MEDIUM','HARD','OLYMPIAD'].filter(d=>byDiff[d]).map(d => `
              <div class="bdcell"><div class="lbl">${d}</div><div class="v">${byDiff[d].c}/${byDiff[d].t}</div></div>`).join('')}
          </div>
          <div class="breakdown" style="grid-template-columns:repeat(3,1fr)">
            ${['MICRO','MACRO','FIN-LIT'].filter(c=>byCat[c]).map(c => `
              <div class="bdcell"><div class="lbl">${CAT_LABEL[c]}</div><div class="v">${byCat[c].c}/${byCat[c].t}</div></div>`).join('')}
          </div>
          <div style="display:flex;gap:10px">
            <button class="pill-btn" id="newQuiz">New quiz</button>
            <button class="pill-btn ghost" id="reviewQuiz">Review answers</button>
          </div>
          <div id="reviewArea" style="margin-top:18px;display:none"></div>
        </div>`;
      root.querySelector('#newQuiz').addEventListener('click', () => { state.quiz = null; render(); });
      root.querySelector('#reviewQuiz').addEventListener('click', () => {
        const area = root.querySelector('#reviewArea');
        if (area.style.display === 'none') {
          area.style.display = '';
          area.innerHTML = q.history.map((h,i) => `
            <div class="card" style="margin-bottom:10px">
              <div class="meta">
                <span class="tag diff-${h.difficulty.toLowerCase()}">${h.difficulty}</span>
                <span class="tag type-${h.qtype.toLowerCase()}">${h.qtype}</span>
                ${tagFor(h.category)}
                <span class="tag page">${h.right ? '✓ correct' : '✗ wrong'}</span>
              </div>
              <h3>Q${i+1}. ${esc(h.topic)}</h3>
              <div class="field"><span class="val">${esc(h.questionText)}</span></div>
              <div class="field"><span class="lbl">Your answer</span><span class="val">${esc(h.userAns || '(blank)')}</span></div>
              <div class="field"><span class="lbl">Correct</span><span class="val">${esc(h.correct)}</span></div>
              <div class="explain ${h.right ? 'right':'wrong'}">${esc(h.explanation)}</div>
            </div>`).join('');
        } else {
          area.style.display = 'none';
        }
      });
      return;
    }

    // Active question
    const cur = q.questions[q.idx];
    const progress = ((q.idx) / q.questions.length) * 100;
    const isMCQ = cur.choices && cur.choices.length > 0;
    const showExplain = q.answered;
    const userRight = q.lastRight;

    root.innerHTML = `
      <div class="quiz-stage">
        <div class="qcard">
          <div class="meta" style="margin-bottom:12px;display:flex;gap:6px;flex-wrap:wrap">
            <span class="tag diff-${cur.difficulty.toLowerCase()}">${cur.difficulty}</span>
            <span class="tag type-${cur.qtype.toLowerCase()}">${cur.qtype}</span>
            ${tagFor(cur.category)}
            <span class="tag page">chunk ${cur.chunk}</span>
          </div>
          <div class="q-topic">${esc(cur.topic)}</div>
          <div class="q-text">${esc(cur.question)}</div>
          ${isMCQ ? (() => {
            const correctLetter = ((cur.correct || '').toUpperCase().match(/[A-E]/) || [''])[0];
            const userLetter = ((q.userAnsLetter || '').toUpperCase().match(/[A-E]/) || [''])[0];
            return `<div class="choices">${cur.choices.map(ch => {
              let cls = '';
              if (showExplain) {
                if (ch.letter === correctLetter) cls = 'correct';
                else if (ch.letter === userLetter) cls = 'wrong';
              }
              return `<button class="choice-btn ${cls}" data-letter="${ch.letter}" ${showExplain?'disabled':''}>
                <span class="letter">${ch.letter}</span>
                <span>${esc(ch.text)}</span>
              </button>`;
            }).join('')}</div>`;
          })() :
            `<div>
              <input type="text" class="free-input" id="freeInput" ${showExplain?'disabled':''} placeholder="Type your answer…" value="${showExplain?esc(q.userAnsLetter||''):''}"/>
              ${showExplain ? '' : '<button class="free-submit" id="freeSubmit">Submit</button>'}
            </div>`}
          ${showExplain ? `
            <div class="explain ${userRight?'right':'wrong'}">
              <div class="verdict ${userRight?'right':'wrong'}">${userRight ? '✓ correct' : '✗ wrong'} — answer: ${esc(cur.correct)}</div>
              ${esc(cur.explanation)}
            </div>
            <div class="quiz-actions">
              <button class="pill-btn ghost" id="quitQuiz">Quit</button>
              <button class="pill-btn" id="nextQ">${q.idx + 1 >= q.questions.length ? 'Finish ▶' : 'Next question →'}</button>
            </div>` : `
            <div class="quiz-actions">
              <button class="pill-btn ghost" id="quitQuiz">Quit</button>
              <span style="color:var(--ink-mute);font-size:12.5px">Choose an answer to see the explanation</span>
            </div>`}
        </div>
        <aside class="qsidebar">
          <h4>Progress</h4>
          <div class="progress"><div style="width:${progress}%"></div></div>
          <div class="stat-row"><span>Question</span><span class="val">${q.idx+1} / ${q.questions.length}</span></div>
          <div class="stat-row"><span>Correct</span><span class="val green">${q.correct}</span></div>
          <div class="stat-row"><span>Wrong</span><span class="val red">${q.wrong}</span></div>
          <div class="stat-row"><span>Streak</span><span class="val">${q.streak} <span style="color:var(--ink-mute);font-weight:500">(max ${q.maxStreak})</span></span></div>
          ${q.mode === 'RAMP' ? `<div style="margin-top:12px;padding:8px 10px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-size:12px;color:#78350f"><strong>Adaptive:</strong> difficulty ramps up after each correct streak of 2+.</div>` : ''}
        </aside>
      </div>`;

    if (isMCQ) {
      // Event delegation: any click inside .choices that lands on (or inside) a
      // .choice-btn — including clicks on the letter span or the text span — is
      // routed to gradeAnswer with the button's data-letter.
      const choicesEl = root.querySelector('.choices');
      if (choicesEl) {
        choicesEl.addEventListener('click', (ev) => {
          if (q.answered) return;
          const btn = ev.target.closest('.choice-btn');
          if (!btn || btn.disabled) return;
          const letter = btn.dataset.letter;
          if (!letter) return;
          gradeAnswer(letter);
        });
        // Also let keyboard A/B/C/D/E pick a choice for faster review
        const keyHandler = (ev) => {
          if (q.answered) return;
          const k = (ev.key || '').toUpperCase();
          if (!/^[A-E]$/.test(k)) return;
          const btn = choicesEl.querySelector(`.choice-btn[data-letter="${k}"]`);
          if (btn) gradeAnswer(k);
        };
        document.addEventListener('keydown', keyHandler, { once: true });
      }
    } else {
      const sub = root.querySelector('#freeSubmit');
      if (sub) sub.addEventListener('click', () => {
        const inp = root.querySelector('#freeInput');
        gradeAnswer(inp.value.trim());
      });
      const inp = root.querySelector('#freeInput');
      if (inp) inp.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter' && !q.answered) gradeAnswer(inp.value.trim());
      });
    }
    const nextBtn = root.querySelector('#nextQ');
    if (nextBtn) nextBtn.addEventListener('click', nextQuestion);
    const quitBtn = root.querySelector('#quitQuiz');
    if (quitBtn) quitBtn.addEventListener('click', () => { state.quiz = null; render(); });
  }

  function gradeAnswer(userInput) {
    const q = state.quiz;
    const cur = q.questions[q.idx];
    q.userAnsLetter = userInput;
    const correctNorm = (cur.correct || '').trim().toUpperCase();
    const inputNorm = (userInput || '').trim().toUpperCase();
    // For MCQ, compare the first A-E letter found in each string
    let right = false;
    if (cur.choices && cur.choices.length > 0) {
      const correctLetterMatch = correctNorm.match(/[A-E]/);
      const inputLetterMatch = inputNorm.match(/[A-E]/);
      right = !!(correctLetterMatch && inputLetterMatch &&
                 correctLetterMatch[0] === inputLetterMatch[0]);
    } else {
      // Free response: accept exact, substring match, or numeric match
      right = inputNorm === correctNorm ||
              (inputNorm && correctNorm.includes(inputNorm)) ||
              (inputNorm && inputNorm.includes(correctNorm));
    }
    q.answered = true;
    q.lastRight = right;
    if (right) {
      q.correct++;
      q.streak++;
      q.maxStreak = Math.max(q.maxStreak, q.streak);
    } else {
      q.wrong++;
      q.streak = 0;
    }
    q.history.push({
      topic: cur.topic, questionText: cur.question, userAns: userInput,
      correct: cur.correct, explanation: cur.explanation, right,
      difficulty: cur.difficulty, qtype: cur.qtype, category: cur.category,
    });
    renderQuiz();
  }

  function nextQuestion() {
    const q = state.quiz;
    q.idx++;
    q.answered = false;
    q.lastRight = null;
    q.userAnsLetter = null;
    // Adaptive ramp: if streak >= 2 and there's a harder question in pool, swap one in
    if (q.mode === 'RAMP' && q.idx < q.questions.length) {
      const cur = q.questions[q.idx];
      const order = ['EASY','MEDIUM','HARD','OLYMPIAD'];
      const targetIdx = Math.min(3, Math.floor(q.idx / 4) + (q.streak >= 2 ? 1 : 0));
      const target = order[targetIdx];
      // Try to find an unused question matching target difficulty + filters
      const used = new Set(q.questions.map(x => x.id));
      const candidate = DATA.questions.find(x =>
        !used.has(x.id) && x.difficulty === target &&
        (q.filterCat === 'ALL' || x.category === q.filterCat) &&
        (q.filterType === 'ALL' || x.qtype === q.filterType));
      if (candidate) {
        q.questions[q.idx] = candidate;
      }
    }
    if (q.idx >= q.questions.length) {
      q.finished = true;
    }
    renderQuiz();
  }

  function startQuiz() {
    const root = document.getElementById('view-quiz');
    const get = (key) => root.querySelector(`.opt-group[data-key="${key}"] .opt.active`).dataset.val;
    const cat = get('qcat'), diff = get('qdiff'), qtype = get('qtype'), lenStr = get('qlen');

    let pool = DATA.questions.slice();
    if (cat !== 'ALL') pool = pool.filter(q => q.category === cat);
    if (qtype !== 'ALL') pool = pool.filter(q => q.qtype === qtype);

    let questions;
    if (diff === 'MIX') {
      questions = shuffle(pool);
    } else if (diff === 'RAMP') {
      // Order by difficulty (Easy → Olympiad) within each tier
      const order = ['EASY','MEDIUM','HARD','OLYMPIAD'];
      questions = order.flatMap(d => shuffle(pool.filter(q => q.difficulty === d)));
    } else {
      questions = shuffle(pool.filter(q => q.difficulty === diff));
    }

    const len = lenStr === 'ALL' ? questions.length : Math.min(parseInt(lenStr, 10), questions.length);
    questions = questions.slice(0, len);

    if (questions.length === 0) {
      alert('No questions match those filters — loosen and try again.');
      return;
    }

    state.quiz = {
      questions,
      idx: 0,
      correct: 0, wrong: 0, streak: 0, maxStreak: 0,
      answered: false, lastRight: null, userAnsLetter: null,
      mode: diff,
      filterCat: cat, filterType: qtype,
      history: [],
      finished: false,
    };
    renderQuiz();
  }

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // ── Top-level render ────────────────────────────────────────────
  function render() {
    document.querySelectorAll('main > section').forEach(s => s.classList.add('hidden'));
    document.getElementById('view-' + state.tab).classList.remove('hidden');
    if (state.tab === 'concepts') renderConcepts();
    if (state.tab === 'figures') renderFigures();
    if (state.tab === 'formulas') renderFormulas();
    if (state.tab === 'synthesis') renderSynthesis();
    if (state.tab === 'map') renderMap();
    if (state.tab === 'quiz') renderQuiz();
  }

  // ── Event wiring ────────────────────────────────────────────────
  document.getElementById('catChips').addEventListener('click', e => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    document.querySelectorAll('#catChips .chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    state.category = chip.dataset.cat;
    if (state.tab !== 'quiz') render();
  });
  document.getElementById('tabs').addEventListener('click', e => {
    const tab = e.target.closest('.tab');
    if (!tab) return;
    document.querySelectorAll('#tabs .tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    state.tab = tab.dataset.tab;
    render();
  });
  document.getElementById('searchBox').addEventListener('input', e => {
    state.search = e.target.value;
    if (state.tab !== 'quiz') render();
  });

  // Initial paint
  setCounts();
  render();
})();
</script>
</body>
</html>
"""

def main():
    out = TEMPLATE.replace('__DATA__', json.dumps(DATA))
    OUT.write_text(out)
    size_kb = OUT.stat().st_size / 1024
    print(f'Wrote {OUT} ({size_kb:.1f} KB)')

if __name__ == '__main__':
    main()
