from apyds import Term, Rule


def rule_get_idea(data):
    if not data.startswith("--"):
        return f"----\n{data.splitlines()[0]}\n"
    return None


def rule_is_fact(data):
    return data.startswith("--")


def rule_get_fact(data):
    return data.splitlines()[-1]


def rule_is_equality(data):
    return data.startswith("----\n(binary == ")


def rule_get_equality(data):
    return term_get_equality(rule_get_fact(data))


def term_get_equality(data):
    term = Term(data)
    lhs = str(term.term[2])
    rhs = str(term.term[3])
    return lhs, rhs


def equality_build_rule(lhs: str, rhs: str) -> str:
    return term_build_rule(equality_build_term(lhs, rhs))


def equality_build_term(lhs: str, rhs: str) -> str:
    return f"(binary == {lhs} {rhs})"


def term_build_rule(data: str) -> str:
    return f"----\n{data}\n"


def conclusion_build_rule(conclusion: Term) -> Rule:
    """Build a Rule from a conclusion Term (no premises)"""
    return Rule(f"----\n{conclusion}\n")


# New Term/Rule-based helper functions
def term_is_equality(term: Term) -> bool:
    """Check if a Term represents an equality (binary ==)"""
    return len(term.term) == 4 and str(term.term[0]) == "binary" and str(term.term[1]) == "=="


def term_get_equality_pair(term: Term) -> tuple[Term, Term]:
    """Get the LHS and RHS terms from an equality Term.
    
    Args:
        term: A Term representing an equality (binary == lhs rhs)
        
    Returns:
        A tuple of (lhs, rhs) Term objects
        
    Raises:
        IndexError: If term is not an equality with the expected structure
    """
    if not term_is_equality(term):
        raise ValueError(f"Term is not an equality: {term}")
    return term.term[2], term.term[3]


def term_build_equality(lhs: Term, rhs: Term) -> Term:
    """Build an equality Term from two terms"""
    return Term(f"(binary == {lhs} {rhs})")
