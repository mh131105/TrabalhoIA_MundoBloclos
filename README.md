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

## Resolução Manual

# Resolução Manual: Mundo dos Blocos de Tamanho Variável

## Notação

Comprimentos: ℓ(a) = ℓ(b) = 1, ℓ(c) = 2, ℓ(d) = 3. A mesa tem 6 slots (s0 a s5).

Cada bloco é escrito como bloco = p/l, onde p é o ponto inicial e l é o nível. A ação move(b, y, p) significa mover b para cima de y (ou da mesa T), começando no ponto p.

Estabilidade: um bloco no nível l > 0 precisa de pelo menos ⌈ℓ/2⌉ slots do seu span ocupados no nível l − 1.

## 1. Situação 1

Estado inicial S0:

a = 3/0, b = 5/0, c = 0/0, d = 3/1

Relações on: on(c, T), on(a, T), on(b, T), on(d, a), on(d, b).

Estados finais:

| Meta | Estado | Relações on |
|---|---|---|
| Sf1 | a = 4/1, b = 5/1, c = 4/2, d = 3/0 | on(d, T), on(a, d), on(b, d), on(c, a), on(c, b) |
| Sf2 | a = 4/2, b = 5/2, c = 4/1, d = 3/0 | on(d, T), on(c, d), on(a, c), on(b, c) |
| Sf3 | a = 2/0, b = 5/0, c = 0/0, d = 0/1 | on(c, T), on(a, T), on(b, T), on(d, c), on(d, a) |
| Sf4 | a = 0/1, b = 5/0, c = 0/0, d = 2/0 | on(c, T), on(d, T), on(b, T), on(a, c) |

### 1.1 S0 até Sf3

| t | Ação | Estado após a ação |
|---|---|---|
| 0 | | a = 3/0, b = 5/0, c = 0/0, d = 3/1 |
| 1 | move(d, c, 0) | d = 0/1 |
| 2 | move(a, T, 2) | a = 2/0 |

### 1.2 S0 até Sf4

| t | Ação | Estado após a ação |
|---|---|---|
| 1 | move(d, c, 0) | d = 0/1 |
| 2 | move(a, b, 5) | a = 5/1 |
| 3 | move(d, T, 2) | d = 2/0 |
| 4 | move(a, c, 0) | a = 0/1 |

### 1.3 S0 até Sf1

| t | Ação | Estado após a ação |
|---|---|---|
| 1 | move(d, c, 0) | d = 0/1 |
| 2 | move(a, T, 2) | a = 2/0 |
| 3 | move(d, a, 1) | d = 1/1 |
| 4 | move(b, c, 0) | b = 0/1 |
| 5 | move(d, T, 3) | d = 3/0 |
| 6 | move(a, d, 4) | a = 4/1 |
| 7 | move(b, d, 5) | b = 5/1 |
| 8 | move(c, a, 4) | c = 4/2 |

### 1.4 S0 até Sf2

| t | Ação | Estado após a ação |
|---|---|---|
| 1 | move(c, T, 1) | c = 1/0 |
| 2 | move(d, c, 0) | d = 0/1 |
| 3 | move(a, T, 0) | a = 0/0 |
| 4 | move(d, c, 1) | d = 1/1 |
| 5 | move(b, a, 0) | b = 0/1 |
| 6 | move(d, T, 3) | d = 3/0 |
| 7 | move(c, d, 4) | c = 4/1 |
| 8 | move(b, c, 5) | b = 5/2 |
| 9 | move(a, c, 4) | a = 4/2 |

## 2. Situação 2

Estados:

| Estado | a | b | c | d |
|---|---|---|---|---|
| S0 | 0/1 | 1/1 | 0/0 | 3/0 |
| S1 | 0/1 | 2/0 | 0/0 | 3/0 |
| S2 | 2/1 | 2/0 | 0/0 | 3/0 |
| S3 | 2/1 | 2/0 | 4/1 | 3/0 |
| S4 | 4/2 | 2/0 | 4/1 | 3/0 |
| S5 | 4/2 | 5/2 | 4/1 | 3/0 |

Plano de S0 até S5:

| t | Ação | Estado |
|---|---|---|
| 1 | move(b, T, 2) | S1 |
| 2 | move(a, b, 2) | S2 |
| 3 | move(c, d, 4) | S3 |
| 4 | move(a, c, 4) | S4 |
| 5 | move(b, c, 5) | S5 |

## 3. Situação 3

Estados:

| Estado | a | b | c | d |
|---|---|---|---|---|
| S0 | 3/0 | 5/0 | 0/0 | 3/1 |
| S1 | 3/0 | 5/0 | 0/0 | 0/1 |
| S2 | 5/1 | 5/0 | 0/0 | 0/1 |
| S3 | 5/1 | 5/0 | 0/0 | 2/0 |
| S4 | 0/1 | 5/0 | 0/0 | 2/0 |
| S5 | 0/1 | 1/1 | 0/0 | 2/0 |
| S6 | 0/1 | 1/1 | 0/0 | 2/0 |
| S7 | 0/1 | 1/1 | 0/0 | 3/0 |

Plano de S0 até S7:

| t | Ação | Estado |
|---|---|---|
| 1 | move(d, c, 0) | S1 |
| 2 | move(a, b, 5) | S2 |
| 3 | move(d, T, 2) | S3 |
| 4 | move(a, c, 0) | S4 |
| 5 | move(b, c, 1) | S5 (= S6) |
| 6 | move(d, T, 3) | S7 |

## 4. Resumo

| Cenário | Meta | Número de ações |
|---|---|---|
| Situação 1 | Sf3 | 2 |
| Situação 1 | Sf4 | 4 |
| Situação 1 | Sf1 | 8 |
| Situação 1 | Sf2 | 9 |
| Situação 2 | S5 | 5 |
| Situação 3 | S7 | 6 |

## 5. Ordem parcial

Ligações causais entre as ações (A ≺ B significa que B depende do efeito de A):

- Sf4: move(d, c, 0) ≺ move(a, b, 5) ≺ move(d, T, 2) ≺ move(a, c, 0).
- Sf1: move(d, c, 0) ≺ move(a, T, 2) ≺ move(d, a, 1) ≺ move(b, c, 0) ≺ move(d, T, 3) ≺ {move(a, d, 4), move(b, d, 5)} ≺ move(c, a, 4). As duas ações entre chaves são independentes entre si.
