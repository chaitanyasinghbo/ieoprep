# ieoprep

A single-file HTML study app for the **International Economics Olympiad (IEO)**,
condensed from Krugman's *Economics for AP®* (2nd edition, 942 pages) into
~500 cards organised by **Micro / Macro / Financial Literacy** with a built-in
adaptive quiz.

> **Open [`econ_study_app.html`](econ_study_app.html) in any modern browser.**
> No build step, no dependencies beyond Google Fonts.

---

## What's inside the app

| Section            | Count | What it is                                                                                  |
| ------------------ | ----: | ------------------------------------------------------------------------------------------- |
| **Concepts**       |   210 | Definition · why it matters · vivid mnemonic · related concepts                             |
| **Figures**        |   113 | Name · PDF page · axes · shape/shifts · "must-memorize" line                                |
| **Formulas**       |    86 | Pretty-typeset equation with colour-coded operators · variables list · worked example       |
| **Questions**      |   113 | MCQ + free-response · Easy / Medium / Hard / Olympiad · with trap-explanations               |
| **High-Yield**     |    30 | Section-by-section top-3 takeaways (your night-before crib sheet)                           |
| **Book Map**       |    10 | Chunk-to-module crosswalk with PDF page ranges                                              |

Every item is tagged **MICRO**, **MACRO**, or **FIN-LIT** for the IEO syllabus.

### Quiz features
- Filter by **category** (Micro / Macro / Fin-Lit / All)
- Filter by **difficulty** (Easy / Medium / Hard / Olympiad / **Adaptive ramp ↑**)
- Filter by **type** (Conceptual / Numerical / Both)
- Choose quiz **length** (10 / 20 / 50 / All)
- Live progress, streak counter, right/wrong feedback with full explanation
- Keyboard shortcuts: **A / B / C / D / E** to pick a choice, **Enter** to submit
- End-of-quiz breakdown by category and difficulty + answer review

---

## How it was built

```
Economics.pdf (942 pp)
    │
    ├── split into 10 chunks of ~95 pages each
    │
    ├── 10 parallel research agents → econ_extracts/extract_NN.md
    │       (figures, concepts, formulas, questions, synthesis)
    │
    ├── parse_extracts.py → econ_data.json   (structured)
    │
    └── build_html.py     → econ_study_app.html  (single-file app)
```

To regenerate from the markdown extracts:

```bash
python3 parse_extracts.py   # extracts → econ_data.json
python3 build_html.py       # JSON     → econ_study_app.html
```

The source PDF and raw page-by-page text are not committed (see `.gitignore`).
You'll need your own copy of Krugman's *Economics for AP®* to re-run the
agent-based extraction step.

---

## File layout

```
ieoprep/
├── econ_study_app.html      # the deliverable — open this
├── econ_data.json           # structured study data (~422 KB)
├── econ_extracts/           # 10 markdown extracts (one per ~95-page slice)
│   ├── extract_01.md        # pp.   1– 95   intro · PPC · trade · demand
│   ├── extract_02.md        # pp.  96–190   supply · equilibrium · GDP · unemployment
│   ├── extract_03.md        # pp. 191–285   AD-AS · multipliers · fiscal · money
│   ├── extract_04.md        # pp. 286–380   Fed · money supply · Phillips
│   ├── extract_05.md        # pp. 381–475   schools · growth · open economy · BOP
│   ├── extract_06.md        # pp. 476–570   trade · elasticity · surplus · tax incidence
│   ├── extract_07.md        # pp. 571–665   production · costs · perfect comp · monopoly
│   ├── extract_08.md        # pp. 666–760   price discrim · oligopoly · factor markets
│   ├── extract_09.md        # pp. 761–855   externalities · public goods · antitrust · inequality
│   └── extract_10.md        # pp. 856–942   info econ · indifference curves · fin-lit handbook
├── parse_extracts.py        # markdown → JSON
└── build_html.py            # JSON → HTML
```

---

## Status & disclaimer

This is a student study aid for the IEO. Content summarises and reorganises
material from Krugman/Wells/Ray/Anderson, *Economics for AP®*, 2e (Worth/BFW).
Mnemonics, question wording, and explanations are original. Copyrighted figures
and verbatim definitions are paraphrased; the original PDF is not redistributed
here. If you are the rights holder and want anything removed, open an issue.
