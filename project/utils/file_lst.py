from dataclasses import dataclass
from typing import List
from pathlib import Path


@dataclass
class FileLst:
    file_lst: List[str] = None
    curr_dir = Path(__file__).parent

    def update_files(self):
        files_lst = self.curr_dir.glob('*')
        files_lst = list(filter(lambda file: file.is_file() and not file.endswith('.py'), files_lst))
        self.file_lst = [str(file) for file in files_lst]
