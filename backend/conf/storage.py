"""
Whitenoise's CompressedManifestStaticFilesStorage class override
"""

import collections
import logging
import re

from django.conf import settings

from whitenoise.storage import CompressedManifestStaticFilesStorage

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# file_log_handler = logging.FileHandler('storage.log')
# file_log_handler.setFormatter(formatter)

stderr_log_handler = logging.StreamHandler()
stderr_log_handler.setFormatter(formatter)

logger = logging.getLogger('Storage')

logger.setLevel('DEBUG')
logger.addHandler(stderr_log_handler)
# logger.addHandler(file_log_handler)


class ExcludeFromStorageMixin:

    _expressions = []
    for expression in getattr(settings, "WHITENOISE_EXCLUDE_PATHS", None):
        _expressions.append(re.compile(expression))

    def stored_name(self, name):
        """
        Retrieve stored file name.
        """
        if self.is_excluded(name):
            return name
        else:
            return super().stored_name(name)

    def is_excluded(self, path):
        """
        Determine if a path is excluded or not.
        """
        for expression in self._expressions:
            value = expression.search(path)
            if value:
                return value

        return None

    def post_process(self, paths, dry_run=False, **options):
        """
        Filter paths to be processed.
        """
        if dry_run:
            return

        included_paths = collections.OrderedDict()
        for path, path_info in paths.items():
            if self.is_excluded(path):
                logger.info('Excluding ' + path)
                yield path, None, False
            else:
                included_paths[path] = path_info

        yield from super().post_process(
            included_paths, dry_run=dry_run, **options)


class CompressedManifestStaticFilesStorage(
    ExcludeFromStorageMixin, CompressedManifestStaticFilesStorage
):
    """
    Same as whitenoise.storage.CompressedManifestStaticFilesStorage.

    Adds a mixin to exclude specified paths.
    """
