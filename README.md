* World Space (世界坐标): 单位在游戏世界里的绝对像素位置。
 * Screen Space (屏幕坐标): 最终画在 Canvas 上的位置。
 * ScreenX = WorldX - CameraX + ScreenCenterX
 * WorldX  = ScreenX - ScreenCenterX + CameraX
每次进入终端请输入：source venv/bin/activate （激活虚拟环境）
这些操作都要cd warchess: 运行程序：python main.py。终止程序：在终端里control+c。git提交代码

v1.1:
基本按照ecs架构：（并且要注意性能）
main.py：world类：负责管理所有的system
entity.py：实体类：允许增加删除组件，查找组件
component.py：各种组件类：只保存数据

camera.py：照相机系统
input.py：输入系统
math.py：静态数学函数，负责各种运算啥的
render.py：渲染系统

turn.py/save.py：单人（偏向模拟经营，打ai，类似矮人要塞/rimworld/mc）多人（类似回合制的魔兽争霸，兵棋，文明6，维多利亚3），切换回合，复盘游戏
gameobject：用于创造初始化各种单位地图啥的。。（可能会比较多余）
console.py：按p键可隐藏ui，f12控制台也可操控游戏

滚轮滚动放大和缩小地图
实现鼠标移动至屏幕边缘自动移动地图
实现多种3D地形
