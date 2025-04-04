"""
WebSocket Audio Client for Translation Service

Module này triển khai một client WebSocket để kết nối với dịch vụ dịch audio.
Có khả năng:
- Tạo nhiều kết nối client song song
- Nhận và giải nén dữ liệu audio được nén bằng zlib
- Tải và phát audio từ URL
- Xử lý các thông báo broadcast từ server

Cách sử dụng:
    asyncio.run(main())  # Sẽ tạo NUM_CLIENTS kết nối song song
"""

import asyncio
import websockets
import aiohttp
import json
import zlib
import random
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

# Cấu hình kết nối API và WebSocket
AUDIO_API_BASE = "https://api.travist.ai"
SESSION_ID = "1234.tourguide"
USERNAME = "client"
LANGUAGE = "en"
WS_BASE_URL = f"wss://api.travist.ai/server/audio/input-stream-translation/{SESSION_ID}/{USERNAME}"
# WS_BASE_URL cho local testing
# WS_BASE_URL = f"ws://localhost:8080/server/audio/input-stream-translation/{SESSION_ID}/{USERNAME}"

NUM_CLIENTS = 40

async def fetch_and_play_audio(session, audio_url, client_id):
    """
    Tải và phát audio từ URL được chỉ định.
    
    Args:
        session (aiohttp.ClientSession): Session HTTP để tải audio
        audio_url (str): URL của file audio cần tải
        client_id (int): ID của client đang thực hiện request
        
    Note:
        Hiện tại phần phát audio đang bị comment out để tránh
        việc phát nhiều audio cùng lúc khi chạy nhiều client
    """
    try:
        async with session.get(audio_url) as response:
            if response.status == 200:
                print(f"[{client_id}] Fetch audio done: {audio_url}")
                # audio_data = await response.read()
                # audio = AudioSegment.from_file(BytesIO(audio_data), format="mp3")
                # play(audio)  # Chạy async nếu cần song song
            else:
                print(f"[AUDIO] Failed to fetch audio: {response.status}")
    except Exception as e:
        print("*"*20)
        print(f"[AUDIO ERROR] {e}")
        print("*"*20)

async def websocket_client(client_id):
    """
    Tạo và duy trì một kết nối WebSocket client.
    
    Quy trình hoạt động:
    1. Thiết lập kết nối WebSocket với server
    2. Liên tục lắng nghe và xử lý các tin nhắn
    3. Giải nén dữ liệu nhận được bằng zlib
    4. Xử lý các tin nhắn broadcast khác nhau
    5. Tải và phát audio khi nhận được thông báo
    
    Args:
        client_id (int): ID để định danh client trong hệ thống
        
    Raises:
        websockets.exceptions.ConnectionClosed: Khi kết nối bị đóng
        Exception: Các lỗi khác trong quá trình xử lý
    """
    ws_url = f"{WS_BASE_URL}"
    print(f"[{client_id}] Connecting to {ws_url}")

    async with aiohttp.ClientSession() as session:
        try:
            async with websockets.connect(ws_url, open_timeout=20, max_size=None) as ws:
                print(f"[{client_id}] Connected.")

                while True:
                    compressed_data = await ws.recv()

                    decompressed = zlib.decompress(compressed_data, wbits=15 + 32)
                    message = json.loads(decompressed)
                    # print(f"[{client_id}] Received message: {message}")
                    if message.get("type", "").startswith("broadcast-"):
                        if "translating" in message.get("type", ""):
                            continue
                        print(f"[{client_id}] Received message: {message['type']}")

                    if message.get("type") == "broadcast-audio-noti":
                        audio_url = f"{AUDIO_API_BASE}/{message['http-url-route']}"
                        # print(f"[{client_id}] Audio URL: {audio_url}")
                        await fetch_and_play_audio(session, audio_url, client_id)


        except websockets.exceptions.ConnectionClosed as e:
            print("*"*20)
            print(f"[{client_id}] WebSocket closed: {e}")
            print("*"*20)
        except Exception as e:
            print("*"*20)
            print(f"[{client_id}] Error: {e}")
            print("*"*20)

async def main():
    """
    Hàm main để khởi chạy nhiều client WebSocket song song.
    
    Tạo NUM_CLIENTS kết nối WebSocket và chạy chúng đồng thời
    sử dụng asyncio.gather(). Mỗi client sẽ hoạt động độc lập
    và có thể xử lý các tin nhắn riêng biệt.
    """
    clients = [websocket_client(i) for i in range(NUM_CLIENTS)]
    await asyncio.gather(*clients)

if __name__ == "__main__":
    asyncio.run(main())
