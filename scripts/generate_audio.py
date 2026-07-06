"""Voice-over audio generator script utilizing gTTS."""

import re
import sys
from pathlib import Path

from gtts import gTTS

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def generate_speech_audio() -> None:
    """Read narration markdown script and synthesize explanation MP3."""
    script_path = PROJECT_ROOT / "demo" / "script" / "narration.md"
    output_dir = PROJECT_ROOT / "demo" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "audio_explanation.mp3"

    if not script_path.exists():
        raise FileNotFoundError(f"Narration script missing at: {script_path}")

    print(f"Reading narration script: {script_path}...")
    content = script_path.read_text(encoding="utf-8")

    # Strip title and subheadings/timing annotations
    paragraphs = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("---"):
            continue
        # Remove quotes surrounding paragraphs
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        paragraphs.append(line)

    narration_text = " ".join(paragraphs)
    # Clean double spaces
    narration_text = re.sub(r"\s+", " ", narration_text).strip()

    print(f"Compiled narration text (Length: {len(narration_text)} characters):")
    print(f'"{narration_text[:120]}..."')

    print("Synthesizing speech via Google TTS engine...")
    tts = gTTS(text=narration_text, lang="en", slow=False)
    tts.save(str(output_file))

    print(f"Success! Audio file saved successfully: {output_file}")


if __name__ == "__main__":
    try:
        generate_speech_audio()
        sys.exit(0)
    except Exception as error:
        print(f"❌ Audio generation failed: {error}", file=sys.stderr)
        sys.exit(1)
