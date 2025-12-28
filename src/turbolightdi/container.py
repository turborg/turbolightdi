import inspect
import logging
from typing import Type, TypeVar, Any, Callable

T = TypeVar("T")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TurboLightDIContainer:
    def __init__(self):
        self._initialized = False
        # @Cy's
        self._cys: dict[Type, Any] = {}
        # (Services, Controllers and yielded Borgs)
        self._singletons: dict[Type, Any] = {}
        # Factory methods
        self._providers: dict[Type, Callable] = {}
        self._registry: list[Type] = []

    def is_initialized(self):
        return self._initialized

    def get_registry(self) -> list[Type]:
        return self._registry

    def mark_initialized(self):
        self._initialized = True

    def _create_instance(self, cls: Type) -> Any:
        signature = inspect.signature(cls.__init__)
        kwargs = {}

        for name, param in signature.parameters.items():
            if name == "self":
                continue

            dep_type = param.annotation
            if dep_type is not inspect.Parameter.empty:
                kwargs[name] = self.resolve_dep(dep_type)

        return cls(**kwargs)

    def register_cy(self, cls: type):
        """
        Called by the Scanner when it finds a @cy decorator
        :param cls:
        :return:
        """
        cy_instance = self._create_instance(cls)
        self._cys[cls] = cy_instance

        # Now we extract the tagged Borgs from the instance
        for name, method in inspect.getmembers(cy_instance, predicate=inspect.ismethod):
            if hasattr(method, "_is_borg"):
                return_type = inspect.signature(method).return_annotation
                if return_type is inspect.Signature.empty:
                    raise TypeError(
                        f"Borg '{cls.__name__}.{name}' must have a return type hint."
                    )
                self._providers[return_type] = method

    def register_component(self, cls: Type):
        """Called by decorators/scanner to record a class."""
        if cls not in self._registry:
            logger.info(f"put registered {cls} ")
            self._registry.append(cls)

    def resolve_dep(self, cls: Type[T]) -> T:
        """
        Figure out if we need to fetch or create new object
        :param cls:
        :return:
        """
        if cls in self._singletons:
            return self._singletons[cls]

        # is there a borg?
        if cls in self._providers:
            instance = self._providers[cls]()
            self._singletons[cls] = instance
            return instance

        instance = self._create_instance(cls)
        self._singletons[cls] = instance
        return instance


context: TurboLightDIContainer = TurboLightDIContainer()
