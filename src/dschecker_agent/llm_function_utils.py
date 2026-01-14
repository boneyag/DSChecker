import json
import libcst as cst
import libcst.matchers as m
from libcst.metadata import QualifiedNameProvider, QualifiedNameSource, PositionProvider
import os
import subprocess
from typing import Union

from dschecker.logging_util.logger import setup_logger

logger = setup_logger(__name__)


class TypeInstrumenter(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, trgn: str, trgl: int, code: str, after: bool = True):
        self.statement = None
        self.trg_name = trgn
        self.trg_line = trgl
        self.new_code = [*cst.parse_module(code).body]
        self.insert_after = after

    def visit_SimpleStatementLine(self, node):
        metadata = self.get_metadata(PositionProvider, node)
        line_number = metadata.start.line

        if line_number != self.trg_line:
            return

        target_assignment_matcher = m.Assign(
            targets=[
                m.AssignTarget(
                    target=(
                        m.Name(self.trg_name) |
                        m.Subscript(value=m.Name(self.trg_name)) |
                        m.Tuple(elements=m.List(m.Element(value=m.Name(self.trg_name))))
                    )
                )
            ]
        )

        if m.matches(node.body[0], target_assignment_matcher):
            self.statement = node
            self.insert_after = True
            return

        # Now, check for function calls where the target name is an argument.
        # This matcher is simpler. It just finds any expression that is a Call.
        call_expr_matcher = m.Expr(value=m.Call())

        if m.matches(node.body[0], call_expr_matcher):
            call_node = node.body[0].value
            target_name_matcher = m.Name(self.trg_name)

            # Iterate through the positional arguments to see if the target name is there.
            for arg in call_node.args:
                if m.matches(arg.value, target_name_matcher):
                    self.statement = node
                    self.insert_after = False
                    return

    def leave_Module(self, original_module: cst.Module, updated_module: cst.Module) -> cst.Module:
        if self.statement:
            original_body = list(original_module.body)

            if self.statement in original_body:
                idx = original_body.index(self.statement)
                if self.insert_after:
                    new_body = cst.FlattenSentinel(original_body[:idx+1] + self.new_code + original_body[idx+1:])
                else:
                    new_body = cst.FlattenSentinel(original_body[:idx] + self.new_code + original_body[idx:])
        else:
            # This means the LLM ask for a something that is not a variable
            original_body = list(original_module.body)
            new_body = cst.FlattenSentinel(original_body + self.new_code)
        updated_module = cst.Module(body=new_body)
        # logger.info(updated_module)
        return updated_module


