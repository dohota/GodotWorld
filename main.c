#define SOKOL_IMPL
#define SOKOL_D3D11//GLCORE33   // 也可以根据平台换成 SOKOL_D3D11 / SOKOL_METAL / SOKOL_GLES3
#define SOKOL_APP_IMPL
#define SOKOL_GFX_IMPL
#include "./sokol_gfx.h"
#include "./sokol_app.h"
// 在此初始化您的应用
static void init(void) {
    sg_desc desc = {};  // 创建一个 sg_desc 变量
    sg_setup(&desc);     // 传递这个变量的地址
    //sg_setup(&(sg_desc){0});
}
// 在此渲染一帧
static void frame(void) {
    
}
// 在此清理资源
static void cleanup(void) {
    sg_shutdown();
}
// 在此处理输入事件
static void event(const sapp_event* ev) {
    switch (ev->type) {
        case SAPP_EVENTTYPE_KEY_DOWN:
                    if (ev->key_code == SAPP_KEYCODE_ESCAPE) {
                        sapp_request_quit();
                    }
                    break;
        case SAPP_EVENTTYPE_MOUSE_DOWN:
            if (ev->mouse_button == SAPP_MOUSEBUTTON_LEFT) {
                sapp_lock_mouse(true);  // 启用鼠标视角
            }
            break;
        case SAPP_EVENTTYPE_MOUSE_MOVE:
            if (sapp_mouse_locked()) {
                // 使用相对移动控制相机
                float dx = ev->mouse_dx;
                float dy = ev->mouse_dy;
                // 更新相机...
            }
            break;
        case SAPP_EVENTTYPE_RESIZED:
            // 处理窗口大小调整
            int new_width = sapp_width();
            int new_height = sapp_height();
            break;
        case SAPP_EVENTTYPE_QUIT_REQUESTED:
            // 显示"真的要退出吗？"对话框或直接退出
            sapp_quit();
            break;
        default:
            // 处理未处理的其他枚举值
            break;
    }
}
//Sokol 是一个专门为跨平台应用设计的库，
// 它会要求你使用 sokol_app.h 提供的特定入口点，而不是直接用标准的 main 函数
sapp_desc sokol_main(int argc, char* argv[]) {
    return (sapp_desc){
        .init_cb = init,
        .frame_cb = frame,
        .cleanup_cb = cleanup,
        .width = 800,
        .height = 600,
        .window_title = "My World",
    };
}
