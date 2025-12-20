每次进入终端请输入：source venv/bin/activate （激活虚拟环境）
这些操作都要cd myworld: 运行程序：python main.py。终止程序：在终端里control+c。git提交代码

项目架构：
pygame+opengl+pyopenal（使用复杂，可以先就用pygame原生声音模块）+asyncio+uvloop +numpy（储存大量方块，性能很好）
除了chunk，部分底层渲染之外，基本按照ecs架构

v1.1:
