import pytest
from turbodi.container import TurboDIContainer


def borg(func):
    func._is_borg = True
    return func


class TestContainer:
    @pytest.fixture
    def container(self):
        return TurboDIContainer()

    def test_singleton_management(self, container):
        """Verifies that the container returns the same instance twice."""

        class SimpleService:
            pass

        instance1 = container.resolve_dep(SimpleService)
        instance2 = container.resolve_dep(SimpleService)

        assert instance1 is instance2
        assert isinstance(instance1, SimpleService)

    def test_recursive_constructor_injection(self, container):
        """Verifies that dependencies are resolved and injected into the constructor."""

        class Repository:
            def __init__(self):
                self.data = "turbodi_data"

        class Service:
            def __init__(self, repo: Repository):
                self.repo = repo

        service = container.resolve_dep(Service)

        assert isinstance(service.repo, Repository)
        assert service.repo.data == "turbodi_data"

    def test_borg_provider_resolution(self, container):
        """Verifies that @borg methods in a @cy class provide dependencies."""

        class ExternalClient:
            def __init__(self, connection_str: str):
                self.connection_str = connection_str

        class MockCy:
            def __init__(self):
                self.config_val = "redis://localhost"

            @borg
            def provide_client(self) -> ExternalClient:
                return ExternalClient(self.config_val)

        container.register_cy(MockCy)

        client = container.resolve_dep(ExternalClient)

        assert isinstance(client, ExternalClient)
        assert client.connection_str == "redis://localhost"

    def test_missing_type_hint_raises_error(self, container):
        """Verifies that a Borg without a return type hint raises a TypeError."""

        class BadCy:
            @borg
            def provide_something(self):  # Missing -> Hint
                return "data"

        with pytest.raises(TypeError) as excinfo:
            container.register_cy(BadCy)

        assert "must have a return type hint" in str(excinfo.value)

    def test_deep_resolution_chain(self, container):
        """Verifies a chain of A -> B -> C resolution."""

        class C:
            pass

        class B:
            def __init__(self, c: C):
                self.c = c

        class A:
            def __init__(self, b: B):
                self.b = b

        a_instance = container.resolve_dep(A)

        assert isinstance(a_instance.b, B)
        assert isinstance(a_instance.b.c, C)
