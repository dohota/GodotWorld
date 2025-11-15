#define SOKOL_IMPL
#define SOKOL_D3D11//GLCORE33   // 也可以根据平台换成 SOKOL_D3D11 / SOKOL_METAL / SOKOL_GLES3
#define SOKOL_APP_IMPL
#define SOKOL_GFX_IMPL
#include "./sokol_gfx.h"
#include "./sokol_app.h"

// // sg_swapchain d3d11_swapchain(void) {
// //     return (sg_swapchain){
// //         .width = state.width,
// //         .height = state.height,
// //         .sample_count = state.sample_count,
// //         .color_format = SG_PIXELFORMAT_BGRA8,
// //         .depth_format = state.no_depth_buffer ? SG_PIXELFORMAT_NONE : SG_PIXELFORMAT_DEPTH_STENCIL,
// //         .d3d11 = {
// //             .render_view = (state.sample_count == 1) ? state.rt_view : state.msaa_view,
// //             .resolve_view = (state.sample_count == 1) ? 0 : state.rt_view,
// //             .depth_stencil_view = state.ds_view,
// //         }
// //     };
// // }

// static void frame(void) {
//     sg_pass_action pass = {};
//     pass.colors[0].load_action = SG_LOADACTION_CLEAR;  // 使用枚举值赋值
//     pass.colors[0].clear_value = (sg_color){0.2f, 0.3f, 0.4f, 1.0f};  // 使用正确的类型赋值
    
//     //sg_begin_pass(&pass,{ .action = pass_action, .swapchain = d3d11_swapchain() });
//     sg_begin_default_pass(&pass, sapp_width(), sapp_height());
//     sg_end_pass();
//     sg_commit();
// }
static void init(void) {
    // 在此初始化您的应用
    sg_desc desc = {};  // 创建一个 sg_desc 变量
    sg_setup(&desc);     // 传递这个变量的地址
    //sg_setup(&(sg_desc){0});
}
 
static void frame(void) {
    // 在此渲染一帧
}
 
static void cleanup(void) {
    // 在此清理资源
    sg_shutdown();
}
 
// static void event(const sapp_event* ev) {
//     // 在此处理输入事件
//     switch (ev->type) {
//         case SAPP_EVENTTYPE_KEY_DOWN:
//             if (ev->key_code == SAPP_KEYCODE_ESCAPE) {
//                 sapp_request_quit();
//             }
//             break;
            
//         case SAPP_EVENTTYPE_MOUSE_DOWN:
//             if (ev->mouse_button == SAPP_MOUSEBUTTON_LEFT) {
//                 sapp_lock_mouse(true);  // 启用鼠标视角
//             }
//             break;
            
//         case SAPP_EVENTTYPE_MOUSE_MOVE:
//             if (sapp_mouse_locked()) {
//                 // 使用相对移动控制相机
//                 float dx = ev->mouse_dx;
//                 float dy = ev->mouse_dy;
//                 // 更新相机...
//             }
//             break;
            
//         case SAPP_EVENTTYPE_RESIZED:
//             // 处理窗口大小调整
//             int new_width = sapp_width();
//             int new_height = sapp_height();
//             break;
            
//         // case SAPP_EVENTTYPE_QUIT_REQUESTED:
//         //     // 显示"真的要退出吗？"对话框或直接退出
//         //     sapp_quit();
//         //     break;
//     }
// }
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
