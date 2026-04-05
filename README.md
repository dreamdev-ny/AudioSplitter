# Audio Splitter

A Python script that splits audio files at specified timestamps.

## Installation

1. Install the required dependency:
```bash
pip install -r requirements.txt
```

Or install pydub directly:
```bash
pip install pydub
```

## Usage

```bash
python AudioSplitter.py <audio_file> <timestamps> [output_dir]
```

### Arguments
- `audio_file`: Path to the input audio file
- `timestamps`: Comma-separated list of timestamps in seconds (e.g., "30,60,90")
- `output_dir`: Optional output directory (default: "split_audio")

### Examples

Split an MP3 file at 30, 60, and 90 seconds:
```bash
python AudioSplitter.py audio.mp3 "30,60,90"
```

Split a WAV file with custom output directory:
```bash
python AudioSplitter.py podcast.wav "10,25,45,60" output_folder
```

Split the included sample file:
```bash
python AudioSplitter.py ChildrenoftheSun.webm "30,60,120"
```

## Supported Formats

The script supports various audio formats including:
- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- AAC (.aac)
- OGG (.ogg)
- WebM (.webm)
- MP4/M4A (.mp4, .m4a)

## Output

The script creates individual audio files with names like:
- `original_segment_001_0.0s-30.0s.mp3`
- `original_segment_002_30.0s-60.0s.mp3`
- `original_segment_003_60.0s-120.0s.mp3`

Each filename includes the segment number and time range for easy identification.

## Notes

- Timestamps must be in seconds and less than the total audio duration
- The last segment automatically extends to the end of the audio file
- Output files maintain the same format as the input file
