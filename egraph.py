from __future__ import annotations
import egglog
from apyds import Rule, Term, List
from apyds_bnf import parse, unparse


class EGraphTerm(egglog.Expr):
    def __init__(self, name: egglog.StringLike) -> None: ...

    @classmethod
    def begin(cls) -> EGraphTerm: ...

    @classmethod
    def pair(cls, lhs: EGraphTerm, rhs: EGraphTerm) -> EGraphTerm: ...


def _ds_to_egraph(data):
    term = data.term
    if isinstance(term, List):
        result = EGraphTerm.begin()
        for i in range(len(term)):
            child = _ds_to_egraph(term[i])
            result = EGraphTerm.pair(result, child)
        return result
    else:
        return EGraphTerm(str(term))


class Search:
    def __init__(self):
        self.egraph = egglog.EGraph()
        self.terms = set()

    def _is_equality(self, data):
        return data.startswith("----\n(binary == ")

    def _extract_lhs_rhs(self, data):
        term = Rule(data).conclusion
        lhs = str(term.term[2])
        rhs = str(term.term[3])
        return lhs, rhs

    def _ast(self, data):
        result = _ds_to_egraph(Term(data))
        self.egraph.register(result)
        return result

    def _set_equality(self, lhs, rhs):
        self.egraph.register(egglog.union(self._ast(lhs)).with_(self._ast(rhs)))

    def _get_equality(self, lhs, rhs):
        return self.egraph.check_bool(self._ast(lhs) == self._ast(rhs))

    def _search_equality(self, data):
        for result in self.terms:
            if self._get_equality(data, result):
                yield result

    def _build_equality(self, lhs, rhs):
        return f"----\n(binary == {lhs} {rhs})"

    def add(self, data):
        data = parse(data)
        if not self._is_equality(data):
            return
        lhs, rhs = self._extract_lhs_rhs(data)
        self.terms.add(lhs)
        self.terms.add(rhs)
        self._set_equality(lhs, rhs)

    def execute(self, data):
        data = parse(data)
        if not self._is_equality(data):
            return
        lhs, rhs = self._extract_lhs_rhs(data)
        if self._get_equality(lhs, rhs):
            result = self._build_equality(lhs, rhs)
            yield unparse(result)
            return
        if lhs.startswith("`"):
            for result in self._search_equality(rhs):
                result = self._build_equality(result, rhs)
                yield unparse(result)
        if rhs.startswith("`"):
            for result in self._search_equality(lhs):
                result = self._build_equality(lhs, result)
                yield unparse(result)
