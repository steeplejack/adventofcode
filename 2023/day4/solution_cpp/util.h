#pragma once
#include <iostream>

struct AoC {
    int day{0};
    int year{2023};
};

std::ostream& operator<<(std::ostream& os, const AoC& aoc);

