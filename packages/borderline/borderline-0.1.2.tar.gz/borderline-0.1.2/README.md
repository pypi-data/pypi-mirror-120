# Borderline

Stop letting modules reach into other modules.

---

![python-package](https://github.com/ctk3b/borderline/actions/workflows/python-package.yml/badge.svg)

This library provides one thing and one thing only: a test class called `TestModuleImports`. 

To use the test, subclass it in the test suite of the module you want to isolate and define that module's borderlines.
The test will fail if a module is not respecting those borderlines.

For example, a module called `report_builder` could have the following definition:

```python
class TestReportBuilder(TestModuleImports):
    module = "reporting.report_builder"
    
    # The public API of the module.
    # External modules should only import from here.
    public_modules = (
        "reporting.report_builder.api",
    )
    # Modules that are considered outside of `module` and should not be imported
    # by `module` unless they are a legitimate dependency.
    external_modules = (
        "reporting",
    )
    # Modules outside of `module` that ARE legitimate dependencies.
    external_dependencies = (
        "reporting.review.api",
        "reporting.common",
    )

    # Directory to store imports that are currently allowed.
    # This is useful when you are trying to isolate an existing module
    # that is not respecting its borderlines.
    grandfather_filedir = Path(
        "reporting/report_builder/tests/data/borderline", parents=True, exist_ok=True
    )
```
