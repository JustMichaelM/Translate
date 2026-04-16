import subprocess
import os
from typing import Optional
from pathlib import Path


class SubtitlesExtractor:
    """Extract subtitle tracks from video files (MKV/MP4) using FFmpeg"""

    def __init__(self, track_index: int = 0):
        self.track_index = track_index
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> None:
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        except FileNotFoundError:
            raise RuntimeError("FFmpeg not found. Install with: brew install ffmpeg")

    def extract(self, path: str, output_folder: Optional[str] = None) -> list[str]:
        """
        Extract subtitle tracks from video file(s).
        Accepts both a single file path and a folder path.

        Args:
            path: Path to video file or folder containing videos
            track_index: Subtitle track index (default: 0)
            output_folder: Custom output folder (default: same as source)
            file_extensions: Video extensions to process (for folders)

        Returns:
            List of paths to extracted .srt files
        """

        path_obj = Path(path)
        file_extensions: tuple = (".mkv", ".mp4")

        if not path_obj.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        # Normalize to list of files
        if path_obj.is_file():
            video_files = [path_obj]
        else:
            video_files = []

            for ext in file_extensions:
                video_files.extend(path_obj.glob(f"*{ext}"))

        if not video_files:
            print(f"⚠️  No video files found in: {path}")
            return []

        print(f"Found {len(video_files)} video file(s)")

        # Extract from each file
        extracted_files = []
        for video_file in video_files:
            try:
                print(f"\nProcessing: {video_file.name}")

                # Determine output path
                if output_folder:
                    os.makedirs(output_folder, exist_ok=True)
                    output_path = os.path.join(
                        output_folder, f"{video_file.stem}_subtitles.srt"
                    )
                else:
                    output_path = f"{video_file.with_suffix('')}_subtitles.srt"

                # Run FFmpeg
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        str(video_file),
                        "-map",
                        f"0:s:{self.track_index}",
                        output_path,
                        "-y",
                    ],
                    check=True,
                    capture_output=True,
                )

                print(f"✅ Extracted to: {output_path}")
                extracted_files.append(output_path)

            except subprocess.CalledProcessError as e:
                print(
                    f"❌ Failed {video_file.name} (track {self.track_index} might not exist)"
                    f"Error: {e}"
                )
                continue

            except Exception as e:
                print(f"❌ Failed {video_file.name}: {e}")
                continue

        print(f"\n✅ Extracted {len(extracted_files)}/{len(video_files)} files")
        return extracted_files
