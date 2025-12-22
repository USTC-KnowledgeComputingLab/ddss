from __future__ import annotations
import typing
from apyds import Term, Rule
from apyds_egg import EGraph as ApydsEGraph, EClassId
from .utility import (
    term_is_equality,
    term_get_equality_pair,
    term_build_equality,
)


class EGraph:
    def __init__(self):
        self.core = ApydsEGraph()
        self.mapping: dict[str, EClassId] = {}

    def _get_or_add(self, term: Term) -> EClassId:
        term_str = str(term)
        if term_str not in self.mapping:
            self.mapping[term_str] = self.core.add(term)
        return self.mapping[term_str]

    def set_equality(self, lhs: Term, rhs: Term) -> None:
        lhs_id = self._get_or_add(lhs)
        rhs_id = self._get_or_add(rhs)
        self.core.merge(lhs_id, rhs_id)

    def get_equality(self, lhs: Term, rhs: Term) -> bool:
        lhs_id = self._get_or_add(lhs)
        rhs_id = self._get_or_add(rhs)
        return self.core.find(lhs_id) == self.core.find(rhs_id)


class Search:
    def __init__(self) -> None:
        self.egraph = EGraph()
        self.terms: set[Term] = set()
        self.facts: set[Term] = set()
        self.pairs: set[Term] = set()

    def rebuild(self) -> None:
        self.egraph.core.rebuild()
        for lhs in self.terms:
            for rhs in self.terms:
                if self.egraph.get_equality(lhs, rhs):
                    equality = term_build_equality(lhs, rhs)
                    self.pairs.add(equality)

    def add(self, rule: Rule) -> None:
        self._add_expr(rule)
        self._add_fact(rule)

    def _add_expr(self, rule: Rule) -> None:
        if len(rule) != 0:
            return
        conclusion = rule.conclusion
        if not term_is_equality(conclusion):
            return
        lhs, rhs = term_get_equality_pair(conclusion)
        self.terms.add(lhs)
        self.terms.add(rhs)
        self.egraph.set_equality(lhs, rhs)

    def _add_fact(self, rule: Rule) -> None:
        if len(rule) != 0:
            return
        conclusion = rule.conclusion
        self.terms.add(conclusion)
        self.facts.add(conclusion)

    def execute(self, rule: Rule) -> typing.Iterator[Rule]:
        yield from self._execute_expr(rule)
        yield from self._execute_fact(rule)

    def _execute_expr(self, rule: Rule) -> typing.Iterator[Rule]:
        if len(rule) != 0:
            return
        conclusion = rule.conclusion
        if not term_is_equality(conclusion):
            return
        lhs, rhs = term_get_equality_pair(conclusion)
        if self.egraph.get_equality(lhs, rhs):
            yield rule
        for target in self.pairs:
            if unification := target @ conclusion:
                result = target.ground(unification, scope="1")
                yield Rule(f"----\n{result}\n")

    def _execute_fact(self, rule: Rule) -> typing.Iterator[Rule]:
        if len(rule) != 0:
            return
        conclusion = rule.conclusion
        for fact in self.facts:
            if self.egraph.get_equality(conclusion, fact):
                yield rule
                return
        for fact in self.facts:
            query = term_build_equality(conclusion, fact)
            for target in self.pairs:
                if unification := target @ query:
                    result = target.ground(unification, scope="1")
                    # Extract the RHS of the equality (result.term[2] is the second argument of ==)
                    yield Rule(f"----\n{result.term[2]}\n")
