.PHONY: help generate-files clean check-deps

# Default target
help:
	@echo "Available targets:"
	@echo "  make generate-files  - Generate example audio, video, image, and compressed files"
	@echo "  make check-deps       - Check if required dependencies are installed"
	@echo "  make clean            - Remove generated example files"
	@echo "  make help             - Show this help message"

# Check if required dependencies are available
check-deps:
	@echo "Checking dependencies..."
	@command -v ffmpeg >/dev/null 2>&1 && echo "✓ ffmpeg found" || echo "✗ ffmpeg not found (required for audio/video generation)"
	@command -v zip >/dev/null 2>&1 && echo "✓ zip found" || echo "✗ zip not found (required for ZIP generation)"
	@command -v gzip >/dev/null 2>&1 && echo "✓ gzip found" || echo "✗ gzip not found (required for GZIP generation)"
	@command -v tar >/dev/null 2>&1 && echo "✓ tar found" || echo "✗ tar not found (required for TGZ generation)"
	@command -v python3 >/dev/null 2>&1 && echo "✓ python3 found" || echo "✗ python3 not found (required to run script)"

# Generate example files
generate-files: check-deps
	@echo "Running file generation script..."
	@python3 bin/generate_files.py

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f audio/example.*
	@rm -f video/example.*
	@rm -f images/example.*
	@rm -f other/example.*
	@echo "Clean complete!"

