import dagger
from dagger import dag, function, object_type


@object_type
class Workspace:
    ctr: dagger.Container = (
        dag.container()
        .from_("alpine:3.14.0").from_("python:3.11")
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
            self.ctr
            .with_service_binding("db", postgresdb)
            .with_env_variable("DATABASE_URL", "postgresql://postgres:secret@db/app_test")
            .with_exec(["pytest", "--tb=line"])
            .stdout()
        )

    @function
    async def write_file(self, path: str, contents: str) -> dagger.File:
        return await self.ctr.with_new_file(path, contents).file(path)

    @function
    async def diff(self) -> str:
        return await self.ctr.with_exec(["git", "diff"]).stdout()
