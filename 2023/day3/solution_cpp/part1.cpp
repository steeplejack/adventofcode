#include <filesystem>
#include <fstream>
#include <iostream>
#include <ranges>
#include <vector>

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
    std::ifstream file{ input };

    std::vector<Number> numbers{};
    std::vector<Symbol> symbols{};

    int row{ 0 };
    while (std::getline(file, line)) {
        auto char_iter = line.begin();
        while (char_iter != line.end()) {
            if (is_digit(*char_iter)) {
                int start{ static_cast<int>(
                    std::distance(line.begin(), char_iter)) };
                int val = parse_number(char_iter);
                int end{ static_cast<int>(
                    std::distance(line.begin(), char_iter)) };
                numbers.push_back(Number{ val, row, start, end });
            }
            else if (*char_iter != '.') {
                int col{ static_cast<int>(
                    std::distance(line.begin(), char_iter)) };
                char val{*char_iter};
                Symbol symbol{.value = val, .row = row, .col = col};
                symbols.push_back(symbol);
            }
            char_iter++;
        }
        row++;
    }

    for (Number& n: numbers) { std::cout << n << '\n'; }
    for (Symbol& s: symbols) { std::cout << s << '\n'; }

    std::cout << "Part 1\n";

    return 0;
}
