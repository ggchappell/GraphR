#!/usr/bin/env python

# genramsey.py
# Glenn G. Chappell
# Date: 25 Aug 2016
# Requires Python 2.6.* or 2.7.*.

"""Functions for finding generalized Ramsey numbers & related extremal
graphs.

CONVENTIONS

See isograph.py for our graph representation. A set is represented as a
sorted list or tuple of its elements.

*Predicates* in this file are functions taking a graph and a set of
vertices of that graph, and returning bool. Given a predicate f, and a
graph g, we say a set s of vertices of g is an *f-set* in g if f(g, s)
is True.

An *induced-hereditary* predicate is a predicate f such that, if h is an
induced subgraph of a graph g, and s is a set of vertices of h, then s
is an f-set in h iff s is an f-set in g.

Given predicates f1 & f2 and nonnegative integers b1 & b2, a
*counterexample* graph is a graph that contains no f1-set of order b1
and no f2-set of order b2. In other words, it is a counterexample to the
statement that every graph contains either an f1-set of order b1 or an
f2-set of order b2.

An *extremal* graph is a counterexample graph of maximum order.

Predicates:
is_independent(g, s)
    Return bool: True if s is an independent set in graph g.
is_clique(g, s)
    Return bool: True if s induces a complete subgraph of graph g.

Checking for f-Sets:
has_fset(f, b, g)
    Return bool: True if graph g contains an f-set of order b.
has_fset_with_last(f, b, g)
    Return bool: True if graph g contains an f-set of order b that
    contains vertex n-1 of g.

Finding Extremal Graphs:
extremals(f1, f2, b1, b2, printflag=None)
    f1, f2 are induced-hereditary predicates. Return (n, gs), where n is
    the least order for which no counterexample graphs exist (and so n-1
    is the order of all extremal graphs), and gs is a list of all
    extremal graphs (exactly one from each isomorphism class). If
    printflag is True, prints, one on each line, pairs of the form u v,
    where u is an integer from 0 to n, and v is the number of
    counterexample graphs of order u.

"""

import isograph   # for graphs, isomorphic, powerset, unique_iso
import itertools  # for combinations, count
import sys        # for argv, exit


# ----------------------------------------------------------------------
# Predicates
# ----------------------------------------------------------------------


def is_independent(g, s):
    """Predicate. Return True if s is an independent set in g.

    s is a list or tuple whose items are vertices of g. We determine
    whether s, considered as a set of vertices, is an independent set
    in g. We return True if so.

    This function is an induced-hereditary predicate.

    Arguments:
    g -- graph
    s -- list or tuple of vertices of g; represents set of vertices

    See isograph.py for our graph representation.

    >>> g = [ [2,3,4], [2,3,4], [0,1], [0,1], [0,1] ]
    >>> s = [0,1]
    >>> is_independent(g, s)
    True
    >>> s = [2,3,4]
    >>> is_independent(g, s)
    True
    >>> s = [1,3]
    >>> is_independent(g, s)
    False

    """
    for v in s:
        for x in g[v]:
            if x in s:
                return False
    return True


def is_clique(g, s):
    """Predicate. Return True if s is a clique in g.

    s is a list or tuple whose items are vertices of g. We determine
    whether s, considered as a set of vertices, induces a complete
    subgraph of g. We return True if so.

    This function is an induced-hereditary predicate.

    Arguments:
    g -- graph
    s -- list or tuple of vertices of g; represents set of vertices

    See isograph.py for our graph representation.

    >>> g = [ [1], [0,2,3], [1,3], [1,2] ]
    >>> s = [0,1]
    >>> is_clique(g, s)
    True
    >>> s = [1,2,3]
    >>> is_clique(g, s)
    True
    >>> s = [0,2]
    >>> is_clique(g, s)
    False

    """
    for v in s:
        for x in s:
            if x != v and x not in g[v]:
                return False
    return True


# ----------------------------------------------------------------------
# Checking for f-Sets
# ----------------------------------------------------------------------


def has_fset(f, b, g):
    """Return True if g contains an f-set of order b.

    Arguments:
    f -- predicate
      Given a graph and a subset of its vertex set, returns bool.
    b -- nonnegative int
      We search for an order-b f-set.
    g -- graph


    See isograph.py for our graph representation.

    >>> g = [ [3], [3], [3], [0,1,2] ]
    >>> has_fset(is_independent, -1, g)
    False
    >>> has_fset(is_independent, 0, g)
    True
    >>> has_fset(is_independent, 1, g)
    True
    >>> has_fset(is_independent, 2, g)
    True
    >>> has_fset(is_independent, 3, g)
    True
    >>> has_fset(is_independent, 4, g)
    False
    >>> has_fset(is_clique, 1, g)
    True
    >>> has_fset(is_clique, 2, g)
    True
    >>> has_fset(is_clique, 3, g)
    False

    """
    if b < 0:
        return False

    n = len(g)
    if b > n:
        return False

    for s in itertools.combinations(xrange(n), b):
        if f(g, s):
            return True
    return False


def has_fset_with_last(f, b, g):
    """Return True if g contains f-set of order b containing vertex n-1.

    Arguments:
    f -- predicate
      Given a graph and a subset of its vertex set, returns bool.
    g -- graph
    b -- nonnegative int
      We search for an order-b f-set.

    See isograph.py for our graph representation.

    >>> g = [ [3], [3], [3], [0,1,2] ]
    >>> has_fset_with_last(is_independent, -1, g)
    False
    >>> has_fset_with_last(is_independent, 0, g)
    False
    >>> has_fset_with_last(is_independent, 1, g)
    True
    >>> has_fset_with_last(is_independent, 2, g)
    False
    >>> has_fset_with_last(is_independent, 3, g)
    False
    >>> has_fset_with_last(is_independent, 4, g)
    False
    >>> has_fset_with_last(is_clique, 1, g)
    True
    >>> has_fset_with_last(is_clique, 2, g)
    True
    >>> has_fset_with_last(is_clique, 3, g)
    False

    """
    if b < 1:
        return False

    n = len(g)
    if b > n:
        return False

    for ss in itertools.combinations(xrange(n-1), b-1):
        s = ss + (n-1,)
        if f(g, s):
            return True
    return False


