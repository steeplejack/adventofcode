#pragma once
#include <iostream>

struct Number {
    int value{0};
    int row{0};
    int start{0};
    int end{0};
};

std::ostream& operator<<(std::ostream& os, const Number& number);

struct Symbol {
    char value{0};
    int row{0};
    int col{0};
};

std::ostream& operator<<(std::ostream& os, const Symbol& symbol);

bool is_digit(char ch);

int parse_number(std::string::iterator& it);