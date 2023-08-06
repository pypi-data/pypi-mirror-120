from flake8.formatting.default import SimpleFormatter
from flake8.style_guide import Violation


class VscodePathFormatter(SimpleFormatter):
    """Reports the path of any files with warnings."""

    error_format = "%(path)s:%(row)d:%(col)d %(code)s %(text)s"

    def format(self, error: Violation) -> str:
        return self.error_format % {
            "code": error.code,
            "text": error.text,
            "path": error.filename[2:],
            "row": error.line_number,
            "col": error.column_number,
        }
