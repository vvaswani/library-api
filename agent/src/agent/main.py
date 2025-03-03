import dagger
from dagger import dag, function, object_type


@object_type
class Agent:
    @function
    async def heal(self, source: dagger.Directory) -> dagger.Container:
        ws = (
            dag.workspace()
            .with_directory("/app", source.without_directory(".dagger"))
            .with_workdir("/app")
            .with_mounted_cache("/root/.cache/pip", dag.cache_volume("python-pip"))
            .with_exec(["pip", "install", "-r", "requirements.txt"])
        )

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
            .with_workspace(ws)
            .with_prompt(prompt)
        )

        return after.container()
