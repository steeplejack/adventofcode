#include <filesystem>
#include <fstream>
#include <iostream>
#include <ranges>

struct Game {
    int id{0};
    int red{0};
    int green{0};
    int blue{0};
};

std::ostream& operator<<(std::ostream& os, const Game& game) {
    os << "Game{id=" << game.id << ",red=" << game.red
       << ",green=" << game.green << ",blue=" << game.blue
       << "}";
    return os;
}

Game game_result(std::string_view s, int id) {
    Game game{.id = id};
    auto objects = std::views::split(s, ',');
    for (auto&& it: objects) {
        auto colour_it = std::views::split(std::string_view(it), ' ');
        auto begin = colour_it.begin();
        auto count = std::stoi(std::string{std::string_view{*(++begin)}});
        auto colour = std::string_view(*(++begin));
        if (colour == "red") { game.red = count; }
        if (colour == "green") { game.green = count; }
        if (colour == "blue") { game.blue = count; }
    }
    return game;
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

    std::string line{};
    std::ifstream file{input};
    long sum{0};
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
            if (max_result.red <= 12 && max_result.green <= 13 && max_result.blue <= 14) {
                sum += max_result.id;
            }
        }
    }

    std::cout << "Sum = " << sum << std::endl;
    return 0;
}