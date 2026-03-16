from fastapi import APIRouter, Depends
# filepath: main.py
import os
import mimetypes
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

# Define a directory to serve files from.
# For security, ensure this path is well-defined and doesn't allow directory traversal.
STATIC_FILES_DIR = "static/downloads"

router = APIRouter(prefix="/download", tags=["download"])

@router.get("/")
async def download():
  """
  Streams a file from the predefined static directory.
  """
  filename = "gr38.zip"
  # Sanitize the filename to prevent directory traversal attacks.
  if ".." in filename or "/" in filename:
      raise HTTPException(status_code=400, detail="Invalid filename.")

  file_path = os.path.join(STATIC_FILES_DIR, filename)

  if not os.path.isfile(file_path):
      raise HTTPException(status_code=404, detail="File not found.")

  # Guess the media type based on the file extension.
  media_type, _ = mimetypes.guess_type(file_path)
  if media_type is None:
      media_type = "application/octet-stream" # Default for unknown file types

  file_size = os.path.getsize(file_path)

  # Return a FileResponse to stream the file.
  return FileResponse(
      path=file_path,
      filename=filename,
      media_type=media_type,
      headers={
          "Content-Disposition": f"attachment; filename=\"{filename}\"",
          "Content-Encoding": "identity",  # Disable gzip compression
          "Content-Length": str(file_size),
      },
  )