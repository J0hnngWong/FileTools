import os
import sys
from hashlib import md5
import tkinter
from collections.abc import Callable
from typing import Any

def get_root_path() -> str:
    try:
        root_path = sys.argv[1]
    except IndexError as inx_err:
        raise Exception('Please Enter Valid Root Path!') from inx_err
    return root_path

class FileHashModel:
    file_path_list: list
    hash_value: str

class SameFileFilter:
    def __init__(self):
        # { hash : [file_path] }
        self.file_md5_dict: dict = {}
        self.process_handler: Callable[[str], Any] | None = None

    def set_process_handler(self, handler: Callable[[str], Any]):
        self.process_handler = handler

    def find_same_file(self, dir_path: str):
        self.check_have_same_file(dir_path=dir_path)
        # print(self.file_md5_dict)

    def check_have_same_file(self, dir_path: str):
        root_dir, dir_names, file_names = next(os.walk(dir_path))
        for file_name in file_names:
            current_file_path = os.path.join(root_dir, file_name) #f'{root_dir}/{file_name}'
            if self.process_handler:
                self.process_handler(current_file_path)
            current_file_md5 = self.file_md5(file_path=current_file_path)
            try:
                file_list = self.file_md5_dict[current_file_md5]
                file_list.append(current_file_path)
                self.file_md5_dict[current_file_md5] = file_list
            except KeyError:
                self.file_md5_dict[current_file_md5] = [current_file_path]
        if dir_names:
            for dir_name in dir_names:
                current_sub_path = os.path.join(root_dir, dir_name) #f'{root_dir}/{dir_name}'
                self.check_have_same_file(dir_path=current_sub_path)

    def same_md5_file_dict(self) -> dict:
        same_file_dict = { k: v for (k, v) in self.file_md5_dict.items() if len(v) > 1 }
        return same_file_dict

    def file_md5(self, file_path: str) -> str:
        hash = md5()
        file = open(file=file_path, mode='rb')
        hash.update(file.read())
        file.close()
        md5_hash_str = hash.hexdigest()
        return md5_hash_str

def main():
    file_filter = SameFileFilter()
    file_filter.find_same_file(dir_path=get_root_path())
    print(file_filter.same_md5_file_dict())

if __name__ == "__main__":
    main()
# end main
