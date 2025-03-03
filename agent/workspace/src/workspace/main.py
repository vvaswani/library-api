import dagger
from dagger import dag, function, object_type


@object_type
class Workspace:
    ctr: dagger.Container = (
        dag.container()
        .from_("alpine:3.14.0").from_("python:3.11")
    )
