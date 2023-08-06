import ast
import sys

from pathlib import Path
from types import ModuleType
from typing import Tuple, Set, Union, NamedTuple, Optional

VIOLATION_DELIMETER = "::"


class ModuleImportViolation(Exception):
    pass


class Violation(NamedTuple):
    location: str
    illegal_import: str

    def serialize(self) -> str:
        return f"{self.location}{VIOLATION_DELIMETER}{self.illegal_import}"

    @staticmethod
    def deserialize(data) -> "Violation":
        location, illegal_import = data.strip().split(VIOLATION_DELIMETER)
        return Violation(location=location, illegal_import=illegal_import)


class ModuleImports:
    """
    Tests that new imports within a module respect the public API boundary.

    To use, subclass this and define the boundaries of the module you are isolating.

    See README.md for example.

    Notes
    -----
    `ast.dump` does not produce identical results across python versions. If you
    are relying on grandfather files, you may need to regenerate them when updating
    python versions.

    Specifically, from python 3.8->3.9, `Import` and `ImportFrom` nodes no longer
    `ast.dump` an `asname` attribute.

    """

    module: str
    # The public API of the module.
    # External modules should only import from here.
    public_submodules: Tuple[str]
    # Modules that are considered outside of `module` and should not be imported
    # by `module` unless they are a legitimate dependency.
    external_modules: Tuple[str]
    # Modules outside of `module` that ARE legitimate dependencies.
    external_dependencies: Tuple[str]

    # Directory to store imports that are currently allowed.
    # This is useful when you are trying to isolate an existing module
    # that is not respecting its borderlines.
    grandfather_filedir: Path
    # Set to `True` when running the test in order to record a new list
    # of grandfathered imports.
    record_grandfather = False

    def test_module(self):
        """
        Statically test whether the module imports respect the module boundary.
        """

        def _get_grandfathered_file(violation_type: str) -> Path:
            self.grandfather_filedir.mkdir(parents=True, exist_ok=True)
            return self.grandfather_filedir / f"{violation_type}_violations.txt"

        def _get_grandfathered_violations(violation_type: str) -> Set:
            if self.grandfather_filedir:
                grandfather_file = _get_grandfathered_file(violation_type)
                grandfather_file.touch(exist_ok=True)
                with open(grandfather_file) as fh:
                    return set(Violation.deserialize(line) for line in fh.readlines())
            else:
                return set()

        # Check if the module imports external modules
        # that are not legitimate dependencies.
        grandfathered_violations = _get_grandfathered_violations(violation_type="internal")
        internal_violations = tuple(
            self._check_modules(
                modules=(self.module,),
                banned_modules=self.external_modules,
                allowed_modules=self.public_submodules + self.external_dependencies,
                grandfathered_violations=grandfathered_violations,
            )
        )

        # Check if external modules import submodules
        # that are not part of the module's public API.
        grandfathered_violations = _get_grandfathered_violations(violation_type="external")
        external_violations = tuple(
            self._check_modules(
                modules=self.external_modules,
                banned_modules=(self.module,),
                allowed_modules=self.public_submodules,
                grandfathered_violations=grandfathered_violations,
            )
        )

        violations = internal_violations + external_violations
        if not self.record_grandfather:
            if violations:
                raise ModuleImportViolation(violations)
        else:
            assert (
                self.grandfather_filedir
            ), "Cannot use `record_grandfather=True` without defining `grandfather_filedir`"
            self._overwrite_grandfathered_violations(
                internal_violations, _get_grandfathered_file("internal")
            )
            self._overwrite_grandfathered_violations(
                external_violations, _get_grandfathered_file("external")
            )

    def _check_modules(
        self,
        modules: Tuple[str],
        banned_modules: Tuple[str],
        allowed_modules: Tuple[str],
        grandfathered_violations: Set[str],
    ):
        for module_path in modules:
            module = sys.modules[module_path]
            py_filepaths = [
                path
                for path in Path(module.__path__[0]).rglob("*.py")  # type:ignore[attr-defined]
            ]
            for py_filepath in py_filepaths:
                yield from self._check_file(
                    module,
                    py_filepath,
                    banned_modules,
                    allowed_modules,
                    grandfathered_violations,
                )

    def _check_file(
        self,
        module: ModuleType,
        filepath: Path,
        banned_modules: Tuple[str],
        allowed_modules: Tuple[str],
        grandfathered_violations: Set[str],
    ):
        file_contents = filepath.read_bytes()
        tree = ast.parse(file_contents)
        for node in ast.walk(tree):
            if isinstance(node, (ast.ImportFrom, ast.Import)):
                illegal_import = self._check_import(node, banned_modules, allowed_modules)
                if illegal_import:
                    violation = Violation(
                        location=f"{module.__name__}.{filepath.name}",
                        illegal_import=ast.dump(illegal_import),
                    )
                    if violation not in grandfathered_violations:
                        yield violation

    def _check_import(
        self,
        import_node: Union[ast.Import, ast.ImportFrom],
        banned_modules: Tuple[str],
        allowed_modules: Tuple[str],
    ) -> Optional[Union[ast.Import, ast.ImportFrom]]:
        allowed = self._node_is_within(import_node, allowed_modules)
        banned = self._node_is_within(import_node, banned_modules)
        if not allowed and banned:
            return import_node
        return None

    @staticmethod
    def _node_is_within(
        import_node: Union[ast.Import, ast.ImportFrom], modules: Tuple[str]
    ) -> bool:
        if isinstance(import_node, ast.Import):
            for ast_alias in import_node.names:
                if not ast_alias.name.startswith(modules):
                    return False
            else:
                return True
        elif isinstance(import_node, ast.ImportFrom):
            assert import_node.module
            node_module_is_within = import_node.module.startswith(modules)
            if node_module_is_within:
                return True

            for ast_alias in import_node.names:
                if not f"{import_node.module}.{ast_alias.name}".startswith(modules):
                    return False
            else:
                return True
        else:
            raise ValueError("Passed incorrect type for `import_node`")

    @staticmethod
    def _overwrite_grandfathered_violations(
        violations: Tuple[Violation],
        grandfather_file: Path,
    ) -> None:
        with open(grandfather_file, "w") as fh:
            for violation in violations:
                fh.write(f"{violation.serialize()}\n")
