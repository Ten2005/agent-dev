import os
import json
from pathlib import Path
from typing import Any, Optional


class DataHandler:
    def __init__(self, base_folder: Optional[str] = None):
        if base_folder is None:
            base_folder = os.path.join(
                os.path.dirname(__file__), "..", "documents", "sample"
            )
        self.folder_path = Path(base_folder).resolve()
        self.folder_path.mkdir(parents=True, exist_ok=True)

    def load(self, file_name: str, format: str = "str") -> Any:
        file_path = self.folder_path / file_name
        try:
            with open(file_path, "r") as f:
                return json.load(f) if format == "json" else f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")

    def save(self, data: Any, file_name: str, format: str = "str") -> None:
        file_path = self.folder_path / file_name
        try:
            with open(file_path, "w") as f:
                if format == "json":
                    json.dump(data, f, indent=2)
                else:
                    f.write(data)
        except Exception as e:
            raise IOError(f"Failed to save {file_path}: {e}")
