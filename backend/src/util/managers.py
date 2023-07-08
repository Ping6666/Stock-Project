from typing import List, Dict
from datetime import datetime, timedelta
from multiprocessing import Process, Lock
from multiprocessing.synchronize import Lock as l_class

import pathlib
import hashlib

import pandas as pd

import util.crawler as crawler

# ---------- class ---------- #


class TimeManager():

    def __init__(self):
        self.past_days = 2
        return

    def get_datetime(self, timedelta_days: int = 0):

        _datetime = {}
        try:
            curr_datetime = datetime.now() - timedelta(days=timedelta_days)

            _date = curr_datetime.strftime('%y%m%d')
            _time = curr_datetime.strftime('%H%M%S')
            _weekday = curr_datetime.weekday()

            is_weekday = True
            if _weekday == 5 or _weekday == 6:
                is_weekday = False

            _datetime = {
                'date': _date,
                'time': _time,
                'weekday': _weekday,
                'is_weekday': is_weekday,
            }

        except Exception as e:
            print(e)

        return _datetime

    def get_past_days(self) -> List[Dict]:
        _datetimes = []

        _days = 0
        while True:
            _datetime = self.get_datetime(timedelta_days=_days)

            is_weekday = _datetime.get('is_weekday')
            if is_weekday is not None and is_weekday:
                _datetimes.append(_datetime)

            _days += 1
            if len(_datetimes) >= self.past_days:
                break

        return _datetimes

    def get_parsed_days(self, _days: List[Dict], param: str = None):

        parsed_days = []

        if _days is None:
            return parsed_days

        for _day in _days:
            if _day is None:
                continue

            if param is not None:
                __day = _day.get(str(param))

                if __day is not None:
                    parsed_days.append(__day)

            else:
                parsed_days.append(_day)

        return parsed_days


class FileManager():

    # ---------- public ---------- #

    def get_files(self,
                  _path: pathlib.Path,
                  is_file: bool = True,
                  is_dir: bool = False,
                  only_name: bool = True,
                  recursive: bool = False):
        """
        to get files under some path

        Args:
            _path: the path need to list files
            only_name: return only the name of the file
            recursive: also return files under the sub folder
        
        Return:
            a list of files

        """

        print('\nFileManager.get_files')

        status = True
        files = set()  # []

        try:
            _path = pathlib.Path(_path)

            for p_iter in _path.iterdir():

                if ((is_dir and p_iter.is_dir())
                        or (is_file and p_iter.is_file())):
                    _p_iter = p_iter.resolve()  # file full path

                    if only_name:
                        _filename = _p_iter.name  # file name
                    else:
                        _filename = str(_p_iter)

                    files.add(_filename)

                elif recursive:  # is_dir
                    _status, _files = self.get_files(p_iter,
                                                     is_file=is_file,
                                                     is_dir=is_dir,
                                                     only_name=only_name,
                                                     recursive=recursive)
                    # TODO concat current base path

                    if _status:
                        files.update(_files)

        except Exception as e:
            status = False
            print(e)

        files = list(files)
        print(files)

        return status, files

    def get_path_is(self,
                    _path: pathlib.Path,
                    mode: str = 'is_file',
                    _folder: pathlib.Path = None):
        """

        to get the path of obj. is a dir. or a file and in the _folder if given

        Args:
            _path: the path need to check
            mode: the path obj. check mode 'is_file' or 'is_dir'
            _folder: if given will also check if the _path is under the _folder

        Return:
            a tuple of str. (_is, _suffix)

            _is: is a dir. or a file dep. on mode and True if exist, vice versa
            _suffix: the suffix of the _path

        """

        print('\nFileManager.get_path_is')

        try:
            # --- check is file (file exist) --- #

            p_file = pathlib.Path(_path)
            p_file = p_file.resolve()

            p_folder = None
            if _folder is not None:
                p_folder = pathlib.Path(_folder)
                p_folder = p_folder.resolve()

            print('p_file', p_file)
            print('p_folder', p_folder)

            # --- p_file is --- #

            _is = False
            if mode == 'is_file':
                _is = p_file.is_file()
            elif mode == 'is_dir':
                _is = p_file.is_dir()
            else:
                raise ValueError

            # --- p_file in p_folder --- #

            if p_folder is not None and p_folder not in p_file.parents:
                _is = False

            # --- suffix --- #

            _suffix = None
            if _is:
                _suffix = p_file.suffix

            print('is', _is)
            print('suffix', _suffix)

            return _is, _suffix

        except Exception as e:
            print(e)

        return False, None

    def make_dir(self, _path: pathlib.Path):
        p_path = pathlib.Path(_path)
        p_path.mkdir(parents=True, exist_ok=True)
        return

    def del_dir(self, _path: pathlib.Path, _folder: pathlib.Path = None):
        del_files = []

        try:

            p = pathlib.Path(_path)

            _is, _ = self.get_path_is(_path, 'is_dir', _folder)
            if not _is:
                return

            for p_iter in p.iterdir():

                if p_iter.is_file():
                    p_iter.unlink()
                    del_files.append(p_iter)
                else:
                    # no need to check under _folder again
                    del_files += self.del_dir(p_iter)

            p.rmdir()

        except Exception as e:
            print(e)

        return del_files


