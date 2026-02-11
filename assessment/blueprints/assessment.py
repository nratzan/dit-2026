from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, current_app
from config import settings as app_settings

bp = Blueprint('assessment', __name__)


@bp.route('/')
def index():
    has_llm = bool([p for p in current_app.llm_registry.get_available_providers() if p['available']])
    return render_template('index.html', has_llm=has_llm)


@bp.route('/assess')
def assess():
    from assessment.questions import get_all_sae_questions
    questions = get_all_sae_questions()
    return render_template('assessment.html', questions=questions)


@bp.route('/api/assess', methods=['POST'])
def submit_assessment():
    from assessment.scorer import score_assessment
    from assessment.matrix import get_placement
    answers = request.get_json()
    score = score_assessment(answers)
    placement = get_placement(score)
    # Find relevant growth path chunks via search
    query = f"growth path for SAE L{placement['sae_level']} {placement['epias_stage']}"
    chunks = current_app.search_engine.search(query, top_k=5)
    placement['growth_chunks'] = [{'text': c['text'], 'section': c.get('section_title', ''), 'source': c.get('source_file', '')} for c in chunks]
    return jsonify(placement)


@bp.route('/results')
def results():
    return render_template('results.html')


@bp.route('/settings')
def settings():
    return render_template('settings.html')


# Ordered list of source documents with short labels
_FRAMEWORK_DOCS = [
    ('ai-upskilling-for-product-designers.md', 'The E-P-I-A-S x SAE Framework'),
    ('ai-upskilling-for-product-designers-L1-to-L2.md', 'L1 to L2 Transition'),
    ('ai-upskilling-for-product-designers-L2-to-L3.md', 'L2 to L3 Transition'),
    ('ai-upskilling-for-product-designers-L3-L4.md', 'L3 to L4 Transition'),
]


@bp.route('/framework')
@bp.route('/framework/<int:doc_index>')
def framework(doc_index=0):
    doc_index = max(0, min(doc_index, len(_FRAMEWORK_DOCS) - 1))
    filename, label = _FRAMEWORK_DOCS[doc_index]
    filepath = app_settings.source_dir / filename
    raw_md = filepath.read_text(encoding='utf-8')
    html_content = _render_markdown(raw_md)
    tabs = [{'label': lbl, 'index': i, 'active': i == doc_index}
            for i, (_, lbl) in enumerate(_FRAMEWORK_DOCS)]
    return render_template('framework.html', tabs=tabs, content=html_content,
                           current_label=label)


def _render_markdown(md: str) -> str:
    """Convert markdown to HTML. Handles headings, bold, italic, code,
    lists, tables, blockquotes, and horizontal rules."""
    import re

    def esc(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def inline(s):
        s = esc(s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
        s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', s)
        return s

    lines = md.split('\n')
    out = []
    in_table = False
    header_done = False
    list_type = None

    def close_list():
        nonlocal list_type
        if list_type:
            out.append(f'</{list_type}>')
            list_type = None

    for line in lines:
        stripped = line.strip()

        # Table rows
        if stripped.startswith('|'):
            close_list()
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if all(re.match(r'^[-:\s]+$', c) for c in cells):
                header_done = True
                continue
            if not in_table:
                out.append('<table class="chunk-table">')
                in_table = True
                header_done = False
            if not header_done:
                out.append('<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in cells) + '</tr></thead><tbody>')
            else:
                out.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells) + '</tr>')
            continue
        if in_table:
            out.append('</tbody></table>')
            in_table = False
            header_done = False

        # Blank line
        if not stripped:
            close_list()
            continue

        # Horizontal rule
        if re.match(r'^[-*_]{3,}\s*$', stripped):
            close_list()
            out.append('<hr>')
            continue

        # Headings
        hm = re.match(r'^(#{1,4})\s+(.*)', stripped)
        if hm:
            close_list()
            level = len(hm.group(1))
            out.append(f'<h{level}>{inline(hm.group(2))}</h{level}>')
            continue

        # Blockquote
        if stripped.startswith('>'):
            close_list()
            text = stripped.lstrip('>').strip()
            out.append(f'<blockquote>{inline(text)}</blockquote>')
            continue

        # Unordered list
        um = re.match(r'^(\s*)[-*]\s+(.*)', line)
        if um:
            if list_type != 'ul':
                close_list()
                out.append('<ul>')
                list_type = 'ul'
            out.append(f'<li>{inline(um.group(2))}</li>')
            continue

        # Ordered list
        om = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if om:
            if list_type != 'ol':
                close_list()
                out.append('<ol>')
                list_type = 'ol'
            out.append(f'<li>{inline(om.group(2))}</li>')
            continue

        # Regular paragraph
        close_list()
        out.append(f'<p>{inline(stripped)}</p>')

    close_list()
    if in_table:
        out.append('</tbody></table>')
    return '\n'.join(out)
