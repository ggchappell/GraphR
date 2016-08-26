#!/usr/bin/env python3

# dividedramsey.py
# Glenn G. Chappell
# Date: 26 Aug 2016
# Requires Python 3.

"""Compute k-divided Ramsey numbers & related extremal graphs.

Command-line usage: dividedramsey.py [OPTIONS] k a b

Compute and print the generalized Ramsey number R*_k(a, b), along with
extremal graphs, using "DOT language". If not in quiet mode (see below),
also print the number of counterexample graphs of each order, up to
isomorphism, as they are computed. By a "counterexample graph" we mean a
graph G for which G has no a-vertex k-divided set, and the complement of
G has no b-vertex k-divided set.

OPTIONS:
-q, --quiet  Quiet mode; do not print info on counterexample graphs.

The following options perform special operations; if they are given,
then arguments k, a, b are ignored and may be omitted.

-h, --help   Print this usage message.
--test       Run module tests (uses Python doctests), non-verbose mode.
--Test       Run module tests, verbose mode.

To call from a Python 3 program, first do

    import dividedramsey

To obtain a Ramsey number and related extremal graphs, do

    value, extremal_list = dividedramsey.find_extremals(k, a, b)

with k, a, b set appropriately. Alternatively do

    dividedramsey.print_extremals(k, a, b)

to print information to the standard output.

This software was written as a companion to the paper "On subgraphs
without large components" by Glenn G. Chappell and John Gimbel. See that
paper for mathematical background and related results.

"""

import isograph   # for dot_str, isomorphic
import genramsey  # for extremals
import sys        # for argv, exit, stderr
import getopt     # for error, getopt


# ----------------------------------------------------------------------
# Checking whether a set is k-divided
# ----------------------------------------------------------------------


def make_k_divided_func(k):
    """Return func f(g,s) -> True if s is k-divided in g.

    Given positive integer k, returns a function f taking a graph g
    and a subset of the vertex set of g, and returning bool. The
    returned function returns True if s is k-divided in g.

    The returned function is an induced-hereditary predicate, as the
    term is used in genramsey.py.

    Arguments:
    k -- positive int; the "k" in k-divided

    See isograph.py for our graph representation.

    >>> f1 = make_k_divided_func(1)
    >>> f2 = make_k_divided_func(2)
    >>> f3 = make_k_divided_func(3)
    >>> f4 = make_k_divided_func(4)
    >>> f5 = make_k_divided_func(5)
    >>> g = [ [1], [0,2], [1,3], [2,4], [3] ]
    >>> s = [0,1,2,3,4]
    >>> f1(g, s)
    False
    >>> f2(g, s)
    False
    >>> f3(g, s)
    False
    >>> f4(g, s)
    False
    >>> f5(g, s)
    True
    >>> s = [0,1,3,4]
    >>> f1(g, s)
    False
    >>> f2(g, s)
    True
    >>> f3(g, s)
    True
    >>> s = [0,2,4]
    >>> f1(g, s)
    True
    >>> f2(g, s)
    True
    >>> f3(g, s)
    True

    """
    def is_k_divided(g, s):
        # k >= 1
        pushed = [False] * len(g)
        for v in s:
            if pushed[v]: continue
            compsize = 1
            stack = [v]
            pushed[v] = True
            while stack:
                x = stack.pop()
                for y in s:
                    if pushed[y] or y not in g[x]: continue
                    if compsize >= k:
                        return False
                    compsize += 1
                    stack.append(y)
                    pushed[y] = True
        return True

    assert k >= 1
    return is_k_divided


def make_k_divided_compl_func(k):
    """Return func f(g,s) -> True if s is k-divided in complement of g.

    Given nonnegative integer k, returns a function f taking a graph g
    and a subset of the vertex set of g, and returning bool. The
    returned function returns True if s is k-divided in the complement
    of g.

    The returned function is an induced-hereditary predicate, as the
    term is used in genramsey.py.

    Arguments:
    k -- nonnegative int; the "k" in k-divided

    See isograph.py for our graph representation.

    >>> f1 = make_k_divided_compl_func(1)
    >>> f2 = make_k_divided_compl_func(2)
    >>> f3 = make_k_divided_compl_func(3)
    >>> f4 = make_k_divided_compl_func(4)
    >>> f5 = make_k_divided_compl_func(5)
    >>> g = [ [2,3,4], [3,4], [0,4], [0,1], [0,1,2] ]
    >>> s = [0,1,2,3,4]
    >>> f1(g, s)
    False
    >>> f2(g, s)
    False
    >>> f3(g, s)
    False
    >>> f4(g, s)
    False
    >>> f5(g, s)
    True
    >>> s = [0,1,3,4]
    >>> f1(g, s)
    False
    >>> f2(g, s)
    True
    >>> f3(g, s)
    True
    >>> s = [0,2,4]
    >>> f1(g, s)
    True
    >>> f2(g, s)
    True
    >>> f3(g, s)
    True

    """
    def is_k_divided_compl(g, s):
        # k >= 1
        pushed = [False] * len(g)
        for v in s:
            if pushed[v]: continue
            compsize = 1
            stack = [v]
            pushed[v] = True
            while stack:
                x = stack.pop()
                for y in s:
                    if pushed[y] or y in g[x]: continue
                        # Note: no ck for y == x, as pushed[x] is True
                    if compsize >= k:
                        return False
                    compsize += 1
                    stack.append(y)
                    pushed[y] = True
        return True

    assert k >= 1
    return is_k_divided_compl


# ----------------------------------------------------------------------
# Finding k-Divided Ramsey Numbers & Extremal Graphs
# ----------------------------------------------------------------------


