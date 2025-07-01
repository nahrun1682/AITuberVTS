import asyncio
import json
import websockets
import os
from dotenv import load_dotenv

# .envの読み込み
def get_env(key, default=None):
    return os.environ.get(key, default)

load_dotenv()

class VTubeStudioAPI:
    API_NAME = "VTubeStudioPublicAPI"
    API_VERSION = "1.0"

    def __init__(self, host="localhost", port=8001):
        self.uri = f"ws://{host}:{port}"
        self.plugin_info = {
            "pluginName": "Test Plugin",
            "pluginDeveloper": "Test Developer",
        }

    async def __aenter__(self):
        self.websocket = await websockets.connect(self.uri)
        await self.authenticate()
        return self

    async def __aexit__(self, *_):
        if hasattr(self, "websocket"):
            await self.websocket.close()

    async def _send_request(self, message_type, data=None):
        payload = {
            "apiName": self.API_NAME,
            "apiVersion": self.API_VERSION,
            "requestID": message_type.lower(),
            "messageType": message_type,
            "data": data,
        }
        await self.websocket.send(json.dumps(payload))
        return json.loads(await self.websocket.recv())

    async def authenticate(self):
        # 認証トークンの要求
        auth_response = await self._send_request(
            "AuthenticationTokenRequest", self.plugin_info
        )

        # 認証の実行
        if token := auth_response.get("data", {}).get("authenticationToken"):
            await self._send_request(
                "AuthenticationRequest",
                {**self.plugin_info, "authenticationToken": token},
            )

    async def get_hotkey_list(self):
        return await self._send_request("HotkeysInCurrentModelRequest")

    async def trigger_hotkey(self, hotkey_id):
        return await self._send_request("HotkeyTriggerRequest", {"hotkeyID": hotkey_id})


async def main():
    vts_host = get_env("VTS_HOST", "localhost")
    vts_port = int(get_env("VTS_PORT", 8001))
    async with VTubeStudioAPI(host=vts_host, port=vts_port) as vts:
        print("VTubeStudioに接続しました")

        # ホットキー一覧の取得と表示
        hotkeys = await vts.get_hotkey_list()
        available_hotkeys = hotkeys.get("data", {}).get("availableHotkeys", [])

        if not available_hotkeys:
            print(
                "ホットキーが見つかりません。VTubeStudioでホットキーを設定してください。"
            )
            return

        # ホットキー一覧を表示（空の名前やIDは除外）
        valid_hotkeys = [h for h in available_hotkeys if h.get("name") and h.get("hotkeyID")]
        for i, hotkey in enumerate(valid_hotkeys):
            print(f"{i+1}: {hotkey['name']}")

        # ホットキーの選択と実行
        try:
            idx = int(input("\n実行するホットキーの番号を選択してください: ")) - 1
            if 0 <= idx < len(valid_hotkeys):
                await vts.trigger_hotkey(valid_hotkeys[idx]["hotkeyID"])
                print("実行完了")
        except ValueError:
            print("無効な入力です")


if __name__ == "__main__":
    asyncio.run(main())
