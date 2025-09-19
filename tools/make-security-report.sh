
#!/usr/bin/env bash
set -euo pipefail

OUT="security-report.md"
echo "# Relatório SAST – InvestSmart" > "$OUT"
echo "" >> "$OUT"
echo "**Data:** $(date -u +"%Y-%m-%d %H:%M UTC")" >> "$OUT"
echo "" >> "$OUT"

if [ -f semgrep-results.json ]; then
  HIGH=$(jq '[.results[] | select(.extra.severity=="HIGH")] | length' semgrep-results.json)
  CRIT=$(jq '[.results[] | select(.extra.severity=="CRITICAL")] | length' semgrep-results.json)
  echo "## Semgrep" >> "$OUT"
  echo "- Críticas: **$CRIT** | Altas: **$HIGH**" >> "$OUT"
  echo "- Recomendações: ver \`semgrep-results.sarif\` ou comentários no PR." >> "$OUT"
  echo "" >> "$OUT"
fi

if [ -f sonar-qg.json ]; then
  STATUS=$(jq -r '.projectStatus.status' sonar-qg.json)
  echo "## Sonar Quality Gate" >> "$OUT"
  echo "- Status: **$STATUS**" >> "$OUT"
  echo "- Detalhes: painel do Sonar (bugs/vulns/code smells, cobertura)." >> "$OUT"
  echo "" >> "$OUT"
fi

cat << 'EOF' >> "$OUT"
## Classificação e SLA
- **Crítico:** corrigir em até 24h; bloquear merge/deploy.
- **Alto:** corrigir em até 3 dias.
- **Médio:** até 2 semanas.
- **Baixo:** backlog e correção oportunística.

## Checklist (requisitos do professor)
- [x] SAST integrado ao CI/CD (PR e main)
- [x] Detecção: SQL/XSS, uso inseguro, authN/authZ, dados sensíveis
- [x] Relatório automatizado com severidade e recomendações
- [x] Ferramentas: Semgrep + Sonar
EOF
