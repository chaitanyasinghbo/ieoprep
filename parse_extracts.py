#!/usr/bin/env python3
"""Parse the 10 econ extract markdown files into a single JSON data structure."""
import json
import re
from pathlib import Path

EXTRACT_DIR = Path('/Users/chaitanyasingh/workspace/econ_extracts')
OUT_PATH = Path('/Users/chaitanyasingh/workspace/econ_data.json')

# Keyword classifiers for category fallback
MICRO_KW = [
    'supply', 'demand', 'elastic', 'monopoly', 'oligopoly', 'cartel', 'duopoly',
    'monopolistic competition', 'perfect competition', 'consumer surplus',
    'producer surplus', 'deadweight', 'price ceiling', 'price floor', 'tax incidence',
    'utility', 'indifference', 'budget constraint', 'mrs', 'mpl', 'mpk', 'marginal product',
    'marginal cost', 'marginal revenue', 'average total cost', 'average variable cost',
    'shutdown', 'break-even', 'long-run', 'short-run', 'externality', 'public good',
    'common resource', 'coase', 'pigou', 'antitrust', 'sherman', 'clayton',
    'gini', 'lorenz', 'labor demand', 'mrp', 'monopsony', 'factor', 'wage discrim',
    'price discrimination', 'game theory', 'nash', 'dominant strategy', 'cournot',
    'comparative advantage', 'opportunity cost', 'production possibilities', 'ppc',
    'gains from trade', 'tribe', 'shifters', 'substitut', 'complement', 'normal good',
    'inferior good', 'giffen', 'veblen', 'cross-price', 'income elasticity',
    'asymmetric information', 'adverse selection', 'moral hazard', 'screening', 'signaling',
    'profit max', 'cost minim', 'returns to scale', 'diminishing returns',
    'individual', 'household', 'firm', 'industry'
]

MACRO_KW = [
    'gdp', 'gnp', 'national income', 'circular flow', 'aggregate demand', 'aggregate supply',
    'ad-as', 'lras', 'sras', 'recession', 'business cycle', 'expansion', 'depression',
    'unemployment', 'inflation', 'deflation', 'cpi', 'ppi', 'gdp deflator', 'price index',
    'real gdp', 'nominal gdp', 'chain', 'fed', 'federal reserve', 'central bank',
    'monetary', 'fiscal', 'money supply', 'money multiplier', 'reserve', 'discount rate',
    'open market', 'loanable funds', 'money market', 'fisher', 'phillips curve',
    'okun', 'nairu', 'taylor rule', 'natural rate', 'liquidity', 'velocity',
    'quantity theory', 'rule of 70', 'aggregate production', 'tfp', 'convergence',
    'solow', 'growth accounting', 'crowding out', 'multiplier', 'mpc', 'mps', 'mpt',
    'balanced budget', 'budget deficit', 'budget surplus', 'public debt',
    'balance of payments', 'current account', 'capital account', 'exchange rate',
    'forex', 'foreign exchange', 'appreciation', 'depreciation', 'ppp',
    'purchasing power parity', 'trade barrier', 'tariff', 'quota', 'protection',
    'human capital', 'physical capital', 'productivity', 'long-run growth',
    'business cycle', 'cyclical', 'frictional', 'structural', 'discouraged worker',
    'labor force', 'participation rate', 'shoe-leather', 'menu cost',
    'unit-of-account', 'fisher effect', 'monetary policy', 'fiscal policy',
    'classical', 'keynesian', 'new keynesian', 'rational expectations', 'lucas',
    'great moderation', 'aggregate', 'output gap', 'potential output',
    'banking', 'bank reserves', 'deposit', 'fractional reserve', 'money creation',
    'present value', 'time value', 'compound interest', 'bond', 'stock market',
    'financial market', 'financial system'
]

