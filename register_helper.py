import pyautogui
import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbx
import pyperclip


def get_mouse_position():
    time.sleep(3)
    x, y = pyautogui.position()
    # pyautogui 当前仅支持主显示器截图
    # 后续计划使用RGB像素值判断网页处理是否成功
    # pix = pyautogui.screenshot().getpixel((x, y))
    # print(f'RGB:\t({pix[0]}, {pix[1]}, {pix[2]})')
    pyperclip.copy(f'({x},{y})')
    print(f'鼠标坐标:\t({x},{y})已复制至剪贴板')


# get_mouse_position()
root = tk.Tk()
result = msgbx.askokcancel(
    title='自动注册',
    message='点击按钮并输入关键坐标点步骤名称'
)
ttk.Label(root, text='点击按钮后3秒后')
btnPtLoc = ttk.Button(root, text='坐标测试', command=get_mouse_position).pack()
# btnSave = ttk.Button(root, text='保存文件', command=dump_json).pack()
root.mainloop()
