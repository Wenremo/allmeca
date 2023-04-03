from pydantic import BaseModel
from box import Box
from textwrap import dedent


class InputDecl(BaseModel):
    name: str
    description: str
    required: bool = True
    show_in_summary: bool = True


class Action:
    command = None
    description = None
    input_declarations: list[InputDecl] = []

    def __init__(
        self, context: str, inputs: dict[str, str] = dict(), errors: list[str] = []
    ):
        self.context = context
        self.inputs = Box(inputs)
        self.errors = []
        self._validate()

    def perform(self, environment):
        raise NotImplementedError

    def is_valid(self):
        return len(self.errors) == 0

    def summary(self):
        return f"{self.command} {self._inputs_summary()}"

    def __str__(self):
        return dedent(
            """
            ACTION: {command}{inputs}
            ENDACTION
            """
        ).format(command=self.command, inputs=self._inputs_str())

    def _validate(self):
        for declaration in self.input_declarations:
            if declaration.required and declaration.name not in self.inputs:
                self.errors.append(f"Missing required input '{declaration.name}'")

        valid_input_names = set(d.name for d in self.input_declarations)
        for input_name in self.inputs:
            if input_name not in [d.name for d in self.input_declarations]:
                self.errors.append(f"Unknown input '{input_name}'")

    def __repr__(self):
        return f"<Action {self.summary()}>"

    def _inputs_summary(self):
        shown_keys = set(
            declaration.name
            for declaration in self.input_declarations
            if declaration.show_in_summary
        )
        kvs = [
            f"{k}={{{{{self._format_input_value(v)}}}}}"
            for k, v in self.inputs.items()
            if k in shown_keys
        ]
        return ", ".join(kvs)

    def _inputs_str(self):
        if len(self.inputs) == 0:
            return ""
        kvs = [f"  {k}={{{{{str(v)}}}}}" for k, v in self.inputs.items()]
        return "\n{kvs}".format(kvs="\n".join(kvs))

    def _format_input_value(self, value):
        formatted = str(value)
        if len(formatted) > 40:
            formatted = formatted[:40] + "..."
        if "\n" in formatted:
            formatted = formatted.split("\n")[0] + "..."
        return formatted
