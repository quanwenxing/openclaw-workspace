#!/usr/bin/env python3
import json
import re
import time
from pathlib import Path
from copy import deepcopy
from deep_translator import GoogleTranslator

ROOT = Path('/Users/username/.openclaw/workspace/udemy-mock')
SRC = ROOT / 'data' / 'tests.pre-japaneseize.2026-02-15.json'
OUT = ROOT / 'data' / 'tests.json'
CACHE = ROOT / 'data' / 'ja_translate_cache.v2.json'

GLOSSARY = [
    'Amazon Bedrock', 'Amazon SageMaker JumpStart', 'Amazon SageMaker', 'SageMaker Studio',
    'Amazon Q Business', 'Amazon Q Developer', 'Amazon Kendra', 'Amazon Textract',
    'Amazon Comprehend', 'Amazon OpenSearch Service', 'Amazon OpenSearch Serverless',
    'Amazon DynamoDB', 'Amazon S3', 'AWS Lambda', 'AWS Step Functions', 'AWS Glue',
    'AWS Glue Data Quality', 'AWS Glue Data Catalog', 'Amazon EventBridge', 'AWS IAM',
    'AWS CloudTrail', 'Amazon CloudWatch', 'AWS KMS', 'AWS Secrets Manager', 'Amazon API Gateway',
    'AWS AppSync', 'AWS Batch', 'AWS Fargate', 'Amazon EC2', 'Amazon EKS', 'Amazon ECS',
    'Amazon Rekognition', 'Amazon Lex', 'Amazon Polly', 'Amazon Transcribe', 'Amazon Translate',
    'Amazon Titan', 'Anthropic Claude', 'AI21 Labs', 'Cohere', 'Meta Llama', 'DeepSeek',
    'Retrieval Augmented Generation', 'RAG', 'DQDL', 'Fine-tuning', 'Prompt engineering',
    'Provisioned Throughput', 'On-Demand', 'Guardrails for Amazon Bedrock'
]
GLOSSARY = sorted(set(GLOSSARY), key=len, reverse=True)
JP_RE = re.compile(r'[ぁ-んァ-ヶ一-龥]')
PLACEHOLDER_RE = re.compile(r'__TERM(\d+)__')

POST_REPLACEMENTS = {
    'アマゾン・コンプリヘンド': 'Amazon Comprehend',
    'Amazon テキストラクト': 'Amazon Textract',
    'Amazon SageMaker ジャンプスタート': 'Amazon SageMaker JumpStart',
    'Amazon SageMaker ジャンプ スタート': 'Amazon SageMaker JumpStart',
    'アマゾン・ベッドロック': 'Amazon Bedrock',
    'Amazon ベッドロック': 'Amazon Bedrock',
    'AWS ステップ関数': 'AWS Step Functions',
    'アマゾンイベントブリッジ': 'Amazon EventBridge',
    'Amazon イベントブリッジ': 'Amazon EventBridge',
    'Amazon クラウドウォッチ': 'Amazon CloudWatch',
    'Amazon ダイナモDB': 'Amazon DynamoDB',
    'アマゾン Q ビジネス': 'Amazon Q Business',
    'アマゾン Q Developer': 'Amazon Q Developer',
    'Amazon Q デベロッパー': 'Amazon Q Developer',
    'Amazon ケンドラ': 'Amazon Kendra',
    'Amazon OpenSearch サービス': 'Amazon OpenSearch Service',
    '検索拡張生成': 'Retrieval Augmented Generation',
    '微調整': 'fine-tuning',
    'フルマネージド サービス': 'フルマネージドサービス',
    'フルマネージド サービス': 'フルマネージドサービス',
    '基盤モデル': '基盤モデル',
}


def load_json(path, default=None):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {} if default is None else default


def save_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')


def protect_terms(text):
    mapping = {}
    out = text
    for i, term in enumerate(GLOSSARY):
        token = f'__TERM{i}__'
        if term in out:
            out = out.replace(term, token)
            mapping[token] = term
    return out, mapping


def restore_terms(text, mapping):
    out = text
    for token, term in mapping.items():
        out = out.replace(token, term)
    return out


def tidy_ja(text):
    if not isinstance(text, str):
        return text
    out = text
    for src, dst in POST_REPLACEMENTS.items():
        out = out.replace(src, dst)
    out = re.sub(r'\s+([。、])', r'\1', out)
    out = re.sub(r'([A-Za-z0-9])\s+([A-Za-z])', r'\1 \2', out)
    out = re.sub(r'\s{2,}', ' ', out)
    out = out.replace('。 ', '。')
    out = out.replace('？ ', '？')
    out = out.replace('! ', '!')
    return out.strip()


