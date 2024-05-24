# ceek-news-to-jsonl

Preprocessing script to convert Ceek News corpus to Transformers' JSONL.

Ceek Newsで配布しているコーパスをTransformers準拠のJSONLファイルに変換するスクリプトです。

## Usage

```shell
# Convert corpus file into JSONL split by published months:
python raw_to_jsonl.py input_tsv output_jsonl_prefix

# Extract URLs from JSONL:
python jsonl_to_url.py input_jsonl_dirname output_txt
```