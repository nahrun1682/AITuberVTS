# 🎭 AITuberVTS (VTube Studio連携AIプロジェクト)

**AITuberVTS** は、Pythonによる会話生成・音声合成を通じて、**VTube Studio** のLive2Dモデルを制御するAIプロジェクトです。  
この構成は「Python = 魂」「VTS = 実体」として、喋る・動く・感じるAIの舞台を実現します。

---

## 🌟 特徴

- 🎤 ChatGPTやLangChainで発話を生成
- 🗣 VOICEVOXなどで音声合成
- 🧠 感情や状況に応じた表情・モーション制御
- 📡 VTube StudioのWebSocket APIで表情・モーションをリアルタイム制御
- 🔄 Unity不要、既存のVTSモデルを活用して高速開発

---

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

---

## 🚀 セットアップ手順（Python側）

### 1. Python 3.11.8 & Poetry

```bash
pyenv install 3.11.8
pyenv local 3.11.8
poetry install
```

### 2. 必要パッケージ追加

```bash
poetry add fastapi websockets openai langchain httpx python-dotenv
```

### 3. `.env` を作成

```env
OPENAI_API_KEY=sk-xxxxxxx
VTS_HOST=localhost
VTS_PORT=8001
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
- [ ] 複数モデル・マルチキャラ構成
- [ ] 視聴者コメントの感情リアクション学習

---