class FullyQualifiedNameResolver(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (QualifiedNameProvider,)

    def __init__(self, target_name: str):
        self.target_name = target_name
        self.fully_qualified_name = ""
        self.var_import_map = {}

    def visit_Assign(self, node: cst.Assign) -> None:
        if isinstance(node.value, (cst.Call, cst.Attribute)):
            self._process_api_chain(
                self._get_called_apis(node.value),
                target_var=self._get_assign_target_name(node)
            )

    def visit_Expr(self, node: cst.Expr) -> None:
        if isinstance(node.value, (cst.Call, cst.Attribute)):
            self._process_api_chain(
                self._get_called_apis(node.value),
                target_var=None
            )

    def visit_Arg(self, node: cst.Arg) -> None:
        if isinstance(node.value, (cst.Call, cst.Attribute)):
            self._process_api_chain(
                self._get_called_apis(node.value),
                target_var=None
            )

    def visit_List(self, node: cst.List) -> None:
        for el in node.elements:
            if isinstance(el.value, (cst.Call, cst.Attribute)):
                self._process_api_chain(
                    self._get_called_apis(el.value),
                    target_var=None
                )

    def visit_Tuple(self, node: cst.Tuple) -> None:
        for el in node.elements:
            if isinstance(el.value, (cst.Call, cst.Attribute)):
                self._process_api_chain(
                    self._get_called_apis(el.value),
                    target_var=None
                )

    def _process_api_chain(self, chain, target_var):
        """
        Given a chain from _get_called_apis, resolve fully qualified name
        for any API in the chain matching self.target_name.
        Optionally map target_var to a base import if given.
        """
        # find base import in the chain
        # find base import in the chain
        base_fqn = None
        base_index = None
        for i, item in enumerate(chain):
            qns = self.get_metadata(QualifiedNameProvider, item["node"])
            for qn in qns:
                if qn.source == QualifiedNameSource.IMPORT:
                    base_fqn = qn.name
                    base_index = i
                    break
            if base_fqn:
                break

        # fallback: check var_import_map
        if base_fqn is None and chain:
            first_api = chain[0]["api"]
            if first_api in self.var_import_map:
                base_fqn = self.var_import_map[first_api]
                base_index = 0

        # map variable to base if assignment
        if target_var and base_fqn:
            if base_index + 1 < len(chain):
                suffix = ".".join(p["api"] for p in chain[base_index+1:])
                self.var_import_map[target_var] = f"{base_fqn}.{suffix}"
            else:
                self.var_import_map[target_var] = base_fqn

        # check for target_name in chain
        for idx, item in enumerate(chain):
            if item["api"] == self.target_name:
                if base_fqn and base_index is not None and base_index <= idx:
                    suffix = ".".join(p["api"] for p in chain[base_index + 1 : idx + 1])
                    self.fully_qualified_name = f"{base_fqn}.{suffix}" if suffix else base_fqn
                else:
                    qns = self.get_metadata(QualifiedNameProvider, item["node"])
                    for qn in qns:
                        if qn.source == QualifiedNameSource.IMPORT:
                            self.fully_qualified_name = qn.name

    def _get_assign_target_name(self, node: cst.Assign):
        if len(node.targets) == 1:
            if isinstance(node.targets[0], cst.AssignTarget):
                if isinstance(node.targets[0].target, cst.Name):
                    # logger.info(f"var: {node.targets[0].target.value}")
                    return node.targets[0].target.value

    def _get_called_apis(self, node: cst.CSTNode) -> list[dict[str, Union[str, cst.CSTNode]]]:
        if isinstance(node, cst.Call):
            return self._get_called_apis(node.func)

        # Attribute(value=..., attr=Name(...)) -> first recurse into value, then append this attribute
        if isinstance(node, cst.Attribute):
            parts = self._get_called_apis(node.value)
            # append the attribute itself; pass the full Attribute node for metadata queries
            parts.append({"api": node.attr.value, "node": node})
            return parts

        # Subscript(foo)[0].bar  -> drop subscript and analyze the value
        if isinstance(node, cst.Subscript):
            return self._get_called_apis(node.value)

        # Name -> base case
        if isinstance(node, cst.Name):
            return [{"api": node.value, "node": node}]

        # anything else (literal, etc.) -> no APIs
        return []


def get_fully_qualified_name(api_name, code):
    if api_name.startswith("_"):
        logger.info(
            f"{api_name}: possibly an internal API. Documentation only available for public APIs."
        )
        return
    if api_name.endswith("_"):
        logger.info(
            f"{api_name}: possibly a member of an object."
        )
        return
    if "." in api_name:  # when LLM do not follow instructions
        api_name = api_name.split(".")[-1]

    # All API names cannot be resolved using AST parsing.
    # e.g., fig, ax = plt.subplots() -- will resolve fig and ax as subplots.
    # We use the map for known cases
    with open(os.path.join(os.path.dirname(__file__), "api_fqn_map.json")) as f:
        api_map = json.load(f)

    if api_name in api_map:
        return api_map[api_name]
    else:
        source_tree = cst.parse_module(code)
        # logger.info(source_tree)
        wrapper = cst.MetadataWrapper(source_tree)
        fqn_resolver = FullyQualifiedNameResolver(api_name)
        wrapper.visit(fqn_resolver)
        logger.info(f"{api_name}:{fqn_resolver.fully_qualified_name}")
        return fqn_resolver.fully_qualified_name


def instrument_code(var_name, line_num, code, file_name, output):
    source_tree = cst.parse_module(code)
    # logger.info(source_tree)
    wrapper = cst.MetadataWrapper(source_tree)
    code_to_insert = f"import pandas\nimport numpy\nif isinstance({var_name}, pandas.core.frame.DataFrame):\n    print(\"----***----\")\n    print(\"pandas.core.frame.DataFrame\")\n    print({var_name}.info())\n    print(\"***\")\n    print({var_name}.head(3))\n    print(\"----***----\")\n\nelif isinstance({var_name}, numpy.ndarray):\n    print(\"----***----\")\n    print(\"numpy.ndarray\")\n    print(\"dtype-\"+str({var_name}.dtype)+\" shape-\"+str({var_name}.shape))\n    slices = tuple(slice(0, 3) for _ in range({var_name}.ndim))\n    print(\"***\")\n    print({var_name}[slices])\n    print(\"----***----\")\n\nelif isinstance({var_name}, list):\n    print(\"----***----\")\n    print(\"list\")\n    print(\"length-\"+str(len({var_name})))\n    print(\"***\")\n    print({var_name}[:3])\n    print(\"----***----\")\n\nelse:\n    print(\"----***----\")\n    print(f\"Type: {{type({var_name}).__name__}}\")\n    print(\"***\")\n    print(\"Unsuported type for instrumentation\")\n    print(\"----***----\")\n"

    instrumented_ast = wrapper.visit(TypeInstrumenter(var_name, line_num, code_to_insert))

    with open(
        os.path.join(
            os.path.dirname(__file__),
            f"../results/{output}/instrumented",
            f"{file_name}_mod.py"), "w") as f:
        f.write(instrumented_ast.code)


def run_code(file_name, output):
    try:
        instrumented_file = os.path.join(
            os.path.dirname(__file__),
            f"../results/{output}/instrumented",
            f"{file_name}_mod.py"
        )
        process_res = subprocess.Popen(
            ["python", instrumented_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = process_res.stdout.readlines()
        errors = process_res.stderr.readlines()
        # logger.info(f"Errors: {errors}")
        if output:
            return output
    except Exception as e:
        logger.error(f"Error running the code: {e}")
        return None


# if __name__ == "__main__":

#     # code = "import seaborn as sns\ntips = sns.load_dataset('tips')\ng = sns.FacetGrid(data=tips, col='time', row='sex')\ng.map(sns.lmplot, 'total_bill', 'tip')"
#     # fqn = get_fully_qualified_name("map", code)

#     code = "import numpy as np\n\narr = np.ones((3, 4))"
#     instrument_code("arr", 3, code, "test", "test-fn")
#     # output = run_code("test")
#     # print(output)