def translate_text(text, translator, cache):
    if not text:
        return ''
    if JP_RE.search(text):
        return tidy_ja(text)
    if text in cache:
        return cache[text]
    protected, mapping = protect_terms(text)
    translated = None
    for attempt in range(4):
        try:
            if len(protected) <= 1200:
                translated = translator.translate(protected)
            else:
                parts = re.split(r'(?<=[.!?])\s+|\n+', protected)
                chunks, cur = [], ''
                for p in parts:
                    if not p:
                        continue
                    if len(cur) + len(p) + 1 <= 900:
                        cur = (cur + ' ' + p).strip()
                    else:
                        if cur:
                            chunks.append(cur)
                        cur = p
                if cur:
                    chunks.append(cur)
                translated = ' '.join(translator.translate(c) for c in chunks)
            break
        except Exception:
            time.sleep(0.8 * (attempt + 1))
    if translated is None:
        translated = text
    translated = restore_terms(translated, mapping)
    translated = tidy_ja(translated)
    cache[text] = translated
    return translated


def split_explain(explain, options):
    correct = ''
    wrong = {}
    text = explain.replace('\r\n', '\n').strip()
    if 'CORRECT:' not in text:
        return {'correct': text, 'wrong': wrong}
    m = re.search(r'CORRECT:\s*(.*?)\s+(?=INCORRECT:)', text, flags=re.S)
    if m:
        correct = m.group(1).strip()
    incorrect_blocks = re.findall(r'INCORRECT:\s*(.*?)(?=(?:INCORRECT:|$))', text, flags=re.S)
    for block in incorrect_blocks:
        block = block.strip()
        matched = None
        for opt in sorted(options, key=len, reverse=True):
            if block.startswith(opt):
                matched = opt
                reason = block[len(opt):].strip(' -:\n')
                wrong[opt] = reason.strip()
                break
        if matched is None:
            parts = block.split(' ', 1)
            if len(parts) == 2:
                wrong[parts[0]] = parts[1].strip()
    return {'correct': correct, 'wrong': wrong}


def normalize_question(q):
    q['question'] = re.sub(r'\.Which AWS service', '. Which AWS service', q['question'])
    q['question'] = re.sub(r'\.Which architecture', '. Which architecture', q['question'])
    q['question'] = re.sub(r'\.Which solution', '. Which solution', q['question'])
    q['question'] = re.sub(r'\.What ', '. What ', q['question'])
    return q


def main(limit_tests=None):
    src = load_json(SRC)
    out = deepcopy(src)
    cache = load_json(CACHE, {})
    translator = GoogleTranslator(source='en', target='ja')

    tests = out.get('tests', [])
    if limit_tests is not None:
        tests = tests[:limit_tests]
        out['tests'] = tests

    for ti, test in enumerate(tests, 1):
        test['title'] = f'模擬試験 {ti}' if ti != 2 else '模擬試験2'
        test['description'] = translate_text(test.get('description', ''), translator, cache)
        for qi, q in enumerate(test.get('questions', []), 1):
            q = normalize_question(q)
            q['question'] = translate_text(q.get('question', ''), translator, cache)
            q['options'] = [tidy_ja(opt) for opt in q.get('options', [])]
            parsed = split_explain(q.get('explain', ''), q['options'])
            correct_text = parsed['correct'] or q.get('explain', '')
            q['explain'] = translate_text(correct_text, translator, cache)
            why_wrong = ['' for _ in q['options']]
            for i, opt in enumerate(q['options']):
                if i == q.get('answer'):
                    continue
                reason = parsed['wrong'].get(opt, '')
                if not reason:
                    reason = f'{opt} はこの設問の要件を満たす主役のサービスではありません。要件に照らすと、正解の選択肢のほうが適切です。'
                    why_wrong[i] = reason
                else:
                    why_wrong[i] = translate_text(reason, translator, cache)
            q['whyWrong'] = [tidy_ja(x) for x in why_wrong]
            q['refs'] = [
                {'label': translate_text(r.get('label', '参考資料'), translator, cache), 'url': r.get('url', '')}
                for r in q.get('refs', []) if r.get('url')
            ]
            if qi % 10 == 0:
                print(f'test {ti}: {qi}/{len(test.get("questions", []))}')
                save_json(CACHE, cache)
                save_json(OUT, out)
    out['updatedAt'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    save_json(CACHE, cache)
    save_json(OUT, out)
    print('done')


if __name__ == '__main__':
    main()
