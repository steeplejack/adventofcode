#include <iostream>
#include <ranges>
#include "day2.h"

int Game::power() {
    return red * green * blue;
}

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