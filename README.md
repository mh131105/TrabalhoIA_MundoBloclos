# Mundo dos Blocos de Tamanho Variável

Inclui formalização em LPO, efeitos e persistência, análise de ordem parcial, codificação CNF, modelos reais do MiniSat22, planos interpretados e relatório LaTeX/PDF.

## Entrega

O conteúdo completo está em [TrabalhoIA_MundoBloclos_equipe_20](TrabalhoIA_MundoBloclos_equipe_20). Equipe 20.

- [Relatório PDF](TrabalhoIA_MundoBloclos_equipe_20/relatorio.pdf)
- [Fonte LaTeX](TrabalhoIA_MundoBloclos_equipe_20/relatorio.tex), pronta para compilar no Overleaf
- [Resultados e modelos](TrabalhoIA_MundoBloclos_equipe_20/resultados)

## Integrantes

- Matheus Henrique de Oliveira Garcia — matheus.garcia@icomp.ufam.edu.br
- Samuel de Sousa Castro — samuel.castro@icomp.ufam.edu.br
- Gabriel Gregório dos Santos Vitor — gabriel.vitor@icomp.ufam.edu.br
- Murillo Rafael de Alcântara Mota — murillo.alcantara@icomp.ufam.edu.br
- Lucas Melo dos Santos — lucas.melo@icomp.ufam.edu.br

## Interpretação explícita

Blocos `a,b,c,d` têm comprimentos `1,1,2,3`. A mesa tem seis slots `0..5`, delimitados pelos pontos `0..6`; níveis `0..3`. Cada bloco acima da mesa requer pelo menos `ceil(comprimento/2)` slots apoiados. Não há colisões no mesmo nível. O bloco movido deve estar livre de qualquer peça acima de seu span. A coluna de chegada precisa estar livre, portanto não é permitido inserir sob pontes.

O destino exige apenas seu **span local livre**, pois exigir o apoio inteiro livre impossibilitaria `a` e `b` lado a lado sobre `c`. O exemplo do manual que leva `a` à mesa no ponto 4 e depois `d` à mesa no ponto 2 colide; a solução corrigida coloca `a` temporariamente sobre `b` no ponto 5. Essas escolhas afetam o domínio e a minimalidade informada.

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

## Execução reproduzível

```sh
cd TrabalhoIA_MundoBloclos_equipe_20
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python resolver.py --todos
python testes.py
python interpretar.py resultados/cenario1/resultado1.txt
pdflatex -interaction=nonstopmode -halt-on-error relatorio.tex
pdflatex -interaction=nonstopmode -halt-on-error relatorio.tex
```

Python 3.10+ e `python-sat==1.8.dev24`. A busca começa em horizonte zero e salva o primeiro modelo SAT. Sem `--todos`, resolve apenas as metas principais: Situação 1/Sf4, Situação 2/S5, Situação 3/S7. Com `--todos`, também resolve os estados intermediários, sempre a partir do S0 da respectiva situação.

Gerar apenas CNF/mapa para um horizonte escolhido:

```sh
python bw2cnf_var.py --cenario 1 --meta Sf4 --horizonte 4 --saida exemplo
```

Opcionalmente, com MiniSAT instalado à parte, `minisat exemplo/trab01_blocos2SAT.cnf exemplo/resultado1.txt`; depois `python interpretar.py exemplo/resultado1.txt`. A execução validada nesta entrega usa a biblioteca MiniSat22 via PySAT.

## Organização e mapeamento

| Arquivo | Responsabilidade |
|---|---|
| `cenarios.py` | Dimensões, figuras e planos de referência |
| `dominio.py` | Simulador geométrico independente da CNF |
| `bw2cnf_var.py` | Unicidade, poses, ocupação, estabilidade, ações e frame em CNF |
| `resolver.py` | Busca por horizonte e execução MiniSat22 |
| `interpretar.py` | Verifica CNF, decodifica modelo e reexecuta geometria |
| `testes.py` | Regressões e mínimos por busca em largura |
| `relatorio.tex` / `.pdf` | Formalização, planos, ordem parcial, execução e comparação |

Cada cenário possui `trab01_blocos2SAT.cnf`, `trab01_blocos2SAT.map`, `resultadoN.txt`, `plano.txt` e `horizontes.json`. As três metas principais ficam diretamente em `resultados/cenarioN`; as demais, em subpastas pelo nome da meta. Não misture mapas ou modelos de instâncias diferentes.

