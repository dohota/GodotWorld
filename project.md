先用sdl2+opengl，然后可以试试加上openal和raknet/boost.asio。再试试换用sdl3/glfw是什么效果（可以仿照minetest的代码）
接下来再试试用bgfx/filament换掉opengl，然后用the forge来写（性能很好），最后全都自己手写，可以参考sokol库
构建方面暂定：cmake+ninja+vcpkg，等项目超过十万行再考虑别的

超大项目构建：
在各个主流平台上都能运行，甚至裸机也可运行，适配任何硬件，并且完全支持交叉编译，有像ccache/sccache的编译缓存。自制+改装硬件：mc游戏机
自研游戏引擎+内置ide，引擎内自带构建工具：
支持多种编程语言，但也不过多；像ubt，bazel一样性能好/功能全面；并且要像bazel一样同样的输入、同样的环境，总能得到相同的输出
包管理器（可能用vcpkg，也可手动管理），编译器（用clang+llvm，或基于此自己定制）
尽量锁死c/c++的版本，锁死编译器的类型，版本，不然会出现bug。最好只有引擎版本变

用户点击 Setup.bat
        ↓
【准备环境】
  - 检查 OS / 架构
  - 检查编译器 / SDK
  - 下载第三方依赖
  - 设置环境变量
        ↓
【生成构建工具所需文件】
  - 生成 .sln / .xcodeproj
  - 或生成 CMake/Bazel 配置
        ↓
【结束】

项目架构：
除了chunk，部分底层渲染之外，基本按照ecs架构

src/main.py：用于启动世界，创建游戏（world）
    /world：
    world.py：管理system，entity，component，管理chunk
    chunk.py：管理chunk（一大组方块），block（单个方块）
    /core：
    input.py：输入系统
    render.py：渲染系统 （含ui绘制）
    system.py: 移动系统，战斗系统
    camera.py：
    shader.py：OpenGL着色器等配置
    /gameobject：
    entity.py：允许增加删除组件，查找组件。用于创造实体（如玩家，掉落物等小东西，不适合创造百万个方块）
    component.py：实体的组件

之后项目再大，可以写成这样：
<!-- world/
 ├── world.py        
 ├── ecs.py          # entity / component / system 管理
 ├── chunk_manager.py
 ├── event_bus.py    #事件系统，job system什么的 --> 事件总线让系统间只通过“事件”通信，降低依赖
一个chunk是一个实体，包含很多block。特殊block可被当作实体
 world/
 ├── world.py  # 生命周期 & 总调度
 ├── chunk.py
 ├── chunk_manager.py
 ├── block.py
 ├── block_registry.py
 ├── world_gen.py
 ├── save_load.py

ecs/
 ├── entity.py
 ├── component.py
 ├── system.py
 ├── ecs_world.py

gameobject/
 ├── player.py
 ├── item_entity.py
 ├── components/
 │   ├── transform.py
 │   ├── velocity.py
 │   ├── collider.py
 │   ├── health.py
 │   ├── inventory.py
 │   └── camera.py

systems/
 ├── input_system.py
 ├── movement_system.py
 ├── collision_system.py
 ├── gravity_system.py
 ├── combat_system.py
 ├── pickup_system.py

render/
 ├── renderer.py
 ├── camera.py
 ├── chunk_renderer.py
 ├── mesh_builder.py
 ├── block_texture_atlas.py
 ├── entity_renderer.py
 ├── ui_renderer.py
 └── debug_draw.py

utils/
 ├── math.py
 ├── aabb.py
 ├── raycast.py
 ├── timer.py
 ├── config.py //各种全局配置

core/
 ├── input.py
 ├── keybinds.py
 ├── ui/
 │   ├── inventory_ui.py
 │   ├── hotbar.py
 │   └── crosshair.py
