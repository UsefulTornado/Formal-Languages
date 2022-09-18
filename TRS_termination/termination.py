from copy import deepcopy
from typing import List, Tuple, Dict, Optional, Union

from trs_parser import Parser
from entities import Variable, Constructor, ConstructorNode, RewritingRule


class TRSTermination:
    """Performs checking for termination of TRS with lexicographic order method."""
    def __init__(self, constructors: List[str], lexicographic: bool):
        self.nodes = {name: ConstructorNode(name) for name in constructors}
        self.lexicographic = lexicographic

    @staticmethod
    def _is_equal(t1: Union[Constructor, Variable],
                  t2: Union[Constructor, Variable]) -> bool:
        if t1.name == t2.name:
            if isinstance(t1, Constructor) and isinstance(t2, Constructor):
                return (len(t1.arguments) == len(t2.arguments) and
                        all((TRSTermination._is_equal(arg1, arg2)
                            for (arg1, arg2) in zip(t1.arguments, t2.arguments))))

            if isinstance(t1, Variable) and isinstance(t2, Variable):
                return True
        return False
    
    def _check_termination(self, rules: List[RewritingRule],
                                 nodes: Dict[str, ConstructorNode]) -> bool:

        def first_condition(left: Constructor, right: Constructor) -> bool:
            return any((self._is_equal(arg, right) for arg in left.arguments))

        def second_condition(left: Constructor, right: Constructor) -> bool:
            return any((is_greater(arg, right) for arg in left.arguments))

        def third_condition(left: Constructor, right: Constructor) -> bool:
            left_node = nodes[left.name]
            right_node = nodes[right.name]

            if left_node.is_greater(right_node):
                return all((is_greater(left, arg) for arg in right.arguments))

            if right_node.is_greater(left_node) or left_node.name == right_node.name:
                return False

            nodes_copy = deepcopy(nodes)
            left_node_copy = nodes_copy[left.name]
            right_node_copy = nodes_copy[right.name]
            right_node_copy.add_parent(left_node_copy)

            terminated = self._check_termination(rules, nodes_copy)
            if terminated:
                right_node.add_parent(left_node)

            return terminated

        def fourth_condition(left: Constructor, right: Constructor) -> bool:
            if left.name == right.name:
                for arg in right.arguments:
                    if not is_greater(left, arg):
                        return False

                if self.lexicographic:
                    return is_lexicographic_greater(
                        left.arguments, right.arguments
                    )

                return is_lexicographic_greater(
                    left.arguments[::-1], right.arguments[::-1]
                )

            return False

        def is_lexicographic_greater(left: list, right: list) -> bool:
            for (left_arg, right_arg) in zip(left, right):
                if not self._is_equal(left_arg, right_arg):
                    return is_greater(left_arg, right_arg)
            return False

        def is_greater(left: Union[Constructor, Variable],
                       right: Union[Constructor, Variable]) -> bool:
            if isinstance(left, Variable):
                return False
            if isinstance(right, Variable):
                return left.has_variable(right)
            
            return (first_condition(left, right) or
                    second_condition(left, right) or
                    third_condition(left, right) or
                    fourth_condition(left, right))

        return all(is_greater(rule.left, rule.right) for rule in rules)

    def check(self, rules: List[RewritingRule]) -> bool:
        """Checks termination of the TRS with specified rules."""
        return self._check_termination(rules, self.nodes)
    
    @property
    def constructors_order(self) -> str:
        """Returns string with the precedence of the constructors."""
        dct = {name: 0 for name in self.nodes.keys()}
        for node in self.nodes.values():
            for anc_name in node.ancestors_names:
                dct[anc_name] += 1
        
        ordered_nodes = sorted(dct.items(), key=lambda x: -x[1])
        order_str = ordered_nodes[0][0]
        for (name, _) in ordered_nodes[1:]:
            order_str += ' > ' + name

        return order_str

def check_termination(file_path: str, encoding='utf-8') -> Tuple[bool, Optional[str]]:
    """Retrieves TRS from the file and checks for it's termination."""
    with open(file_path, mode='r', encoding=encoding) as file:
        lines = file.readlines()
    
    parser = Parser()
    parser.parse_constructors(lines[1])
    parser.parse_variables(lines[2])
    rules = parser.parse_rules(lines[3:])
    
    termination = TRSTermination(
        parser.constructors, (lines[0].strip() == 'lexicographic')
    )
    res = termination.check(rules)
    
    if res:
        return res, termination.constructors_order
    
    return res, None
