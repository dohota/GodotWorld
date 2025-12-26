#### 1
有了vcpkg.json：vcpkg 自动进入 manifest 模式, VS Code + CMake Tools 会自动配合：
✅ 不用手动执行 vcpkg install xxx
✅ 只改 vcpkg.json
✅ CMake / VS Code 会自动下载、自动删除

### 2
vcpkg 所管理的库叫 ports
每个库都有一个目录和配置文件（portfile.cmake），指定：
源码 URL（通常是 GitHub、官方 release 压缩包）
依赖的其他库
构建选项（CMake、编译宏、patch 等）

### 3
该项目配置：目前用的是m4系列的macos，ide用vscode（装了clangd和cmake的插件）
brew下载了cmake，ninja，vcpkg，然后项目好像就能自动识别了
点击左下角的启动按钮，就能自动启动项目了

## google项目代码规范：
每行代码不过长，尽量避免ascii字符（除了注释）
预处理，条件编译永远顶格写，不要缩进
为了让github上的人/自己以后也能看懂自己的代码，所以要写注释
文件注释：在开头加入版权公告（许可证+版本）
//todo 表示接下来要做的功能
//deprecated表示该功能被弃用
命名空间/文件名/变量/函数参数/数据成员：只用小写字母和下划线
类/结构体/typedef/枚举/类型模版参数/函数：只用字母，且单词首字母大写
宏：只用大写字母和下划线 （c++不要像c一样喜欢用宏，尽量用内联函数，枚举，常量代替）
类成员变量：要以下划线结尾。const类型常量：开头加上k，合理使用const特别好，可以用constexpr。最高级命名空间名字即为项目名称
几乎别用缺省参数。尽量用函数重载。不用变长数组和allocoa（）。空指针用nullptr
尽量用 <stdint.h> 里的类型。就算都是正数，也少用无符号整型。空字符用'\0'。auto只用于局部变量
可以将非成员函数放入某个命名空间里用。只把小于10行的函数定义为内联
一般都需要头文件保护：防止互相循环调用

## 项目构思：
先用sdl2+opengl，然后可以试试加上openal和raknet/boost.asio,ui就使用imgui，物理引擎也可以抄开源的
再试试换用sdl3/glfw是什么效果（可以仿照minetest的代码）
接下来再试试用bgfx/filament换掉opengl，然后用the forge来写（性能很好），最后全都自己手写，可以参考sokol库
构建方面暂定：cmake+ninja+vcpkg，等项目超过十万行再考虑别的

底层和操作系统/硬件打交道的代码用c语言，上层用c++ ecs架构，其中chunk会特殊一点，一堆方块视为一个entity
## v1.x:
src/main.cpp：用于创建窗口，开始游戏（world）

    /world：
    world.cpp：管理system，entity，component，管理chunk
    chunk.c：管理chunk（一大组方块），block（单个方块）

    /system：
    input.c：输入系统
    render.c：渲染系统 （含ui绘制）
    system.cpp: 移动系统，战斗系统
    camera.c：
    shader.xx：OpenGL着色器等配置

    /gameobject：
    entity.cpp：允许增加删除组件，查找组件。用于创造实体（如玩家，掉落物等小东西，不适合创造百万个方块）
    component.c：实体的组件(一般都是结构体)

    /util：
    math.c：有关数学类的

    /core：
    # 有关窗口，输入，声音，渲染的底层库，之后这里可以放sokol文件

### 之后项目再大，可以写成这样：
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

## v1.2:
...
