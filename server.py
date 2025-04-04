"""
WebSocket Audio Server

Module này triển khai một WebSocket server để nhận và xử lý dữ liệu audio được stream từ client.
Server có khả năng:
- Xử lý nhiều kết nối client cùng lúc
- Nhận thông tin về format audio
- Nhận và xử lý từng chunk audio
- Gửi phản hồi xác nhận (acknowledgment) cho client

Cách sử dụng:
    server = AudioServer()
    await server.start()
"""

import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioServer:
    """
    WebSocket server để xử lý stream audio.
    
    Server này lắng nghe các kết nối WebSocket và xử lý hai loại tin nhắn chính:
    1. Format messages: Chứa thông tin về định dạng audio (sample rate, channels, etc.)
    2. Audio chunks: Chứa dữ liệu audio được mã hóa base64
    """
    async def handle_connection(self, websocket):
        """
        Xử lý một kết nối WebSocket từ client.
        
        Phương thức này:
        - Nhận và phân tích các tin nhắn JSON từ client
        - Xử lý tin nhắn dựa trên loại ('format' hoặc 'audio')
        - Gửi phản hồi xác nhận cho mỗi chunk audio nhận được
        
        Args:
            websocket: Đối tượng WebSocket của kết nối client
        """
        logger.info("Client connected")
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get('type', '')
                    
                    if msg_type == 'format':
                        logger.info(f"Received audio format: {data}")
                    elif msg_type == 'audio':
                        # Log only the length of the audio data to avoid console spam
                        audio_length = len(data.get('data', ''))
                        logger.info(f"Received audio chunk: {audio_length} bytes")
                        
                        # Echo back a simple acknowledgment
                        response = {
                            'type': 'ack',
                            'status': 'received',
                            'bytes': audio_length
                        }
                        await websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received")
                
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        except Exception as e:
            logger.error(f"Error handling connection: {str(e)}")

    async def start(self, host='localhost', port=8765):
        """
        Khởi động WebSocket server.
        
        Phương thức này:
        - Tạo một WebSocket server trên host và port được chỉ định
        - Lắng nghe và chấp nhận các kết nối đến
        - Chạy vô thời hạn cho đến khi bị dừng
        
        Args:
            host (str): Địa chỉ host để lắng nghe (mặc định: 'localhost')
            port (int): Port để lắng nghe (mặc định: 8765)
        """
        async with websockets.serve(self.handle_connection, host, port):
            logger.info(f"Audio server running on ws://{host}:{port}")
            await asyncio.Future()  # run forever

async def main():
    """
    Hàm main để khởi tạo và chạy server.
    Tạo một instance của AudioServer và khởi động nó với cấu hình mặc định.
    """
    server = AudioServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())