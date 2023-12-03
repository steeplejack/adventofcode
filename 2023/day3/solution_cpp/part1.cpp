#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <ranges>
#include <vector>

#include "util.h"

using NumberMap = std::map<int, std::vector<Number>>;
using SymbolMap = std::map<int, std::vector<Symbol>>;

void check_collisions(NumberMap& numbers, SymbolMap& symbols) {
    auto max_number_key = std::ranges::max(numbers | std::views::keys);
    auto max_symbol_key = std::ranges::max(symbols | std::views::keys);
    int maxrow = std::max(max_number_key, max_symbol_key);
    for (auto& [row, svec]: symbols) {
        for (Symbol& symbol: svec) {
            for (int rownum = row - 1; rownum < row + 2; ++rownum) {
                if (rownum < 0 || rownum > maxrow) { continue; }
                for (auto& number : numbers[rownum]) {
                    number.collides(&symbol);
                }
            }
        }
    }
}

int main(int argc, const char* argv[]) {
    std::filesystem::path input{};
    if (argc == 1) {
        input = "../input.txt";
    } else {
        input = argv[1];
    }

    if (!std::filesystem::exists(input)) {
        std::cerr << "Input file " << input << " does not exist\n";
        return 1;
    }

    std::string line{};
    std::ifstream file{ input };

    std::map<int, std::vector<Number>> numbers{};
    std::map<int, std::vector<Symbol>> symbols{};

    int row{ 0 };
    while (std::getline(file, line)) {
        auto char_iter = line.begin();
        while (char_iter != line.end()) {
        if (is_digit(*char_iter)) {
            int start{ static_cast<int>(
                std::distance(line.begin(), char_iter)) };
            int val = parse_number(char_iter);
            int end{ static_cast<int>(std::distance(line.begin(), char_iter)) };
            numbers[row].push_back(Number{ val, row, start, end });
        } else if (*char_iter != '.') {
            int col{ static_cast<int>(std::distance(line.begin(), char_iter)) };
            char val{ *char_iter };
            Symbol symbol{ .value = val, .row = row, .col = col };
            symbols[row].push_back(symbol);
        }
        char_iter++;
        }
        row++;
    }

    check_collisions(numbers, symbols);

    int sum{0};
    for (auto [row, nvec]: numbers) {
        for (auto& n: nvec) {
            if (n.collisions.size() > 0) {
                sum += n.value;
            }
        }
    }

    int part2_sum{0};
    for (auto [row, svec]: symbols) {
        for (auto& s: svec) {
            int prod = 1;
            if (s.value == '*' && s.collisions.size() == 2) {
                for (Number* number: s.collisions) {
                    prod *= number->value;
                }
                part2_sum += prod;
            }
        }
    }

    std::cout << "Part 1 sum = " << sum << '\n';
    std::cout << "Part 2 sum = " << part2_sum << '\n';

    return 0;
}
