今天算是第一次用clion正式写项目吧！（以前总是各种环境问题，烦的）clion应该是自带cmake和ninja的，挺方便
编译器我是下的llvm for MSVC（即clang）, 第一次安装的版本较低与MSVC不太兼容，第二次重新下了一个最新版（截至2025.11.7的最新版clang）
下的最新版之后，cmake又报错，chatGPT说要安装winSDK，然后我就安装了最新版，结果cmake还是报错！说什么找不到.rc
但是程序却可以正常启动（我也不知道为啥，但是先跑起来再说吧）
目前还得在终端编译：E:\CC#C++\MyCraft> D:\llvm\bin\clang++.exe main.cpp -o main.exe -luser32 -lkernel32
然后运行E:\CC#C++\MyCraft> .\main.exe
接下来想模仿sdl，把各个平台的窗口类统一封装起来。还得模仿UE底层，对基础类型的封装（便于跨平台，自己实现类型转化，尽量避免浮点数问题，字符统一用UTF-8）
