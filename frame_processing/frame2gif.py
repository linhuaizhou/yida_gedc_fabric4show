import os
import cv2
import imageio


class frame2gif:
    def __init__(self, frames_input_path, gif_output, fps):
        self.frames_input_path = frames_input_path
        self.gif_output = gif_output
        self.fps = fps

    def do(self):
        path = self.frames_input_path
        files = [os.path.join(path, f) for f in os.listdir(path)]
        frames = []
        for f in files:
            img = imageio.imread(f)  # RGB格式的array
            frames.append(img)
        imageio.mimsave(self.gif_output, frames, fps=3)


if __name__ == '__main__':
    fg = frame2gif(r"D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_shortcut",
                   r"D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_result_gif\1.gif", 5)
    fg.do()
