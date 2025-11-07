cmake_minimum_required(VERSION 3.0)
project(MyCraft)
# 在 CMakeLists.txt 或 CLion CMake 选项中添加
set(CMAKE_RC_COMPILER "C:/Program Files (x86)/Windows Kits/10/bin/10.0.26100.0/x64/rc.exe" CACHE FILEPATH "Resource compiler")

set(CMAKE_CXX_STANDARD 11)

add_executable(MyCraft main.cpp)
