# Contribuindo

Obrigado por querer melhorar o heditor.

## Novo estilo
1. Produza pelo menos um vídeo com o estilo e passe por todos os gates de `references/quality-gates.md`.
2. Escreva `skills/heditor/references/styles/<slug>.md` seguindo `references/adding-styles.md` (mesma estrutura dos estilos existentes, em inglês, sem dados privados nem marcas de terceiros).
3. Adicione a linha em `references/styles/INDEX.md`, na tabela do `SKILL.md` e no `README.md`.

## Código do kit
- Python 3.10+, PEP 8, funções pequenas e determinísticas (nada de aleatoriedade sem semente).
- Rode `bash skills/heditor/scripts/setup.sh` e um corte completo (`heditor new` → `finalize`) antes de abrir o PR.
- Não adicione arquivos de áudio, vídeo ou fontes ao repositório: use o catálogo (`assets/catalog.json`) e o `fetch_assets.py`.

## Issues
Descreva sistema operacional, agente usado, saída do `heditor doctor` e o comando que falhou.
