#pragma once

struct Game {
    int id{0};
    int red{0};
    int green{0};
    int blue{0};

    int power();
};

std::ostream& operator<<(std::ostream& os, const Game& game);

Game game_result(std::string_view s, int id);