FINLIT_KW = [
    'budget', 'budgeting', 'saving', 'savings account', 'investment',
    'retirement', '401k', 'roth', 'ira', 'pension', 'credit', 'credit card',
    'credit score', 'fico', 'loan', 'mortgage', 'apr', 'apy', 'auto loan',
    'student loan', 'debt', 'insurance', 'tax bracket', 'effective tax rate',
    'marginal tax', 'progressive tax', 'income tax', 'social security',
    'medicare', 'paycheck', 'w2', 'w-2', '1099', 'gross income', 'net income',
    'take-home', 'net worth', 'home equity', 'down payment', 'principal',
    'interest rate', 'rule of 72', 'diversification', 'asset allocation',
    'risk tolerance', 'emergency fund', 'cash flow', 'financial literacy',
    'fdic', 'checking', 'overdraft', 'compound', 'simple interest',
    'late fee', 'minimum payment', 'amortization'
]

def classify(text: str, default: str = 'MACRO') -> str:
    t = text.lower()
    score_micro = sum(1 for k in MICRO_KW if k in t)
    score_macro = sum(1 for k in MACRO_KW if k in t)
    score_fin = sum(1 for k in FINLIT_KW if k in t)
    if score_fin > 0 and score_fin >= max(score_micro, score_macro):
        return 'FIN-LIT'
    if score_micro > score_macro:
        return 'MICRO'
    if score_macro > score_micro:
        return 'MACRO'
    return default

