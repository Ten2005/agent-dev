import pytest
import tempfile
from pathlib import Path
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_handler import DataHandler


class TestDataHandlerInit:
    """DataHandlerの初期化テスト"""

    def test_init_with_default_path(self):
        """デフォルトパスで初期化"""
        handler = DataHandler()
        assert handler.folder_path is not None
        assert "documents/sample" in str(
            handler.folder_path
        ) or "documents\\sample" in str(handler.folder_path)

    def test_init_with_custom_path(self):
        """カスタムパスで初期化"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)
            assert handler.folder_path == Path(temp_dir).resolve()

    def test_folder_creation(self):
        """フォルダが存在しない場合、自動作成されること"""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = os.path.join(temp_dir, "new", "nested", "folder")
            handler = DataHandler(custom_path)
            assert handler.folder_path.exists()
            assert handler.folder_path.is_dir()


class TestDataHandlerLoadSaveText:
    """テキストファイルの読み書きテスト"""

    def test_save_and_load_text(self):
        """テキストファイルの保存と読み込み"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)
            test_data = "Hello, World!"

            handler.save(test_data, "test.txt", format="str")
            loaded_data = handler.load("test.txt", format="str")

            assert loaded_data == test_data

    def test_save_multiline_text(self):
        """複数行のテキストファイル"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)
            test_data = "Line 1\nLine 2\nLine 3"

            handler.save(test_data, "multiline.txt", format="str")
            loaded_data = handler.load("multiline.txt", format="str")

            assert loaded_data == test_data

    def test_load_default_format_is_str(self):
        """デフォルトフォーマットは str"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)
            test_data = "Default format test"

            handler.save(test_data, "default.txt")
            loaded_data = handler.load("default.txt")

            assert loaded_data == test_data


class TestDataHandlerLoadSaveJSON:
    """JSONファイルの読み書きテスト"""

    def test_save_and_load_json(self):
        """JSONファイルの保存と読み込み"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)
            test_data = {"name": "Test", "age": 30, "active": True}

            handler.save(test_data, "data.json", format="json")
            loaded_data = handler.load("data.json", format="json")

            assert loaded_data == test_data

    def test_save_and_load_nested_json(self):
        """ネストされたJSONファイル"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)
            test_data = {
                "user": {"name": "Alice", "profile": {"bio": "Test user"}},
                "items": [1, 2, 3],
            }

            handler.save(test_data, "nested.json", format="json")
            loaded_data = handler.load("nested.json", format="json")

            assert loaded_data == test_data

    def test_save_json_with_formatting(self):
        """JSONが整形されて保存されること"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)
            test_data = {"key": "value"}

            handler.save(test_data, "formatted.json", format="json")

            with open(os.path.join(temp_dir, "formatted.json"), "r") as f:
                content = f.read()
                # indent=2で保存されているため、改行が含まれることを確認
                assert "\n" in content


class TestDataHandlerErrors:
    """エラーハンドリングテスト"""

    def test_load_nonexistent_file(self):
        """存在しないファイルを読み込む場合、FileNotFoundErrorが発生"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)

            with pytest.raises(FileNotFoundError):
                handler.load("nonexistent.txt")

    def test_load_invalid_json(self):
        """不正なJSONを読み込む場合、ValueErrorが発生"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)

            # 不正なJSONファイルを作成
            invalid_json = '{"invalid": json}'
            with open(os.path.join(temp_dir, "invalid.json"), "w") as f:
                f.write(invalid_json)

            with pytest.raises(ValueError):
                handler.load("invalid.json", format="json")

    def test_save_to_invalid_path(self):
        """書き込み権限がないパスに保存する場合、IOErrorが発生"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 読み取り専用フォルダを作成
            readonly_dir = os.path.join(temp_dir, "readonly")
            os.makedirs(readonly_dir)
            os.chmod(readonly_dir, 0o444)

            handler = DataHandler(readonly_dir)

            try:
                with pytest.raises(IOError):
                    handler.save("test", "file.txt")
            finally:
                # テスト後、削除可能にする
                os.chmod(readonly_dir, 0o755)


class TestDataHandlerIntegration:
    """統合テスト"""

    def test_mixed_text_and_json_operations(self):
        """テキストとJSONの混合操作"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)

            # テキストファイルを保存
            text_data = "Sample text"
            handler.save(text_data, "sample.txt", format="str")

            # JSONファイルを保存
            json_data = {"type": "json", "value": 42}
            handler.save(json_data, "data.json", format="json")

            # 読み込んで確認
            assert handler.load("sample.txt", format="str") == text_data
            assert handler.load("data.json", format="json") == json_data

    def test_overwrite_existing_file(self):
        """既存ファイルの上書き"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)

            # 最初のデータを保存
            handler.save("original", "file.txt", format="str")
            assert handler.load("file.txt", format="str") == "original"

            # 上書き
            handler.save("updated", "file.txt", format="str")
            assert handler.load("file.txt", format="str") == "updated"

    def test_multiple_files(self):
        """複数ファイルの操作"""
        with tempfile.TemporaryDirectory() as temp_dir:
            handler = DataHandler(temp_dir)

            files = {
                "file1.txt": "content1",
                "file2.txt": "content2",
                "data1.json": {"id": 1},
                "data2.json": {"id": 2},
            }

            # 保存
            for name, data in files.items():
                fmt = "json" if name.endswith(".json") else "str"
                handler.save(data, name, format=fmt)

            # 読み込んで確認
            for name, data in files.items():
                fmt = "json" if name.endswith(".json") else "str"
                assert handler.load(name, format=fmt) == data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
