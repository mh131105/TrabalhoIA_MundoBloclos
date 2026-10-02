"""Grounding finito LPO -> CNF; ações qualitativas e geometria por slots."""
import argparse
from itertools import combinations
from pathlib import Path
from cenarios import BLOCKS, MAX_POINT, MAX_LEVEL, FIGURAS, METAS


def overlap(b, p, c, q):
    return max(p, q) < min(p + BLOCKS[b], q + BLOCKS[c])


class Encoding:
    def __init__(self):
        self.ids, self.clauses = {}, []

    def v(self, kind, *args):
        name = f'{kind}({",".join(map(str, args))})'
        if name not in self.ids:
            self.ids[name] = len(self.ids) + 1
        return self.ids[name]

    def add(self, *literals):
        self.clauses.append(list(literals))

    def exactly_one(self, variables):
        self.add(*variables)
        for x, y in combinations(variables, 2):
            self.add(-x, -y)

    def equivalent_or(self, variable, alternatives):
        self.add(-variable, *alternatives)
        for x in alternatives:
            self.add(-x, variable)

    def write(self, directory):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / 'trab01_blocos2SAT.cnf').open('w') as out:
            out.write(f'p cnf {len(self.ids)} {len(self.clauses)}\n')
            out.writelines(' '.join(map(str, c)) + ' 0\n' for c in self.clauses)
        (directory / 'trab01_blocos2SAT.map').write_text(
            ''.join(f'{v} {name}\n' for name, v in self.ids.items()), encoding='utf-8')


def encode(initial, goal, horizon):
    if horizon < 0:
        raise ValueError('horizonte deve ser não negativo')
    e = Encoding()
    v, add = e.v, e.add
    positions = {b: range(MAX_POINT - length + 1) for b, length in BLOCKS.items()}
    poses = [(b, p, level) for b in BLOCKS for p in positions[b]
             for level in range(MAX_LEVEL + 1)]
    actions = [(b, y, p) for b in BLOCKS for y in (*BLOCKS, 'T')
               if y != b for p in positions[b]]
    for t in range(horizon + 1):
        # Unicidade de coordenadas e pose <-> at & lev (Tseitin).
        for b in BLOCKS:
            e.exactly_one([v('at', b, p, t) for p in positions[b]])
            e.exactly_one([v('lev', b, level, t) for level in range(MAX_LEVEL + 1)])
        for b, p, level in poses:
            q, a, h = v('pose', b, p, level, t), v('at', b, p, t), v('lev', b, level, t)
            add(-q, a); add(-q, h); add(-a, -h, q)
        # Ocupação de cada célula e ausência de colisões.
        for slot in range(MAX_POINT):
            for level in range(MAX_LEVEL + 1):
                occupants = [v('pose', b, p, level, t) for b in BLOCKS for p in positions[b]
                             if p <= slot < p + BLOCKS[b]]
                e.equivalent_or(v('occ', slot, level, t), occupants)
        for (b, p, level), (c, q, height) in combinations(poses, 2):
            if b != c and level == height and overlap(b, p, c, q):
                add(-v('pose', b, p, level, t), -v('pose', c, q, height, t))
        # >= k de n slots: toda combinação de n-k+1 contém um ocupado.
        for b, p, level in poses:
            if level:
                below = [v('occ', slot, level - 1, t) for slot in range(p, p + BLOCKS[b])]
                k = (BLOCKS[b] + 1) // 2
                for subset in combinations(below, len(below) - k + 1):
                    add(-v('pose', b, p, level, t), *subset)
            above = [v('pose', c, q, height, t) for c, q, height in poses
                     if c != b and height > level and overlap(b, p, c, q)]
            # Para a pose ativa, clr sse não há bloco sobre sua coluna.
            add(-v('pose', b, p, level, t), v('clr', b, t), *above)
            for other in above:
                add(-v('pose', b, p, level, t), -v('clr', b, t), -other)
    for t, state in ((0, initial), (horizon, goal)):
        for b, (p, level) in state.items():
            if b not in BLOCKS or p not in positions[b] or not 0 <= level <= MAX_LEVEL:
                raise ValueError('estado com coordenadas fora do domínio')
            add(v('at', b, p, t)); add(v('lev', b, level, t))
    for t in range(horizon):
        e.exactly_one([v('mv', b, y, p, t) for b, y, p in actions])
        for b in BLOCKS:
            moved = v('moved', b, t)
            e.equivalent_or(moved, [v('mv', c, y, p, t) for c, y, p in actions if c == b])
            # Blocos não movidos preservam cada coordenada nos dois sentidos.
            for kind, domain in (('at', positions[b]), ('lev', range(MAX_LEVEL + 1))):
                for x in domain:
                    old, new = v(kind, b, x, t), v(kind, b, x, t + 1)
                    add(moved, -old, new); add(moved, old, -new)
        for b, y, p in actions:
            m = v('mv', b, y, p, t)
            add(-m, v('clr', b, t)); add(-m, v('at', b, p, t + 1))
            if y != 'T':
                for q in positions[y]:
                    if not overlap(b, p, y, q):
                        add(-m, -v('at', y, q, t))
                add(-m, -v('lev', y, MAX_LEVEL, t))
            for level in (range(MAX_LEVEL + 1) if y == 'T' else range(1, MAX_LEVEL + 1)):
                if y == 'T' and level != 0:
                    continue
                guard = [-m] + ([] if y == 'T' else [-v('lev', y, level - 1, t)])
                add(*guard, v('lev', b, level, t + 1))
                add(*guard, -v('at', b, p, t), -v('lev', b, level, t))
                # Espaço local, não clr(y): admite a e b lado a lado sobre c.
                for c, q, height in poses:
                    if c != b and height >= level and overlap(b, p, c, q):
                        add(*guard, -v('pose', c, q, height, t))
    return e


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cenario', type=int, choices=FIGURAS, default=1)
    parser.add_argument('--meta', help='nome do estado da figura; padrão Sf4/S5/S7')
    parser.add_argument('--horizonte', type=int, default=4)
    parser.add_argument('--saida', type=Path, default=Path('.'))
    args = parser.parse_args()
    goal = args.meta or METAS[args.cenario]
    if goal not in FIGURAS[args.cenario]:
        parser.error('meta inexistente no cenário')
    e = encode(FIGURAS[args.cenario]['S0'], FIGURAS[args.cenario][goal], args.horizonte)
    e.write(args.saida)
    print(f'Gerado: {len(e.ids)} variáveis, {len(e.clauses)} cláusulas')


if __name__ == '__main__':
    main()