def parse_extract(path: Path, chunk: int):
    """Parse one extract markdown file into structured dict."""
    text = path.read_text()
    out = {
        'chunk': chunk,
        'modules': [],
        'figures': [],
        'concepts': [],
        'formulas': [],
        'questions': [],
        'synthesis': [],
    }

    # Split into sections by `^## `
    sections = re.split(r'\n## ', '\n' + text)
    section_map = {}
    for s in sections:
        if not s.strip():
            continue
        # Remove leading '#' if it's the title
        if s.startswith('# '):
            continue
        first_line, _, body = s.partition('\n')
        section_map[first_line.strip()] = body

    # Module coverage — bullet list
    mc = section_map.get('Module Coverage', '')
    for line in mc.splitlines():
        line = line.strip()
        if line.startswith('- '):
            out['modules'].append(line[2:].strip())

    # Category tags
    ct = section_map.get('Category Tags', '')
    cat_map = {}  # module name -> tag
    for line in ct.splitlines():
        line = line.strip()
        if not line.startswith('- '):
            continue
        # format: Module N — TAG — rationale
        m = re.match(r'-?\s*(Module\s+\d+[a-zA-Z]*|Section\s+\S+|.*?)\s*[—–-]+\s*(MICRO|MACRO|FIN-LIT|META)', line[2:])
        if m:
            cat_map[m.group(1).strip().lower()] = m.group(2)
    out['category_tags'] = cat_map

    # Default category from majority of tags
    tag_counts = {}
    for v in cat_map.values():
        tag_counts[v] = tag_counts.get(v, 0) + 1
    default_cat = max(tag_counts, key=tag_counts.get) if tag_counts else 'MACRO'
    if default_cat == 'META':
        default_cat = 'MICRO'

    # Helper: split a section by '### Prefix' headers, returning (header_remainder, body) pairs.
    def split_by_prefix(section: str, prefix: str):
        # Match '### Prefix' optionally followed by '<stuff>:' on the same line
        regex = re.compile(rf'^### {re.escape(prefix)}([^\n]*)$', re.MULTILINE)
        items = []
        matches = list(regex.finditer(section))
        for idx, m in enumerate(matches):
            header_rest = m.group(1).strip()
            start = m.end()
            end = matches[idx+1].start() if idx + 1 < len(matches) else len(section)
            body = section[start:end]
            items.append((header_rest, body))
        return items

    # Important Figures — '### Figure: name' or '### Figure 25.4: name'
    figs = section_map.get('Important Figures', '')
    for header_rest, body in split_by_prefix(figs, 'Figure'):
        # header_rest is like ": Supply Curve... (p. 97)" OR " 25.4: The Monetary Base... (p. 287)"
        name = header_rest.lstrip(':').strip()
        # Strip leading numbering like "25.4:" → already handled by lstrip(':')
        name = re.sub(r'^[\d.]+\s*:\s*', '', name).strip()  # e.g., "25.4: name" -> "name"
        page = ''
        pm = re.search(r'\(p\.\s*([^)]+)\)', name)
        if pm:
            page = pm.group(1).strip()
            name = re.sub(r'\s*\(p\.\s*[^)]+\)', '', name).strip()
        fields = parse_bullets(body)
        full_text = name + ' ' + ' '.join(fields.values())
        out['figures'].append({
            'name': name,
            'page': page,
            'what_shows': fields.get('What it shows', ''),
            'axes': fields.get('Axes / variables', ''),
            'shifts': fields.get('Key shapes / shifts', ''),
            'memorize': fields.get('Must-memorize', ''),
            'category': classify(full_text, default_cat),
        })

    # Key Concepts — '### Concept: name'
    cc = section_map.get('Key Concepts (with mnemonics)', '') or section_map.get('Key Concepts', '')
    for header_rest, body in split_by_prefix(cc, 'Concept'):
        name = header_rest.lstrip(':').strip()
        name = re.sub(r'^[\d.]+\s*:\s*', '', name).strip()
        fields = parse_bullets(body)
        full_text = name + ' ' + ' '.join(fields.values())
        out['concepts'].append({
            'name': name,
            'definition': fields.get('Definition', ''),
            'why': fields.get('Why it matters', ''),
            'mnemonic': fields.get('Mnemonic / way to remember', '') or fields.get('Mnemonic', ''),
            'related': fields.get('Related', ''),
            'category': classify(full_text, default_cat),
        })

    # Important Formulas — '### Formula: name'
    ff = section_map.get('Important Formulas', '')
    for header_rest, body in split_by_prefix(ff, 'Formula'):
        name = header_rest.lstrip(':').strip()
        name = re.sub(r'^[\d.]+\s*:\s*', '', name).strip()
        fields = parse_bullets(body)
        full_text = name + ' ' + ' '.join(fields.values())
        out['formulas'].append({
            'name': name,
            'equation': fields.get('Equation', ''),
            'variables': fields.get('Variables', ''),
            'units': fields.get('Units / sign conventions', '') or fields.get('Units', ''),
            'example': fields.get('Worked example', ''),
            'category': classify(full_text, default_cat),
        })

    # Practice Questions — items prefixed by '### Q'
    qq = section_map.get('Practice Questions', '')
    header_iter = re.finditer(r'### Q(\d+)\s*\[([^\]]+)\]\s*\[([^\]]+)\]\s*(?:—|--|-)\s*([^\n]+)', qq)
    headers = list(header_iter)
    for idx, h in enumerate(headers):
        qnum = int(h.group(1))
        difficulty = h.group(2).strip().upper()
        qtype = h.group(3).strip().upper()
        topic = h.group(4).strip()
        start = h.end()
        end = headers[idx+1].start() if idx + 1 < len(headers) else len(qq)
        body = qq[start:end]
        # Parse the body for **Question:**, **Choices:**, **Correct:**, **Explanation:**
        q_text = extract_field(body, 'Question')
        choices_block = extract_field(body, 'Choices')
        correct = extract_field(body, 'Correct')
        explanation = extract_field(body, 'Explanation')
        # Parse choices block into a list of {letter, text}.
        # Some agents put each choice on its own line; others put them inline like
        # "A) foo  B) bar  C) baz". Handle both by splitting on the (?<=\s)[A-E]\) pattern.
        choices = []
        if choices_block:
            block = choices_block.strip()
            # Use regex to find all "X) text" segments, where text runs until the next
            # "  Y)" boundary or end-of-block.
            matches = list(re.finditer(r'\b([A-Ea-e])\)\s*', block))
            if len(matches) >= 2:
                for idx, mm in enumerate(matches):
                    letter = mm.group(1).upper()
                    text_start = mm.end()
                    text_end = matches[idx+1].start() if idx + 1 < len(matches) else len(block)
                    text = block[text_start:text_end].strip().rstrip(',').rstrip()
                    if text:
                        choices.append({'letter': letter, 'text': text})
            else:
                # Fallback: line-based parsing
                for cl in block.splitlines():
                    cl = cl.strip()
                    m = re.match(r'^([A-Ea-e])\)\s*(.*)', cl)
                    if m:
                        choices.append({'letter': m.group(1).upper(), 'text': m.group(2).strip()})
        full_text = topic + ' ' + (q_text or '') + ' ' + (explanation or '')
        out['questions'].append({
            'id': f'c{chunk}q{qnum}',
            'qnum': qnum,
            'difficulty': difficulty,
            'qtype': qtype,
            'topic': topic,
            'question': q_text or '',
            'choices': choices,
            'correct': (correct or '').strip(),
            'explanation': explanation or '',
            'category': classify(full_text, default_cat),
        })

    # High-Yield Synthesis
    hs = section_map.get('High-Yield Synthesis', '')
    for line in hs.splitlines():
        line = line.strip()
        if line.startswith('- '):
            out['synthesis'].append(line[2:].strip())

    out['default_category'] = default_cat
    return out


