#include <cctype>
#include "util.h"

std::ostream& operator<<(std::ostream& os, const Number& number) {
    os << "Number: " << number.value << " : (" << number.row << ", ("
       << number.start << '-' << number.end << "))";
    return os;
}

std::ostream& operator<<(std::ostream& os, const Symbol& symbol) {
    os << "Symbol: " << symbol.value << " : (" << symbol.row << ", "
       << symbol.col << ")";
    return os;
}

bool is_digit(char c) {
    return std::isdigit(static_cast<unsigned char>(c));
}

int parse_number(std::string::iterator& it) {
    std::string val{};
    while (is_digit(*it)) { val += *(it++); }
    --it;
    return std::stoi(val);
}
