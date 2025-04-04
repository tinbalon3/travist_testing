"""
Streaming Audio Translation Client

Module này triển khai một client WebSocket để stream audio và xử lý dịch theo thời gian thực.
Nó có khả năng:
- Tiền xử lý file audio (chuyển đổi stereo sang mono, resampling)
- Stream audio theo chunks tới server thông qua WebSocket
- Xử lý phản hồi từ server theo thời gian thực

Cách sử dụng:
    client = AudioTranslationClient()
    await client.process_audio_file("path/to/audio.wav")
"""

import asyncio
import websockets
import json
import base64
import numpy as np
import librosa
from scipy.io import wavfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AudioTranslationClient:
    def __init__(self, 
                 websocket_endpoint="ws://localhost:8765",  # Local test server
                 from_lang="vi",
                 to_langs=None):
        """
        Initialize the audio translation client.
        
        Args:
            websocket_endpoint (str): WebSocket server endpoint
            from_lang (str): Source language code (e.g., 'vi' for Vietnamese)
            to_langs (list): List of target language codes (e.g., ['en', 'ja'])
        """
        self.websocket_endpoint = websocket_endpoint
        self.from_lang = from_lang
        self.to_langs = to_langs or ["en", "ja"]
        self.buffer_size = 6400  # 6400 bytes = 3200 samples (PCM16)
        self.target_sample_rate = 16000

    def preprocess_audio(self, audio_path: str) -> np.ndarray:
        """
        Tiền xử lý file audio để chuẩn bị cho việc streaming.
        
        Quy trình xử lý bao gồm:
        1. Đọc file audio và chuyển đổi sang định dạng PCM16
        2. Chuyển đổi stereo thành mono nếu cần
        3. Resampling về tần số mẫu mục tiêu (16kHz)
        4. Loại bỏ khoảng lặng ở đầu file
        
        Args:
            audio_path (str): Đường dẫn tới file audio cần xử lý
            
        Returns:
            np.ndarray: Mảng numpy chứa dữ liệu audio đã xử lý
        """
        try:
            logger.info(f"Processing audio file: {audio_path}")
            rate, data = wavfile.read(audio_path)
            
            # Convert to PCM16 format if necessary
            if data.dtype != np.int16:
                data = (data * 32767).astype(np.int16)

            # Convert stereo to mono
            if len(data.shape) > 1 and data.shape[1] == 2:
                logger.info("Converting stereo to mono")
                data = data.mean(axis=1).astype(np.int16)

            # Resample if necessary
            if rate != self.target_sample_rate:
                logger.info(f"Resampling audio from {rate}Hz to {self.target_sample_rate}Hz")
                data = librosa.resample(data.astype(np.float32), 
                                     orig_sr=rate, 
                                     target_sr=self.target_sample_rate)
                data = (data * 32767).astype(np.int16)

            # Remove leading silence
            nonzero_indices = np.where(data != 0)[0]
            if len(nonzero_indices) > 0:
                data = data[nonzero_indices[0]:]
                logger.info("Removed leading silence")

            return data
            
        except Exception as e:
            logger.error(f"Error preprocessing audio: {str(e)}")
            raise

    async def stream_audio(self, websocket, data: np.ndarray):
        """
        Stream dữ liệu audio qua kết nối WebSocket.
        
        Đầu tiên gửi thông tin về format audio (sample rate, bits per sample, etc.).
        Sau đó chia audio thành các chunks nhỏ và gửi tuần tự với độ trễ
        để đảm bảo server có thể xử lý kịp thời.
        
        Args:
            websocket: Kết nối WebSocket đang hoạt động
            data (np.ndarray): Dữ liệu audio đã được tiền xử lý
        """
        try:
            # Send audio format information
            format_info = {
                "type": "format",
                "sampleRate": self.target_sample_rate,
                "bitsPerSample": 16,
                "channels": 1,
                "encoding": "PCM"
            }
            await websocket.send(json.dumps(format_info))
            logger.info("Sent audio format information")

            # Stream audio chunks
            chunks_sent = 0
            for i in range(0, len(data), self.buffer_size // 2):
                chunk = data[i:i + self.buffer_size // 2]
                audio_data = {
                    "type": "audio",
                    "data": base64.b64encode(chunk.tobytes()).decode('utf-8')
                }
                await websocket.send(json.dumps(audio_data))
                chunks_sent += 1
                if chunks_sent % 10 == 0:
                    logger.info(f"Sent {chunks_sent} audio chunks")
                await asyncio.sleep(0.2)  # Control streaming rate

            logger.info(f"Finished sending {chunks_sent} audio chunks")

        except Exception as e:
            logger.error(f"Error streaming audio: {str(e)}")
            raise

    async def receive_messages(self, websocket):
        """
        Nhận và xử lý tin nhắn từ WebSocket server.
        
        Xử lý 2 loại tin nhắn chính:
        - Tin nhắn xác nhận (ack): Server báo nhận được bao nhiêu bytes
        - Các tin nhắn khác: Có thể là kết quả dịch hoặc thông báo lỗi
        
        Args:
            websocket: Kết nối WebSocket đang hoạt động
        """
        try:
            async for message in websocket:
                try:
                    response = json.loads(message)
                    if response.get('type') == 'ack':
                        logger.info(f"Server acknowledged {response.get('bytes')} bytes")
                    else:
                        logger.info(f"Received: {message}")
                except json.JSONDecodeError:
                    logger.warning(f"Received invalid JSON: {message}")
                
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed")
        except Exception as e:
            logger.error(f"Error receiving messages: {str(e)}")
            raise

    async def process_audio_file(self, audio_path: str):
        """
        Xử lý và stream một file audio.
        
        Quy trình hoạt động:
        1. Tiền xử lý file audio thông qua preprocess_audio()
        2. Thiết lập kết nối WebSocket với server
        3. Tạo và chạy song song 2 tasks:
           - Task gửi dữ liệu audio
           - Task nhận phản hồi từ server
        
        Args:
            audio_path (str): Đường dẫn tới file audio cần xử lý
        """
        try:
            # Preprocess audio
            data = self.preprocess_audio(audio_path)
            
            # Connect to WebSocket and stream audio
            logger.info(f"Connecting to WebSocket server at {self.websocket_endpoint}")
            async with websockets.connect(self.websocket_endpoint) as websocket:
                # Create tasks for sending and receiving
                send_task = asyncio.create_task(self.stream_audio(websocket, data))
                receive_task = asyncio.create_task(self.receive_messages(websocket))
                
                # Wait for both tasks to complete
                await asyncio.gather(send_task, receive_task)
                
        except Exception as e:
            logger.error(f"Error processing audio file: {str(e)}")
            raise

async def main():
    """Main entry point for the audio streaming client"""
    # Create client instance
    client = AudioTranslationClient()
    
    try:
        await client.process_audio_file("noise.wav")
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())