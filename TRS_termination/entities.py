from typing import List, Union


class Variable:
    """Represents variable in TRS."""
    def __init__(self, name: str):
        self.name = name

class Constructor:
    """Represents constructor in TRS."""
    def __init__(self, name: str, arguments: List[Union[Variable, 'Constructor']]):
        self.name = name
        self.arguments = arguments

    def has_variable(self, variable: Variable) -> bool:
        """Verifies if constructor contains given variable."""
        elems = [*self.arguments]
        while len(elems) != 0:
            elem = elems.pop()
            if elem.name == variable.name:
                return True
            if isinstance(elem, Constructor):
                elems.extend(elem.arguments)
        return False

class RewritingRule:
    """Represents rewriting rule in TRS."""
    def __init__(self, left: Union[Constructor, Variable],
                      right: Union[Constructor, Variable]):
        self.left = left
        self.right = right

class ConstructorNode:
    """Represents constructor in hierarchical tree."""
    def __init__(self, name: str):
        self.name = name
        self.parents = set()
    
    @property
    def parents_names(self) -> set:
        return set(parent.name for parent in self.parents)

    @property
    def ancestors(self) -> set:
        elems = set()

        def collect(node):
            for parent in node.parents:
                elems.add(parent)
                collect(parent)
        
        collect(self)
        return elems
    
    @property
    def ancestors_names(self) -> set:
        return set(ancestor.name for ancestor in self.ancestors)

    def add_parent(self, new_parent: 'ConstructorNode') -> None:
        self.parents.add(new_parent)

    def remove_parent(self, parent: 'ConstructorNode') -> None:
        self.parents.remove(parent)

    def is_greater(self, node: 'ConstructorNode') -> bool:
        return any(self.name == anc.name for anc in node.ancestors)
