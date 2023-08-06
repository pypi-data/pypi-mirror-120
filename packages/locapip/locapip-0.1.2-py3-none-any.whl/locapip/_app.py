from locapip import name, __version__ as version
import fastapi
import pydantic
import pathlib
import os


class AppConfig:
    def __init__(self):
        self.name = name
        self.version = version
        self.data_root_dir: pathlib.Path = pathlib.Path()
        self.host: str = "127.0.0.1"
        self.port: int = 6547

        readme = pathlib.Path(os.path.dirname(__file__)) / "README.md"
        with open(readme, "r", encoding="UTF-8") as f:
            self.description = f.read()

    def is_valid_path(self, path):
        return str(self.data_root_dir.resolve()) in str(path.resolve())


app_config = AppConfig()

app = fastapi.FastAPI(
    title=app_config.name,
    version=app_config.version,
    description=app_config.description,
    contact={
        "name": "洛卡皮迪奥",
        "url": "https://locapidio.com/",
        "email": "88172828@qq.com",
    },
    license_info={
        "name": "GPLv3+",
        "url": "https://jxself.org/translations/gpl-3.zh.shtml/",
    },
    openapi_tags=[
        {"name": "base", "description": "有关服务的基础方法"},
        {"name": "explorer", "description": "场景数据资源管理"},
    ]
)


class Detail(pydantic.BaseModel):
    completed: bool = True
    detail: str = ""

    def set(self, completed: bool, detail: str):
        self.completed = completed
        self.detail = detail
        return self


@app.get("/base/connect", tags=["base"], response_model=Detail)
async def base_connect():
    """
    测试连接
    """
    return Detail().set(True, "连接成功")
