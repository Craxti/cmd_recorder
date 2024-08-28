import unittest
from unittest.mock import patch, MagicMock
from recorder import TerminalRecorder
from PIL import Image
import numpy as np
from moviepy.editor import ImageSequenceClip


class TestTerminalRecorder(unittest.TestCase):

    @patch('pyautogui.screenshot')
    @patch('pygetwindow.getAllWindows')
    @patch('pygetwindow.getActiveWindow')
    @patch('ctypes.windll.user32.ShowWindow')
    @patch('ctypes.windll.user32.SetForegroundWindow')
    def test_start_recording(self, mock_set_foreground, mock_show_window, mock_get_active_window, mock_get_all_windows, mock_screenshot):
        # Mock the return values
        mock_get_all_windows.return_value = [MagicMock(title='Terminal')]
        mock_get_active_window.return_value = MagicMock(title='Original Window')
        mock_screenshot.return_value = Image.new('RGB', (100, 100))

        recorder = TerminalRecorder(output_file='test.gif', duration=1, interval=0.1, max_frames=5)
        recorder.start_recording()

        self.assertGreater(len(recorder.frames), 0)
        self.assertEqual(len(recorder.frames), 1)

    @patch('moviepy.editor.ImageSequenceClip.write_videofile')
    @patch('moviepy.editor.ImageSequenceClip.__init__')
    @patch('numpy.array')
    def test_save_as_mp4(self, mock_np_array, mock_image_sequence_clip_init, mock_write_videofile):
        recorder = TerminalRecorder(output_file='test.mp4', save_as='mp4')
        recorder.frames = [Image.new('RGB', (100, 100)) for _ in range(10)]

        recorder.save_as_mp4()

    @patch('PIL.Image.Image.save')
    @patch('PIL.Image.Image.convert')
    def test_save_as_gif(self, mock_convert, mock_save):
        recorder = TerminalRecorder(output_file='test.gif', save_as='gif')
        recorder.frames = [Image.new('RGB', (100, 100)) for _ in range(10)]

        recorder.save_as_gif()


    @patch('pyautogui.screenshot')
    def test_capture_frame(self, mock_screenshot):
        mock_screenshot.return_value = Image.new('RGB', (100, 100))
        recorder = TerminalRecorder()

        recorder.focus_window = MagicMock()
        recorder.ensure_window_is_active = MagicMock()
        recorder.terminal_window = MagicMock(left=0, top=0, width=100, height=100)

        recorder.capture_frame()

        self.assertEqual(len(recorder.frames), 1)
        mock_screenshot.assert_called_once()

if __name__ == '__main__':
    unittest.main()
