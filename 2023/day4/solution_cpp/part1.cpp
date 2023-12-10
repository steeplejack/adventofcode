#include <filesystem>
#include <fstream>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

#include "util.h"

namespace fs = std::filesystem; 

int check_card(std::string_view line) {
    auto spl = line | std::views::split(':') | std::views::drop(1);
    auto xx = spl | std::views::transform([](auto subrange) {
        return subrange | std::views::split('|');
    });
    for (auto&& item : xx) {
        for (auto&& subitem : item) {
            std::cout << "zxcx" << std::string(subitem) << '\n';
        }
    }
    // |
    //     std::views::transform([](auto&& subrange) {
    //         return subrange | std::views::split('|');
    //     });
    // for (auto&& item : spl) {
    //     for (auto&& subrange : item) {
    //         std::cout << std::string(subrange) << std::endl;
    //     }
    // }
    return 0;
}

std::vector<int> preprocess_file(fs::path infile) {
    std::string line{};
    std::ifstream file{infile};
    std::vector<int> result{};
    while (std::getline(file, line)) {
        result.push_back(check_card(line));
    }
    return result;
}

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

    std::string line{"Card   1: 42 68 56  3 28 97  1 78 55 48 | 78 54  3 38 94 73 72 57 51 31 86 43  7 81  4 27 26 58 75 69 74 55  5 28 40"};
    check_card(line);
    return 0;
}
