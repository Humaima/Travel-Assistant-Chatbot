import json
import os
from typing import Dict, List

class JSONMemoryManager:
    def __init__(self, file_path: str = "conversation_memory.json"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"conversations": []}, f)

    def add_conversation(self, conversation_id: str, messages: List[Dict]):
        with open(self.file_path, 'r+') as f:
            data = json.load(f)
            data["conversations"].append({
                "id": conversation_id,
                "messages": messages
            })
            f.seek(0)
            json.dump(data, f, indent=2)

    def get_conversation(self, conversation_id: str) -> List[Dict]:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            for conv in data["conversations"]:
                if conv["id"] == conversation_id:
                    return conv["messages"]
        return []

    def update_conversation(self, conversation_id: str, messages: List[Dict]):
        with open(self.file_path, 'r+') as f:
            data = json.load(f)
            for conv in data["conversations"]:
                if conv["id"] == conversation_id:
                    conv["messages"] = messages
                    break
            else:
                data["conversations"].append({
                    "id": conversation_id,
                    "messages": messages
                })
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()