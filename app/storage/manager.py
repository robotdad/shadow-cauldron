"""
Storage management for Shadow Cauldron.

Handles file uploads, experiment data persistence, and result archiving.
"""

import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import BinaryIO

import structlog

logger = structlog.get_logger(__name__)


class StorageManager:
    """
    File and data storage manager.

    Provides abstracted storage operations that can work with different
    backends (local filesystem, S3, etc.) through configuration.
    """

    def __init__(self, storage_root: str = "./storage"):
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(exist_ok=True)

        # Create subdirectories
        (self.storage_root / "uploads").mkdir(exist_ok=True)
        (self.storage_root / "experiments").mkdir(exist_ok=True)
        (self.storage_root / "results").mkdir(exist_ok=True)

        logger.info("Storage manager initialized", storage_root=str(self.storage_root))

    async def upload_file(
        self,
        file_data: BinaryIO,
        filename: str,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Upload a file to storage.

        Args:
            file_data: File data stream
            filename: Original filename
            content_type: MIME content type
            metadata: Additional file metadata

        Returns:
            File information dictionary with ID, path, and metadata
        """
        # Generate unique file ID
        file_id = str(uuid.uuid4())

        # Preserve file extension
        file_ext = Path(filename).suffix
        stored_filename = f"{file_id}{file_ext}"

        # Determine storage path
        file_path = self.storage_root / "uploads" / stored_filename

        # Write file to disk
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file_data, f)

        # Create metadata
        file_info = {
            "file_id": file_id,
            "original_filename": filename,
            "stored_filename": stored_filename,
            "file_path": str(file_path),
            "content_type": content_type,
            "size_bytes": file_path.stat().st_size,
            "uploaded_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
        }

        # Save metadata file
        metadata_path = file_path.with_suffix(file_path.suffix + ".meta")
        with open(metadata_path, "w") as f:
            json.dump(file_info, f, indent=2)

        logger.info("File uploaded", file_id=file_id, filename=filename, size_bytes=file_info["size_bytes"])

        return file_info

    async def get_file(self, file_id: str) -> dict[str, Any] | None:
        """
        Get file information and path.

        Args:
            file_id: Unique file identifier

        Returns:
            File information dictionary or None if not found
        """
        # Search for metadata file
        uploads_dir = self.storage_root / "uploads"

        for meta_file in uploads_dir.glob(f"{file_id}*.meta"):
            with open(meta_file) as f:
                file_info = json.load(f)

            # Check if actual file exists
            file_path = Path(file_info["file_path"])
            if file_path.exists():
                return file_info
            logger.warning("File metadata found but file missing", file_id=file_id)
            return None

        return None

    async def delete_file(self, file_id: str) -> bool:
        """
        Delete a file from storage.

        Args:
            file_id: Unique file identifier

        Returns:
            True if file was deleted, False if not found
        """
        file_info = await self.get_file(file_id)
        if not file_info:
            return False

        # Delete actual file
        file_path = Path(file_info["file_path"])
        if file_path.exists():
            file_path.unlink()

        # Delete metadata file
        meta_path = file_path.with_suffix(file_path.suffix + ".meta")
        if meta_path.exists():
            meta_path.unlink()

        logger.info("File deleted", file_id=file_id)
        return True

    async def save_experiment_data(self, experiment_id: str, data: dict[str, Any]) -> str:
        """
        Save experiment data to storage.

        Args:
            experiment_id: Experiment identifier
            data: Experiment data to save

        Returns:
            Path where data was saved
        """
        experiment_path = self.storage_root / "experiments" / f"{experiment_id}.json"

        # Add timestamp
        data["saved_at"] = datetime.utcnow().isoformat()

        with open(experiment_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

        logger.info("Experiment data saved", experiment_id=experiment_id)
        return str(experiment_path)

    async def load_experiment_data(self, experiment_id: str) -> dict[str, Any] | None:
        """
        Load experiment data from storage.

        Args:
            experiment_id: Experiment identifier

        Returns:
            Experiment data or None if not found
        """
        experiment_path = self.storage_root / "experiments" / f"{experiment_id}.json"

        if not experiment_path.exists():
            return None

        with open(experiment_path) as f:
            data = json.load(f)

        return data


# Global storage manager instance
_storage_manager = StorageManager()


async def upload_file(
    file_data: BinaryIO, filename: str, content_type: str | None = None, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Upload a file using the global storage manager."""
    return await _storage_manager.upload_file(file_data, filename, content_type, metadata)


async def get_file(file_id: str) -> dict[str, Any] | None:
    """Get file information using the global storage manager."""
    return await _storage_manager.get_file(file_id)


async def delete_file(file_id: str) -> bool:
    """Delete a file using the global storage manager."""
    return await _storage_manager.delete_file(file_id)
