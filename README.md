* World Space (世界坐标): 单位在游戏世界里的绝对像素位置。
 * Screen Space (屏幕坐标): 最终画在 Canvas 上的位置。
 * ScreenX = WorldX - CameraX + ScreenCenterX
 * WorldX  = ScreenX - ScreenCenterX + CameraX
每次进入终端请输入：source venv/bin/activate （激活虚拟环境）
这些操作都要cd warchess: 运行程序：python main.py。终止程序：在终端里control+c。git提交代码

v1.1:

从外部加载常量（类似json），然后形成一个类
滚轮滚动放大和缩小地图


实现鼠标移动至屏幕边缘自动移动地图
实现多种3D地形
按p键可隐藏ui，f12控制台也可操控游戏

该游戏有单人模式（偏向模拟经营，打ai，类似矮人要塞/rimworld/mc），也有多人模式（类似回合制的魔兽争霸，兵棋，文明6，维多利亚3）
之后项目大了肯定需要ecs架构。每个实体就只有一个id，通过挂载不同组件实现功能，便于生成大批量单位。系统用于处理各个组件
