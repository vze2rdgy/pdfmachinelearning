from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class FileMonitor(FileSystemEventHandler):
    """Monitor changes in the drop directory"""
    __slots__ = [
        '_observer',
        '_q'
        ]

    def __init__(self, dropLocation, q):
        self._q = q
        self._observer = Observer()
        self._observer.schedule(self, dropLocation, recursive=True)
        self._observer.start()
        return 

    def Stop(self):
        self._observer.unschedule_all()
        self._observer.stop()
        self._observer.join()
        return

    def on_created(self, event):
        """Called when a file or directory is created.

        :param event:
            Event representing file/directory creation.
        :type event:
            :class:`DirCreatedEvent` or :class:`FileCreatedEvent`
        """
        # check for event.src_path property and event.is_directory
        self._q.put(event.src_path)
        return
