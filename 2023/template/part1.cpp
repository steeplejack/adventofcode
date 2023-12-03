#include <filesystem>
#include <fstream>
#include <iostream>
#include <ranges>

#include "util.h"

int main(int argc, const char* argv[]) {
    std::filesystem::path input{};
    if (argc == 1) {
        input = "../input.txt";
    } else {
        input = argv[1];
    }

    if (!std::filesystem::exists(input)) {
        throw std::invalid_argument("Input file does not exist");
    }

    std::string line{};
    std::ifstream file{input};

    int n_lines{0};
    while (std::getline(file, line)) {
        n_lines++;
    }

    std::cout << "Part 1\n";
    std::cout << "Total lines in input = " << n_lines << std::endl;
    return 0;
}
