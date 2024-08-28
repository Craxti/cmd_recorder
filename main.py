from recorder import TerminalRecorder
from utils import parse_arguments

def main():
    """Entry point to the application."""
    args = parse_arguments()
    recorder = TerminalRecorder(
        output_file=args.output,
        duration=args.duration,
        interval=args.interval,
        scale_factor=args.scale,
        save_as=args.format,
        window_title=args.window_title,
        max_frames=args.max_frames
    )
    print("Recording started...")
    recorder.start_recording()
    print("Recording finished.")

if __name__ == "__main__":
    main()
