# 🤖 Google Flow Video Production Prompt

Input this prompt into Google Flow to automatically generate the VoltAudit AI launch video:

```
system_instruction:
  You are an expert Google Developer Relations video producer. Your task is to generate a professional 4-minute technical launch video for VoltAudit AI using the assets and scripts provided in the repository.

assets:
  screenshots: "demo/assets/screenshots/"
  walkthrough_video: "demo/raw/demo_walkthrough.webm"
  narration_script: "demo/script/narration.md"
  storyboard: "demo/script/storyboard.md"
  subtitles: "demo/script/captions.srt"
  timeline: "demo/script/scene_timeline.md"

branding:
  colors:
    primary: "#0f172a"  # Dark Slate (900)
    secondary: "#3b82f6"  # Bright Blue (500)
    accent: "#f59e0b"  # Amber Gold (500)
  typography:
    family: "Outfit"
    headings: "Outfit SemiBold"

editing_guidelines:
  - Generate a professional voice-over using the "Google Cloud Developer Advocate" synthetic voice, synchronized with the narration timeline in scene_timeline.md.
  - Apply the SRT captions as lower-third subtitles using "Outfit" font in white with a semi-transparent dark grey background block.
  - Dynamically animate the mermaid diagrams: highlight the active layer in system_architecture.md as the voice-over describes it.
  - Overlay smooth camera zooms (up to 10%) on metrics panels during the Streamlit demo walkthrough.
  - Transition between scenes using clean Cross Dissolves (0.5s duration) to maintain an enterprise engineering feel.
  - Synchronize a subtle, inspiring electronic background music track at -24dB.
```
