from allmeca.actions.base import Action, InputDecl


class CreateFile(Action):
    command = "create_file"
    description = "Create a file"
    input_declarations = [
        InputDecl(name="path", description="The path of the file to create"),
        InputDecl(
            name="contents",
            description="The contents of the file to create",
            show_in_summary=False,
        ),
    ]

    def perform(self, environment):
        environment.write_file(self.inputs.path, self.inputs.contents)
        return f"Created file {self.inputs.path}"
