# 🎭 AITuberVTS

## 📁 フォルダ構成

```
AITuberVTS/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPIエントリポイント
│   │   ├── llm/               # 発話生成ロジック
│   │   ├── tts/               # 音声合成
│   │   ├── vts_client/        # VTS API制御クライアント
│   │   ├── memory/            # 会話履歴やキャラ設定
│   │   └── config/            # VTS接続・モデル設定
│   ├── tests/
│   └── scripts/
│       └── launch_vts_ai.py   # 実行用スクリプト
│
├── data/
│   ├── voices/                # 音声ファイル保存先
│   └── logs/                  # ログ出力
│
├── shared/
│   ├── message_protocol.md    # VTS送信メッセージ仕様
│   └── vts_actions.json       # アクション/表情マッピング
│
├── docs/
│   ├── architecture.md
│   └── vts_integration.md
│
├── .env                       # OPENAI_API_KEYなど
├── pyproject.toml
├── .gitignore
└── README.md
```

## 🛠 初期セットアップ手順（pyenv + Poetry）

1. **pyenvのインストール**（未導入の場合）
   - 公式: https://github.com/pyenv/pyenv#installation

2. **Python 3.11.8のインストールと有効化**

   ```bash
   pyenv install 3.11.8
   pyenv local 3.11.8
   python --version  # => 3.11.8 になっていることを確認
   ```

3. **Poetryのインストール**（未導入の場合）

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   # または
   pip install poetry
   ```

4. **依存パッケージのインストール**

   ```bash
   poetry install
   ```

5. **仮想環境の有効化**

   ```bash
   poetry shell
   ```

6. **.envファイルの作成**

   プロジェクトルートに`.env`ファイルを作成し、以下の内容を記入してください。

   ```env
   OPENAI_API_KEY=sk-xxxxxxx
   VTS_HOST=localhost
   VTS_PORT=8001
   ```

7. **動作確認**

   ```bash
   python backend/scripts/launch_vts_ai.py
   ```

---

## 🔁 通信イメージ

```text
[YouTubeコメント]
       ↓
[Python：LLM＋TTSで応答生成]
       ↓
[VTS WebSocket APIでPush送信]
       ↓
[VTube Studio：口パク・表情・音声再生]
```

---

## 🔧 VTS制御例（Python）

```python
import asyncio
import websockets
import json

async def trigger_expression(hotkey_id: str, host="localhost", port=8001):
    uri = f"ws://{host}:{port}"
    async with websockets.connect(uri) as websocket:
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "hotkeytrigger",
            "messageType": "HotkeyTriggerRequest",
            "data": {"hotkeyID": hotkey_id}
        }
        await websocket.send(json.dumps(payload))
        response = await websocket.recv()
        print(response)

# 使い方例
# asyncio.run(trigger_expression("HotkeyIDをここに"))
```

---

## 📖 今後の拡張

- [ ] LangChainによる人格プロンプト制御
- [ ] キャラごとの感情マッピング対応
- [ ] OBS連携

---

