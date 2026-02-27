import fitz
import time
import re
import os
from deep_translator import GoogleTranslator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(BASE_DIR, 'docs', 'aws', 'AWSCertifiedGenerativeAIDeveloper.pdf')
DEFAULT_OUT = os.path.join(BASE_DIR, 'docs', 'aws', 'AWSCertifiedGenerativeAIDeveloper_ja.pdf')
LEGACY_SRC = os.path.join(BASE_DIR, 'AWSCertifiedGenerativeAIDeveloper.pdf')
LEGACY_OUT = os.path.join(BASE_DIR, 'AWSCertifiedGenerativeAIDeveloper_ja.pdf')

SRC = os.getenv('SRC_PDF') or (DEFAULT_SRC if os.path.exists(DEFAULT_SRC) else LEGACY_SRC)
OUT = os.getenv('OUT_PDF') or (DEFAULT_OUT if os.path.exists(os.path.dirname(DEFAULT_OUT)) else LEGACY_OUT)

START_PAGE = int(os.getenv('START_PAGE', '0'))
END_PAGE = os.getenv('END_PAGE')
END_PAGE = int(END_PAGE) if END_PAGE else None
SLEEP_SEC = float(os.getenv('SLEEP_SEC', '0.08'))

translator = GoogleTranslator(source='en', target='ja')
cache = {}

def needs_translation(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    letters = sum(c.isalpha() for c in t)
    return letters >= 2

def clean_text(t: str) -> str:
    return re.sub(r'\s+', ' ', t).strip()

def html_escape(s: str) -> str:
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>'))

def translate_text(text: str) -> str:
    key = clean_text(text)
    if key in cache:
        return cache[key]

    chunks = []
    if len(key) <= 3800:
        chunks = [key]
    else:
        parts = re.split(r'(?<=[\.!?])\s+', key)
        cur = ''
        for p in parts:
            if len(cur) + len(p) + 1 > 3200:
                if cur:
                    chunks.append(cur)
                cur = p
            else:
                cur = (cur + ' ' + p).strip()
        if cur:
            chunks.append(cur)

    out_parts = []
    for c in chunks:
        try:
            out_parts.append(translator.translate(c))
        except Exception:
            out_parts.append(c)
        time.sleep(SLEEP_SEC)

    out = '\n'.join(out_parts)
    cache[key] = out
    return out

def process_page(page: fitz.Page):
    blocks = page.get_text('dict').get('blocks', [])
    text_items = []

    for b in blocks:
        if b.get('type') != 0:
            continue
        lines = b.get('lines', [])
        texts = []
        max_size = 12
        for ln in lines:
            for sp in ln.get('spans', []):
                st = sp.get('text', '')
                if st and st.strip():
                    texts.append(st)
                    max_size = max(max_size, float(sp.get('size', 12)))
        text = '\n'.join(texts).strip()
        if not needs_translation(text):
            continue
        rect = fitz.Rect(b['bbox'])
        if rect.width < 24 or rect.height < 9:
            continue
        text_items.append((rect, text, max_size))

    for rect, text, size in text_items:
        ja = translate_text(text)
        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
        font_size = max(6, min(size * 0.8, 22))
        html = f'<div style="font-size:{font_size}px; font-family:sans-serif; color:#000; line-height:1.15;">{html_escape(ja)}</div>'
        page.insert_htmlbox(rect, html, overlay=True)

def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    in_path = OUT if (os.path.exists(OUT) and START_PAGE > 0) else SRC
    doc = fitz.open(in_path)
    end = doc.page_count if END_PAGE is None else min(END_PAGE, doc.page_count)
    print(f'input: {in_path}')
    print(f'pages: {doc.page_count}, processing {START_PAGE+1}..{end}')

    for i in range(START_PAGE, end):
        if i % 5 == 0:
            print('page', i + 1)
        process_page(doc[i])

    # If editing the same file, PyMuPDF requires incremental save.
    same_file = os.path.abspath(in_path) == os.path.abspath(OUT)
    if same_file:
        doc.save(OUT, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    else:
        doc.save(OUT)
    print('saved', OUT)

if __name__ == '__main__':
    main()
