import shutil

import mmcv
import os
import re
import sys


class frame2video():
    '''
    批量重命名文件夹中的图片文件
    '''

    def __init__(self, raw_path, save_path, save2format_path, video_path, fps):
        # self.path = r'D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_shortcut'  # 表示需要命名处理的文件夹
        # self.save_path = r'D:\1_related_documents\30_研究生电赛\server_lhz\running_saved\fabric_video'  # 保存重命名后的图片地址
        # self.save2format_path = r'D:\1_related_documents\fabric4show\test.avi'
        self.path = raw_path
        self.save_path = save_path
        self.save2format_path = save2format_path
        self.video_path = video_path
        self.fps = fps

    def rename(self):
        filelist = os.listdir(self.path)  # 获取文件路径
        total_num = len(filelist)  # 获取文件长度（个数）
        i = 0  # 表示文件的命名是从200000开始的
        for item in filelist:
            print(item)
            if item.endswith('.jpg'):  # 初始的图片的格式为jpg格式的（或者源文件是png格式及其他格式，后面的转换格式就可以调整为自己需要的格式即可）
                src = os.path.join(os.path.abspath(self.path), item)  # 当前文件中图片的地址
                dst = os.path.join(os.path.abspath(self.save_path), '' + str(i) + '.jpg')  # 处理后文件的地址和名称,可以自己按照自己的要求改进
                try:
                    os.rename(src, dst)
                    print('converting %s to %s ...' % (src, dst))
                    i = i + 1
                except:
                    continue
        print('total %d to rename & converted %d jpgs' % (total_num, i))

    def rename2format(self):
        rename_path = self.save_path  # 图片路径
        for file in os.listdir(rename_path):
            if os.path.isfile(os.path.join(rename_path, file)):
                fname, ext = os.path.splitext(file)
                on = os.path.join(rename_path, file)
                nn = os.path.join(rename_path, str(fname).zfill(6) + ext)  # 数字6是定义为6位数，可随意修改需要的
                os.rename(on, nn)

    def frame2video(self):

        for file in os.listdir(self.save_path):
            # 遍历原文件夹中的文件
            full_file_name = os.path.join(self.save_path, file)  # 把文件的完整路径得到
            print("要被复制的全文件路径全名:", full_file_name)
            if os.path.isfile(full_file_name):  # 用于判断某一对象(需提供绝对路径)是否为文件
                shutil.copy(full_file_name, self.save2format_path)  # shutil.copy函数放入原文件的路径文件全名  然后放入目标文件夹
        mmcv.frames2video(self.save2format_path, self.video_path, self.fps)


# if __name__ == '__main__':
    # demo = BatchRename()
    # demo.rename()
    # fv = frame2video(raw_path=r"/running_saved/fabric_shortcut",
                     # save_path=r"/running_saved/fabric_video/frames", save2format_path=r"D:\1_related_documents\fabric4show\frames", video_path=r"D:\1_related_documents\fabric4show\frames\test.avi", fps=5)

    # fv.rename()
    # fv.rename2format()
    # fv.frame2video()
