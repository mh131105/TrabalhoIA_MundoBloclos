# Trabalho 1 — Mundo dos Blocos de Tamanho Variável

Repositório da equipe para o trabalho de Fundamentos de Inteligência Artificial (UFAM). **Estrutura inicial: ainda não há implementação, planos ou resultados.**

## Objetivo

Representar os três cenários em lógica de primeira ordem, descrever ações e relações de ordem parcial, construir planos manuais e codificar o problema em CNF para obter planos com um SAT solver. Comparar os planos gerados com os manuais.

## Arquivos

| Arquivo | Finalidade |
| --- | --- |
| `bw2cnf_var.py` | Gerador da codificação proposicional em CNF e do mapa de variáveis. |
| `interpretar.py` | Leitura do resultado do SAT solver com o mapa e apresentação do plano. |
| `relatorio.tex` | Descrição da solução em LaTeX, seguindo as seções pedidas no enunciado. |
| `README.md` | Documentação em Markdown, incluindo instruções de execução quando o código estiver pronto. |

## Trabalho pendente

- [ ] Formalizar blocos, posições, níveis, apoios, estabilidade e ação `move`, com pré-condições, efeitos e ordem parcial.
- [ ] Descrever os planos manuais das Situações 1, 2 e 3.
- [ ] Codificar os estados, metas, ações e restrições em CNF e gerar `trab01_blocos2SAT.cnf` e `trab01_blocos2SAT.map`.
- [ ] Executar o SAT solver nos três cenários e entregar `resultado1.txt`, `resultado2.txt` e `resultado3.txt`.
- [ ] Interpretar e comparar os resultados com os planos manuais; documentar a execução no README e no relatório.

As figuras de referência e os critérios completos estão em `T1_MundoDosBlocos.pdf` e `manual_variable_blocks.pdf`, fornecidos com o enunciado.

