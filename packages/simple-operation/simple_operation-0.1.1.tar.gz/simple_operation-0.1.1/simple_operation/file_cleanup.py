import pathlib
import shutil
import time
import re

from .common import simple_operation_log


class FileCleanup:

    def __init__(
        self, file_dir: str,
        glob_pattern: str,
        re_pattern: str = None,
        remain: int = 3600 * 24,
        delete=True,
        log=None
    ) -> None:

        if not log:
            self.log = simple_operation_log
        else:
            self.log = log

        self.file_dir = file_dir
        self.glob_pattern = glob_pattern
        self.re_pattern = re_pattern
        self.remain = remain
        self.delete = delete

        if self.check_params():
            self.cleanup()

    def cleanup(self):
        file_generator = pathlib.Path(self.file_dir).glob(self.glob_pattern)
        count = 0
        for f in file_generator:
            if (time.time() - f.stat().st_mtime) < self.remain:
                continue
            if self.re_pattern and not re.search(self.re_pattern, f.name):
                continue
            count += 1
            self.log.info(f'{type(f)}, {f}')
            if self.delete:
                if f.is_file():
                    f.unlink()
                elif f.is_dir():
                    shutil.rmtree(f)
                else:
                    self.log.error(f'cleanup, {type(f)}， {f}')

        self.log.info(f'count: {count}, pattern: {self.glob_pattern}, {self.re_pattern}, '
                      f'to_remain: {self.remain}s, file_dir: {self.file_dir}')

    def check_params(self):
        if not self.file_dir or not isinstance(self.file_dir, str) or not pathlib.Path(self.file_dir).is_dir():
            self.log.error("Param file_dir is illegal.")
            return False

        if not self.glob_pattern or not isinstance(self.glob_pattern, str):
            self.log.error("Param glob_pattern is illegal.")
            return False

        if not self.re_pattern or not isinstance(self.re_pattern, str):
            self.re_pattern = None

        if not isinstance(self.remain, int) or self.remain < 0:
            self.log.error("Param remain is illegal.")
            return False

        return True
