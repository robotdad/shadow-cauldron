"""
Storage Brick

PUBLIC CONTRACT:
- StorageManager: File and data storage management
- upload_file(): Upload file to storage
- get_file(): Retrieve file from storage
- delete_file(): Delete file from storage

RESPONSIBILITIES:
- File upload and management
- Experiment data persistence
- Result archiving and retrieval
- Storage backend abstraction (local, S3, etc.)
"""

from .manager import StorageManager
from .manager import delete_file
from .manager import get_file
from .manager import upload_file

__all__ = ["StorageManager", "upload_file", "get_file", "delete_file"]
