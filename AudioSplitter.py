#!/usr/bin/env python3
"""
Audio Splitter - Split audio files at specified timestamps

Usage:
    python AudioSplitter.py <audio_file> <timestamps> [output_dir] [format]

Arguments:
    audio_file: Path to the input audio file
    timestamps: Comma-separated list of timestamps in seconds (e.g., "30,60,90")
    output_dir: Optional output directory (default: "split_audio")
    format: Optional output format (mp3, wav, flac, aac, ogg, webm, mp4). Default: same as input

Example:
    python AudioSplitter.py input.mp3 "30,60,90,120" output_folder mp3
    python AudioSplitter.py input.webm "30,60" output wav
"""

import os
import sys
import argparse
from pathlib import Path
try:
    from pydub import AudioSegment
except ImportError:
    print("Error: pydub is required. Install it with: pip install pydub")
    sys.exit(1)


def parse_timestamps(timestamp_str):
    """Parse comma-separated timestamps into a list of floats"""
    try:
        timestamps = [float(t.strip()) for t in timestamp_str.split(',')]
        return sorted(timestamps)
    except ValueError:
        raise ValueError("Invalid timestamp format. Use comma-separated seconds, e.g., '30,60,90'")


def get_audio_format(file_path):
    """Get audio format from file extension"""
    ext = Path(file_path).suffix.lower()
    format_map = {
        '.mp3': 'mp3',
        '.wav': 'wav',
        '.flac': 'flac',
        '.aac': 'aac',
        '.ogg': 'ogg',
        '.webm': 'webm',
        '.mp4': 'mp4',
        '.m4a': 'mp4'
    }
    return format_map.get(ext, 'wav')


def split_audio(input_file, timestamps, output_dir="split_audio", output_format=None):
    """Split audio file at specified timestamps"""
    
    # Validate input file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load audio file
    print(f"Loading audio file: {input_file}")
    try:
        audio = AudioSegment.from_file(input_file)
    except Exception as e:
        raise Exception(f"Error loading audio file: {e}")
    
    duration_seconds = len(audio) / 1000.0
    print(f"Audio duration: {duration_seconds:.2f} seconds")
    
    # Validate timestamps
    if any(t >= duration_seconds for t in timestamps):
        raise ValueError(f"All timestamps must be less than audio duration ({duration_seconds:.2f} seconds)")
    
    # Add end timestamp to include the last segment
    timestamps.append(duration_seconds)
    
    # Get base name and determine output format
    base_name = Path(input_file).stem
    if output_format:
        output_format = output_format.lower().lstrip('.')
        # Validate format
        valid_formats = ['mp3', 'wav', 'flac', 'aac', 'ogg', 'webm', 'mp4']
        if output_format not in valid_formats:
            raise ValueError(f"Invalid format '{output_format}'. Supported formats: {', '.join(valid_formats)}")
    else:
        output_format = get_audio_format(input_file)
    
    # Split audio
    start_time = 0
    split_files = []
    
    for i, end_time in enumerate(timestamps):
        # Extract segment
        segment = audio[start_time * 1000:end_time * 1000]
        
        # Generate output filename
        output_filename = f"{base_name}_segment_{i+1:03d}_{start_time:.1f}s-{end_time:.1f}s.{output_format}"
        output_path = os.path.join(output_dir, output_filename)
        
        # Export segment with specified format
        print(f"Creating segment {i+1}: {start_time:.1f}s - {end_time:.1f}s (format: {output_format})")
        segment.export(output_path, format=output_format)
        split_files.append(output_path)
        
        start_time = end_time
    
    print(f"\nSuccessfully created {len(split_files)} audio segments in '{output_dir}/'")
    return split_files


def main():
    parser = argparse.ArgumentParser(
        description="Split audio files at specified timestamps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python AudioSplitter.py audio.mp3 "30,60,90"
  python AudioSplitter.py podcast.wav "10,25,45,60" output_folder
  python AudioSplitter.py music.flac "15,30,45,60,90" splits mp3
  python AudioSplitter.py input.webm "30,60" output wav
        """
    )
    
    parser.add_argument('audio_file', help='Path to the input audio file')
    parser.add_argument('timestamps', help='Comma-separated timestamps in seconds (e.g., "30,60,90")')
    parser.add_argument('output_dir', nargs='?', default='split_audio', 
                       help='Output directory (default: split_audio)')
    parser.add_argument('format', nargs='?', 
                       help='Output audio format (mp3, wav, flac, aac, ogg, webm, mp4). Default: same as input')
    
    args = parser.parse_args()
    
    try:
        timestamps = parse_timestamps(args.timestamps)
        print(f"Split points: {timestamps}")
        
        split_files = split_audio(args.audio_file, timestamps, args.output_dir, args.format)
        
        print("\nCreated files:")
        for file_path in split_files:
            print(f"  - {file_path}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()