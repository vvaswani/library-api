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
        You are an expert in the Python FastAPI framework, with a deep understanding of its lifecycle and ecosystem. You are also an expert in Pydantic, SQLAlchemy and the Repository pattern.

        Your task is to resolve failing unit tests in a FastAPI application which uses Pydantic and SQLAlchemy. If the error is due to an additional or missing field, update the models and the test cases accordingly.

        You have access to a workspace with write_file, read_file, ls, diff, and test tools. You must use these tools to identify the errors and fix the failing tests. Provide a brief explanation of your reasoning and process.

        Do not assume that errors are related to database connectivity or initialization. The database service is ephemeral. It can only be initialized and used with the test tool. Do not directly modify database configuration settings in your attempts to fix the failing tests.

        Additional requirements:

        Focus only on Python files within the /app directory.
        Begin by reading relevant files from the workspace.
        Use the write_file, read_file, ls, diff, and test tools only.
        Do not interact directly with the database; use the test tool only.
        Make the smallest change required to fix the failing tests.
        Write changes directly to the files in the workspace and only run the tests after.
        Use diff to compare your changes with the original files.
        Confirm the tests pass by running the test tool (not pytest or any other tool).
        Do not install new tools.
        Do not stop until all tests pass with the test tool.
        """
        after = (
            dag.llm()
            .with_workspace(before)
            .with_prompt(prompt)
            .workspace()
        )

        return after.container()