## Resultados verificados

| Situação | Meta | Plano de referência | Mínimo SAT | Variáveis | Cláusulas |
|---|---|---:|---:|---:|---:|
| 1 | Sf1 | 9 | 9 | 2282 | 82710 |
| 1 | Sf2 | 11 | 10 | 2519 | 91711 |
| 1 | Sf3 | 10 | 10 | 2519 | 91711 |
| 1 | Sf4 | 4 | 4 | 1097 | 37705 |
| 2 | S1 | - | 1 | 386 | 10702 |
| 2 | S2 | - | 2 | 623 | 19703 |
| 2 | S3 | - | 3 | 860 | 28704 |
| 2 | S4 | - | 4 | 1097 | 37705 |
| 2 | S5 | 5 | 5 | 1334 | 46706 |
| 3 | S1 | - | 1 | 386 | 10702 |
| 3 | S2 | - | 2 | 623 | 19703 |
| 3 | S3 | - | 3 | 860 | 28704 |
| 3 | S4 | - | 4 | 1097 | 37705 |
| 3 | S5 | - | 5 | 1334 | 46706 |
| 3 | S6 | - | 5 | 1334 | 46706 |
| 3 | S7 | 6 | 6 | 1571 | 55707 |

Todos os horizontes inferiores deram UNSAT. A busca em largura confirma os mínimos no mesmo domínio. `S5` e `S6` da Situação 3 são idênticos: a passagem não exige ação.

Os planos de referência da seção formal foram elaborados e revisados com assistência de IA; não alegamos uma etapa manual independente realizada pelo aluno. A alternativa suplementar Sf3 foi auxiliada por busca. A geração SAT usa os estados inicial/final, sem fixar os planos de referência. O relatório distingue essas origens e mostra todos os passos.

### Planos SAT extraídos

#### Situação 1, Sf1

```text
PLANO ENCONTRADO (9 ações); CNF e simulação validadas.
1. t=0: mover d para c, p=0
2. t=1: mover a para b, p=5
3. t=2: mover d para MESA, p=2
4. t=3: mover a para c, p=0
5. t=4: mover b para c, p=1
6. t=5: mover d para MESA, p=3
7. t=6: mover a para d, p=4
8. t=7: mover b para d, p=5
9. t=8: mover c para a, p=4
S0: a=(3,0); b=(5,0); c=(0,0); d=(3,1)
S1: a=(3,0); b=(5,0); c=(0,0); d=(0,1)
S2: a=(5,1); b=(5,0); c=(0,0); d=(0,1)
S3: a=(5,1); b=(5,0); c=(0,0); d=(2,0)
S4: a=(0,1); b=(5,0); c=(0,0); d=(2,0)
S5: a=(0,1); b=(1,1); c=(0,0); d=(2,0)
S6: a=(0,1); b=(1,1); c=(0,0); d=(3,0)
S7: a=(4,1); b=(1,1); c=(0,0); d=(3,0)
S8: a=(4,1); b=(5,1); c=(0,0); d=(3,0)
S9: a=(4,1); b=(5,1); c=(4,2); d=(3,0)
Apoios finais: a sobre d; b sobre d; c sobre a,b; d sobre T
```

#### Situação 1, Sf2

```text
PLANO ENCONTRADO (10 ações); CNF e simulação validadas.
1. t=0: mover c para MESA, p=1
2. t=1: mover d para c, p=0
3. t=2: mover a para b, p=5
4. t=3: mover d para c, p=1
5. t=4: mover a para MESA, p=0
6. t=5: mover b para a, p=0
7. t=6: mover d para MESA, p=3
8. t=7: mover c para d, p=4
9. t=8: mover b para c, p=5
10. t=9: mover a para c, p=4
S0: a=(3,0); b=(5,0); c=(0,0); d=(3,1)
S1: a=(3,0); b=(5,0); c=(1,0); d=(3,1)
S2: a=(3,0); b=(5,0); c=(1,0); d=(0,1)
S3: a=(5,1); b=(5,0); c=(1,0); d=(0,1)
S4: a=(5,1); b=(5,0); c=(1,0); d=(1,1)
S5: a=(0,0); b=(5,0); c=(1,0); d=(1,1)
S6: a=(0,0); b=(0,1); c=(1,0); d=(1,1)
S7: a=(0,0); b=(0,1); c=(1,0); d=(3,0)
S8: a=(0,0); b=(0,1); c=(4,1); d=(3,0)
S9: a=(0,0); b=(5,2); c=(4,1); d=(3,0)
S10: a=(4,2); b=(5,2); c=(4,1); d=(3,0)
Apoios finais: a sobre c; b sobre c; c sobre d; d sobre T
```

