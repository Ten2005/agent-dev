import typer
import sys
import json
from typing import Optional
from utils.data_handler import DataHandler

app = typer.Typer()


@app.command("read")
def read(file_name: str, format: str = "str", folder: Optional[str] = None):
    """Read data from file."""
    handler = DataHandler(base_folder=folder)
    data = handler.load(file_name, format=format)
    print(data)


@app.command("write")
def write(
    file_name: str,
    data: Optional[str] = None,
    format: str = "str",
    folder: Optional[str] = None,
):
    """Write data to file."""
    handler = DataHandler(base_folder=folder)
    content = data or sys.stdin.read()
    if format == "json":
        content = json.loads(content)
    handler.save(content, file_name, format=format)
    print(f"Saved to {file_name}")
