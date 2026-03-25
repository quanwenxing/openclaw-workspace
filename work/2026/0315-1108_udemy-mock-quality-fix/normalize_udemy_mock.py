#!/usr/bin/env python3
import json, re
from pathlib import Path

path = Path('/Users/username/.openclaw/workspace/udemy-mock/data/tests.json')
data = json.loads(path.read_text(encoding='utf-8'))

def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return s
    reps = {
        'Amazon の岩盤': 'Amazon Bedrock',
        'Amazon Bedrock の Amazon Guardrails': 'Amazon Bedrock Guardrails',
        'Amazon の Guardrails': 'Amazon Bedrock Guardrails',
        'Agentsを': 'Agents を',
        'Agentsが': 'Agents が',
        'Agentsは': 'Agents は',
        'Agentsの': 'Agents の',
        'Knowledge Basesを': 'Knowledge Bases を',
        'Knowledge Basesは': 'Knowledge Bases は',
        'Knowledge Basesの': 'Knowledge Bases の',
        'GenAIアプリケーション': 'GenAI アプリケーション',
        'GenAI API': 'GenAI API',
        'Amazon Guardrails': 'Amazon Bedrock Guardrails',
        'Amazon Bedrock Flows': 'Amazon Bedrock Prompt Flows',
        'Amazon Bedrock プロンプト フロー': 'Amazon Bedrock Prompt Flows',
        'Amazon Bedrock プロンプトフロー': 'Amazon Bedrock Prompt Flows',
        'Amazon SageMaker Clear': 'Amazon SageMaker Clarify',
        'Amazon SageMaker AI': 'Amazon SageMaker',
        'Amazon Bedrock データオートメーション': 'Amazon Bedrock Data Automation',
        'データ オートメーション': 'Data Automation',
        'アマゾンイベントブリッジ': 'Amazon EventBridge',
        'AWSクラウドトレイルレイク': 'AWS CloudTrail Lake',
        'Eveidently': 'Evidently',
        'fresh_interval': 'refresh_interval',
        '超大規模 FM': '大規模 FM',
    }
    for a,b in reps.items():
        s = s.replace(a,b)
    s = s.replace('  ', ' ')
    s = re.sub(r'\s+([。、「」])', r'\1', s)
    s = re.sub(r'([A-Za-z0-9])\s+([A-Za-z0-9])', r'\1 \2', s)
    s = s.replace('。 は、', ' は、')
    s = s.replace('。 2', '。2')
    s = s.replace('。 95.', '。95%')
    s = s.replace('<; の場合', '95% 未満の場合')
    return s.strip()

def explain_only_correct(explain: str, answer_opt: str) -> str:
    s = clean_text(explain)
    s = re.sub(r'^正[解]?:\s*', '', s)
    s = re.sub(r'^CORRECT:\s*', '', s)
    s = re.sub(r'\s+主要な概念:.*$', '', s)
    s = re.sub(r'\s+重要な概念:.*$', '', s)
    s = re.sub(r'\s+主要な\w+.*$', '', s)
    if ' INCORRECT:' in s:
        s = s.split(' INCORRECT:')[0].strip()
    if s.startswith(answer_opt + ' '):
        s = s[len(answer_opt):].strip()
    elif s.startswith(answer_opt):
        s = s[len(answer_opt):].strip(' ：:。')
    return s.strip(' 。') + '。'

def summarize(text: str, maxlen=72) -> str:
    text = clean_text(text)
    text = re.sub(r'^[正解]?:\s*', '', text)
    text = text.split('。')[0].strip()
    if len(text) > maxlen:
        text = text[:maxlen].rstrip(' 、,') + '…'
    return text

def classify_reason(opt: str, question: str, correct_explain: str) -> str:
    o = clean_text(opt)
    c = clean_text(correct_explain)
    key = summarize(c, 34)
    if any(k in o for k in ['CloudWatch', 'X-Ray', 'Logs', 'Synthetics', 'CloudTrail', 'EventBridge', 'Config']):
        return f'監視・可観測性・イベント処理の仕組みであり、{key}を直接実現する解ではありません。'
    if any(k in o for k in ['Guardrails', 'WAF', 'Inspector', 'Macie', 'Security Hub']):
        return f'主に安全性やセキュリティ制御のための機能で、{key}という主目的には直結しません。'
    if any(k in o for k in ['Lambda', 'Step Functions', 'API Gateway', 'AppSync', 'SQS', 'SNS', 'DynamoDB', 'EC2', 'ECS', 'Batch']) and 'Bedrock' not in o and 'Knowledge Bases' not in o:
        return f'AWS の周辺実装としては成立しても、{key}を最短で満たすマネージド機能そのものではありません。'
    if any(k in o for k in ['SageMaker', 'JumpStart', 'Canvas', 'CodeGuru', 'DeepAR', 'BlazingText']):
        return f'SageMaker 系や別用途の ML 機能に寄せた案で、{key}に対しては過剰または用途違いです。'
    if any(k in o for k in ['Textract', 'Transcribe', 'Polly', 'Comprehend', 'Rekognition', 'Kendra', 'Q Business']):
        return f'{o.split()[0]} は特定用途向けのサービスであり、{key}に必要な役割と一致しません。'
    if any(k in o for k in ['manual', '手動', 'QA', 'ドキュメント', 'GitHub', 'CodeCommit', 'S3 バージョニング']):
        return f'運用や手動プロセス中心の案で、設問が求める AWS 機能による自動化された解決になっていません。'
    return f'この案は別の目的には使えても、設問の要件である「{key}」を満たす最適解ではありません。'

count = 0
for test in data['tests']:
    test['title'] = clean_text(test['title'])
    test['description'] = clean_text(test['description'])
    for q in test['questions']:
        q['question'] = clean_text(q['question'])
        q['options'] = [clean_text(x) for x in q['options']]
        ans = q['answer']
        q['explain'] = explain_only_correct(q['explain'], q['options'][ans])
        new_ww = []
        for i, (opt, ww) in enumerate(zip(q['options'], q['whyWrong'])):
            if i == ans:
                new_ww.append('')
                continue
            w = clean_text(ww or '')
            w = w.replace('詳細は上の解説を確認してください。', '').replace('この問題で求められている要件を満たしていません。', '').strip()
            w = re.sub(r'\s+主要な概念:.*$', '', w)
            w = re.sub(r'\s+重要な概念:.*$', '', w)
            w = w.strip()
            if not w or w == opt or '正解です' in w:
                w = classify_reason(opt, q['question'], q['explain'])
                count += 1
            elif w.startswith(opt):
                rest = w[len(opt):].strip(' 。:：-')
                if rest:
                    w = rest
            if len(w) > 220:
                parts = [p.strip() for p in w.split('。') if p.strip()]
                w = '。'.join(parts[:2]).strip()
                if w and not w.endswith('。'):
                    w += '。'
            new_ww.append(clean_text(w))
        q['whyWrong'] = new_ww

path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print('rewritten', count)
