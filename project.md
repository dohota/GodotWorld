src/main.cpp：用于创建窗口，开始游戏（world）
    /world：
    world.cpp：管理system，entity，component，管理chunk
    chunk.c：管理chunk（一大组方块），block（单个方块）
    /core：
    input.c：输入系统
    render.c：渲染系统 （含ui绘制）
    system.cpp: 移动系统，战斗系统
    camera.c：
    shader.xx：OpenGL着色器等配置
    /gameobject：
    entity.cpp：允许增加删除组件，查找组件。用于创造实体（如玩家，掉落物等小东西，不适合创造百万个方块）
    component.c：实体的组件(一般都是结构体)

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
