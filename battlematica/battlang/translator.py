import os
from copy import deepcopy
from functools import partial

import networkx as nx

import battlematica.library as lib
from battlematica.state_querier import StateQuerier
from battlematica.battlang.mappings import selectors_map, filters_map, identifiers_map
from battlematica.battlang.preparsing import preparse
from battlematica.battlang.pynetree import Parser, Node
from battlematica.battlang.templates import *

this_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(this_dir, 'BATTLANG.bnf'), 'r') as bf:
    BNF_BATTLANG = bf.read()


def translate_battlang_file(filename):
    b = BattlangTranslator()
    return b.from_file(filename)


def translate_battlang_string(s, program_name):
    b = BattlangTranslator()
    return b.translate(s, program_name)


class BattlangTranslator:

    def __init__(self):
        self.parser = Parser(BNF_BATTLANG)
        self._reset_working_vars()
        self.last_full_prog = None

    def from_file(self, filename):
        with open(filename, 'r') as tf:
            prog = tf.read()
        return self.translate(prog, os.path.splitext(os.path.basename(filename))[0])

    def dump(self, filename):
        with open(filename, 'w') as tf:
            tf.write(self.last_full_prog)

    def translate(self, program, name):
        self._name = name
        preparsed_program = preparse(program)
        raw_ast = self.parser.parse(preparsed_program)
        self._build_tree(raw_ast)
        self._tree_rewrite()
        object_code = compile(self._full_prog, self._name, 'exec')
        eval(object_code)
        translated_fun = locals()[self._name]
        ai_fun = partial(translated_fun, sq=StateQuerier, lib=lib)
        self.last_full_prog = self._full_prog
        self._reset_working_vars()
        return ai_fun

    def _reset_working_vars(self):
        self._name = None
        self._full_prog = None
        self._tree = None
        self._root = None
        self._depth = None
        self._labels = None
        self._labels_0 = None
        self._an_n = 0

    @staticmethod
    def _d100(par):
        ps = par.split(',')
        try:
            ps = [f'{float(p)/100:.2}' for p in ps]
        except ValueError:
            return ''
        return ', '.join(ps)

    def _build_tree(self, ast_root: Node):

        # recursively build graph with node ids and labels
        node_labels = {}
        ast_tree = nx.DiGraph()

        def name(node):
            if node.children:
                node_labels[id(node)] = node.symbol  # terminal label is the construct
            else:
                node_labels[id(node)] = node.match  # terminal label is the content
            return id(node)

        def explore_node(cnode):
            for node in cnode.children:
                ast_tree.add_edge(name(cnode), name(node))
                explore_node(node)

        explore_node(ast_root)

        self._tree = ast_tree
        self._labels = node_labels
        self._labels_0 = node_labels

        # find root
        root = [n for n in self._tree.nodes if len(nx.ancestors(self._tree, n)) == 0]
        assert len(root) == 1
        self._root = root[0]

        # find max depth
        dd = ['dummy']
        self._depth = 1
        while dd:
            dd = list(nx.descendants_at_distance(self._tree, self._root, self._depth))
            self._depth += 1

    def _get_twig(self):

        # take a node from the current lowest depth
        dd = list(nx.descendants_at_distance(self._tree, self._root, self._depth))
        while not dd:
            self._depth -= 1
            dd = list(nx.descendants_at_distance(self._tree, self._root, self._depth))
        n = dd[0]

        # take its father
        p = list(self._tree.predecessors(n))
        assert len(p) <= 1

        if len(p) == 0:
            return None, None

        # list children of the father
        p = p[0]
        c = list(self._tree.successors(p))

        # comment the tree
        if self._labels_0[p] == 'statement':
            # on a full statement, we reset the comment because we are abandoning
            # an inner block
            self._tree.nodes[p]['comment'] = ''
        else:
            comm = ''
            for x in c:
                comm += ' '
                if 'comment' in self._tree.nodes[x].keys():
                    comm += (self._tree.nodes[x]['comment'])
                else:
                    comm += (str(self._labels_0[x]))
            self._tree.nodes[p]['comment'] = comm[1:]

        # detach the twig from the tree
        twig = deepcopy(nx.subgraph(self._tree, [p] + c))
        self._tree.remove_nodes_from(c)

        return twig, p

    @staticmethod
    def _expand_selector(cnodes):
        sel = cnodes[0]
        if sel not in selectors_map.keys():
            raise NotImplementedError(sel)
        n_args, fn_name, fn_args = selectors_map[sel]
        assert len(cnodes) == n_args

        for ca in range(1, n_args):
            fn_args = fn_args.format(**{f'cnodes_{ca}': cnodes[ca]})
        sub = f'lib.{fn_name}({fn_args})'
        return sub

    def _expand_filter(self, cnodes):
        fil = cnodes[0]
        if fil not in filters_map.keys():
            raise NotImplementedError(fil)
        n_args, fn_name, fn_args = filters_map[fil]
        assert len(cnodes) == n_args

        for ca in range(1, n_args):
            fn_args = fn_args.format(**{f'd100nodes_{ca}': self._d100(cnodes[ca]),
                                        f'cnodes_{ca}': cnodes[ca]})
        sub = f'lib.{fn_name}({fn_args})'
        return sub

    def _expand_anyfilter(self, cnodes):
        fil = cnodes[0]
        if fil not in filters_map.keys():
            raise NotImplementedError(fil)
        n_args, fn_name, fn_args = filters_map[fil]
        anyfil = f'lib.{lib.AnyFilter.__name__}(lib.{fn_name})(xy_list_{self._an_n}())'
        return anyfil

    @staticmethod
    def _expand_identifier(cnodes):
        idnt = cnodes[0]
        if idnt not in identifiers_map.keys():
            raise NotImplementedError(idnt)
        n_args, fn_name, fn_args = identifiers_map[idnt]
        assert n_args == 1  # n_args is kept explicit for homogeneousness
        assert len(cnodes) == 1

        sub = f'lib.{fn_name}({fn_args})'
        return sub

    def _tree_rewrite(self):

        qual_lists = []
        cl_lists = []
        any_lists = []
        ql_n = 0
        cl_n = 0
        self._an_n = 0

        inner_prog = ''

        while True:
            twig, contact_node = self._get_twig()
            if twig is None:
                break

            fnode = self._labels[contact_node]
            cnodes = [self._labels[x] for x in list(twig.successors(contact_node))]

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

            # case command
            elif fnode == 'xy_specified_filter':
                sub = cnodes[0]

            # case list negator
            elif fnode == 'list_negator':
                sub = cnodes[0]

            # case xy_negator
            elif fnode == 'xy_sign':
                sub = cnodes[0]

            # case anyfilter
            elif fnode == 'anyfilter':
                comm = self._tree.nodes[contact_node]['comment']
                any_lists.append(MULTI_XY_LIST.format(comment=comm, n=self._an_n,
                                                      series=cnodes[2] + ',\n        '))
                sub = self._expand_anyfilter(cnodes)
                self._an_n += 1

            # case filter
            elif fnode == 'filter':
                sub = self._expand_filter(cnodes)

            # case selector
            elif fnode == 'selector':
                sub = self._expand_selector(cnodes)

            # case identifier
            elif fnode == 'identifier':
                sub = self._expand_identifier(cnodes)

            # case list_descriptor
            elif fnode == 'list_descriptor':
                sub = ',\n        '.join(sorted(cnodes, reverse=True))

            # case qualified list
            elif fnode == 'qualifying_list':
                comm = self._tree.nodes[contact_node]['comment']
                if len(cnodes) == 3:
                    if cnodes[0] == 'AWAY_FROM':
                        qual_lists.append(XY_QUAL_LIST_AWAY.format(series=cnodes[2] + ',\n        ' + cnodes[1],
                                                                   n=ql_n,
                                                                   comment=comm))
                    elif cnodes[0] in ('TO', 'AT'):
                        qual_lists.append(XY_QUAL_LIST.format(series=cnodes[2] + ',\n        ' + cnodes[1],
                                                              n=ql_n,
                                                              comment=comm))
                    else:
                        raise NotImplementedError(cnodes[0])
                else:
                    assert len(cnodes) == 2
                    qual_lists.append(XY_QUAL_LIST.format(series=cnodes[1] + ',\n        ' + cnodes[0],
                                                          n=ql_n,
                                                          comment=comm))
                sub = f'*target_{ql_n}()'
                ql_n += 1

            # case action
            elif fnode == 'action':
                comm = self._tree.nodes[contact_node]['comment']
                sub = VALIDATED_COMMAND.format(comment=comm, command_name=cnodes[0], command_args=cnodes[1])
                # sub = f'\n# {comm}\nct = validate_command(("{cnodes[0]}", {cnodes[1]}))\nif ct is not None:\n
                # return ct'

            # case condition
            elif fnode == 'condition':
                if len(cnodes) == 2:
                    assert cnodes[0] == 'NOT'
                    cl_lists.append(LIST_EXISTENCE.format(series=cnodes[1], n=cl_n, flip=True,
                                                          comment=self._tree.nodes[contact_node]['comment']))
                elif len(cnodes) == 1:
                    cl_lists.append(LIST_EXISTENCE.format(series=cnodes[0], n=cl_n, flip=False,
                                                          comment=self._tree.nodes[contact_node]['comment']))
                else:
                    raise NotImplementedError

                sub = f'exists_{cl_n}()'
                cl_n += 1

            # case conditional
            elif fnode == 'conditional':
                condition = cnodes[0]
                comm = self._tree.nodes[contact_node]['comment']
                lines = []
                for statement in cnodes[1:]:
                    for subline in statement.splitlines():
                        lines.append('    ' + subline)

                lines = '\n'.join(lines)
                sub = CONDITIONAL.format(comment=comm, condition=condition, body=lines)

            # case statement
            elif fnode == 'statement':
                sub = cnodes[0]

            # case root, break
            elif fnode is None:
                inner_prog = MAIN_PROC.format(body='\n'.join(cnodes))
                break

            # node class unknown
            else:
                raise NotImplementedError(fnode)

            self._labels[contact_node] = sub
            # print(sub)

        full_prog = '\n'.join([*qual_lists, *cl_lists, *any_lists, inner_prog])

        # adding base indentation level
        full_prog = '\n'.join(['    ' + line for line in full_prog.splitlines()])
        # header
        full_prog = HEAD.format(name=self._name, prog=full_prog)

        self._full_prog = full_prog


if __name__ == '__main__':
    with open('../../sample_battlang_ai/ultimate.blng', 'r') as tf:
        prog_string = tf.read()

    t = BattlangTranslator()
    fn = t.translate(prog_string, 'ultimate')
    print(fn)
