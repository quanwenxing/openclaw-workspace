#!/usr/bin/env bash
set -euo pipefail
cd /Users/username/.openclaw/workspace
echo mkdir -p docs/security/macmini_2026-02 docs/references research/ops archive/misc archive/delete-candidate
echo mv 'macmini_open_ports_full_20260205_101754.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_audit_20260204_135636.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_audit_addendum_20260204_135650.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_audit_ssh_20260204_135704.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_audit_ssh_d_20260204_135710.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_listeners_20260205_101355.txt' 'docs/security/macmini_2026-02/'
echo mv 'macmini_security_post_gui_disable_20260205_101350.txt' 'docs/security/macmini_2026-02/'
echo mv 'codex_gpt-5.3-codex_overview_2026-02-06.html' 'docs/references/'
echo mv 'dexter_guide_ja.html' 'docs/references/'
echo mv 'claude-analysis_openclaw-structure_2026-02-18.md' 'research/ops/'
echo mv 'claude_analysis_openclaw_structure_2026-02-18.md' 'research/ops/'
echo mv '棚卸し_2026-02-03.md' 'research/ops/'
echo mv 'out_en.txt' 'archive/misc/'
echo mv 'test_ja.pdf' 'archive/delete-candidate/'
echo mv 'test_html_ja.pdf' 'archive/delete-candidate/'
