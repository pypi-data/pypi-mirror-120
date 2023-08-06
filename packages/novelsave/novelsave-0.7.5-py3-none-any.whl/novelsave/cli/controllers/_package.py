import sys
from typing import Iterable

from dependency_injector.wiring import inject, Provide
from loguru import logger

from novelsave.cli.helpers import get_novel
from novelsave.containers import Application
from novelsave.core.services import BasePathService
from novelsave.core.services.packagers import BasePackagerProvider


@inject
def package(
        id_or_url: str,
        keywords: Iterable[str],
        packager_provider: BasePackagerProvider = Provide[Application.packagers.packager_provider],
        path_service: BasePathService = Provide[Application.services.path_service],
):
    """Package the selected novel into the formats of choosing

    Note: currently supports epub format only
    """
    try:
        novel = get_novel(id_or_url)
    except ValueError:
        sys.exit(1)

    for packager in packager_provider.filter_packagers(keywords):
        path = packager.package(novel)
        logger.info(f"Packaging completed (type='{packager.keywords()[0]}', path='{path_service.relative_to_novel_dir(path)}')")
