有了vcpkg.json：vcpkg 自动进入 manifest 模式, VS Code + CMake Tools 会自动配合：
✅ 不用手动执行 vcpkg install xxx
✅ 只改 vcpkg.json
✅ CMake / VS Code 会自动下载、自动删除

vcpkg 所管理的库叫 ports
每个库都有一个目录和配置文件（portfile.cmake），指定：
源码 URL（通常是 GitHub、官方 release 压缩包）
依赖的其他库
构建选项（CMake、编译宏、patch 等）

该项目配置：目前用的是m4系列的macos，ide用vscode（装了clangd和cmake的插件）
brew下载了cmake，ninja，vcpkg，然后项目好像就能自动识别了

点击左下角的启动按钮，就能自动启动项目了

v1.1:
