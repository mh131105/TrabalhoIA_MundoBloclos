"""Regressões geométricas, modelos SAT, mapas e comparação com busca em largura."""
from collections import deque
from pathlib import Path
import tempfile
import contextlib
import io
import unittest
from pysat.solvers import Minisat22
from cenarios import METAS, BLOCKS, FIGURAS, MANUAIS, Q, R, S0, SITUACAO1, SITUACAO2, SITUACAO3
from dominio import valid_state, move, replay, successors, derive_on
from bw2cnf_var import encode
from resolver import solve
from interpretar import check_cnf, decode, read_map, read_result, interpret


def key(state):
    return tuple(state[b] for b in BLOCKS)


def distances(initial):
    distances = {key(initial): 0}
    queue = deque([initial])
    while queue:
        state = queue.popleft()
        for _, child in successors(state):
            k = key(child)
            if k not in distances:
                distances[k] = distances[key(state)] + 1
                queue.append(child)
    return distances


class Tests(unittest.TestCase):
    def test_manual_plans_and_figures(self):
        for (scenario, goal), actions in MANUAIS.items():
            self.assertEqual(replay(FIGURAS[scenario]['S0'], actions)[-1], FIGURAS[scenario][goal])
        self.assertEqual(replay(SITUACAO2['S0'], R), list(SITUACAO2.values()))
        self.assertEqual(replay(S0, Q), [s for name, s in SITUACAO3.items() if name != 'S6'])
        self.assertEqual(SITUACAO3['S5'], SITUACAO3['S6'])
        self.assertTrue(all(valid_state(s) for states in FIGURAS.values() for s in states.values()))

    def test_bridge_and_local_destination(self):
        self.assertEqual(derive_on(S0)['d'], ['a', 'b'])
        final = replay(SITUACAO2['S0'], R)[-1]
        self.assertEqual(derive_on(final)['b'], ['c'])
        with self.assertRaises(ValueError):
            move(S0, ('c', 'T', 3))  # coluna de d bloqueada
        s = move(S0, ('d', 'c', 0))
        with self.assertRaises(ValueError):
            move(s, ('a', 'T', 2))  # espaço sob a extremidade suspensa de d
        with self.assertRaises(ValueError):
            move(s, ('a', 'T', 3))  # no-op
        erroneous = move(s, ('a', 'T', 4))
        with self.assertRaises(ValueError):
            move(erroneous, ('d', 'T', 2))  # erro no exemplo do manual

    def test_invalid_states(self):
        bad = dict(S0, d=(4, 1))  # d ultrapassa a mesa
        self.assertFalse(valid_state(bad))
        self.assertFalse(valid_state(dict(S0, d=(2, 1))))  # só a fornece um slot
        self.assertFalse(valid_state(dict(S0, a=(0, 0))))  # colisão com c
        with Minisat22(bootstrap_with=encode(dict(S0, d=(2, 1)), {}, 0).clauses) as sat:
            self.assertFalse(sat.solve())

    def test_zero_horizon(self):
        with Minisat22(bootstrap_with=encode(S0, S0, 0).clauses) as sat:
            self.assertTrue(sat.solve())
        with Minisat22(bootstrap_with=encode(S0, SITUACAO1['Sf4'], 0).clauses) as sat:
            self.assertFalse(sat.solve())
        with self.assertRaises(ValueError):
            encode(S0, S0, -1)

    def test_each_action_matches_geometry(self):
        # Ações legais e ilegais, sobre todos os estados desenhados (deduplicados).
        states = {key(s): s for fig in FIGURAS.values() for s in fig.values()}
        for state in states.values():
            e = encode(state, {}, 1)
            with Minisat22(bootstrap_with=e.clauses) as sat:
                for b in BLOCKS:
                    for y in (*BLOCKS, 'T'):
                        if y == b:
                            continue
                        for p in range(7 - BLOCKS[b]):
                            action = (b, y, p)
                            try:
                                target = move(state, action)
                                legal = True
                            except ValueError:
                                legal = False
                            result = sat.solve(assumptions=[e.ids[f'mv({b},{y},{p},0)']])
                            self.assertEqual(result, legal, (state, action))
                            if result:
                                mapping = {n: (name.split('(')[0], name[:-1].split('(')[1].split(','))
                                           for name, n in e.ids.items()}
                                plan, trace = decode(mapping, sat.get_model())
                                self.assertEqual(plan, [action])
                                self.assertEqual(trace[-1], target)

    def test_partial_order_linearizations(self):
        # S1 Sf1: colocar a e b em d em qualquer ordem, depois c.
        prefix = replay(S0, Q)[-1]
        for actions in ([('a', 'd', 4), ('b', 'd', 5), ('c', 'a', 4)],
                        [('b', 'd', 5), ('a', 'd', 4), ('c', 'a', 4)]):
            self.assertEqual(replay(prefix, actions)[-1], SITUACAO1['Sf1'])
        # Em S2, b sustenta a; b não pode sair antes de a.
        prefix = replay(SITUACAO2['S0'], R[:3])[-1]
        with self.assertRaises(ValueError):
            move(prefix, ('b', 'c', 5))

    def test_saved_models_and_bfs(self):
        # Todas as 16 instâncias são verificadas sem exigir saídas auxiliares no Git.
        root = Path(__file__).parent
        for scenario, fig in FIGURAS.items():
            bfs = distances(fig['S0'])
            for goal, state in fig.items():
                if goal == 'S0':
                    continue
                minimum = bfs[key(state)]
                with tempfile.TemporaryDirectory() as directory:
                    folder = Path(directory)
                    with contextlib.redirect_stdout(io.StringIO()):
                        history = solve(fig['S0'], state, folder, 'modelo.txt', minimum)
                    self.assertEqual([x['horizonte'] for x in history], list(range(minimum + 1)))
                    self.assertEqual([x['status'] for x in history], ['UNSAT'] * minimum + ['SAT'])
                    text = interpret(folder / 'modelo.txt', folder / 'trab01_blocos2SAT.map',
                                     folder / 'trab01_blocos2SAT.cnf')
                    self.assertIn(f'({minimum} ações)', text)
                    mapping = read_map(folder / 'trab01_blocos2SAT.map')
                    _, trace = decode(mapping, read_result(folder / 'modelo.txt'))
                    self.assertEqual(trace[0], fig['S0'])
                    self.assertEqual(trace[-1], state)
                    if goal == METAS[scenario]:
                        saved_folder = root / 'resultados' / f'cenario{scenario}'
                        stem = 'trab01_blocos2SAT'
                        saved = interpret(saved_folder / f'resultado{scenario}.txt',
                                          saved_folder / f'{stem}.map', saved_folder / f'{stem}.cnf')
                        self.assertIn(f'({minimum} ações)', saved)
                        _, saved_trace = decode(read_map(saved_folder / f'{stem}.map'),
                                                read_result(saved_folder / f'resultado{scenario}.txt'))
                        self.assertEqual(saved_trace[0], fig['S0'])
                        self.assertEqual(saved_trace[-1], state)
                        for ext in ('cnf', 'map'):
                            self.assertEqual((folder / f'trab01_blocos2SAT.{ext}').read_bytes(),
                                             (saved_folder / f'{stem}.{ext}').read_bytes())

    def test_corrupt_model_rejected(self):
        e = encode(S0, S0, 0)
        with tempfile.TemporaryDirectory() as directory:
            e.write(directory)
            with Minisat22(bootstrap_with=e.clauses) as solver:
                self.assertTrue(solver.solve())
                model = solver.get_model()
            path = Path(directory)
            (path / 'result.txt').write_text('SAT\n1 0\n')
            with self.assertRaises(ValueError):
                interpret(path / 'result.txt', path / 'trab01_blocos2SAT.map', path / 'trab01_blocos2SAT.cnf')
            mapping = read_map(path / 'trab01_blocos2SAT.map')
            check_cnf(path / 'trab01_blocos2SAT.cnf', model, len(mapping))
            model[e.ids['at(a,3,0)'] - 1] *= -1
            with self.assertRaises(ValueError):
                check_cnf(path / 'trab01_blocos2SAT.cnf', model, len(mapping))


if __name__ == '__main__':
    unittest.main(verbosity=2)