class FileHashManager():
    """
    manage the hash of the files

    file_hash_table:
        a dict that can turn file name into file's md5sum

    """

    check_hash: bool
    file_hash_table: Dict

    def __init__(self):
        self.fm = FileManager()

        self.check_hash = False
        self.file_hash_table = {}

        # TODO
        # remove from dict that the file does not exist on the

        return

    # ---------- private ---------- #

    def _get_hash(self, _filename: str, chunk_size: int = 4096):
        """
        get file md5sum

            Return:
                the file's md5sum
        """

        h = ""

        try:
            m = hashlib.md5()

            with open(_filename, "rb") as f:
                # speed up with chunk
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    m.update(chunk)

            h = m.hexdigest()

        except:
            print('\nFileHashManager._get_hash')
            print(f'ERROR on file {_filename}')

        return h

    # ---------- public ---------- #

    def set_check_hash(self, _set: bool = False):
        self.check_hash = _set
        return

    def check_file(self, _filename: str):
        """
        check if the file exists and was the same as the last check
            if the file exist, do check if in the file_hash_table
                if not, do md5sum
                if do, check if the md5sum was the same

            Return:
                True: if the file is the same
                False: vice versa

        """

        _filename = str(_filename)
        print(f'\nFileHashManager.check_file | {_filename}', end=' ')

        if self.check_hash:
            # check is file (file exist)
            _is_file, _ = self.fm.get_path_is(_filename)

            if _is_file:
                # get hash of the file
                hash_value = self._get_hash(_filename)

                last_hash_value = self.file_hash_table.get(_filename)
                if ((last_hash_value is not None)
                        and (last_hash_value == hash_value)):

                    # is the same
                    print('IDENTICAL')

                    return True
                else:
                    # not exist or not the same do update the file_hash_table
                    print('DISTINCT')

                    self.file_hash_table[_filename] = hash_value
            else:
                print('MISSING')
        else:
            print('PASS')

        return False


class FileProtector():
    """
    use locks to protect the file atomicity / consistency while creating files and avoid race condition

        use when
            1. on write
            2. file that check with check_file()

    """

    lock_table: Dict[str, l_class]

    def __init__(self):
        self.lock_table = {}
        return

    def get_lock(self, _name: str):
        """
        get lock from given name
            the name usually stand for a file name (absolute)

        """

        print('\nFileProtector.get_lock')

        l = None
        try:
            p = pathlib.Path(_name)
            resolved_name = p.resolve()
            print(f'getting lock {resolved_name}')

            l = self.lock_table.get(resolved_name)

            if l is None:
                l = Lock()
                self.lock_table[resolved_name] = l
        except:
            print(f'fail to get_lock {_name}')

        return l

    def remove_lock(self, _name: str):
        # need to guarantee that the lock has been released before calling this fn
        # if anyone hold the lock and waiting for acquire
        # it is ok that they can hold it and the lock was being removing from the dict
        # dict will be guarded from the is_file so that lock as well

        try:
            p = pathlib.Path(_name)
            resolved_name = p.resolve()

            l = self.lock_table.get(resolved_name)

            if l is not None:
                _str = f"FileProtector.remove_lock | removing lock {resolved_name}"
                print(_str)
                del self.lock_table[resolved_name]

        except Exception as e:
            print('FileProtector.remove_lock', e)

        return

    def acquire_locks(self, locks: List[l_class]):

        for l in locks:
            # WARNING potential deadlock may occur
            # BUT given proper order of the locks may not get into deadlock

            if l is not None:
                l.acquire()

        return

    def release_locks(self, locks: List[l_class]):

        for l in locks:

            if l is not None:
                l.release()

        return