#### Situação 1, Sf3

```text
PLANO ENCONTRADO (10 ações); CNF e simulação validadas.
1. t=0: mover d para c, p=0
2. t=1: mover a para b, p=5
3. t=2: mover d para MESA, p=2
4. t=3: mover a para c, p=1
5. t=4: mover b para c, p=0
6. t=5: mover d para MESA, p=3
7. t=6: mover a para MESA, p=2
8. t=7: mover d para c, p=1
9. t=8: mover b para MESA, p=5
10. t=9: mover d para a, p=0
S0: a=(3,0); b=(5,0); c=(0,0); d=(3,1)
S1: a=(3,0); b=(5,0); c=(0,0); d=(0,1)
S2: a=(5,1); b=(5,0); c=(0,0); d=(0,1)
S3: a=(5,1); b=(5,0); c=(0,0); d=(2,0)
S4: a=(1,1); b=(5,0); c=(0,0); d=(2,0)
S5: a=(1,1); b=(0,1); c=(0,0); d=(2,0)
S6: a=(1,1); b=(0,1); c=(0,0); d=(3,0)
S7: a=(2,0); b=(0,1); c=(0,0); d=(3,0)
S8: a=(2,0); b=(0,1); c=(0,0); d=(1,1)
S9: a=(2,0); b=(5,0); c=(0,0); d=(1,1)
S10: a=(2,0); b=(5,0); c=(0,0); d=(0,1)
Apoios finais: a sobre T; b sobre T; c sobre T; d sobre a,c
```

#### Situação 1, Sf4

```text
PLANO ENCONTRADO (4 ações); CNF e simulação validadas.
1. t=0: mover d para c, p=0
2. t=1: mover a para b, p=5
3. t=2: mover d para MESA, p=2
4. t=3: mover a para c, p=0
S0: a=(3,0); b=(5,0); c=(0,0); d=(3,1)
S1: a=(3,0); b=(5,0); c=(0,0); d=(0,1)
S2: a=(5,1); b=(5,0); c=(0,0); d=(0,1)
S3: a=(5,1); b=(5,0); c=(0,0); d=(2,0)
S4: a=(0,1); b=(5,0); c=(0,0); d=(2,0)
Apoios finais: a sobre c; b sobre T; c sobre T; d sobre T
```

#### Situação 2, S5

```text
PLANO ENCONTRADO (5 ações); CNF e simulação validadas.
1. t=0: mover b para d, p=3
2. t=1: mover a para b, p=3
3. t=2: mover c para d, p=4
4. t=3: mover a para c, p=4
5. t=4: mover b para c, p=5
S0: a=(0,1); b=(1,1); c=(0,0); d=(3,0)
S1: a=(0,1); b=(3,1); c=(0,0); d=(3,0)
S2: a=(3,2); b=(3,1); c=(0,0); d=(3,0)
S3: a=(3,2); b=(3,1); c=(4,1); d=(3,0)
S4: a=(4,2); b=(3,1); c=(4,1); d=(3,0)
S5: a=(4,2); b=(5,2); c=(4,1); d=(3,0)
Apoios finais: a sobre c; b sobre c; c sobre d; d sobre T
```

#### Situação 3, S7

```text
PLANO ENCONTRADO (6 ações); CNF e simulação validadas.
1. t=0: mover d para c, p=0
2. t=1: mover a para b, p=5
3. t=2: mover d para MESA, p=2
4. t=3: mover a para c, p=0
5. t=4: mover b para c, p=1
6. t=5: mover d para MESA, p=3
S0: a=(3,0); b=(5,0); c=(0,0); d=(3,1)
S1: a=(3,0); b=(5,0); c=(0,0); d=(0,1)
S2: a=(5,1); b=(5,0); c=(0,0); d=(0,1)
S3: a=(5,1); b=(5,0); c=(0,0); d=(2,0)
S4: a=(0,1); b=(5,0); c=(0,0); d=(2,0)
S5: a=(0,1); b=(1,1); c=(0,0); d=(2,0)
S6: a=(0,1); b=(1,1); c=(0,0); d=(3,0)
Apoios finais: a sobre c; b sobre c; c sobre T; d sobre T
```
