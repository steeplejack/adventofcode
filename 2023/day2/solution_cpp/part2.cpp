#include <filesystem>
#include <fstream>
#include <iostream>
#include <ranges>

#include "day2.h"

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
    long power_sum{0};
    while (std::getline(file, line)) {
        auto spl = std::views::split(line, ':');
        if (spl.begin() != spl.end()) {
            auto it = spl.begin();
            auto game_id = std::string_view{*it};
            int id = std::stoi(std::string(game_id.substr(std::string{"Game "}.size(), 3)));

            it++;
            auto rest = std::string_view{*it};
            auto games = std::views::split(rest, ';');
            Game max_result{.id = id};
            for (auto games_it = games.begin(); games_it != games.end(); ++games_it) {
                Game game = game_result(std::string_view{*games_it}, id);
                if (game.red > max_result.red) { max_result.red = game.red; }
                if (game.green > max_result.green) { max_result.green = game.green; }
                if (game.blue > max_result.blue) { max_result.blue = game.blue; }
            }
            power_sum += max_result.power();
        }
    }

    std::cout << "Part 2\n";
    std::cout << "Power Sum = " << power_sum << std::endl;
    return 0;
}