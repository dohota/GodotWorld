// int main(int argc, char** argv)
// {
//     // 1. 初始化 SDL
//     if (SDL_Init(SDL_INIT_VIDEO) != 0) {
//         std::cerr << "SDL_Init error: " << SDL_GetError() << "\n";
//         return 1;
//     }

//     // 2. 创建 OpenGL 窗口（使用兼容模式）
//     SDL_Window* window = SDL_CreateWindow(
//         "SDL + OpenGL Triangle",
//         SDL_WINDOWPOS_CENTERED,
//         SDL_WINDOWPOS_CENTERED,
//         800, 600,
//         SDL_WINDOW_OPENGL
//     );

//     if (!window) {
//         std::cerr << "CreateWindow error: " << SDL_GetError() << "\n";
//         return 1;
//     }

//     // 3. 创建 OpenGL 上下文
//     SDL_GLContext glContext = SDL_GL_CreateContext(window);
//     if (!glContext) {
//         std::cerr << "CreateContext error: " << SDL_GetError() << "\n";
//         return 1;
//     }

//     bool running = true;
//     while (running) {
//         // 4. 事件处理
//         SDL_Event e;
//         while (SDL_PollEvent(&e)) {
//             if (e.type == SDL_QUIT) {
//                 running = false;
//             }
//         }

//         // 5. OpenGL 渲染
//         glClearColor(0.1f, 0.1f, 0.15f, 1.0f);
//         glClear(GL_COLOR_BUFFER_BIT);

//         // 画一个三角形（老派但稳定）
//         glBegin(GL_TRIANGLES);
//             glColor3f(1.0f, 0.0f, 0.0f);
//             glVertex2f(-0.5f, -0.5f);

//             glColor3f(0.0f, 1.0f, 0.0f);
//             glVertex2f( 0.5f, -0.5f);

//             glColor3f(0.0f, 0.0f, 1.0f);
//             glVertex2f( 0.0f,  0.5f);
//         glEnd();

//         // 6. 交换缓冲
//         SDL_GL_SwapWindow(window);
//     }

//     // 7. 清理
//     SDL_GL_DeleteContext(glContext);
//     SDL_DestroyWindow(window);
//     SDL_Quit();

//     return 0;
// }
#include <SDL.h>
#include <SDL_opengl.h> // macOS 上直接用这个
#include <iostream>
#include <cmath>
//#include <OpenGL/glu.h> //在 macOS 上，必须额外 include GLU，半弃用的状态
void setPerspective(float fov, float aspect, float zNear, float zFar) {
    float fH = std::tan(fov * 0.5f * M_PI / 180.0f) * zNear;
    float fW = fH * aspect;

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glFrustum(-fW, fW, -fH, fH, zNear, zFar);
    glMatrixMode(GL_MODELVIEW);
}

void setupProjection(int w, int h) {
    glViewport(0, 0, w, h);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    float aspect = (float)w / (float)h;
    setPerspective(60.0, aspect, 0.1, 100.0);

    glMatrixMode(GL_MODELVIEW);
}

void drawCube() {
    glBegin(GL_QUADS);

    // Front
    glColor3f(1, 0, 0);
    glVertex3f(-1, -1,  1);
    glVertex3f( 1, -1,  1);
    glVertex3f( 1,  1,  1);
    glVertex3f(-1,  1,  1);

    // Back
    glColor3f(0, 1, 0);
    glVertex3f(-1, -1, -1);
    glVertex3f(-1,  1, -1);
    glVertex3f( 1,  1, -1);
    glVertex3f( 1, -1, -1);

    // Left
    glColor3f(0, 0, 1);
    glVertex3f(-1, -1, -1);
    glVertex3f(-1, -1,  1);
    glVertex3f(-1,  1,  1);
    glVertex3f(-1,  1, -1);

    // Right
    glColor3f(1, 1, 0);
    glVertex3f( 1, -1, -1);
    glVertex3f( 1,  1, -1);
    glVertex3f( 1,  1,  1);
    glVertex3f( 1, -1,  1);

    // Top
    glColor3f(0, 1, 1);
    glVertex3f(-1,  1, -1);
    glVertex3f(-1,  1,  1);
    glVertex3f( 1,  1,  1);
    glVertex3f( 1,  1, -1);

    // Bottom
    glColor3f(1, 0, 1);
    glVertex3f(-1, -1, -1);
    glVertex3f( 1, -1, -1);
    glVertex3f( 1, -1,  1);
    glVertex3f(-1, -1,  1);

    glEnd();
}

int main(int argc, char** argv) {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow(
        "Rotating Cube",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        800, 600,
        SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE
    );

    SDL_GLContext context = SDL_GL_CreateContext(window);

    glEnable(GL_DEPTH_TEST);
    glClearColor(0.1f, 0.1f, 0.15f, 1.0f);

    int w, h;
    SDL_GetWindowSize(window, &w, &h);
    setupProjection(w, h);

    bool running = true;
    float angle = 0.0f;

    while (running) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT)
                running = false;

            if (e.type == SDL_WINDOWEVENT &&
                e.window.event == SDL_WINDOWEVENT_SIZE_CHANGED) {
                setupProjection(e.window.data1, e.window.data2);
            }
        }

        angle += 0.03f;//调整旋转速度

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glLoadIdentity();
        glTranslatef(0.0f, 0.0f, -6.0f);
        glRotatef(angle, 1.0f, 1.0f, 0.0f);

        drawCube();

        SDL_GL_SwapWindow(window);
    }

    SDL_GL_DeleteContext(context);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