def find_extremals(k, a, b, printflag=None):
    """Return R*_k(a,b), list of extremal graphs.

    If printflag is True, prints, one on each line, pairs of the form
    u v, where u is an integer from 0 to R*_k(a, b), and v is the number
    of counterexample graphs of order u.

    Arguments:
    k -- positive int; the "k" in R*_k(a,b)
    a -- nonnegative int; the "a" in R*_k(a,b)
    b -- nonnegative int; the "b" in R*_k(a,b)
    printflag -- optional bool: whether to print ongoing messages
        Default is False.

    See isograph.py for our graph representation.

    >>> n, gs = find_extremals(1, 3, 3)
    >>> n
    6
    >>> len(gs)
    1
    >>> c5 = [[1,4],[0,2],[1,3],[2,4],[3,0]]
    >>> isograph.isomorphic(c5, gs[0])
    True
    >>> n, gs = find_extremals(1, 3, 3, printflag=True)
    Order & number of counterexample graphs:
    0 1
    1 1
    2 2
    3 2
    4 3
    5 1
    6 0

    """
    assert k >= 1
    assert a >= 0
    assert b >= 0

    f1 = make_k_divided_func(k)
    f2 = make_k_divided_compl_func(k)
    return genramsey.extremals(f1, f2, a, b, printflag)
    

def print_extremals(k, a, b, printflag=None):
    """Print R*_k(a,b) + extremal graphs in DOT language.

    If printflag is True, prints, one on each line, pairs of the form
    u v, where u is an integer from 0 to R*_k(a, b), and v is the number
    of counterexample graphs of order u.

    Arguments:
    k -- positive int; the "k" in R*_k(a,b)
    a -- nonnegative int; the "a" in R*_k(a,b)
    b -- nonnegative int; the "b" in R*_k(a,b)
    printflag -- optional bool: whether to print ongoing messages
        Default is False.

    See isograph.py for our graph representation.

    >>> print_extremals(1, 2, 2)
    Finding R*_1(2,2)
    <BLANKLINE>
    1 extremal graph(s):
    <BLANKLINE>
    graph rs1_2_2e1 {
        1;
    }
    <BLANKLINE>
    R*_1(2,2) = 2
    1 extremal graph(s)
    >>> print_extremals(1, 2, 2, printflag=True)
    Finding R*_1(2,2)
    <BLANKLINE>
    Order & number of counterexample graphs:
    0 1
    1 1
    2 0
    <BLANKLINE>
    1 extremal graph(s):
    <BLANKLINE>
    graph rs1_2_2e1 {
        1;
    }
    <BLANKLINE>
    R*_1(2,2) = 2
    1 extremal graph(s)

    """
    assert k >= 1
    assert a >= 0
    assert b >= 0

    print("Finding R*_"+str(k)+"("+str(a)+","+str(b)+")")
    print()

    n, gs = find_extremals(k, a, b, printflag)

    if printflag:
        print()
    print(len(gs), "extremal graph(s):")
    print()
    graphbasename = "rs"+str(k)+"_"+str(a)+"_"+str(b)+"e"
    gcount = 0
    for g in gs:
        gcount += 1
        graphname = graphbasename + str(gcount)
        print(isograph.dot_str(g, graphname))
        print()
    print("R*_"+str(k)+"("+str(a)+","+str(b)+") = "+str(n))
    print(len(gs), "extremal graph(s)")


# ----------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------


class UsageError(Exception):

    """Exception class for command-line usage errors.

    >>> isinstance(UsageError(""), Exception)
    True
    >>> UsageError("abc").msg
    'abc'

    """

    def __init__(self, msg):
        """Create UsageError object with the given message."""
        self.msg = msg


def main(argv=None):
    """Print R*_k(a,b) & extremal graphs, based on command-line options.

    Argument argv is an optional list or tuple of strings, in the format
    of sys.argv (which is its default value).

    If command-line arguments k, a, b are passed, find R*_k(a,b) and all
    extremal graphs (up to isomorphism) and print these, along with
    explanatory output. Graphs are printed in DOT language.

    Return zero on no error, nonzero on error.

    The code in this function does command-line option processing and
    error checking. Function print_extremals is called to do the actual
    computation.

    """
    if argv is None:
        argv = sys.argv

    printcounterexamples = True
    try:
        try:
            optlist, args = getopt.getopt(argv[1:], "hq",
                ["help", "quiet", "test", "Test"])
        except getopt.error as msg:
            raise UsageError(msg)
        for o, a in optlist:
            if o in ["-h", "--help"]:
                print(__doc__, end="")  # Usage message
                return 0
            elif o in ["-q", "--quiet"]:
                printcounterexamples = False
            elif o == "--test" or o == "--Test":
                import doctest  # for testmod
                verbose = (o == "--Test")
                if verbose:
                    print("Running doctests (verbose mode)")
                else:
                    print("Running doctests")
                doctest.testmod(verbose=verbose)
                return 0
            else:
                assert False, "unhandled option"
        if len(args) != 3:
            raise UsageError("Must have exactly 3 arguments")
        try:
            k = int(args[0])
            a = int(args[1])
            b = int(args[2])
        except:
            raise UsageError("Arguments must be integers")
    except UsageError as err:
        print(argv[0]+":", err.msg, file=sys.stderr)
        print("For help use --help", file=sys.stderr)
        return 2

    print_extremals(k, a, b, printflag=printcounterexamples)
    return 0


# Execute main() if running as program, not if imported as module
if __name__ == "__main__":
    sys.exit(main())