class StorageManager():

    def __init__(self):
        self.tm = TimeManager()
        self.fm = FileManager()
        self.fp = FileProtector()

        self._make_dir_workhouse()
        return

    # ---------- private ---------- #

    def _make_dir_workhouse(self):
        self.fm.make_dir('./symbols')
        self.fm.make_dir('./data')
        return

    def _purge_dirs(self, check_dir: pathlib.Path):
        """
        a watcher that watch the file sys.
        if some dir is out-of-date then purge them

        """

        try:

            # --- all_days --- #

            _, _dirs = self.fm.get_files(check_dir, is_file=False, is_dir=True)
            all_days = set(_dirs)

            _days = self.tm.get_past_days()

            # --- stay_days --- #

            stay_days = set(self.tm.get_parsed_days(_days, 'date'))
            del_days = all_days.difference(stay_days)

            print('all_days', all_days)
            print('stay_days', stay_days)
            print('del_days', del_days)

            del_files = []
            for del_day in del_days:
                del_files = self.fm.del_dir(f'{check_dir}/{del_day}')

            for _file in del_files:
                self.fp.remove_lock(_file)

        except Exception as e:
            print(e)

        return

    def _download_helper(self,
                         symbol,
                         save_path: str,
                         _overwrite: bool = False):

        try:
            l1 = self.fp.get_lock(save_path)

            locks = [l1]
            self.fp.acquire_locks(locks)

            _is, _ = self.fm.get_path_is(save_path)

            if _overwrite or not _is:
                crawler.download_yahoo_finance(symbol, save_path)

            self.fp.release_locks(locks)
        except Exception as e:
            print(e)

        return

    def _crawl_helper(self,
                      _filename: str,
                      base_path: str,
                      _overwrite: bool = False):
        ps: List[Process]

        try:

            symbols = crawler.file_reader(_filename)
            parsed_symbols = crawler.symbol_parser(symbols)

            # parsed_symbols = parsed_symbols[:2]
            print(parsed_symbols)

            ps = []
            for symbol in parsed_symbols:
                save_path = f'{base_path}/{symbol}.csv'

                p = Process(target=self._download_helper,
                            args=(symbol, save_path, _overwrite))
                ps.append(p)
                p.start()

            for p in ps:
                p.join(10)

        except Exception as e:
            print(e)

        return

    def _result_helper(self, base_path: str):
        try:
            _, _files = self.fm.get_files(base_path, only_name=False)
            __files = [_file for _file in _files if 'result' not in _file]

            result_path = f'{base_path}/^^result.csv'

            locks = [self.fp.get_lock(_file) for _file in __files]
            locks.append(self.fp.get_lock(result_path))

            self.fp.acquire_locks(locks)

            crawler.postprocess(__files, result_path)

            self.fp.release_locks(locks)

        except Exception as e:
            print(e)

        return

    # ---------- public ---------- #

    ## --- get item --- ##

    def get_file(self, filename: str):
        """
        get a file

        Return
            a Tuple (status, _file)

            status: if a file is not exist or not under the _folder return False, vice versa.

        """

        status = True
        _file = None

        _folder = '.'  # folder that is '.' = '.../backend/'
        _is, _suffix = self.fm.get_path_is(filename, _folder=_folder)

        if not _is:
            status = False
            return status, _file

        try:
            _ctx, _mimetype = None, None
            with open(filename, 'rb') as f:
                _ctx = f.read()

                if _suffix == '.txt':
                    _mimetype = "text/plain"
                elif _suffix == '.csv':
                    _mimetype = "text/csv"

            _file = _ctx, _mimetype

            if _ctx is None or _mimetype is None:
                status = False

        except:
            status = False

        return status, _file

    def get_csv(self, date_path: str, csv_path: str):
        status = True
        _file = None

        try:
            _folder = f'./data/{date_path}'
            curr_path = f'./data/{date_path}/{csv_path}'

            _is, _ = self.fm.get_path_is(curr_path, _folder=_folder)

            if _is:
                df = pd.read_csv(curr_path)
                _file = df.to_dict('records')
                # _file = df.to_json()

        except:
            status = False

        return status, _file

    ## --- get folders --- ##

    def get_dates(self):
        self._purge_dirs('./data')
        return self.fm.get_files('./data', is_file=False, is_dir=True)

    def get_symbols(self):
        return self.fm.get_files('./symbols')

    ## --- get items --- ##

    def get_date(self, _path: pathlib.Path):

        curr_path = f'./data/{_path}'

        _is, _ = self.fm.get_path_is(curr_path, 'is_dir', './data')

        if _is:
            return self.fm.get_files(curr_path)

        return False, []

    def get_symbol(self,
                   _path: pathlib.Path,
                   _download: bool = False,
                   _overwrite: bool = False):
        self._purge_dirs('./data')

        curr_path = f'./symbols/{_path}'
        status, _file = self.get_file(curr_path)

        if _download and status:

            _days = self.tm.get_past_days()
            parsed_days = self.tm.get_parsed_days(_days, 'date')
            curr_day = parsed_days[0]

            save_path = f'./data/{curr_day}'

            self.fm.make_dir('./data/')
            self.fm.make_dir(save_path)

            self._crawl_helper(curr_path, save_path, _overwrite)
            self._result_helper(save_path)

        return status, _file
