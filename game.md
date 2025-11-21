v1.0:今天算是第一次用clion正式写项目吧！（以前总是各种环境问题，烦的）clion应该是自带cmake和ninja的，挺方便
编译器我是下的llvm for MSVC（即clang）, 第一次安装的版本较低与MSVC不太兼容，第二次重新下了一个最新版（截至2025.11.7的最新版clang）
下的最新版之后，cmake又报错，chatGPT说要安装winSDK，然后我就安装了最新版，结果cmake还是报错！说什么找不到.rc
但是程序却可以正常启动（我也不知道为啥，但是先跑起来再说吧）
目前还得在终端编译：E:\CC#C++\MyCraft> D:\llvm\bin\clang++.exe main.cpp -o main.exe -luser32 -lkernel32
然后运行E:\CC#C++\MyCraft> .\main.exe
接下来想模仿sdl，把各个平台的窗口类统一封装起来。还得模仿UE底层，对基础类型的封装（便于跨平台，自己实现类型转化，尽量避免浮点数问题，字符统一用UTF-8）
v1.1:我准备借鉴the forge源码，但因为其比较复杂（编译流程很复杂，且不像sdl完全是C++写的）
所以我得一点一点改，目前我主要看forge的os文件夹，先实现各个平台的窗口。然后在main.cpp里调用窗口
v1.2:上面的那个1.1我没实现，现在用sokol库重新写（相当于一个更简单更高性能的GLFW）但是该库似乎不支持vulkan和openGL（linux平台似乎需要），也不支持各个游戏机操作系统
要仔细比较sokol和别的库，取其精华去其糟粕。比如它对各操作系统，各显卡api，各硬件的支持怎么样，性能高吗。sokol很基础，许多forge有的功能他都没有，我该怎么实现？实现完了forge的功能，我又应该怎么实现基础的mc。以及我写的代码是否适合mc这种沙盒游戏
v1.3:相当于一个新的v1.0，用sokol写了一个简单的窗口，但是键盘鼠标输入和渲染对我都有点问题
v1.4:我把.cpp改为了.c文件,我觉得底层的东西都应该用C写(就像sdl,bgfx一样).编译:clang main.c -o main 运行:.\main
目前还是没能搞好渲染和键盘鼠标事件
v1.5: 尝试渲染一些简单的基本图形，可以2D也可以3D

#define SOKOL_IMPL
#define SOKOL_D3D11//GLCORE33   // 也可以根据平台换成 SOKOL_D3D11 / SOKOL_METAL / SOKOL_GLES3
#define SOKOL_APP_IMPL
#define SOKOL_GFX_IMPL
#include "./sokol_app.h"

#define SOKOL_IMPL //或 #define SOKOL_GFX_IMPL
#include "sokol_gfx.h"
#define SOKOL_GLUE_IMPL
#include "sokol_glue.h"

typedef struct {
    float pos[2];
    float color[4];
} vertex_t;

vertex_t vertices[] = {
    {{ 0.0f,  0.5f}, {1,0,0,1}},
    {{-0.5f, -0.5f}, {0,1,0,1}},
    {{ 0.5f, -0.5f}, {0,0,1,1}}
};

const char* vs_src =
    "#version 330\n"
    "layout(location=0) in vec2 position;\n"
    "layout(location=1) in vec4 color;\n"
    "out vec4 vcolor;\n"
    "void main(){\n"
    "  gl_Position = vec4(position,0,1);\n"
    "  vcolor = color;\n"
    "}\n";

const char* fs_src =
    "#version 330\n"
    "in vec4 vcolor;\n"
    "out vec4 frag_color;\n"
    "void main(){ frag_color = vcolor; }\n";

sg_pipeline pip;
sg_bindings bind;
sg_pass_action pass_action;

void init(void) {
    sg_desc desc = {0};
    desc.environment = sglue_environment(); // 设置环境
    sg_setup(&desc);
    sg_shader shd = sg_make_shader(&(sg_shader_desc){
        .vs = {
            .source = vs_src,
        },
        .fs = {
            .source = fs_src,
        }
    });

    // buffers
    bind.vertex_buffers[0] = sg_make_buffer(&(sg_buffer_desc){
        .data = SG_RANGE(vertices)
    });

    // pipeline
    pip = sg_make_pipeline(&(sg_pipeline_desc){
        .shader = shd,
        .layout = {
            .attrs[0].format = SG_VERTEXFORMAT_FLOAT2,
            .attrs[1].format = SG_VERTEXFORMAT_FLOAT4,
        }
    });

    pass_action = (sg_pass_action){
        .colors[0] = { .load_action = SG_LOADACTION_CLEAR,
                       .clear_value = {0.2f,0.3f,0.4f,1} }
    };
}

void frame(void) {
    sg_pass pass = {
        .action = pass_action,
        .swapchain = sglue_swapchain()
    };

    sg_begin_pass(&pass);
    sg_apply_pipeline(pip);
    sg_apply_bindings(&bind);
    sg_draw(0, 3, 1);
    sg_end_pass();
    sg_commit();
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
