from termcolor import colored

from .snapshot import Snapshot
from .snapshot_file import from_canvas_file
from .snapshot_link import SnapshotLink
from ..request_batcher import RequestBatcher
from canvasapi.exceptions import ResourceDoesNotExist
from ..utils import normalize_path, file_regex

class CanvasFileSnapshot(Snapshot):
    """Takes a snapshot of files on Canvas, organized by file tab.

    ``CanvasFileSnapshot`` generates a snapshot of files on Canvas. In this snapshot mode,
    all files under "File" tab will be scanned as-is. Besides, it will add pages into
    the snapshot at `pages/xxx` path, if `with_link` option is enabled.
    """

    def __init__(self, course, with_link=False):
        """Create a file-based Canvas snapshot-taker

        Args:
            course (canvasapi.course.Course): The course object
            with_link (bool, optional): If true, pages will be included in snapshot. Defaults to False.
        """
        self.course = course
        self.with_link = with_link
        self.snapshot = {}

    def add_to_snapshot(self, key, value):
        """Add a key-value pair into snapshot. If duplicated, this function will report error and ignore the pair.

        Args:
            key (str): key or path of the object
            value (any): content of the object
        """
        if key in self.snapshot:
            print(colored(
                f'  Duplicated file found: {key}, please download it using web browser.', 'yellow'))
            return
        self.snapshot[key] = value

    def take_snapshot(self):
        """Take a snapshot

        Raises:
            ResourceDoesNotExist: this exception will be raised if file tab is not available

        Returns:
            dict: snapshot of Canvas in `SnapshotFile` or `SnapshotLink` type.
        """
        for _ in self.yield_take_snapshot():
            pass
        return self.get_snapshot()

    def yield_take_snapshot(self):
        course = self.course
        request_batcher = RequestBatcher(course)

        yield (0, '请稍候', '正在获取文件列表')
        files = request_batcher.get_files()
        if files is None:
            raise ResourceDoesNotExist("File tab is not supported.")

        folders = request_batcher.get_folders()

        for _, file in files.items():
            folder = normalize_path(folders[file.folder_id].full_name) + "/"
            if "unfiled" in folder:
                pass
            else:
                if folder.startswith("course files/"):
                    folder = folder[len("course files/"):]
                snapshot_file = from_canvas_file(file)
                filename = f'{folder}{normalize_path(snapshot_file.name, file_regex)}'
                self.add_to_snapshot(filename, snapshot_file)

        print(f'  {len(files)} files in total')
        yield (0.1, None, f'共 {len(files)} 个文件')

        if self.with_link:
            yield (None, '正在解析链接', None)
            pages = request_batcher.get_pages() or []
            for page in pages:
                key = f'pages/{normalize_path(page.title, file_regex)}.html'
                value = SnapshotLink(
                    page.title, page.html_url, "Page")
                self.add_to_snapshot(key, value)
            print(f'  {len(pages)} pages in total')
            yield (0.2, '请稍候', f'共 {len(pages)} 个链接')

    def get_snapshot(self):
        """Get the previously-taken snapshot

        Returns:
            dict: snapshot of Canvas
        """
        return self.snapshot
