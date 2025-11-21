v2.0: 抄袭了别人的吃豆人，学习基本的2D渲染，窗口，控制
编译：clang main.c -o main.exe
运行：./main

written in C99 using the sokol headers for platform abstraction.
    git repository:https://github.com/floooh/pacman.c
    WASM version:https://floooh.github.io/pacman.c/pacman.html

渲染和音频代码类似于原始 Pacman 街机硬件：
    1.图块和精灵像素数据、硬件调色板数据和声波表数据直接取自嵌入式街机 ROM 转储
    2.背景图块从两个 28x36 字节缓冲区（一个用于图块代码，另一个用于颜色代码）渲染，
    这类似于实际的街机，唯一的区别是图块和颜色缓冲区具有简单的线性内存布局
    3.背景图块渲染是通过动态上传的顶点数据（每个图块两个三角形）完成的，并在像素着色器中完成调色板解码
    4.最多 8 个 16x16 精灵被渲染为顶点四边形，像素着色器中发生与背景图块相同的调色板解码
    5.音频输出通过实际的 Namco WSG 模拟器进行工作，该模拟器从 20 位频率计数器、4 位音量和 3 位波形类型生成 3 个硬件语音的声音样本
    （对于由 32 个样本值组成的 8 个波表，每个波表存储在 ROM 转储中）
    6.音效是通过每 60Hz 滴答向硬件语音“寄存器”写入一次新值来实现的，这可以通过两种方式发生：
     作为“进程”音效，其中回调函数计算新的语音寄存器值
     或通过“寄存器转储”播放，其中语音寄存器值已从实际 Pacman 街机模拟器中以 60Hz 频率捕获
    7.只有两种音效是寄存器转储的：游戏开始时的小音乐曲目，以及吃豆人死亡时的音效。所有其他效果都是简单的进程效果

游戏代码中唯一值得解释的概念是计时和“异步操作”如何工作：
    1. 整个游戏逻辑由全局 60 Hz 向上计数的游戏滴答声驱动。
    2. 游戏动作是通过“时间触发器”和简单词汇的组合来启动的，以初始化和测试触发条件。
    这个时间触发系统是“适当”游戏引擎中更强大的事件系统的极其简单的替代品。
    翻译：(Gameplay actions are initiated by a combination of 'time triggers' and a simple
    vocabulary to initialize and test trigger conditions. This time trigger system
    is an extremely simple replacement for more powerful event systems in
    'proper' game engines.)

    以下是一些如何使用时间触发器的伪代码示例（与 Pacman 无关）：
    To immediately trigger an action in one place of the code, and 'realize'
    this action in one or several other places:

        // if a monster has been eaten, trigger the 'monster eaten' action:
        if (monster_eaten()) {
            start(&state.game.monster_eaten);
        }

        // ...somewhere else, we might increase the score if a monster has been eaten:
        if (now(state.game.monster_eaten)) {
            state.game.score += 10;
        }

        // ...and yet somewhere else in the code, we might want to play a sound effect
        if (now(state.game.monster_eaten)) {
            // play sound effect...
        }
    我们还可以在将来开始操作，这允许在一个地方批量处理多个后续操作：
        // start fading out now, after one second (60 ticks) start a new
        // game round, and fade in, after another second when fadein has
        // finished, start the actual game loop
        start(&state.gfx.fadeout);
        start_after(&state.game.started, 60);
        start_after(&state.gfx.fadein, 60);
        start_after(&state.game.gameloop_started, 2*60);

