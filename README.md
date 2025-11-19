# Matrix-Cam

A Python CLI tool that renders your webcam feed as live ASCII art in your terminal, styled like the Matrix.

## Features
- Real-time webcam capture
- ASCII rendering with density mapping
- "Matrix" green-on-black aesthetic
- Auto-resizing to terminal window

## Installation

1.  **Clone the repository** (or download the files).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script from the project root:

```bash
python src/main.py
```

- **Quit**: Press `q` to exit.

## Troubleshooting
- If you see "Error: Could not open webcam", ensure your webcam is not being used by another application.
- If the characters look stretched, try adjusting your terminal font size or window aspect ratio.
