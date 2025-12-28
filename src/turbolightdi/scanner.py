import inspect
import logging
import sys
import pkgutil
import importlib
from typing import Any

from turbolightdi.container import context

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def scan_packages(base_module_name: str):
    """
    Entry point for discovery.
    Scans the specific module and all sub-packages in depth.
    """
    if context.is_initialized():
        return
    context.mark_initialized()

    try:
        root_module = sys.modules.get(base_module_name)
        if not root_module:
            root_module = importlib.import_module(base_module_name)
    except ImportError as e:
        logger.error(f"❌ [TurboDI] Could not import {base_module_name}: {e}")
        return

    found_classes: list[Any] = []

    _extract_from_mod(root_module, found_classes)

    if hasattr(root_module, "__path__"):
        for info in pkgutil.walk_packages(
            root_module.__path__, root_module.__name__ + "."
        ):
            try:
                sub_mod = importlib.import_module(info.name)
                _extract_from_mod(sub_mod, found_classes)
            except Exception as e:
                logger.debug(f"Skipping {info.name}: {e}")

    _register_found_units(found_classes)


def _extract_from_mod(module, found_classes):
    """Internal: Pulls classes with TurboDI decorators into a collection."""
    for _, obj in inspect.getmembers(module, inspect.isclass):
        # We only care about classes with our specific "Graffiti" (decorators)
        if any(
            hasattr(obj, attr) for attr in ["_is_component", "_is_controller", "_is_cy"]
        ):
            if obj not in found_classes:
                found_classes.append(obj)


def _register_found_units(classes):
    """Internal: Pushes classes into the Container registry."""
    for cls in classes:
        context.register_component(cls)
        if hasattr(cls, "_is_cy"):
            context.register_cy(cls)

        role = getattr(cls, "_turbodi_role", "Unit")
        logger.info(f"📦 [TurboDI] Discovered {role}: {cls.__name__}")
