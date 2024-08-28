import argparse

def parse_arguments():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description='Record terminal window to GIF or MP4.')
    parser.add_argument('--output', default='output.gif', help='Output file name (GIF or MP4)')
    parser.add_argument('--duration', type=int, default=10, help='Recording duration in seconds')
    parser.add_argument('--interval', type=float, default=0.5, help='Interval between frames in seconds')
    parser.add_argument('--scale', type=float, default=1.0, help='Scaling factor for the frames')
    parser.add_argument('--format', choices=['gif', 'mp4'], default='gif', help='Output format: gif or mp4')
    parser.add_argument('--window-title', default='',
                        help='Title of the window to capture. If not specified, will use default titles.')
    parser.add_argument('--max-frames', type=int, default=None,
                        help='Maximum number of frames to capture. If None, captures frames until duration is reached.')
    return parser.parse_args()
