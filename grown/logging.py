"""
rudimentary monkey_patch till module has fileio write
"""
import ulogging
from grown.store import storage
import os
import gc


def _reduce_logging(store_dict, data):
    store_dict.update(data)
    return store_dict


storage.register_leaf(
    'logging', {
        'level': "ERROR",
        'max_logsize': 4096,
    },
    _reduce_logging
)

get_logging = storage.get_leaf('logging')


ulogging.basicConfig(
    getattr(ulogging, get_logging.get('level'), 'ERROR')
)


def _trim_log(file_name):
    """
    if log is over the maximum we trim 10% old logs
    """
    max_log_size = storage.get_leaf('logging').get('max_logsize', 4096)
    file_size_in_bytes = os.stat(file_name)[6]
    if file_size_in_bytes <= max_log_size:
        return
    # trim log
    os.rename(file_name, "temp.log")
    file_ptr = open("temp.log", "r")
    trim_size = int(max_log_size*0.1)
    sum_trimmed = 0
    while True:
        size = len(file_ptr.readline())
        sum_trimmed += size
        gc.collect()
        if sum_trimmed >= trim_size or size == 0:
            break

    new_file_ptr = open(file_name, "a")
    while True:
        read = file_ptr.readline()
        if read == "":
            break
        else:
            new_file_ptr.write(read)
        gc.collect()

    new_file_ptr.close()
    file_ptr.close()
    os.remove("temp.log")


def log(self, level, msg, *args):
    # there were an error 28 comming from line 9
    # so write to file also micropython filesys looks not prety anymore
    # 11 blocks free i guess system had no space left anymore
    # need to make it configurable logsize last 100 messages?
    _log_file = open('run_information.log', 'a')
    _log_file.write("%s:%s: %s \n" % (self._level_str(level), self.name, msg))
    _log_file.close()
    _trim_log('run_information.log')

    if level >= (self.level or ulogging._level):
        ulogging._stream.write("%s:%s:" % (self._level_str(level), self.name))
        if not args:
            print(msg, file=ulogging._stream)
        else:
            print(msg % args, file=ulogging._stream)


ulogging.Logger.log = log
grown_log = ulogging.getLogger("grown")
