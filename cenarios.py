"""Coordenadas (ponto inicial, nível) transcritas das figuras do enunciado."""
BLOCKS = {'a': 1, 'b': 1, 'c': 2, 'd': 3}
MAX_POINT, MAX_LEVEL = 6, 3

def state(a, b, c, d):
    return dict(zip(BLOCKS, (a, b, c, d)))

S0 = state((3, 0), (5, 0), (0, 0), (3, 1))
SITUACAO1 = {
    'S0': S0,
    'Sf1': state((4, 1), (5, 1), (4, 2), (3, 0)),
    'Sf2': state((4, 2), (5, 2), (4, 1), (3, 0)),
    'Sf3': state((2, 0), (5, 0), (0, 0), (0, 1)),
    'Sf4': state((0, 1), (5, 0), (0, 0), (2, 0)),
}
SITUACAO2 = {
    'S0': state((0, 1), (1, 1), (0, 0), (3, 0)),
    'S1': state((0, 1), (2, 0), (0, 0), (3, 0)),
    'S2': state((2, 1), (2, 0), (0, 0), (3, 0)),
    'S3': state((2, 1), (2, 0), (4, 1), (3, 0)),
    'S4': state((4, 2), (2, 0), (4, 1), (3, 0)),
    'S5': SITUACAO1['Sf2'],
}
SITUACAO3 = {
    'S0': S0,
    'S1': state((3, 0), (5, 0), (0, 0), (0, 1)),
    'S2': state((5, 1), (5, 0), (0, 0), (0, 1)),
    'S3': state((5, 1), (5, 0), (0, 0), (2, 0)),
    'S4': SITUACAO1['Sf4'],
    'S5': state((0, 1), (1, 1), (0, 0), (2, 0)),
    'S6': state((0, 1), (1, 1), (0, 0), (2, 0)),
    'S7': SITUACAO2['S0'],
}
FIGURAS = {1: SITUACAO1, 2: SITUACAO2, 3: SITUACAO3}
METAS = {1: 'Sf4', 2: 'S5', 3: 'S7'}
# Planos de referência analíticos, conferidos pelo simulador independente.
Q = [('d', 'c', 0), ('a', 'b', 5), ('d', 'T', 2),
     ('a', 'c', 0), ('b', 'c', 1), ('d', 'T', 3)]
R = [('b', 'T', 2), ('a', 'b', 2), ('c', 'd', 4),
     ('a', 'c', 4), ('b', 'c', 5)]
MANUAIS = {
    (1, 'Sf1'): Q + [('a', 'd', 4), ('b', 'd', 5), ('c', 'a', 4)],
    (1, 'Sf2'): Q + R,
    # Alternativa suplementar corrigida com busca e conferida passo a passo.
    (1, 'Sf3'): [('d', 'c', 0), ('a', 'b', 5), ('d', 'T', 2),
                  ('a', 'c', 1), ('b', 'c', 0), ('d', 'T', 3),
                  ('a', 'T', 2), ('d', 'a', 1), ('b', 'T', 5), ('d', 'a', 0)],
    (1, 'Sf4'): Q[:4], (2, 'S5'): R, (3, 'S7'): Q,
}
