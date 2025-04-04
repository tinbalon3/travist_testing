"""Test data for API testing"""

# Conference data
conference_data = {
    "single_shot_request": {
        "content": "Hello, how are you?",
        "client_id": "tourguide",
        "session_id": "1234.tourguide",  # Default session for conference
        "tour_code": "CONF-F&B-admin"  # Default tour for conference
    },
    "history_request": {
        "client_id": "tourguide",
        "session_id": "1234.tourguide",  # Default session for conference
        "window_size": 20  # Default window size
    },
    "assign_fb_request": {
        "client_id": "tourguide",
        "session_id": "1234.tourguide"  # Default session for conference
    }
}

# Authentication data
auth_data = {
    "login": {
        "username": "tourguide",
        "password": "123456"
    },
    "register": {
        "username": "new_user",
        "client_name": "Test User",
        "password": "Test@123",
        "role": "user"
    },
    "update": {
        "username": "tourguide",
        "new_info": {
          
        }
    },
    "delete": {
        "username": "tourguide123",
        "password": "123456"
    }
}

# Session data  
session_data = {
    "tour_request": {
        "client_id": "tourguide",
        "search_params": None
    },
    "assign_tour": {
        "session_id": "1234.tourguide",
        "tour_code": "DNHB-4D3N-2025",
        "host_id": "tourguide",
        "languages": [
            {
                "key": "en",
                "code": "en-US",
                "name": "English",
                "voice": "en-US-AndrewNeural"
            }
        ]
    },
    "tour_by_session": {
        "session_id": "1234.tourguide"
    },
    "assign_client": {
        "client_id": "tourguide123",
        "session_id": "1234.tourguide",
        "host_id": "host123"
    },
    "sessions_in_tour": {
        "tour_code": "DNHB-4D3N-2025",
        "search_params": None
    },
    "rating": {
        "rate_value": 5,
        "comment": "Great session!",
        "session_id": "1234.tourguide",
        "client_id": "tourguide123",
        "tour_code": "DNHB-4D3N-2025"
    },
    "session_code": {
        "session_id": "1234.tourguide",
        "client_id": "tourguide123"
    },
    "chat_request": {
        "session_id": "1234.tourguide"
    },
    "get_speakers": {
        "session_id": "1234.tourguide"
    },
    "get_current_speaker": {
        "session_id": "1234.tourguide"
    },
    "get_broadcast_history": {
        "session_id": "1234.tourguide",
        "limitation": 20
    },
    "get_checkpoints": {
        "tour_code": "DNHB-4D3N-2025"
    },
    "get_all_sessions": {
        "search_params": None,
        "search_accuracy": None
    }
}

# Monitor data
monitor_data = {
    "new_tour": {
        "tour_info": {
            "name": "Test Tour",
            "description": "Test tour description",
            "tour_code": "DNHB-4D3N-2025"
        },
        "checkpoints_info": [
            {
                "name": "Point 1",
                "description": "Description 1",
                "duration": 300
            },
            {
                "name": "Point 2", 
                "description": "Description 2",
                "duration": 300
            }
        ],
        "client_id": "tourguide123"
    },
    "delete_tour": {
        "tour_code": "DNHB-4D3N-2025"
    }
}

# Stream paths
stream_paths = {
    "audio_stream": "/stream/audio/{session_id}/{broadcast_id}/{language}",
    "playback_stream": "/stream/audio/session-playback/{session_id}"
}

# Common headers 
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", # Add proper JWT token
    "clientId": "tourguide" 
}