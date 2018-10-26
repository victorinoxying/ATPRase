# 打包方法：
[使用pyinstaller](https://blog.csdn.net/freewind06/article/details/52140921)
pyinstaller -w yourprogram.py
-F, –onefile 打包成一个exe文件
-D, –onedir 创建一个目录，包含exe文件，但会依赖很多文件（默认选项）
-c, –console, –nowindowed 使用控制台，无界面(默认)
-w, –windowed, –noconsole 使用窗口，无控制台

# 遇到的错误
## 运行exe报错：Could not find or load the Qt platform plugin “windows”
解决办法：将PyQt5\Qt\plugins\platform文件夹移动到exe目录下