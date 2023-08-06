import datetime
import os
import shutil


class SourceWrapper:
    source = None

    def __init__(self, source, **kwargs):
        pass

    def get_date_info(self, filename):
        raise NotImplementedError()

    def get_file_list(self):
        raise NotImplementedError()

    def open(self, filename):
        raise NotImplementedError()


class DirectoryWrapper(SourceWrapper):
    is_temporary = False

    def __init__(self, source, is_temporary=False, **kwargs):
        super().__init__(source=source, **kwargs)
        self.is_temporary = is_temporary
        self.source = os.path.abspath(source)

    def get_date_info(self, filename):
        st = os.stat(os.path.join(self.source, filename))
        return datetime.datetime.fromtimestamp(st.st_mtime)

    def get_file_list(self):
        file_list = []

        for path, _, files in os.walk(self.source):
            for name in files:
                if not name.startswith('.'):
                    file_list.append(os.path.join(self.source, name))

        return file_list

    def get_full_path(self, filename):
        return os.path.join(self.source, filename)

    def open(self, filename):
        return open(self.get_full_path(filename), 'rb')

    def __del__(self):
        if self.is_temporary:
            shutil.rmtree(self.source, ignore_errors=True)


class LocalArchiveWrapper(SourceWrapper):

    def __init__(self, source, **kwargs):
        super().__init__(source=source, **kwargs)
        self.source = source

    def get_date_info(self, filename):
        date_str = filename.split('_')[-2]
        return datetime.datetime.strptime(date_str, '%Y%m%d').date()

    def get_file_list(self):
        return self.source.namelist()

    def open(self, filename):
        return self.source.open(filename)
