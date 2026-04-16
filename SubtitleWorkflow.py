from pathlib import Path
from Extractor import SubtitlesExtractor
from Translator import Translator


class SubtitleWorkflow:
    """
    Facade that coordinates subtitle extraction and translation.
    Single entry point for the full pipeline: video -> .srt -> translated .srt
    """

    def __init__(self, extractor: SubtitlesExtractor, translator: Translator):
        self.extractor = extractor
        self.translator = translator

    def process(self, path: str, output_folder: str) -> list[str]:
        """
        Full pipeline: extract subtitles from video(s) and translate.
        Accepts both a single file path and a folder path.

        Args
            path:str - path to file or folder

        Returns
            list of paths to translated .srt files
        """
        path_obj = Path(path)

        if not path_obj.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        # Normalize to list of files
        if path_obj.is_file():
            video_files = [path_obj]
        else:
            video_files = list(path_obj.glob("*.mkv")) + list(path_obj.glob("*.mp4"))

        if not video_files:
            print(f"⚠️  No video files found in: {path}")
            return []

        print(f"Processing {len(video_files)} file(s)")

        # Process each file
        results = []
        for video_file in video_files:
            try:
                print(f"\n{'=' * 50}")
                print(f"Processing: {video_file.name}")
                print("=" * 50)

                srt_paths = self.extractor.extract(
                    path=str(video_file), output_folder=output_folder
                )

                if not srt_paths:
                    print(f"⚠️  No subtitles extracted from {video_file.name}")
                    continue

                srt_path = srt_paths[0]

                translated_path = self.translator.translate()

                results.append(translated_path)

            except Exception as e:
                print(f"❌ Failed {video_file.name}: {e}")
                continue

        print(f"\n✅ Completed {len(results)}/{len(video_files)} files")
        return results
