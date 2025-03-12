# Web Page Source Extractor

Webページのソースコード（HTML、CSS、JavaScript）を取得し、単一ファイルまたは個別ファイルとして保存するツールです。

## 機能

- Webページの完全なソースコード取得
- 外部CSS/JavaScriptファイルの自動取得とインライン化
- UTF-8エンコーディング対応
- 柔軟な出力形式（単一ファイル/個別ファイル）

## 必要要件

- Python 3.x
- 必要なパッケージ（requirements.txtを参照）

## インストール

```bash
# リポジトリのクローン
git clone [リポジトリURL]
cd [リポジトリ名]

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

対話形式でURLの入力と出力形式の選択を行います：
1. URLを入力
2. 出力形式を選択（y: 単一ファイル / n: 個別ファイル）

### 出力形式

- 単一ファイル形式（y）:
  - `combined.html`: すべてのリソースが統合されたファイル

- 個別ファイル形式（n）:
  - `page.html`: メインのHTMLファイル
  - `script_[番号].js`: JavaScriptファイル
  - `style_[番号].css`: CSSファイル
  - `resources.json`: 外部リソース情報

## 注意事項

1. **利用規約の遵守**:
   - 対象サイトのロボット規約を確認してください
   - 過度なリクエストは避けてください

2. **著作権**:
   - 取得したコンテンツの利用は、各サイトの利用規約に従ってください
   - 商用利用する場合は、必ず権利者の許可を得てください

3. **免責事項**:
   - 本ツールの使用によって生じたいかなる損害についても、作者は責任を負いません
   - 利用者の責任において使用してください

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。 