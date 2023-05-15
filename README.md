# XXDown

一款b站视频下载器
网络上已经有很多的类似产品了，但是它们大多下载格式都是mkv格式
对于我平时剪视频不是很方便，还得手动转换成mp4格式
此代码在登录部分引用了DecryptLogin库
github地址为:https://github.com/CharlesPikachu/DecryptLogin




## 安装

首先请确保环境中有Python

之后从控制台cd至脚本位置，执行

```shell
pip install .
```

> 关于Windows系统如何打开控制台：
> 按Win + X键，之后选择“终端（管理员）”或“PowerShell（管理员）”

由于b站的音频与视频是分开传输的
所以需要合并音视频，这里使用了ffmpeg
使用时需要将ffmpeg.exe放置到与setup.py同目录下
可访问https://ffmpeg.org/download.html下载



## 用法

```
python XXDown.py
```

之后根据提示操作即可



## 贡献

感谢BienBoy提供的接口解释

感谢bilibili提供的api
