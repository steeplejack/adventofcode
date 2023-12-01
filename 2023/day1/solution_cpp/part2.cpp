#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string_view>

// using digit_pair_type = std::pair<std::string, std::string>;
using digit_pair_type = std::pair<std::size_t, std::size_t>;

// Use a lookahead to get overlapping matches
static std::regex digit_regex{"(?=one|two|three|four|five|six|seven|eight|nine|[1-9])"};

/*
* Gets the first and last matching position in s of digit_regex
* */
digit_pair_type get_digit_pair(std::string_view s) {
    std::regex_iterator seek_begin{s.begin(), s.end(), digit_regex};
    decltype(seek_begin) seek_end{};
    if (std::distance(seek_begin, seek_end) == 0) {
        throw std::invalid_argument("Nothing found ):");
    }

    std::match_results first_match{*seek_begin};
    decltype(first_match) last_match;

    for (; seek_begin != seek_end; seek_begin++) {
        last_match = *seek_begin;
    }
    return digit_pair_type{first_match.position(), last_match.position()};
}

/*
* Given the i, the position of the start of the match, in s, the
* original string, reads just enough of the string to work out
* what number must have triggered the match
* */
int decode_match(std::string_view s, std::size_t i) {
    std::string prefix{s.substr(i, 2)};
    if (std::isdigit(prefix[0])) {
        return std::stoi(prefix.substr(0, 1));
    }
    std::map<std::string, int> m {
        {"on", 1}, {"tw", 2}, {"th", 3}, {"fo", 4}, {"fi", 5},
        {"si", 6}, {"se", 7}, {"ei", 8}, {"ni", 9}
    };
    return m.at(prefix);
}

/*
* Searches the string for digits, decodes the matches, and converts
* the result into a two-digit number
* */
int get_two_digit_number(std::string_view s) {
    digit_pair_type digits = get_digit_pair(s);
    return decode_match(s, digits.first) * 10 + decode_match(s, digits.second);
}

/*
* Not so satisfied with my solution here. I got caught out by the overlapping
* matches (e.g. ...twone...), so had to fix up the regex with a (?=...) pattern
* so it would still work. Unfortunately, this meant the convenient 
* match_result.str() I used to access the matching text stopped working. The 
* scrappy decode_match is the result.
* */ 
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
        sum += get_two_digit_number(s);
    }

    std::cout << "Sum = " << sum << std::endl;

    return 0;
}
