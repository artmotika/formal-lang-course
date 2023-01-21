import antlr4
import pydot

from typing import Callable, Any
from project.grammar_query_language.GQLLexer import GQLLexer
from project.grammar_query_language.GQLListener import GQLListener
from project.grammar_query_language.GQLParser import GQLParser

# Returns GQL parser by input
def _get_parser(input: str) -> GQLParser:
    chars = antlr4.InputStream(input)
    lexer = GQLLexer(chars)
    tokens = antlr4.CommonTokenStream(lexer)
    return GQLParser(tokens)


# Check if the input belongs to the language
def check(
    input: str, parsing_func: Callable[[GQLParser], Any] = lambda input: input.prog()
) -> bool:
    parser = _get_parser(input)
    parser.removeErrorListeners()
    parsing_func(parser)
    return parser.getNumberOfSyntaxErrors() == 0


# Save the parsing tree in a dot file
def save_parsing_tree_as_dot(input: str, file_path: str):
    parser = _get_parser(input)
    if parser.getNumberOfSyntaxErrors() > 0:
        raise ValueError("Incorrect syntax of GQL")
    builder = _DotTreeBuilder()
    walker = antlr4.ParseTreeWalker()
    walker.walk(builder, parser.prog())
    builder.dot.write(file_path)


class _DotTreeBuilder(GQLListener):
    def __init__(self):
        self.dot = pydot.Dot("parsing_tree", strict=True)
        self._curr_id = 0
        self._id_stack = []

    def enterEveryRule(self, ctx: antlr4.ParserRuleContext):
        self.dot.add_node(
            pydot.Node(self._curr_id, label=GQLParser.ruleNames[ctx.getRuleIndex()])
        )
        if len(self._id_stack) > 0:
            self.dot.add_edge(pydot.Edge(self._id_stack[-1], self._curr_id))
        self._id_stack.append(self._curr_id)
        self._curr_id += 1

    def exitEveryRule(self, ctx: antlr4.ParserRuleContext):
        self._id_stack.pop()

    def visitTerminal(self, node: antlr4.TerminalNode):
        self.dot.add_node(pydot.Node(self._curr_id, label=f"'{node}'", shape="box"))
        self.dot.add_edge(pydot.Edge(self._id_stack[-1], self._curr_id))
        self._curr_id += 1
