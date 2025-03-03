from typing import Annotated

import dagger
from dagger import DefaultPath, dag, function, object_type

@object_type
class Book:
    source: Annotated[dagger.Directory, DefaultPath(".")]

    @function
    def env(self, version: str = "3.11") -> dagger.Container:
        return (
            dag.container()
            .from_(f"python:{version}")
            .with_directory("/app", self.source.without_directory(".dagger"))
            .with_workdir("/app")
            .with_mounted_cache("/root/.cache/pip", dag.cache_volume("python-pip"))
            .with_exec(["pip", "install", "-r", "requirements.txt"])
        )

    @function
    async def test(self) -> str:
        postgresdb = (
            dag.container()
            .from_("postgres:alpine")
            .with_env_variable("POSTGRES_DB", "app_test")
            .with_env_variable("POSTGRES_PASSWORD", "secret")
            .with_exposed_port(5432)
            .as_service(args=[], use_entrypoint=True)
        )

        return await (
            self.env()
            .with_service_binding("db", postgresdb)
            .with_env_variable("DATABASE_URL", "postgresql://postgres:secret@db/app_test")
            .with_exec(["pytest"])
            .stdout()
        )

    @function
    async def write_file(self, path: str, contents: str) -> dagger.File:
        return await self.env().with_new_file(path, contents).file(path)

    @function
    async def diff(self) -> str:
        return await self.env().with_exec(["git", "diff"]).stdout()

    @function
    async def heal(self) -> dagger.Container:
        prompt = f"""
        You are an expert in the Python FastAPI framework. You understand the framework and its ecosystem. You have a deep understanding of the FastAPI lifecycle and can build complex applications with ease. You are comfortable with the command line and can navigate the FastAPI directory structure with ease.

        - Only consider Python files in the directory for this task.
        - Avoid unnecessary or unrelated changes. Make the smallest possible change that meets the goal
        - Continue until your assignment is completed, and the tests succeed
        - Always write changes to files to the original files
        - Check that your work meets requirements with the 'test' tool
        - Only use the 'test' tool to verify your work
        - Use the 'diff' tool to compare the changes made to the code.
        - Use the 'write_file' tool to write your changes to the files
        - Use the 'test' tool to run all available tests

        Your assignment is to identify the error(s) that prevent the unit tests from passing and propose changes to ensure all tests pass.
        """
        after = await (
            dag().llm()
            .with_container(self.env())
            .with_prompt_var("diff", self.diff())
            .with_prompt(prompt)
        )

        return after.container()
