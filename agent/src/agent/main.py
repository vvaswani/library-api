import dagger
from dagger import dag, function, object_type


@object_type
class Agent:
    @function
    def heal(self, source: dagger.Directory) -> dagger.Container:
        before = dag.workspace(source=source)

        prompt = f"""
        You are an expert in the Python FastAPI framework. You understand the framework and its ecosystem. You have a deep understanding of the FastAPI lifecycle and can build complex applications with ease. You are comfortable with the command line and can navigate the FastAPI directory structure with ease.

        The tests in this FastAPI application are failing. You need to identify the error(s) that prevent the unit tests from passing and propose changes to ensure all tests pass. Use the 'write_file', 'read_file', 'write_directory', 'ls', 'diff', 'test', 'exec' tools from the workspace only.

        You have been given the following additional instructions:

        - Only consider Python files in the /app directory for this task.
        - Always read the relevant files from the workspace before starting your work
        - Continue until your assignment is completed, and the tests succeed
        - Avoid unnecessary or unrelated changes. Make the smallest possible change that meets the goal
        - Always write changes to files to the original files
        - Only use the 'test' tool to run all tests. Do not use 'pytest' or any other testing tool.
        - Only use the 'diff' tool to compare your work with the original files in the workspace.
        - Check that tests pass with the 'test' tool
        - Only use the 'write_file' tool to write your changes to the files

        Explain your process or reasoning. Make the changes needed to make the tests pass.
        """
        after = (
            dag.llm()
            .with_workspace(before)
            .with_prompt(prompt)
            .workspace()
        )

        return after.container()