# ----------------------------------------------------------------------
# Finding Extremal Graphs
# ----------------------------------------------------------------------


def _counterexamples_zero(f1, f2, b1, b2):
    """Yield all counterexample graphs of order zero.

    Arguments:
    f1 -- predicate
    f2 -- predicate
    b1 -- nonnegative int
    b2 -- nonnegative int

    See isograph.py for our graph representation.

    """
    gs = list(isograph.graphs(0))  # list of all graphs of order 0
    for g in gs:
        if not has_fset(f1, b1, g) and not has_fset(f2, b2, g):
            yield g


def _counterexamples_up(f1, f2, b1, b2, n, old):
    """Yield counterexample n-graphs, given list for n-1.

    Given induced-hereditary predicates f1, f2, and nonnegative integers
    b1, b2, yield one graph from each isomorphism class of n-vertex
    counterexample graphs, given an iterable (old) yielding all
    counterexample graphs of order n-1.

    Arguments:
    f1 -- induced-hereditary predicate
    f2 -- induced-hereditary predicate
    b1 -- nonnegative int
    b2 -- nonnegative int
    n -- positive int
      Order of graphs to yield.
    old -- iterable yielding graphs of order n-1
      Graphs yielded should be all counterexample graphs of order n-1.

    See isograph.py for our graph representation.

    >>> f1 = is_independent
    >>> f2 = is_clique
    >>> ce4_0_3_3 = [[[2], [3], [0], [1]], [[1,2], [0,3], [0], [1]],
    ... [[1,2], [0,3], [0,3], [1,2]]] # order-4 ctrexamples for R_0(3,3)
    >>> ce5_0_3_3 = list(_counterexamples_up(f1,f2,3,3,5,ce4_0_3_3))
    >>> len(ce5_0_3_3)
    1
    >>> c5 = [[1,4], [0,2], [1,3], [2,4], [0,3]]
    >>> isograph.isomorphic(ce5_0_3_3[0], c5)
    True
    >>> list(_counterexamples_up(f1,f2,3,3,6,ce5_0_3_3))
    []

    """
    # Helper function counterexamples_up_big_list: generates every
    # counterexample graph of order n whose subgraph induced by vertices
    # 0 .. n-2 is an item in old.
    def counterexamples_up_big_list(f1, f2, n, b1, b2, old):
        for oldg in old:
            for vset in isograph.powerset(xrange(n-1)):
                g = oldg + [list(vset)]
                for v in vset:
                    g[v] = g[v]+[n-1]
                    # NOT g[v] += ... or g[v].append(...),
                    #  to avoid changing items in oldg
                # Now g is candidate graph.
                # Yield it if no order-b1 f1-set & no order-b2 f2-set
                if (not has_fset_with_last(f1, b1, g) and
                    not has_fset_with_last(f2, b2, g)):
                    yield g

    return isograph.unique_iso(
        counterexamples_up_big_list(f1, f2, n, b1, b2, old))


def extremals(f1, f2, b1, b2, printflag=None):
    """Return 1 + order of extremal graphs, list of extremal graphs.

    Return (n, gs), where n is 1 + order of an extremal graph, or 0 if
    no counterexample graph exists, and gs is a list of all extremal
    graphs.

    If printflag is True, prints, one on each line, pairs of the form
    u v, where u is an integer from 0 to n, and v is the number of
    counterexample graphs of order u.

    Arguments:
    f1 -- induced-hereditary predicate
    f2 -- induced-hereditary predicate
    b1 -- nonnegative int
    b2 -- nonnegative int
    printflag -- optional bool: whether to print ongoing messages
        Default is False.

    See isograph.py for our graph representation.

    >>> f1 = is_independent
    >>> f2 = is_clique
    >>> extremals(f1, f2, 3, 3)
    (6, [[[2, 3], [3, 4], [0, 4], [0, 1], [1, 2]]])
    >>> extremals(f1, f2, 3, 3, True)
    Order & number of counterexample graphs:
    0 1
    1 1
    2 2
    3 2
    4 3
    5 1
    6 0
    (6, [[[2, 3], [3, 4], [0, 4], [0, 1], [1, 2]]])

    """
    if printflag:
        print "Order & number of counterexample graphs:"

    gs = list(_counterexamples_zero(f1, f2, b1, b2))
    howmany = len(gs)
    if printflag:
        print 0, howmany
    if howmany == 0:
        return (0, [])

    for n in itertools.count(1):
        oldgs = gs
        gs = list(_counterexamples_up(f1, f2, b1, b2, n, oldgs))
        howmany = len(gs)
        if printflag:
            print n, howmany
        if howmany == 0:
            return (n, oldgs)


# ----------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------


def main(argv=None):
    """Run doctests; verbose mode if argv[1] is "--Test"

    """
    if argv is None:
        argv = sys.argv

    import doctest
    verbose = (len(argv) >= 2 and argv[1] == "--Test")
    if verbose:
        print "Running doctests (verbose mode)"
    else:
        print "Running doctests"
    doctest.testmod(verbose=verbose)
    return 0


# Execute main() if running as program, not if imported as module
if __name__ == "__main__":
    sys.exit(main())

