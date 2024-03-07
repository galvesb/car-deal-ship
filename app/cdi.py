from typing import Any, Generic, Optional, Type, TypeVar, Union

import lazy_object_proxy
from opyoid import Injector as RealInjector
from opyoid import InstanceBinding
from opyoid import Module as RealModule
from opyoid import PerLookupScope
from opyoid import Provider as RealProvider
from opyoid import SingletonScope
from opyoid.utils import EMPTY

T = TypeVar("T", bound=Any)


class Provider(Generic[T], RealProvider[T]):
    __slots__ = ()


class Module(RealModule):
    __slots__ = ("_is_configured", "_binding_registry")

    # pylint: disable=too-many-arguments
    def bind_singleton(
        self,
        target_type: Type[T],
        *,
        to_class: Type[T] = EMPTY,
        to_instance: T = EMPTY,
        to_provider: Union[Provider, Type[Provider]] = EMPTY,
        named: Optional[str] = None,
    ) -> None:
        self.bind(
            target_type,
            to_class=to_class,
            to_instance=to_instance,
            to_provider=to_provider,
            named=named,
            scope=SingletonScope,
        )


class Injector:

    _injector: Optional[RealInjector] = None

    @classmethod
    def _create_injector(cls, settings) -> RealInjector:
        from app.apis.fastapi import FastAPIModule
        from app.businesses.cdi import BusinessModule
        from app.integrations.cdi import IntegrationModule
        from app.repositories.cdi import RepositoryModule
        from app.utils import Settings

        modules = [
            BusinessModule(),
            FastAPIModule(),
            IntegrationModule(),
            RepositoryModule(),
        ]

        return RealInjector(
            modules, bindings=[InstanceBinding(Settings, settings)]
        )

    @classmethod
    def startup(cls) -> None:
        if cls._injector is None:
            from dotenv import load_dotenv

            from app.utils import Settings

            load_dotenv()

            cls._injector = cls._create_injector(Settings())

    @classmethod
    def inject(cls, target_type: Type[T], *, named: Optional[str] = None) -> T:
        return cls._injector.inject(target_type=target_type, named=named)

    @classmethod
    def auto_wired(
        cls, target_type: Type[T], *, named: Optional[str] = None
    ) -> T:
        def lazy_inject():
            return cls.inject(target_type, named=named)

        return lazy_object_proxy.Proxy(lazy_inject)
