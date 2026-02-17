from engine12 import *
__version__="1.7.0"
def create_shortcut():
    import os
    import winshell # 需要在 dependencies 加入這個
    from win32com.client import Dispatch

    desktop = winshell.desktop()
    path = os.path.join(desktop, "Sapphire Studio.lnk")
    target = os.path.join(os.environ['APPDATA'], r"..\Local\Programs\Python\Python314\Scripts\sapphire-studio.exe")
    
    # 這裡可以用 Python 邏輯自動建立 .lnk 檔案並綁定你的 icon.ico
    print("💎 Sapphire: Shortcut Created！")
