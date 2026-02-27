#!/usr/bin/env bash
set -euo pipefail
cd /Users/username/.openclaw/workspace

# Dry-run only: preview commands below, then remove leading echo to execute
mkdir -p docs/aws docs/security/macmini_2026-02 docs/references research/pqc-roadmap research/ops archive/misc archive/tmp-tools archive/delete-candidate

echo mv 'AWSCertifiedGenerativeAIDeveloper.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_p1.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_p1a.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_p1b.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_p2.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_p3.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_p4.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_part1.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_part2.pdf' 'docs/aws/'
echo rm 'AWSCertifiedGenerativeAIDeveloper_ja_small.pdf'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_split01.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_split02.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_split03.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_split04.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_split05.pdf' 'docs/aws/'
echo mv 'AWSCertifiedGenerativeAIDeveloper_ja_split06.pdf' 'docs/aws/'
echo rm 'AWSCertifiedGenerativeAIDeveloper_ja_tg.pdf'
echo mv 'claude-analysis_openclaw-structure_2026-02-18.md' 'research/ops/'
echo mv 'claude_analysis_openclaw_structure_2026-02-18.md' 'research/ops/'
echo mv 'codex_gpt-5.3-codex_overview_2026-02-06.html' 'docs/references/'
echo mv 'dexter_guide_ja.html' 'docs/references/'
echo mv 'macmini_open_ports_full_20260205_101754.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_audit_20260204_135636.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_audit_addendum_20260204_135650.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_audit_ssh_20260204_135704.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_audit_ssh_d_20260204_135710.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_listeners_20260205_101355.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_post_gui_disable_20260205_101350.txt' 'docs/security/macmini_2026-02/'
echo mv 'out_en.txt' 'archive/misc/'
echo mv 'pqc-roadmap-slidev-styled.pdf' 'research/pqc-roadmap/'
echo mv 'pqc-roadmap-slidev.md' 'research/pqc-roadmap/'
echo mv 'pqc-roadmap-slidev.pdf' 'research/pqc-roadmap/'
echo mv 'sources.yaml' 'docs/references/'
echo mv 'test_html_ja.pdf' 'archive/delete-candidate/'
echo mv 'test_ja.pdf' 'archive/delete-candidate/'
echo mv 'translate_pdf_ja.log' 'archive/tmp-tools/'
echo mv 'translate_pdf_ja.py' 'archive/tmp-tools/'
echo mv '棚卸し_2026-02-03.md' 'research/ops/'

# End dry-run
