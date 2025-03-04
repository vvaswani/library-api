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
            .with_directory("/app", self.source.without_directory(".dagger").without_directory("agent"))
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
            .with_exec(["pytest", "--tb=line"])
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

        The tests in this FastAPI application are failing. Use the 'write_file', 'diff', 'test' tools from the workspace only. You need to identify the error(s) that prevent the unit tests from passing and propose changes to ensure all tests pass. You have been given the following additional instructions:

        - Only consider Python files in the /app directory for this task. Ignore any and all syntax errors you may find.
        - Avoid unnecessary or unrelated changes. Make the smallest possible change that meets the goal
        - Always write changes to files to the original files
        - Only use the 'test' tool to run all tests. Do not use 'pytest' or any other testing tool.
        - Only use the 'diff' tool to run all tests. Do not use any other tool.
        - Check that your work meets requirements with the 'test' tool
        - Only use the 'write_file' tool to write your changes to the files
        - Before using the 'write_file' tool, use the 'test' tool to check that all changes are correct

        Do not explain your process or reasoning. Only make the changes needed to make the tests pass.
        """
        after = await (
            dag.llm()
            .with_container(self.env())
            #.with_prompt_var("diffe", self.diff())
            .with_prompt(prompt)
        )

        return after.container()
