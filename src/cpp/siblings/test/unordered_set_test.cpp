#include "../unordered_set.hpp"
#include <cassert>
#include <string>

using namespace siblings;

namespace {
    const int int_data[] = { 1972, 1974, 2004, 2007, 1337, 1984, 2001, 1999,
                             1994, 2003 };
    const std::size_t int_data_size = sizeof(int_data) / sizeof(int_data[0]);

    const std::string string_data[] = { "green", "yellow", "blue", "red",
                                        "orange", "black", "white", "gray",
                                        "brown", "pink" };
    int string_data_size = sizeof(string_data) / sizeof(string_data[0]);

    void test_erase_absent_key()
    {
        typedef unordered_set<int> set_type;
        set_type s(&int_data[0], int_data + int_data_size);
        set_type::size_type old_size = s.size();
        set_type::size_type count = s.erase(1000);
        assert(count == 0);
        assert(s.size() == old_size);
    }

    void test_erase_present_key()
    {
        typedef unordered_set<int> set_type;
        set_type s(&int_data[0], int_data + int_data_size);
        set_type::size_type old_size = s.size();
        set_type::size_type count = s.erase(1337);
        assert(count == 1);
        assert(s.size() == old_size - count);
    }
}

int main()
{
    test_erase_absent_key();
    test_erase_present_key();
    return 0;
}
