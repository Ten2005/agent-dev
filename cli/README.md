# CLI Usage

## データ読み書き

### 読み込み
```bash
uv run dev data read <file_name> [--format str|json] [--folder <path>]
```

例:
```bash
uv run dev data read sample.json --format json
uv run dev data read sample.txt
```

### 書き込み
```bash
uv run dev data write <file_name> [--data <text>] [--format str|json] [--folder <path>]
```

例:
```bash
uv run dev data write output.json --data '{"key":"value"}' --format json
uv run dev data write output.txt --data "Hello World"
```

