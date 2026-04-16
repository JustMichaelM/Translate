import subprocess
import os
from typing import Optional
from pathlib import Path


class SubtitlesExtractor:
    """Extract subtitle tracks from video files (MKV/MP4) using FFmpeg"""

    def __init__(self):
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> None:
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        except FileNotFoundError:
            raise RuntimeError("FFmpeg not found. Install with: brew install ffmpeg")

    def list_subtitle_tracks(self, video_path: str) -> None:
        """Display all subtitle tracks in the video file"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        print(f"\nAnalyzing: {video_path}\n")
        subprocess.run(["ffmpeg", "-i", video_path], stderr=subprocess.STDOUT)

    def extract_from_file(
        self, video_path: str, track_index: int = 0, output_path: Optional[str] = None
    ) -> str:
        """
        Extract subtitle track from video file

        Args:
            video_path: Path to video file (MKV/MP4)
            track_index: Subtitle track index (default: 0 = first track)
            output_path: Custom output path (default: auto-generated)

        Returns:
            Path to extracted .srt file
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Generate output path if not provided
        if output_path is None:
            base_name = os.path.splitext(video_path)[0]
            output_path = f"{base_name}_subtitles.srt"

        # Extract using FFmpeg
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    video_path,
                    "-map",
                    f"0:s:{track_index}",
                    output_path,
                    "-y",  # Overwrite if exists
                ],
                check=True,
                capture_output=True,
            )

            print(f"✅ Extracted subtitles to: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Failed to extract subtitles. "
                f"Make sure track index {track_index} exists. "
                f"Use list_subtitle_tracks() to see available tracks."
                f"Error: {e}"
            )

    def extract_from_folder(
        self,
        folder_path: str,
        track_index: int = 0,
        output_folder: Optional[str] = None,
        file_extensions: tuple = (".mkv", ".mp4"),
    ) -> list[str]:
        """
        Extract subtitles from all video files in a folder

        Args:
            folder_path: Path to folder containing video files
            track_index: Subtitle track index (default: 0)
            file_extensions: Tuple of video extensions to process

        Returns:
            List of paths to extracted .srt files
        """
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        if not folder.is_dir():
            raise ValueError(f"Path is not a folder: {folder_path}")

        # Find all video files
        video_files = []
        for ext in file_extensions:
            video_files.extend(folder.glob(f"*{ext}"))

        if not video_files:
            print(f"⚠️  No video files found in: {folder_path}")
            return []

        print(f"Found {len(video_files)} video file(s)")

        # Extract subtitles from each file
        extracted_files = []
        for video_file in video_files:
            try:
                print(f"\nProcessing: {video_file.name}")
                if output_folder:
                    output_path = os.path.join(
                        output_folder, f"{video_file.stem}_subtitles.srt"
                    )
                else:
                    output_path = None  # Auto-generate next to video

                srt_path = self.extract_from_file(
                    video_path=str(video_file),
                    track_index=track_index,
                    output_path=output_path,
                )
                extracted_files.append(srt_path)
            except Exception as e:
                print(f"❌ Failed to extract from {video_file.name}: {e}")
                continue

        print(
            f"\n✅ Successfully extracted {len(extracted_files)}/{len(video_files)} subtitle files"
        )
        return extracted_files
