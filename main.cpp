#ifdef _WIN32
#include <windows.h>
// 窗口回调函数
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch (uMsg)
    {
        case WM_DESTROY: // 当窗口被关闭
            PostQuitMessage(0); // 告诉消息循环退出
            return 0;
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}
int main()
{
    // 注册窗口类
    WNDCLASS wc = {};
    wc.lpfnWndProc   = WindowProc;
    wc.hInstance     = GetModuleHandle(nullptr);
    wc.lpszClassName = "win";
    wc.hCursor       = LoadCursor(nullptr, IDC_ARROW);
    RegisterClass(&wc);
    //创建窗口
    HWND hwnd = CreateWindowEx(
            0,                              // 扩展样式
            "win",                // 窗口类名
            "我的窗口",                      // 窗口标题
            WS_OVERLAPPEDWINDOW,            // 窗口风格
            CW_USEDEFAULT, CW_USEDEFAULT,   // 初始位置
            800, 600,                       // 宽度和高度
            nullptr,                        // 父窗口
            nullptr,                        // 菜单
            GetModuleHandle(nullptr),       // 实例句柄
            nullptr                         // 附加参数
    );
    if (!hwnd) return -1; // 创建失败
    ShowWindow(hwnd, SW_SHOW);
    // 消息循环
    MSG msg = {};
    while (GetMessage(&msg, nullptr, 0, 0)){
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return 0;
}

//PS E:\CC#C++\MyCraft> D:\llvm\bin\clang++.exe main.cpp -o main.exe -luser32 -lkernel32
//        PS E:\CC#C++\MyCraft> .\main.exe

#elif __linux__
#include <X11/Xlib.h>
#include <unistd.h>

int main() {
    Display* display = XOpenDisplay(NULL);
    if (!display) {
        std::cerr << "Cannot open display\n";
        return 1;
    }

    int screen = DefaultScreen(display);
    Window root = RootWindow(display, screen);

    Window window = XCreateSimpleWindow(
        display, root,
        10, 10, 800, 600,
        1,
        BlackPixel(display, screen),
        WhitePixel(display, screen)
    );

    XSelectInput(display, window, ExposureMask | KeyPressMask | StructureNotifyMask);
    XMapWindow(display, window);

    bool running = true;
    XEvent event;
    while (running) {
        XNextEvent(display, &event);
        if (event.type == DestroyNotify) {
            running = false;
        }
        if (event.type == KeyPress) {
            running = false; // 按任意键也退出
        }
    }

    XDestroyWindow(display, window);
    XCloseDisplay(display);

    return 0;
}

#else
#error Platform not supported
#endif