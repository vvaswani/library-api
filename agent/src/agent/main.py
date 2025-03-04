from typing import Annotated

import dagger
from dagger import DefaultPath, dag, function, object_type


@object_type
class Agent:
    @function
    def heal(
        self,
        source: Annotated[dagger.Directory, DefaultPath("/")]
    ) -> dagger.Container:
        before = dag.workspace(source=source)

        prompt = f"""
        You are an expert in the Python FastAPI framework. You understand the framework and its ecosystem. You have a deep understanding of the FastAPI lifecycle and can build complex applications with ease. You are comfortable with the command line and can navigate the FastAPI directory structure with ease.

        The tests in this FastAPI application are failing. You need to identify the error(s) that prevent the unit tests from passing and propose changes to ensure all tests pass.

        You have access to a workspace and tools. Use the 'write_file', 'read_file', 'write_directory', 'ls', 'diff', 'test' tools from the workspace only.

        The database service is ephemeral and activates only when the 'test' tool is run. Do not attempt to access the database service directly or manipulate the database schema with SQL queries. You can only access the database service through the 'test' tool.

        You have been given the following additional instructions:

        - Only consider Python files in the /app directory for this task.
        - Always read the relevant files from the workspace before starting your work
        - Continue until your assignment is completed, and the tests succeed
        - Avoid unnecessary or unrelated changes. Make the smallest possible change that meets the goal
        - Always write changes to files to the original files
        - Only use the 'test' tool to run all tests. Do not use 'pytest' or any other testing tool.
        - Only use the 'diff' tool to compare your work with the original files in the workspace.
        - Only use the 'write_file' tool to write your changes to the files
        - Remember to update the tests after making changes
        - Check that tests pass with the 'test' tool

        Explain your process or reasoning very briefly, limiting yourself to 60 words or less. Make the changes needed to make the tests pass.
        """
        after = (
            dag.llm()
            .with_workspace(before)
            .with_prompt(prompt)
            .workspace()
        )

        return after.container()
