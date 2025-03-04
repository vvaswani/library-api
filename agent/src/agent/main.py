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
        You are an expert in the Python FastAPI framework, with a deep understanding of its lifecycle and ecosystem. You are tasked with resolving failing unit tests in a FastAPI application. You hae access to a workspace wth write_file, read_file, ls, diff, and test tools.

        Follow these instructions:

        Focus only on Python files within the /app directory.
        Begin by reading relevant files from the workspace.
        Use the write_file, read_file, ls, diff, and test tools only.
        Do not interact directly with the database; use the test tool only.
        Make the smallest change required to fix the failing tests.
        Write changes directly to the original files.
        Use diff to compare your changes with the original files.
        Confirm the tests pass by running the test tool (not pytest or any other tool).
        Provide concise explanations of your process (up to 60 words).
        """
        after = (
            dag.llm()
            .with_workspace(before)
            .with_prompt(prompt)
            .workspace()
        )

        return after.container()
