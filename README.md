每次进入终端请输入：source venv/bin/activate （激活虚拟环境）
这些操作都要cd warchess: 运行程序：python main.py。终止程序：在终端里control+c。git提交代码
v1.2:
基本按照ecs架构：（并且要注意性能）
main.py：world类：负责管理所有的system。一开始进去什么都没有
entity.py：实体类：允许增加删除组件，查找组件。用于创造初始化各种单位地图啥的。。
component.py：各种组件类：只保存数据，包含camera.py：照相机组件
input.py：输入系统
setting.py：各种全局设置，静态数学函数，控制台，ui相关
render.py：渲染系统 （含ui绘制）
turn.py：单人（偏向模拟经营，打ai，类似矮人要塞/rimworld/mc）多人（类似回合制的魔兽争霸，兵棋，文明6，维多利亚3），能像sabaki跳转至任何节点

实现鼠标移动至屏幕边缘自动移动地图

坐标体系
世界坐标：真实兵棋的3d坐标，很精确
屏幕坐标：渲染在窗口上的坐标。其中还有地图坐标：专门表示渲染到哪一个六角格上的坐标
