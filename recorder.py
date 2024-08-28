import pygetwindow as gw
import pyautogui
from PIL import Image
import time
from moviepy.editor import ImageSequenceClip
import numpy as np
import ctypes
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TerminalRecorder:
    def __init__(self, output_file='output.gif', duration=10, interval=0.5, scale_factor=1.0, save_as='gif',
                 window_title='', max_frames=None):
        """
       Initializes the TerminalRecorder class.

        :param output_file: The filename to save the output to (GIF or MP4).
        :param duration: The duration of the recording in seconds.
        :param interval: The interval between frames in seconds.
        :param scale_factor: The frame scaling factor.
        :param save_as: The format of saving ('gif' or 'mp4').
        :param window_title: The title of the window to record. If not specified, the default will be searched.
        :param max_frames: The maximum number of frames to record. If None, records until the time expires.
        """
        self.output_file = output_file
        self.duration = duration
        self.interval = interval
        self.scale_factor = scale_factor
        self.save_as = save_as
        self.frames = []
        self.start_time = None
        self.window_title = window_title
        self.max_frames = max_frames
        self.default_titles = [
            'Terminal', 'консоль', 'console', 'terminal',
            'Командная строка', 'Обработчик команд Windows', 'Администратор: Командная строка'
        ]
        self.original_window = None

    def start_recording(self):
        """Starts the screen recording process."""
        self.start_time = time.time()
        if not self.focus_window():
            print("Could not find or focus on the specified window. Exiting...")
            sys.exit(1)

        print(f"Recording for {self.duration} seconds with an interval of {self.interval} seconds.")
        while True:
            if self.max_frames and len(self.frames) >= self.max_frames:
                print("Reached maximum number of frames.")
                break

            if time.time() - self.start_time >= self.duration:
                print("Recording duration completed.")
                break

            if not self.ensure_window_is_active():
                print("Target window is no longer active. Re-focusing...")
                if not self.focus_window():
                    print("Failed to re-focus on the window. Exiting...")
                    break

            self.capture_frame()
            time.sleep(self.interval)

        self.save_video()
        self.restore_original_window()

    def focus_window(self):
        """Focuses on the specified window."""
        all_windows = gw.getAllWindows()
        titles_to_search = [self.window_title] if self.window_title else self.default_titles
        terminal_windows = [win for win in all_windows if
                            any(title.lower() in win.title.lower() for title in titles_to_search)]

        if not terminal_windows:
            print("No active terminal windows found.")
            return False

        self.terminal_window = terminal_windows[0]
        try:
            self.original_window = gw.getActiveWindow()
            ctypes.windll.user32.ShowWindow(self.terminal_window._hWnd, 9)
            ctypes.windll.user32.SetForegroundWindow(self.terminal_window._hWnd)
            time.sleep(0.5)
            print(f"Focused on window: {self.terminal_window.title}")
            return True

        except Exception as e:
            print(f"Error focusing on window: {e}")
            return False

    def restore_original_window(self):
        """Restores focus to the original window."""
        if self.original_window:
            try:
                ctypes.windll.user32.ShowWindow(self.original_window._hWnd, 9)
                ctypes.windll.user32.SetForegroundWindow(self.original_window._hWnd)
                print(f"Restored focus to original window: {self.original_window.title}")
            except Exception as e:
                print(f"Error restoring original window: {e}")

    def ensure_window_is_active(self):
        """Checks that the desired window is active and activates it if necessary."""
        try:
            current_active_window = gw.getActiveWindow()
            if current_active_window == self.terminal_window:
                return True

            self.terminal_window.activate()
            time.sleep(0.5)
            return gw.getActiveWindow() == self.terminal_window

        except Exception as e:
            print(f"Error checking window focus: {e}")
            return False

    def capture_frame(self):
        """Captures the current frame from the specified window."""
        try:
            screenshot = pyautogui.screenshot(
                region=(self.terminal_window.left, self.terminal_window.top, self.terminal_window.width,
                        self.terminal_window.height)
            )
            if self.scale_factor != 1.0:
                new_size = (int(screenshot.width * self.scale_factor), int(screenshot.height * self.scale_factor))
                screenshot = screenshot.resize(new_size, Image.ANTIALIAS)
            self.frames.append(screenshot)
            logging.info(f"Captured frame {len(self.frames)}")
        except Exception as e:
            logging.error(f"Error capturing frame: {e}")

    def save_video(self):
        """Saves frames in the specified format.."""
        if not self.frames:
            print("No frames to save.")
            return

        print(f"Saving {self.save_as.upper()} with {len(self.frames)} frames.")
        try:
            if self.save_as == 'gif':
                self.save_as_gif()
            elif self.save_as == 'mp4':
                self.save_as_mp4()
            print(f"{self.save_as.upper()} saved as {self.output_file}")

        except Exception as e:
            print(f"Error saving video: {e}")

    def save_as_gif(self):
        """Saves frames as GIF."""
        try:
            if len(self.frames) > 1:
                converted_frames = [frame.convert("RGB") for frame in self.frames]
                converted_frames[0].save(
                    self.output_file,
                    save_all=True,
                    append_images=converted_frames[1:],
                    duration=int(self.interval * 1000),
                    loop=0
                )
            else:
                self.frames[0].save(self.output_file, format='GIF')

        except Exception as e:
            print(f"Error saving GIF: {e}")

    def save_as_mp4(self):
        """Saves frames as MP4."""
        try:
            frame_arrays = [np.array(frame.convert("RGB")) for frame in self.frames]
            clip = ImageSequenceClip(frame_arrays, fps=int(1 / self.interval))
            clip.write_videofile(self.output_file, codec='libx264')

        except Exception as e:
            print(f"Error saving MP4: {e}")
