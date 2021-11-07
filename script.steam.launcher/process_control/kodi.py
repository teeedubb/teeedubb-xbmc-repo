from subprocess import check_output
from re import search
from re import IGNORECASE


class Kodi:

    def __init__(self):
        self.__bin_pattern = r'(kodi)(\.bin|-x11|-wayland|-gbm)[_v7|_v8]*'
        self.__bin_name = self.get_bin_name()
        self.__pid = self.__get_pid()

    def get_bin_name(self):
        running_process_names = check_output(['ps', '-eo', 'comm='])
        return search(self.__bin_pattern, running_process_names, IGNORECASE).group()

    def __get_pid(self):
        unformatted_pid = check_output(['ps', '-C', self.__bin_name, '-o', 'pid='])
        formatted_pid = int(unformatted_pid)
        return formatted_pid
