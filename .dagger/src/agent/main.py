from typing import Annotated

import dagger
from dagger import DefaultPath, Secret, dag, function, object_type


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

        The write_file tool creates a new file. When making changes with the write_file tool, you must be extremely careful to avoid overwriting the entire file. To make changes with the write_file tool, read the original file contents, modify in place, and write the complete modified contents back. Double check that you have not deleted important code when modifying existing files.

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

    @function
    def diagnose(
        self,
        source: Annotated[dagger.Directory, DefaultPath("/")],
        token: Secret,
    ) -> dagger.Container:
        before = dag.workspace(source=source)

        prompt = f"""
        You are an expert in the Python FastAPI framework, with a deep understanding of its lifecycle and ecosystem. You are also an expert in Pydantic, SQLAlchemy and the Repository pattern.

        Your task is to assist with resolving failing unit tests in a FastAPI application which uses Pydantic and SQLAlchemy.

        You have access to a workspace with write_file, read_file, ls, diff, comment, and test tools. You must use these tools to identify the errors and fix the failing tests. Once you are successful, you must use the comment tool to create and post a detailed comment explaining the error and how you resolved it.

        Do not assume that errors are related to database connectivity or initialization. The database service is ephemeral. It can only be initialized and used with the test tool. Do not directly modify database configuration settings in your attempts to fix the failing tests.

        The write_file tool creates a new file. When making changes with the write_file tool, you must be extremely careful to avoid overwriting the entire file. To make changes with the write_file tool, read the original file contents, modify in place, and write the complete modified contents back. Double check that you have not deleted important code when modifying existing files.

        The comment tool creates a new comment. When using the comment tool, you must provide a detailed explanation of the error and how you resolved it. You must also provide a brief explanation of your reasoning and process. When using the comment tool, specify the repository and ref where the comment should be posted. The repository is  in the GITHUB_REPOSITORY environment variable. The ref is in the GITHUB_REF_NAME environment variable. The GitHub token is provided as a secret in the GITHUB_API_TOKEN environment variable.

        Additional requirements:

        Focus only on Python files within the /app directory.
        Begin by reading relevant files from the workspace.
        Use the write_file, read_file, ls, diff, comment, and test tools only.
        Do not interact directly with the database; use the test tool only.
        Make the smallest change required to fix the failing tests.
        Write changes directly to the files in the workspace and only run the tests after.
        Use diff to compare your changes with the original files.
        Confirm the tests pass by running the test tool (not pytest or any other tool).
        Do not install new tools.
        Do not post a comment until all tests pass with the test tool.
        """
        after = (
            dag.llm()
            .with_workspace(before)
            .with_prompt(prompt)
            .workspace()
        )

        return after.container()
