from _app import app, app_config, Detail
import pathlib
import shutil
import base64
import hashlib
import os


class RemotePath(Detail):
    path: str = None
    size: int = None
    modified_timestamp: float = None
    created_timestamp: float = None
    is_dir: bool = None
    is_file: bool = None


def create_remote_path(p: pathlib.Path):
    if p.exists():
        remote_path = RemotePath()
        s = os.stat(p)
        remote_path.path = str(p.relative_to(app_config.data_root_dir))
        remote_path.size = s.st_size
        remote_path.modified_timestamp = s.st_mtime
        if hasattr(s, "st_birthtime"):
            remote_path.created_timestamp = s.st_birthtime
        else:
            remote_path.created_timestamp = s.st_ctime
        remote_path.is_dir = p.is_dir()
        remote_path.is_file = p.is_file()
        return remote_path
    else:
        return None


class Listdir(Detail):
    parent: str
    recursive: bool = False
    parent_folder: RemotePath = None
    folders: list[RemotePath] = None
    files: list[RemotePath] = None


@app.post("/explorer/listdir", tags=["explorer"], response_model=Listdir)
async def listdir(args: Listdir):
    """
    列出目录的所有子项
    """
    parent = app_config.data_root_dir / args.parent

    args.parent_folder = create_remote_path(parent)
    args.folders = []
    args.files = []

    if not app_config.is_valid_path(parent):
        return args.set(False, "路径不合规")
    if not parent.exists():
        return args.set(False, "路径不存在")
    if not parent.is_dir():
        return args.set(False, "路径不是目录")

    if args.recursive:
        for dir_path, dir_names, file_names in os.walk(parent):
            for name in (dir_names + file_names):
                path = pathlib.Path(dir_path) / name
                if path.samefile(parent):
                    continue
                path = create_remote_path(path)
                if path.is_dir:
                    args.folders.append(path)
                elif path.is_file:
                    args.files.append(path)
    else:
        for name in os.listdir(parent):
            path = create_remote_path(parent / name)
            if path.is_dir:
                args.folders.append(path)
            elif path.is_file:
                args.files.append(path)
    return args


class Makedir(Detail):
    path: str
    recursive: bool = True
    exists: bool = False


@app.post("/explorer/makedir", tags=["explorer"], response_model=Makedir)
async def makedir(args: Makedir):
    """
    创建目录
    """
    path = pathlib.Path(app_config.data_root_dir) / args.path
    if not app_config.is_valid_path(path):
        return args.set(False, "路径不合规")

    if path.exists():
        args.exists = True
        return args.set(True, "路径已存在")

    if args.recursive:
        os.makedirs(path)
    else:
        os.mkdir(path)
    args.exists = False
    return args.set(True, "创建目录成功")


class Rename(Detail):
    path: str
    new_path: str


@app.post("/explorer/rename", tags=["explorer"], response_model=Rename)
async def rename(args: Rename):
    """
    重命名
    """
    new_path = pathlib.Path(app_config.data_root_dir) / args.new_path
    if not app_config.is_valid_path(new_path):
        return args.set(False, "路径不合规")

    path = pathlib.Path(app_config.data_root_dir) / args.path
    if not app_config.is_valid_path(path):
        return args.set(False, "路径不合规")

    path.rename(new_path)
    return args.set(True, "重命名成功")


class Remove(Detail):
    path: str
    recursive: bool = False


@app.post("/explorer/remove", tags=["explorer"], response_model=Remove)
async def remove(args: Remove):
    """
    移除
    """
    path = pathlib.Path(app_config.data_root_dir) / args.path
    if not app_config.is_valid_path(path):
        return args.set(False, "路径不合规")

    if not path.exists():
        return args.set(False, "路径不存在")

    if args.recursive:
        shutil.rmtree(path)
    else:
        if path.is_dir() and len(os.listdir(path)) > 0:
            return args.set(False, "不能删除非空文件夹")
        path.rmdir() if path.is_dir() else path.unlink()
    return args.set(True, "移除成功")


class MatchFile(Detail):
    path: str
    sha1: str = None
    remove_if_not_matched = False
    matched: bool = False
    matched_file_if_exists: RemotePath = None


@app.post("/explorer/match_file", tags=["explorer"], response_model=MatchFile)
async def match_file(args: MatchFile):
    """
    检查文件匹配
    """
    path = app_config.data_root_dir / args.path
    if not app_config.is_valid_path(path):
        return args.set(False, "路径不合规")

    if path.exists():
        if path.is_file():
            args.matched_file_if_exists = create_remote_path(path)
            if args.sha1 is not None:
                sha1 = hashlib.sha1()
                sha1.update(path.read_bytes())
                sha1 = sha1.hexdigest()
                if args.sha1.lower() == sha1.lower():
                    args.matched = True
                    return args.set(True, "文件已存在")
                elif args.remove_if_not_matched:
                    path.unlink()
        elif args.remove_if_not_matched:
            shutil.rmtree(path)

    args.matched = False
    return args.set(True, "文件不存在")


class UploadFileChunk(Detail):
    path: str
    offset: int
    content: str


@app.post("/explorer/upload_file_chunk", tags=["explorer"], response_model=UploadFileChunk)
async def upload_file_chunk(args: UploadFileChunk):
    """
    上传文件块
    """
    path = app_config.data_root_dir / args.path
    if not app_config.is_valid_path(path):
        return args.set(False, "路径不合规")

    content = base64.b64decode(args.content)
    args.content = ""

    if not path.parent.exists():
        os.makedirs(path.parent)
    path.touch()

    with path.open("r+b") as file:
        file.seek(args.offset)
        file.write(content)
    return args.set(True, "上传文件块成功")


class DownloadFileChunk(Detail):
    path: str
    offset: int
    size: int
    content: str = None


@app.post("/explorer/download_file_chunk", tags=["explorer"], response_model=DownloadFileChunk)
async def download_file_chunk(args: DownloadFileChunk):
    """
    下载文件块
    """
    path = app_config.data_root_dir / args.path
    if not app_config.is_valid_path(path):
        return args.set(False, "路径不合规")

    if not path.parent.exists():
        return args.set(False, "文件不存在")

    with path.open("r+b") as file:
        file.seek(args.offset)
        args.content = file.read(args.size)

    args.content = base64.b64encode(args.content)
    return args.set(True, "下载文件块成功")
