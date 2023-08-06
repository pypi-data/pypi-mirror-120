import click
import uvicorn
import pathlib
import os


@click.command()
@click.argument("data_root_dir", type=click.Path(file_okay=False, dir_okay=True, path_type=pathlib.Path))
@click.option("--host", type=click.STRING, default="127.0.0.1", show_default=True)
@click.option("--port", type=click.IntRange(1024, 49151), default=6547, show_default=True)
def main(data_root_dir: pathlib.Path, host: str, port: int):
    if not data_root_dir.exists():
        os.makedirs(data_root_dir)

    from _app import app, app_config
    app_config.data_root_dir = data_root_dir.resolve()
    app_config.host = host
    app_config.port = port

    print(f"{app_config.name} {app_config.version}\n"
          f"root: {data_root_dir}\n"
          f"info: http://{host}:{port}/redoc or http://{host}:{port}/docs")

    import _explorer
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
