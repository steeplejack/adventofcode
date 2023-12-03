cmake_minimum_required(VERSION 3.10)
project(AdventOfCode2023)
set(CMAKE_CXX_STANDARD 23)
add_executable(part1 part1.cpp
        util.h
        util.cpp)
add_executable(part2 part2.cpp
        util.h
        util.cpp)
