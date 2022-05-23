from inotify_simple import INotify, flags

class DirWatcher():

    def __init__(self, directory, flags):
        self.directory = directory
        self.flags = flags
        self.watch = None
        self.inotify = None

    def __enter__(self):
        self.inotify = INotify()
        self.watch = self.inotify.add_watch(self.directory, self.flags)
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.inotify.rm_watch(self.watch)
        except:
            pass

    def next(self, timeout=None):
        for event in self.inotify.read(timeout=timeout):
            yield event