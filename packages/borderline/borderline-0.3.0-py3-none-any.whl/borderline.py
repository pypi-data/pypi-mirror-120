import ast
import importlib
import sys

from pathlib import Path
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

    # The module you want to isolate.
    # We assume that this module lives in a subdirectory of `external_modules`.
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
    grandfather_filedir: Optional[Path] = None
    # Set to `True` when running the test in order to record a new list
    # of grandfathered imports.
    record_grandfather = False

    project_root: Path

    def _validate_config(self):
        for module in self.public_submodules:
            assert module.startswith(self.module), "Public submodules must actually be submodules."

        if self.record_grandfather:
            assert (
                self.grandfather_filedir
            ), "Cannot use `record_grandfather=True` without defining `grandfather_filedir`."

        # Ensure that all of the specified modules are importable and bring them into sys.modules
        for module in (
            (self.module,)
            + self.public_submodules
            + self.external_modules
            + self.external_dependencies
        ):
            importlib.import_module(module)

        # TODO: validate that multiple external paths do not
        # violate directory structure assumptions

    def test_module(self):
        """Statically test whether the module imports respect the module boundary."""
        self._validate_config()
        external_paths = [Path(sys.modules[mod].__path__[0]) for mod in self.external_modules]
        external_paths.sort(key=lambda x: len(x.parts))
        self.project_root = external_paths[0]

        def _get_grandfathered_file(violation_type: str) -> Path:
            assert self.grandfather_filedir
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
        module = sys.modules[self.module]
        inside_paths = {path for path in Path(module.__path__[0]).rglob("*.py")}
        internal_violations = tuple(
            self._check_modules(
                module_paths=inside_paths,
                banned_modules=self.external_modules,
                allowed_modules=(self.module,) + self.external_dependencies,
                grandfathered_violations=grandfathered_violations,
            )
        )

        # Check if external modules import submodules
        # that are not part of the module's public API.
        grandfathered_violations = _get_grandfathered_violations(violation_type="external")
        modules = {sys.modules[mod] for mod in self.external_modules}
        outside_paths = {
            path for module in modules for path in Path(module.__path__[0]).rglob("*.py")
        } - inside_paths  # Do not check paths within the module we want to isolate.
        external_violations = tuple(
            self._check_modules(
                module_paths=outside_paths,
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
            _overwrite_grandfathered_violations(
                internal_violations, _get_grandfathered_file("internal")
            )
            _overwrite_grandfathered_violations(
                external_violations, _get_grandfathered_file("external")
            )

    def _check_modules(
        self,
        module_paths: Set[Path],
        banned_modules: Tuple[str],
        allowed_modules: Tuple[str],
        grandfathered_violations: Set[str],
    ):
        """Check a set of modules for borderline violations."""
        for module_path in module_paths:
            yield from self._check_file(
                module_path,
                banned_modules,
                allowed_modules,
                grandfathered_violations,
            )

    def _check_file(
        self,
        filepath: Path,
        banned_modules: Tuple[str],
        allowed_modules: Tuple[str],
        grandfathered_violations: Set[str],
    ):
        """Check all imports within a file for borderline violations."""
        file_contents = filepath.read_bytes()
        tree = ast.parse(file_contents)
        for node in ast.walk(tree):
            if isinstance(node, (ast.ImportFrom, ast.Import)):
                illegal_import = _check_import(node, banned_modules, allowed_modules)
                if illegal_import:
                    violation = Violation(
                        location=f"{filepath.relative_to(self.project_root)}",
                        illegal_import=ast.dump(illegal_import),
                    )
                    if violation not in grandfathered_violations:
                        yield violation


def _check_import(
    import_node: Union[ast.Import, ast.ImportFrom],
    banned_modules: Tuple[str],
    allowed_modules: Tuple[str],
) -> Optional[Union[ast.Import, ast.ImportFrom]]:
    """Check if an import violates the borderline."""
    allowed = _import_is_within(import_node, allowed_modules)
    banned = _import_is_within(import_node, banned_modules)
    if not allowed and banned:
        return import_node
    return None


def _import_is_within(import_node: Union[ast.Import, ast.ImportFrom], modules: Tuple[str]) -> bool:
    """Check if an import is within a specified list of modules."""
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


def _overwrite_grandfathered_violations(
    violations: Tuple[Violation], grandfather_file: Path
) -> None:
    with open(grandfather_file, "w") as fh:
        for violation in violations:
            fh.write(f"{violation.serialize()}\n")
