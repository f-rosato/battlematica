import os
from copy import deepcopy

import networkx as nx
from functools import partial

import battlematica.library as lib
from battlematica.battlang.preparsing import blockify
from battlematica.battlang.pynetree import Parser, Node
from battlematica.battlang.templates import COND_LIST, XY_QUAL_LIST, XY_QUAL_LIST_AWAY, HEAD
from battlematica import StateQuerier

this_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(this_dir, 'BATTLANG.bnf'), 'r') as bf:
    BNF_BATTLANG = bf.read()


class BattlangTransl:

    def __init__(self):
        self.parser = Parser(BNF_BATTLANG)
        self.full_prog = ''
        self.name = ''

    def translate(self, program, name):
        self.name = name
        preparsed_program = blockify(program)
        raw_ast = self.parser.parse(preparsed_program)
        program_ast_graph, node_labels = self.ast_2_nx(raw_ast)
        ob = self.tree_rewrite(program_ast_graph, node_labels)
        eval(ob)
        fn = locals()[self.name]
        pfn = partial(fn, sq=StateQuerier, lib=lib)
        return pfn

    def dump(self, filename):
        with open(filename, 'w') as tf:
            tf.write(self.full_prog)

    @staticmethod
    def _d100(par):
        ps = par.split(',')
        ps = [f'{float(p)/100:.2}' for p in ps]
        return ', '.join(ps)

    @staticmethod
    def ast_2_nx(ast_root: Node):

        node_labels = {}

        def name(node):
            if node.children:
                node_labels[id(node)] = node.symbol
            else:
                node_labels[id(node)] = node.match
            return id(node)

        gg = nx.DiGraph()

        def explore_node(cnode):
            for node in cnode.children:
                gg.add_edge(name(cnode), name(node))
                explore_node(node)

        explore_node(ast_root)

        return gg, node_labels

    def tree_rewrite(self, ast_graph: nx.DiGraph, labels):

        # find root
        root = [n for n in ast_graph.nodes if len(nx.ancestors(ast_graph, n)) == 0]
        assert len(root) == 1
        root = root[0]

        # find max depth
        dd = ['dummy']
        depth = 1
        while dd:
            dd = list(nx.descendants_at_distance(ast_graph, root, depth))
            depth += 1

        # kopi
        labels0 = deepcopy(labels)

        # this function returns a random twig
        def get_twig():

            nonlocal depth
            nonlocal ast_graph

            # take a node from the current lower depth
            dd = list(nx.descendants_at_distance(ast_graph, root, depth))
            while not dd:
                depth -= 1
                dd = list(nx.descendants_at_distance(ast_graph, root, depth))
            n = dd[0]

            # take its father
            p = list(ast_graph.predecessors(n))
            assert len(p) <= 1

            if len(p) == 0:
                return None, None

            # list children of the father
            p = p[0]
            c = list(ast_graph.successors(p))

            # comment the tree
            if labels0[p] == 'statement':
                # on a full statement, we reset the comment because we are abandoning
                # an inner block
                ast_graph.nodes[p]['comment'] = ''
            else:
                comm = ''
                for x in c:
                    comm += ' '
                    if 'comment' in ast_graph.nodes[x].keys():
                        comm += (ast_graph.nodes[x]['comment'])
                    else:
                        comm += (str(labels0[x]))
                ast_graph.nodes[p]['comment'] = comm[1:]

            # detach the twig from the tree
            twig = deepcopy(nx.subgraph(ast_graph, [p] + c))
            ast_graph.remove_nodes_from(c)

            return twig, p

        qual_lists = []
        cl_lists = []
        ql_n = 0
        cl_n = 0

        inner_prog = ''

        while True:
            twig, contact_node = get_twig()
            if twig is None:
                break

            fnode = labels[contact_node]
            cnodes = [labels[x] for x in list(twig.successors(contact_node))]

            # bottom-up code generation

            # case xy
            if fnode == 'xy':
                if cnodes[0] == 'HERE':
                    assert len(cnodes) == 1
                    sub = 'self.x, self.y'
                elif cnodes[0].startswith('*target'):
                    sub = cnodes[0]
                else:
                    try:
                        _pn = float(cnodes[0])
                        assert len(cnodes) == 2
                    except (ValueError, TypeError, AssertionError):
                        raise NotImplementedError
                    sub = f'{float(cnodes[0])}, {float(cnodes[1])}'

            # case parn
            elif fnode in ('par2', 'par3', 'par4'):
                sub = ', '.join(cnodes)

            # case command
            elif fnode == 'command':
                sub = cnodes[0]

            # case list negator
            elif fnode == 'list_negator':
                sub = cnodes[0]

            # case xy_negator
            elif fnode == 'xy_negator':
                sub = cnodes[0]

            # case filter
            elif fnode == 'filter':
                if cnodes[0] == 'CARRYING':
                    assert len(cnodes) == 1
                    sub = f'lib.{lib.f_is_carrying.__name__}()'
                elif cnodes[0] == 'TARGETING':
                    assert len(cnodes) == 2  # kw and xy
                    sub = f'lib.{lib.f_has_target.__name__}({cnodes[1]})'
                elif cnodes[0] == 'ENEMY':
                    assert len(cnodes) == 1
                    sub = f'lib.{lib.f_not_of_teams.__name__}(self.hg, None)'
                elif cnodes[0] == 'ALLY':
                    assert len(cnodes) == 1
                    sub = f'lib.{lib.f_of_teams.__name__}(self.hg)'
                elif cnodes[0] == 'IN_RANGE':
                    assert len(cnodes) == 2
                    sub = f'lib.{lib.f_position_in_ring.__name__}(self.x, self.y, {cnodes[1]})'
                elif cnodes[0] == 'SHIELD_LEVEL':
                    assert len(cnodes) == 2
                    sub = f'lib.{lib.f_shield_between_pct.__name__}({self._d100(cnodes[1])})'
                elif cnodes[0] == 'ME':
                    assert len(cnodes) == 1
                    sub = f'lib.{lib.f_has_uid.__name__}(self.uid)'
                else:
                    raise NotImplementedError(cnodes[0])

            # case selector
            elif fnode == 'selector':
                assert len(cnodes) == 1
                if cnodes[0] == 'WEAKEST':
                    sub = f'lib.{lib.s_lowest_abs_health.__name__}()'
                elif cnodes[0] == 'NEAREST':
                    sub = f'lib.{lib.s_closest_to_xy.__name__}(self.x, self.y)'
                elif cnodes[0] == 'LEAST_SHIELD':
                    sub = f'lib.{lib.s_lowest_abs_shield.__name__}()'
                else:
                    raise NotImplementedError(cnodes[0])

            # case identifier
            elif fnode == 'identifier':
                assert len(cnodes) == 1
                if cnodes[0] == 'BOT':
                    sub = f'lib.{lib.i_bots.__name__}()'
                elif cnodes[0] == 'ARTIFACT':
                    sub = f'lib.{lib.i_artifacts.__name__}()'
                elif cnodes[0] == 'PORT':
                    sub = f'lib.{lib.i_drop_ports.__name__}()'
                else:
                    raise NotImplementedError(cnodes[0])

            # case list_descriptor
            elif fnode == 'list_descriptor':
                sub = ',\n        '.join(sorted(cnodes, reverse=True))

            # case qualified list
            elif fnode == 'qualifying_list':
                comm = ast_graph.nodes[contact_node]['comment']
                if len(cnodes) == 3:
                    assert cnodes[0] == 'AWAY_FROM'
                    qual_lists.append(XY_QUAL_LIST_AWAY.format(series=cnodes[2] + ',\n        ' + cnodes[1],
                                                               n=ql_n,
                                                               comment=comm))
                else:
                    assert len(cnodes) == 2
                    qual_lists.append(XY_QUAL_LIST.format(series=cnodes[1] + ',\n        ' + cnodes[0],
                                                          n=ql_n,
                                                          comment=comm))
                sub = f'*target_{ql_n}()'
                ql_n += 1

            # case action
            elif fnode == 'action':
                comm = ast_graph.nodes[contact_node]['comment']
                sub = f'\n# {comm}\nct = validate_command(("{cnodes[0]}", {cnodes[1]}))\nif ct is not None:\n    return ct'

            # case condition
            elif fnode == 'condition':
                if len(cnodes) == 2:
                    assert cnodes[0] == 'NOT'
                    cl_lists.append(COND_LIST.format(series=cnodes[1], n=cl_n, flip=True,
                                                     comment=ast_graph.nodes[contact_node]['comment']))
                elif len(cnodes) == 1:
                    cl_lists.append(COND_LIST.format(series=cnodes[0], n=cl_n, flip=False,
                                                     comment=ast_graph.nodes[contact_node]['comment']))
                else:
                    raise NotImplementedError

                sub = f'exists_{cl_n}()'
                cl_n += 1

            # case conditional
            elif fnode == 'conditional':
                condition = cnodes[0]
                comm = ast_graph.nodes[contact_node]['comment']
                lines = []
                for statement in cnodes[1:]:
                    for subline in statement.splitlines():
                        lines.append('    ' + subline)

                lines = '\n'.join(lines)
                sub = f'if {condition}:  # {comm}\n{lines}'

            # case statement
            elif fnode == 'statement':
                sub = cnodes[0]

            # case root, break
            elif fnode is None:
                inner_prog = '\n# MAIN PROCEDURE ----------\n\n' + '\n'.join(cnodes)
                break

            # node class unknown
            else:
                raise NotImplementedError(fnode)

            labels[contact_node] = sub
            # print(sub)

        full_prog = '\n'.join([*qual_lists, *cl_lists, inner_prog])

        # adding base indentation level
        full_prog = '\n'.join(['    ' + line for line in full_prog.splitlines()])
        # header
        full_prog = HEAD.format(name=self.name, prog=full_prog)

        self.full_prog = full_prog
        object_code = compile(full_prog, self.name, 'exec')
        return object_code


if __name__ == '__main__':
    with open('../../sample_battlang_ai/ultimate.blng', 'r') as tf:
        prog_string = tf.read()

    t = BattlangTransl()
    fn = t.translate(prog_string, 'ultimate')
    print(fn)
