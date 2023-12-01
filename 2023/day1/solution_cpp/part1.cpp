#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <string_view>

int get_two_digit(std::string_view s) {
    // Find the first and last digits
    auto first_digit = std::find_if(s.begin(), s.end(), [](char c) { return std::isdigit(c); });
    auto last_digit = std::find_if(s.rbegin(), s.rend(), [](char c) { return std::isdigit(c); });

    if (first_digit == s.end() || last_digit == s.rend()) {
        throw std::invalid_argument("No digits found");
    }

    // Combine two digits into a string
    std::string two_digit{};
    two_digit += *first_digit;
    two_digit += *last_digit;
    
    // Convert the string to an integer
    return std::stoi(two_digit);
}

int main(int argc, const char* argv[]) {
    std::string s{};
    std::filesystem::path p{};
    if (argc == 1) {
        p = "./input.txt";
    } else {
        p = argv[1];
    }

    if (!std::filesystem::exists(p)) {
        throw std::invalid_argument("File does not exist");
    }

    // Open the file pointed to by p
    std::ifstream f{p};
    
    long sum{0};
    while (std::getline(f, s)) {
        sum += get_two_digit(s);
    }

    std::cout << "Sum = " << sum << std::endl;

    return 0;
}