def parse_bullets(body: str) -> dict:
    """Parse a block of '- **Field:** value' lines into a dict.

    Each field continues on the same line; field name terminates at colon."""
    fields = {}
    # Bullets begin with '- **'; continuation lines indented or just text.
    lines = body.splitlines()
    cur_field = None
    cur_val = []
    for line in lines:
        stripped = line.strip()
        m = re.match(r'-\s*\*\*([^*]+?):\*\*\s*(.*)', stripped)
        if m:
            if cur_field:
                fields[cur_field] = ' '.join(cur_val).strip()
            cur_field = m.group(1).strip()
            cur_val = [m.group(2).strip()]
        elif cur_field is not None and stripped:
            # Continuation
            cur_val.append(stripped)
        elif cur_field is not None and not stripped:
            # Blank line ends field
            if cur_field:
                fields[cur_field] = ' '.join(cur_val).strip()
            cur_field = None
            cur_val = []
    if cur_field:
        fields[cur_field] = ' '.join(cur_val).strip()
    return fields


def extract_field(body: str, name: str) -> str:
    """Extract `**Name:** value` (possibly multiline until next **Field:** or end)."""
    pattern = rf'\*\*{re.escape(name)}:\*\*\s*(.*?)(?=\n\*\*[A-Z][^:]*:\*\*|\Z)'
    m = re.search(pattern, body, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ''


def main():
    all_data = {
        'modules': [],
        'figures': [],
        'concepts': [],
        'formulas': [],
        'questions': [],
        'synthesis': [],
    }
    chunk_meta = []
    for i in range(1, 11):
        p = EXTRACT_DIR / f'extract_{i:02d}.md'
        d = parse_extract(p, i)
        chunk_meta.append({'chunk': i, 'default_category': d['default_category'], 'modules': d['modules']})
        for f in d['figures']:
            f['chunk'] = i
            all_data['figures'].append(f)
        for c in d['concepts']:
            c['chunk'] = i
            all_data['concepts'].append(c)
        for fo in d['formulas']:
            fo['chunk'] = i
            all_data['formulas'].append(fo)
        for q in d['questions']:
            q['chunk'] = i
            all_data['questions'].append(q)
        for s in d['synthesis']:
            all_data['synthesis'].append({'chunk': i, 'text': s})
        for m in d['modules']:
            # Look up category by leading "Module N" prefix (or Section X), tolerating em-dash separators
            cat_map = d.get('category_tags', {})
            key_match = re.match(r'\s*(Module\s+\d+|Section\s+\S+|Appendix[^:—–-]*)', m)
            lookup_key = key_match.group(1).strip().lower() if key_match else m.split(':')[0].strip().lower()
            cat = cat_map.get(lookup_key, d['default_category'])
            if cat == 'META':
                cat = d['default_category']
            all_data['modules'].append({'chunk': i, 'text': m, 'category': cat})

    all_data['chunks'] = chunk_meta

    # Stats
    print(f"Modules: {len(all_data['modules'])}")
    print(f"Figures: {len(all_data['figures'])}")
    print(f"Concepts: {len(all_data['concepts'])}")
    print(f"Formulas: {len(all_data['formulas'])}")
    print(f"Questions: {len(all_data['questions'])}")
    print(f"Synthesis pts: {len(all_data['synthesis'])}")

    # Category breakdown
    for kind in ['figures', 'concepts', 'formulas', 'questions']:
        counts = {}
        for item in all_data[kind]:
            c = item.get('category', '?')
            counts[c] = counts.get(c, 0) + 1
        print(f"  {kind} by cat: {counts}")

    OUT_PATH.write_text(json.dumps(all_data, indent=2))
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")

if __name__ == '__main__':
    main()
