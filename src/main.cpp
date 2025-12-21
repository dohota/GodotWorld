#include <SDL.h>
#include <SDL_opengl.h>   // macOS 上直接用这个
#include <iostream>

int main(int argc, char** argv)
{
    // 1. 初始化 SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        std::cerr << "SDL_Init error: " << SDL_GetError() << "\n";
        return 1;
    }

    // 2. 创建 OpenGL 窗口（使用兼容模式）
    SDL_Window* window = SDL_CreateWindow(
        "SDL + OpenGL Triangle",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        800, 600,
        SDL_WINDOW_OPENGL
    );

    if (!window) {
        std::cerr << "CreateWindow error: " << SDL_GetError() << "\n";
        return 1;
    }

    // 3. 创建 OpenGL 上下文
    SDL_GLContext glContext = SDL_GL_CreateContext(window);
    if (!glContext) {
        std::cerr << "CreateContext error: " << SDL_GetError() << "\n";
        return 1;
    }

    bool running = true;
    while (running) {
        // 4. 事件处理
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) {
                running = false;
            }
        }

        // 5. OpenGL 渲染
        glClearColor(0.1f, 0.1f, 0.15f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // 画一个三角形（老派但稳定）
        glBegin(GL_TRIANGLES);
            glColor3f(1.0f, 0.0f, 0.0f);
            glVertex2f(-0.5f, -0.5f);

            glColor3f(0.0f, 1.0f, 0.0f);
            glVertex2f( 0.5f, -0.5f);

            glColor3f(0.0f, 0.0f, 1.0f);
            glVertex2f( 0.0f,  0.5f);
        glEnd();

        // 6. 交换缓冲
        SDL_GL_SwapWindow(window);
    }

    // 7. 清理
    SDL_GL_DeleteContext(glContext);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
