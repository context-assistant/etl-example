#!/usr/bin/env python3
"""
Generate example audio, video, image, and compressed files for the ETL example project.
Requires: ffmpeg, zip, gzip, and optionally pdftk or similar for PDF generation
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Get the project root directory (parent of bin/)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Base directories (relative to project root)
AUDIO_DIR = PROJECT_ROOT / "audio"
VIDEO_DIR = PROJECT_ROOT / "video"
IMAGES_DIR = PROJECT_ROOT / "images"
OTHER_DIR = PROJECT_ROOT / "other"

# Create directories if they don't exist
AUDIO_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)
OTHER_DIR.mkdir(exist_ok=True)

def check_command(cmd):
    """Check if a command is available"""
    # First check if command exists in PATH
    if shutil.which(cmd) is None:
        return False
    # Some commands (like ffmpeg) return non-zero exit codes even for --version
    # So we check if the command exists and can be executed, not the exit code
    try:
        result = subprocess.run([cmd, "--version"], capture_output=True, check=False)
        # Command exists if we got any output (stdout or stderr) as indication it ran
        return len(result.stdout) > 0 or len(result.stderr) > 0
    except (FileNotFoundError, OSError):
        return False

def generate_audio_files():
    """Generate example audio files using FFmpeg"""
    if not check_command("ffmpeg"):
        print("Warning: ffmpeg not found. Skipping audio file generation.")
        return
    
    # Generate a simple sine wave tone for testing
    # 2 seconds, 440Hz (A note), sample rate 44100
    base_cmd = [
        "ffmpeg", "-f", "lavfi",
        "-i", "sine=frequency=440:duration=2",
        "-y"  # Overwrite output files
    ]
    
    audio_files = [
        ("example.mp3", ["-codec:a", "libmp3lame", "-b:a", "128k"]),
        ("example.wav", ["-codec:a", "pcm_s16le"]),
        ("example.ogg", ["-codec:a", "libvorbis", "-b:a", "128k"]),
        ("example.oga", ["-codec:a", "libvorbis", "-b:a", "128k"]),
        ("example.spx", ["-codec:a", "libspeex", "-b:a", "16k"]),
        ("example.aac", ["-codec:a", "aac", "-b:a", "128k"]),
        ("example.adts", ["-codec:a", "aac", "-b:a", "128k"]),
        ("example.flac", ["-codec:a", "flac"]),
        ("example.m4a", ["-codec:a", "aac", "-b:a", "128k", "-f", "mp4"]),
        ("example.weba", ["-codec:a", "libopus", "-b:a", "128k", "-f", "webm"]),
    ]
    
    # WMA requires special handling (may not be available on all systems)
    try:
        subprocess.run(
            base_cmd + ["-codec:a", "wmav2", "-b:a", "128k"] + 
            [str(AUDIO_DIR / "example.wma")],
            capture_output=True, check=True
        )
        print("Generated example.wma")
    except:
        print("Warning: Could not generate WMA file (codec may not be available)")
    
    # Generate MIDI file (simple approach - create a minimal MIDI)
    midi_content = bytes([
        0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,  # MIDI header
        0x00, 0x01, 0x00, 0x01, 0x00, 0x60,  # Format 1, 1 track, 96 ticks/quarter
        0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x0B,  # Track header
        0x00, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20,  # Set tempo
        0x00, 0x90, 0x3C, 0x60,  # Note on (middle C)
        0x60, 0x80, 0x3C, 0x00,  # Note off
        0x00, 0xFF, 0x2F, 0x00   # End of track
    ])
    (AUDIO_DIR / "example.mid").write_bytes(midi_content)
    (AUDIO_DIR / "example.midi").write_bytes(midi_content)
    (AUDIO_DIR / "example.kar").write_bytes(midi_content)
    (AUDIO_DIR / "example.rmi").write_bytes(midi_content)
    print("Generated MIDI files (example.mid, example.midi, example.kar, example.rmi)")
    
    # Generate other audio formats
    for filename, extra_args in audio_files:
        output_path = AUDIO_DIR / filename
        try:
            subprocess.run(
                base_cmd + extra_args + [str(output_path)],
                capture_output=True, check=True
            )
            print(f"Generated {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not generate {filename}: {e}")

def generate_video_files():
    """Generate example video files using FFmpeg"""
    if not check_command("ffmpeg"):
        print("Warning: ffmpeg not found. Skipping video file generation.")
        return
    
    # Generate a simple test pattern video (5 seconds, 640x480, 30fps)
    base_cmd = [
        "ffmpeg", "-f", "lavfi",
        "-i", "testsrc=duration=5:size=640x480:rate=30",
        "-y"
    ]
    
    video_files = [
        ("example.mp4", ["-codec:v", "libx264", "-codec:a", "aac", "-pix_fmt", "yuv420p"]),
        ("example.mp4v", ["-codec:v", "libx264", "-codec:a", "aac", "-pix_fmt", "yuv420p"]),
        ("example.mpg4", ["-codec:v", "libx264", "-codec:a", "aac", "-pix_fmt", "yuv420p"]),
        ("example.webm", ["-codec:v", "libvpx-vp9", "-codec:a", "libopus"]),
        ("example.ogv", ["-codec:v", "libtheora", "-codec:a", "libvorbis"]),
        ("example.avi", ["-codec:v", "libx264", "-codec:a", "aac", "-f", "avi"]),
        ("example.mov", ["-codec:v", "libx264", "-codec:a", "aac", "-f", "mov"]),
        ("example.qt", ["-codec:v", "libx264", "-codec:a", "aac", "-f", "mov"]),
        ("example.mkv", ["-codec:v", "libx264", "-codec:a", "aac", "-f", "matroska"]),
        ("example.mpeg", ["-codec:v", "mpeg2video", "-codec:a", "mp2", "-f", "mpeg"]),
        ("example.mpg", ["-codec:v", "mpeg2video", "-codec:a", "mp2", "-f", "mpeg"]),
        ("example.mpe", ["-codec:v", "mpeg2video", "-codec:a", "mp2", "-f", "mpeg"]),
        ("example.m1v", ["-codec:v", "mpeg2video", "-f", "mpeg1video"]),
        ("example.m2v", ["-codec:v", "mpeg2video", "-f", "mpeg2video"]),
        ("example.mpa", ["-codec:a", "mp2", "-f", "mpeg"]),
        ("example.h264", ["-codec:v", "libx264", "-codec:a", "aac", "-pix_fmt", "yuv420p"]),
    ]
    
    # 3GP/3G2 formats (mobile video)
    try:
        subprocess.run(
            base_cmd + ["-codec:v", "libx264", "-codec:a", "aac", "-s", "320x240", "-f", "3gp"] +
            [str(VIDEO_DIR / "example.3gp")],
            capture_output=True, check=True
        )
        print("Generated example.3gp")
    except:
        print("Warning: Could not generate 3GP file")
    
    try:
        subprocess.run(
            base_cmd + ["-codec:v", "libx264", "-codec:a", "aac", "-s", "320x240", "-f", "3g2"] +
            [str(VIDEO_DIR / "example.3g2")],
            capture_output=True, check=True
        )
        print("Generated example.3g2")
    except:
        print("Warning: Could not generate 3G2 file")
    
    # FLV format
    try:
        subprocess.run(
            base_cmd + ["-codec:v", "libx264", "-codec:a", "aac", "-f", "flv"] +
            [str(VIDEO_DIR / "example.flv")],
            capture_output=True, check=True
        )
        print("Generated example.flv")
    except:
        print("Warning: Could not generate FLV file")
    
    # Generate other video formats
    for filename, extra_args in video_files:
        output_path = VIDEO_DIR / filename
        try:
            subprocess.run(
                base_cmd + extra_args + [str(output_path)],
                capture_output=True, check=True
            )
            print(f"Generated {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not generate {filename}: {e}")

def generate_compressed_files():
    """Generate compressed files"""
    # Create a sample text file to compress
    sample_text = "This is a sample text file for compression testing. " * 50
    sample_file = OTHER_DIR / "sample.txt"
    sample_file.write_text(sample_text)
    
    # Generate ZIP file
    if check_command("zip"):
        zip_path = OTHER_DIR / "example.zip"
        # Change to OTHER_DIR to ensure relative paths work
        original_cwd = os.getcwd()
        try:
            os.chdir(OTHER_DIR)
            subprocess.run(
                ["zip", "-q", "example.zip", "sample.txt"],
                check=True
            )
            print("Generated example.zip")
        finally:
            os.chdir(original_cwd)
    else:
        print("Warning: zip command not found")
    
    # Generate GZIP file
    if check_command("gzip"):
        gz_path = OTHER_DIR / "example.gz"
        sample_file_gz = OTHER_DIR / "sample.txt"
        subprocess.run(
            ["cp", str(sample_file_gz), str(gz_path) + ".tmp"],
            check=True
        )
        subprocess.run(
            ["gzip", "-f", str(gz_path) + ".tmp"],
            check=True
        )
        subprocess.run(
            ["mv", str(gz_path) + ".tmp.gz", str(gz_path)],
            check=True
        )
        print("Generated example.gz")
        
        # Generate TGZ (tar.gz)
        if check_command("tar"):
            tgz_path = OTHER_DIR / "example.tgz"
            original_cwd = os.getcwd()
            try:
                os.chdir(OTHER_DIR)
                subprocess.run(
                    ["tar", "-czf", "example.tgz", "sample.txt"],
                    check=True
                )
                print("Generated example.tgz")
            finally:
                os.chdir(original_cwd)
    else:
        print("Warning: gzip command not found")
    
    # Clean up sample file
    sample_file.unlink()

def generate_image_files():
    """Generate example image files using FFmpeg"""
    if not check_command("ffmpeg"):
        print("Warning: ffmpeg not found. Skipping image file generation.")
        return
    
    # Generate a test pattern image (640x480, RGB)
    # We'll use FFmpeg to create a test pattern and convert to various formats
    base_cmd = [
        "ffmpeg", "-f", "lavfi",
        "-i", "testsrc=duration=1:size=640x480:rate=1",
        "-frames:v", "1",  # Only generate 1 frame
        "-y"
    ]
    
    image_files = [
        ("example.png", ["-codec:v", "png"]),
        ("example.jpg", ["-codec:v", "mjpeg", "-q:v", "5"]),
        ("example.jpeg", ["-codec:v", "mjpeg", "-q:v", "5"]),
        ("example.bmp", ["-codec:v", "bmp"]),
        ("example.gif", ["-codec:v", "gif"]),
        ("example.webp", ["-codec:v", "libwebp", "-quality", "80"]),
        ("example.tif", ["-codec:v", "tiff"]),
        ("example.tiff", ["-codec:v", "tiff"]),
        ("example.ico", ["-codec:v", "bmp", "-s", "32x32"]),  # ICO needs smaller size
    ]
    
    # Generate APNG (animated PNG) - 2 frames
    try:
        subprocess.run(
            ["ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=0.1:size=640x480:rate=10",
             "-frames:v", "2", "-codec:v", "apng", "-y",
             str(IMAGES_DIR / "example.apng")],
            capture_output=True, check=True
        )
        print("Generated example.apng")
    except:
        print("Warning: Could not generate APNG file")
    
    # Generate AVIF (requires libavif codec)
    try:
        subprocess.run(
            base_cmd + ["-codec:v", "libavif", "-quality", "80"] +
            [str(IMAGES_DIR / "example.avif")],
            capture_output=True, check=True
        )
        print("Generated example.avif")
    except:
        print("Warning: Could not generate AVIF file (codec may not be available)")
    
    # Generate other image formats
    for filename, extra_args in image_files:
        output_path = IMAGES_DIR / filename
        try:
            subprocess.run(
                base_cmd + extra_args + [str(output_path)],
                capture_output=True, check=True
            )
            print(f"Generated {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not generate {filename}: {e}")
    
    # Generate .cur file (Windows cursor file - has special format)
    # Create a minimal valid .cur file (similar to .ico but with cursor hotspot)
    try:
        # First generate a small BMP for the cursor
        subprocess.run(
            ["ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=0.1:size=32x32:rate=1",
             "-frames:v", "1", "-codec:v", "bmp", "-y",
             str(IMAGES_DIR / "example_cur_temp.bmp")],
            capture_output=True, check=True
        )
        # Read the BMP and create a .cur file with proper header
        bmp_data = (IMAGES_DIR / "example_cur_temp.bmp").read_bytes()
        # .cur file header: 2 bytes reserved, 2 bytes type (2=cursor), 2 bytes count
        # Then for each image: 1 byte width, 1 byte height, 1 byte colors, 1 byte reserved,
        # 2 bytes hotspot X, 2 bytes hotspot Y, 4 bytes size, 4 bytes offset
        cur_header = bytes([0x00, 0x00, 0x02, 0x00, 0x01, 0x00])  # Cursor, 1 image
        bmp_size = len(bmp_data) - 14  # Size without BMP header
        cur_entry = (bytes([0x20, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) +  # 32x32, hotspot 0,0
                     bmp_size.to_bytes(4, 'little') +  # Size
                     (22).to_bytes(4, 'little'))  # Offset (6 header + 16 entry)
        (IMAGES_DIR / "example.cur").write_bytes(cur_header + cur_entry + bmp_data[14:])  # Skip BMP header
        (IMAGES_DIR / "example_cur_temp.bmp").unlink()
        print("Generated example.cur")
    except Exception as e:
        print(f"Warning: Could not generate .cur file: {e}")
    
    # Generate SVG (text-based XML, so we write it directly)
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480" viewBox="0 0 640 480">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(0,0,255);stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="640" height="480" fill="url(#grad1)"/>
  <circle cx="320" cy="240" r="100" fill="white" opacity="0.8"/>
  <text x="320" y="250" font-family="Arial" font-size="24" fill="black" text-anchor="middle">Example SVG</text>
</svg>'''
    (IMAGES_DIR / "example.svg").write_text(svg_content)
    if check_command("gzip"):
        (IMAGES_DIR / "example.svgz").write_bytes(
            subprocess.run(
                ["gzip", "-c"], input=svg_content.encode(), capture_output=True, check=True
            ).stdout
        )
        print("Generated example.svgz")
    print("Generated example.svg")

def generate_other_files():
    """Generate other binary files"""
    # Generate a simple binary file
    binary_content = bytes(range(256)) * 10  # 2560 bytes
    (OTHER_DIR / "example.bin").write_bytes(binary_content)
    print("Generated example.bin")
    
    # Generate a simple PDF (minimal PDF structure)
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Example PDF Document) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000306 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
400
%%EOF"""
    (OTHER_DIR / "example.pdf").write_bytes(pdf_content)
    print("Generated example.pdf")
    
    # Generate a minimal WASM file (empty module)
    wasm_content = bytes([
        0x00, 0x61, 0x73, 0x6D,  # WASM magic number
        0x01, 0x00, 0x00, 0x00,  # Version 1
    ])
    (OTHER_DIR / "example.wasm").write_bytes(wasm_content)
    print("Generated example.wasm")
    
    # Generate other binary formats (just create placeholder files)
    for ext in [".dmg", ".iso", ".img"]:
        # Create a small binary file
        (OTHER_DIR / f"example{ext}").write_bytes(binary_content[:1024])
        print(f"Generated example{ext}")

def main():
    print("Generating example files...")
    print("=" * 50)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Audio directory: {AUDIO_DIR}")
    print(f"Video directory: {VIDEO_DIR}")
    print(f"Images directory: {IMAGES_DIR}")
    print(f"Other directory: {OTHER_DIR}")
    print("=" * 50)
    
    print("\nGenerating audio files...")
    generate_audio_files()
    
    print("\nGenerating video files...")
    generate_video_files()
    
    print("\nGenerating image files...")
    generate_image_files()
    
    print("\nGenerating compressed files...")
    generate_compressed_files()
    
    print("\nGenerating other binary files...")
    generate_other_files()
    
    print("\n" + "=" * 50)
    print("File generation complete!")

if __name__ == "__main__":
    main()

