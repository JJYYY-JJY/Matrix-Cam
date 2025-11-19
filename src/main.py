import cv2
import curses
import numpy as np
import sys
import time

class MatrixCam:
    def __init__(self):
        self.chars = " .:-=+*#%@"  # Simple ASCII ramp
        self.n_chars = len(self.chars)
        self.cap = None

    def get_frame(self, height, width):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Resize to fit terminal (maintain aspect ratio roughly)
        # Terminal characters are usually about twice as tall as they are wide
        # So we might want to squash the width or height differently
        # But for simplicity, let's just resize to (width, height)
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Resize
        resized = cv2.resize(gray, (width, height))
        return resized

    def map_pixels_to_ascii(self, image):
        # Normalize pixels to range 0 to n_chars-1
        normalized = (image / 255) * (self.n_chars - 1)
        indices = normalized.astype(int)
        
        # Vectorized lookup is a bit tricky with strings in numpy, 
        # but we can do a simple list comprehension or map
        # For performance, let's try a simple approach first
        
        lines = []
        for row in indices:
            line = "".join([self.chars[i] for i in row])
            lines.append(line)
        return lines

    def run(self, stdscr):
        # Setup curses
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True) # Non-blocking input
        curses.use_default_colors()
        
        # Initialize colors
        # Pair 1: Green text on Black background (Matrix style)
        try:
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        except:
            pass # Fallback if terminal doesn't support colors

        # Open webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            stdscr.addstr(0, 0, "Error: Could not open webcam.")
            stdscr.refresh()
            time.sleep(2)
            return

        try:
            while True:
                # Check for 'q' key to quit
                key = stdscr.getch()
                if key == ord('q'):
                    break

                # Get terminal size
                height, width = stdscr.getmaxyx()
                
                # Get frame
                # Note: cv2 resize expects (width, height)
                # We leave 1 line at bottom to avoid scrolling issues
                frame = self.get_frame(height - 1, width)
                
                if frame is None:
                    break

                # Convert to ASCII
                ascii_lines = self.map_pixels_to_ascii(frame)

                # Draw
                stdscr.erase()
                for y, line in enumerate(ascii_lines):
                    try:
                        # Draw with green color
                        stdscr.addstr(y, 0, line, curses.color_pair(1))
                    except curses.error:
                        pass # Ignore edge case errors

                stdscr.refresh()
                
                # Cap framerate slightly to reduce CPU usage
                time.sleep(0.03)

        finally:
            self.cap.release()

def main():
    cam = MatrixCam()
    curses.wrapper(cam.run)

if __name__ == "__main__":
    main()
