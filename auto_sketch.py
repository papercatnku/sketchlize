import pyautogui
import time
import os
import numpy as np
import cv2
from tqdm import tqdm
import pyperclip

# TODO: 添加GUI界面，如果需要的话

IMG_POST = [
    'png',
    'jpg',
    'jpeg',
]


class AutoSketchProcess:
    def __init__(self,):
        self.button_pt_mapping = {}
        self.custom_setting()
        # 可根据实际网络情况调整操作延时以提高效率
        self.upload_sleep = 8
        self.crop_sleep = 6
        self.process_sleep = 5
        self.download_sleep = 5
        return

    # TODO: 载入已保存的点的配置
    def custom_setting_from_json(self, json_file):
        return

    def custom_setting(self,):
        # 渐隐边缘
        # 选择照片
        # 从设备上传
        # 裁剪 横向/纵向
        # 继续 - 同选择照片
        # 画面
        # 素描

        # home pc
        # self.set_button_pt('fade_edge', (583, 592))
        # self.set_button_pt('choospic',  (700, 516))
        # self.set_button_pt('upload',    (944, 1292))
        # self.set_button_pt('crop_landscape',      (945, 1493))
        # self.set_button_pt('crop_portrait',      (945, 1551))
        # self.set_button_pt('pic',  (1118, 768))
        # self.set_button_pt('save', (1235, 846))
        # self.set_button_pt('sketch',   (600, 364))
        # self.set_button_pt('continue', (700, 675))

        # office pc 副屏

        self.set_button_pt('fade_edge', (3625, 400))
        self.set_button_pt('choospic',  (3709, 354))
        self.set_button_pt('upload',    (3993, 650))
        self.set_button_pt('crop_landscape', (3986, 799))
        self.set_button_pt('crop_portrait', (3985, 834))
        self.set_button_pt('pic',  (3980, 565))
        self.set_button_pt('save', (4057, 605))
        self.set_button_pt('sketch',   (3642, 252))
        self.set_button_pt('continue', ((3705, 447)))

        return

    def set_button_pt(self, k, pt):
        self.button_pt_mapping[k] = pt
        return

    def process(self, src_dir, ori_dir, res_dir):
        # 生成列表
        os.makedirs(ori_dir, exist_ok=True)
        os.makedirs(res_dir, exist_ok=True)
        imgfn_ls = os.listdir(src_dir)
        for imgfn in tqdm(imgfn_ls):
            # 用于素描效果的图片路径
            res_img_path = os.path.join(res_dir, 'sketch_' + imgfn)
            if os.path.exists(res_img_path):
                continue

            if not imgfn[imgfn.rfind(".")+1:].lower() in IMG_POST:
                continue
            srcimg_fn = os.path.join(src_dir, imgfn)
            srcimg = cv2.imread(srcimg_fn, cv2.IMREAD_COLOR +
                                cv2.IMREAD_IGNORE_ORIENTATION)

            if not isinstance(srcimg, np.ndarray):
                print(f'failed to load {srcimg_fn}')
                continue

            pre_processed_img, if_portrait = self.center_crop(srcimg)
            # 用于上传的输入图片保存至ori_dir内, 由于pyautogui键盘输入限制,所有路径需为英文
            ori_img_path = os.path.join(ori_dir, 'ori_' + imgfn)
            ret = cv2.imwrite(ori_img_path, pre_processed_img)
            if not ret:
                print(f'failed to write {ori_img_path}')

            self.sketch(ori_img_path, res_img_path, if_portrait)
            print(f'{ori_img_path}=>{res_img_path} done')

        return

    def sketch(self, ori_img_path, res_img_path, if_portrait):
        # pyautogui.moveTo(self.button_pt_mapping['fade_edge'])
        pyautogui.leftClick(self.button_pt_mapping['fade_edge'])
        time.sleep(0.5)
        pyautogui.leftClick(self.button_pt_mapping['choospic'])
        time.sleep(2)
        pyautogui.leftClick(self.button_pt_mapping['upload'])
        time.sleep(1)
        # pyautogui.typewrite(ori_img_path, 0.15)
        pyperclip.copy(ori_img_path)
        time.sleep(1)
        # pyperclip.paste()
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press(['enter'])
        # pyautogui.press(['enter'])
        time.sleep(self.upload_sleep)
        if if_portrait:
            pyautogui.leftClick(self.button_pt_mapping['crop_portrait'])
        else:
            pyautogui.leftClick(self.button_pt_mapping['crop_landscape'])
        time.sleep(self.crop_sleep)
        pyautogui.leftClick(self.button_pt_mapping['continue'])
        time.sleep(self.process_sleep)
        pyautogui.rightClick(self.button_pt_mapping['pic'])
        time.sleep(1)
        pyautogui.leftClick(self.button_pt_mapping['save'])
        time.sleep(2)
        # pyautogui.typewrite(res_img_path, 0.15)
        # pyautogui.typewrite(res_img_path)
        # time.sleep(1)
        pyperclip.copy(res_img_path)
        time.sleep(1)
        # pyperclip.paste()
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press(['enter'])
        # pyautogui.press(['enter'])
        time.sleep(self.download_sleep)
        pyautogui.leftClick(self.button_pt_mapping['sketch'])
        time.sleep(5)
        return

    def process_list(self, src_list, dst_dir):
        return

    def center_crop(self, src_img, tar_long=700, tar_short=523):
        h, w = src_img.shape[:2]
        # 是否是竖向(宽小于高)的素材
        if_portrait = False
        if (h > w):
            final_h = tar_long
            final_w = tar_short
            h_r = float(h) / tar_long
            w_r = float(w) / tar_short
            if(h_r > w_r):
                dst_h = h / w_r
                dst_w = w / w_r
            else:
                dst_h = h / h_r
                dst_w = w / h_r
            if_portrait = True
        else:
            final_h = tar_short
            final_w = tar_long
            h_r = float(h) / tar_short
            w_r = float(w) / tar_long
            if(h_r > w_r):
                dst_h = h / w_r
                dst_w = w / w_r
            else:
                dst_h = h / h_r
                dst_w = w / h_r

        rsz_img = cv2.resize(src_img, (int(dst_w), int(dst_h)),
                             interpolation=cv2.INTER_LANCZOS4)

        x_start = int(max((dst_w - final_w)/2, 0))
        y_start = int(max((dst_h - final_h)/2, 0))
        cropped_img = rsz_img[y_start:y_start +
                              final_h, x_start:x_start + final_w, :]

        # safe pad
        cropped_h, cropped_w = cropped_img.shape[:2]
        if if_portrait:
            pad_h = max(0, tar_long - cropped_h)
            pad_w = max(0, tar_short - cropped_w)
        else:
            pad_h = max(0, tar_long - cropped_w)
            pad_w = max(0, tar_short - cropped_h)

        if (pad_h > 0) or (pad_w > 0):
            cropped_img = np.pad(
                cropped_img, ((0, pad_h), (0, pad_w)), mode='edge')
        return cropped_img, if_portrait


if __name__ == "__main__":
    src_dir = r'D:\dataset\COCO\test2017'
    ori_dir = r'D:\dataset\sketchlize\coco_ori'
    res_dir = r'D:\dataset\sketchlize\coco_sketch'

    x = AutoSketchProcess()
    x.process(src_dir, ori_dir, res_dir)
