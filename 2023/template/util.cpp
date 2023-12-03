#include "util.h"

std::ostream& operator<<(std::ostream& os, const AoC& aoc) {
    os << "Day: " << aoc.day << " Year: " << aoc.year << '\n';
    return os;
}
