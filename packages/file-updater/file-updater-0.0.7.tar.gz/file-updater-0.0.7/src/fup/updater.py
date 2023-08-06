import os
import win32com.client
import shutil
from datetime import datetime
from .progress_bar import *
import sys
import re

from colorama import init
init()
from colorama import Fore, Back, Style

class FileUpdater: 
    def __init__(self, output_console=True, fup_file_path=None):
        self.output_console = output_console
        self.fup_file_path = fup_file_path

    def __read_fup_file(self, path):
        filename = path.split('\\')[-1]
        if(filename != '.fupignore.txt' and filename != '.fupinclude.txt'):
            raise ValueError('No fup file found')
        self.isIgnoreFile = filename == '.fupignore.txt'
        self.general_ignores = []
        self.specific_ignores = []
        self.general_includes = []
        self.specific_includes = []
        try:
            f = open(path, 'r')
            content = f.read()
        except Exception:
            raise IOError('Could not read fup file')
        lines = content.split('\n')
        file_ext_pattern = re.compile('^\*\.\w+$')
        rel_path_pattern = re.compile('^\!\w+(\\\w+)*(\.\w+)?$')
        for line in lines:
            if(len(line) == 0):
                continue
            if(file_ext_pattern.fullmatch(line)):
                file_ext = line.split('.')[-1]
                self.general_ignores.append(file_ext) if(self.isIgnoreFile) else self.general_includes.append(file_ext)
            elif(rel_path_pattern.fullmatch(line)):
                full_path = fr'{self.start_path_source}\{line[1:]}'
                self.specific_ignores.append(full_path) if(self.isIgnoreFile) else self.specific_includes.append(full_path)
            else:
                self.specific_ignores.append(line) if(self.isIgnoreFile) else self.specific_includes.append(line)

    def __should_ignore(self, path):
        if(os.path.isfile(path)):
            file_ext = path.split('.')[-1]
            if(file_ext in self.general_ignores):
                return True
        return path in self.specific_ignores

    def __should_include(self, path):
        if(os.path.isfile(path)):
            file_ext = path.split('.')[-1]
            if(file_ext in self.general_includes):
                return True
        for specific_include in self.specific_includes:
            if(path.startswith(specific_include + '\\')):
                return True
        return path in self.specific_includes

    def __get_num_files(self, path):
        num_files = 0
        for base, dirs, files in os.walk(path):
            num_files += len(dirs) + len(files);
        return num_files

    def __modified_date_file(self, path, file_name):
        sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
        ns = sh.NameSpace(path)

        item = ns.ParseName(str(file_name))
        last_modified = ns.GetDetailsOf(item, 3) # 3 --> last modified
        return datetime.strptime(last_modified, '%d.%m.%Y %H:%M')

    def __replace_file_if_newer(self, path_source, path_dest, file_name):
        source_last_modified = self.__modified_date_file(path_source, file_name)
        dest_last_modified = self.__modified_date_file(path_dest, file_name)

        if(source_last_modified > dest_last_modified):
            full_path_source = fr"{path_source}\{file_name}"
            full_path_dest = fr"{path_dest}\{file_name}"
            os.remove(full_path_dest)
            shutil.copy2(full_path_source, full_path_dest)
            self.progressbar.print_progress(self.iteration, f'{Fore.MAGENTA}Updated {Fore.CYAN}{file_name} {Fore.MAGENTA}in{Style.RESET_ALL} {path_dest}')

    def __update_files_rec(self, path_source, path_dest, sub_path):
        for file_name in os.listdir(path_source):
            if(sub_path is None):
                full_sub_path = file_name
            else:
                full_sub_path = fr"{sub_path}\{file_name}"
            full_path_source = fr"{path_source}\{file_name}"
            full_path_dest = fr"{path_dest}\{file_name}"
            if(self.fup_file_path is not None):
                if(self.isIgnoreFile):
                    if(self.__should_ignore(full_path_source)):
                        if(os.path.isdir(full_path_source)):
                            self.iteration += self.__get_num_files(full_path_source) + 1
                        else:
                            self.iteration += 1
                        self.progressbar.print_progress(self.iteration)
                        continue
                else:
                    if(not self.__should_include(full_path_source)):
                        if(os.path.isdir(full_path_source)):
                            self.iteration += self.__get_num_files(full_path_source) + 1
                        else:
                            self.iteration += 1
                        self.progressbar.print_progress(self.iteration)
                        continue
            if(os.path.isfile(full_path_source)):
                if(not os.path.exists(full_path_dest)):
                    shutil.copy2(full_path_source, full_path_dest)
                    self.progressbar.print_progress(self.iteration, f'{Fore.GREEN}Copied {Fore.CYAN}{file_name} {Fore.GREEN}to{Style.RESET_ALL} {path_dest}')
                else:
                    self.__replace_file_if_newer(path_source, path_dest, file_name)

            else:
                next_source_path = fr"{path_source}\{file_name}"
                next_dest_path = fr"{path_dest}\{file_name}"
                if(not os.path.exists(next_dest_path)):
                    os.mkdir(next_dest_path)
                    self.progressbar.print_progress(self.iteration, f'{Fore.GREEN}Created folder {Fore.CYAN}{file_name}{Style.RESET_ALL}')
                self.__update_files_rec(next_source_path, next_dest_path, full_sub_path)
            self.iteration += 1
            self.progressbar.print_progress(self.iteration)

    def update_files(self, path_source, path_dest):
        self.start_path_source = path_source
        if(self.fup_file_path is not None):
            self.__read_fup_file(self.fup_file_path)   
        self.num_files = self.__get_num_files(path_source)
        self.progressbar = Progressbar(self.num_files, 50, 'Progress', 'Complete', 2, self.output_console)
        self.iteration = 0

        self.__update_files_rec(path_source, path_dest, None)
        
    

    