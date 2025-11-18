#define SOKOL_IMPL
#define SOKOL_D3D11//GLCORE33   // 也可以根据平台换成 SOKOL_D3D11 / SOKOL_METAL / SOKOL_GLES3
#define SOKOL_APP_IMPL
#define SOKOL_GFX_IMPL
#include "./sokol_gfx.h"
#include "./sokol_app.h"
// 顶点数据结构
typedef struct {
    float position[2];
    float color[4];
} vertex_t;
// 定义一个简单的三角形顶点数据
vertex_t vertices[] = {
    {{ 0.0f,  0.5f}, {1.0f, 0.0f, 0.0f, 1.0f}}, // 顶部，红色
    {{-0.5f, -0.5f}, {0.0f, 1.0f, 0.0f, 1.0f}}, // 左下，绿色
    {{ 0.5f, -0.5f}, {0.0f, 0.0f, 1.0f, 1.0f}}  // 右下，蓝色
};
// 顶点着色器
const char* vertex_shader = R"(
    #version 330 core
    layout(location = 0) in vec2 position;
    layout(location = 1) in vec4 color;
    out vec4 frag_color;
    void main() {
        gl_Position = vec4(position, 0.0, 1.0);
        frag_color = color;
    }
)";
// 片段着色器
const char* fragment_shader = R"(
    #version 330 core
    in vec4 frag_color;
    out vec4 color;
    void main() {
        color = frag_color;
    }
)";
// 创建管线和缓冲区
sg_pipeline pip;
sg_buffer vertex_buffer;
sg_buffer index_buffer;
sg_shader shader;
sg_pass_action pass_action;

// 在此初始化您的应用
static void init(void) {
    sg_desc desc = {0};
    sg_setup(&desc);     // 传递这个sg_desc变量的地址
    // 创建着色器
    shader = sg_make_shader((sg_shader_desc){
        .vs.source = vertex_shader,
        .fs.source = fragment_shader
    });
    
    // 创建顶点缓冲区
    vertex_buffer = sg_make_buffer(&(sg_buffer_desc){
        .size = sizeof(vertices),
        .usage = SG_USAGE_STATIC,
        .data = SG_RANGE(vertices)
    });
    // 创建索引缓冲区
    static const uint16_t indices[] = {0, 1, 2};
    index_buffer = sg_make_buffer(&(sg_buffer_desc){
        .size = sizeof(indices),
        .usage = SG_USAGE_STATIC,
        .data = SG_RANGE(indices)
    });
    // 创建渲染管线
    pip = sg_make_pipeline(&(sg_pipeline_desc){
        .shader = shader,
        .layout = {
            .attrs = {
                [0] = { .format = SG_VERTEXFORMAT_FLOAT2 },  // 顶点位置
                [1] = { .format = SG_VERTEXFORMAT_FLOAT4 }   // 顶点颜色
            }
        }
    });
    // 设置清除背景颜色
    pass_action = (sg_pass_action){
        .colors[0] = { .load_action = SG_LOADACTION_CLEAR, .clear_value = {0.2f, 0.3f, 0.4f, 1.0f} }
    };
}
// 在此渲染一帧
static void frame(void) {
    // 开始渲染
    sg_begin_pass(&pass_action);
    // 应用管线
    sg_apply_pipeline(pip);
    sg_apply_bindings(&(sg_bindings){
        .vertex_buffers[0] = vertex_buffer,
        .index_buffer = index_buffer
    });
    // 绘制三角形
    sg_draw(0, 3, 1);  // 3个顶点，1个绘制实例
    // 结束渲染
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
