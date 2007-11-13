#include "../unordered_set.hpp"
#include <cassert>
#include <set>
#include <string>

using namespace siblings;

namespace {
    const int int_data[] = { 1972, 1974, 2004, 2007, 1337, 1984, 2001, 1999,
                             1994, 2003 };
    const std::size_t int_count = sizeof(int_data) / sizeof(int_data[0]);
    const int* const first_int = int_data + 0;
    const int* const last_int = int_data + int_count;

    const std::string string_data[] = { "green", "yellow", "blue", "red",
                                        "orange", "black", "white", "gray",
                                        "brown", "pink" };
    int string_count = sizeof(string_data) / sizeof(string_data[0]);
    // const std::string* const first_string = string_data + 0;
    // const std::string* const last_string = string_data + string_count;

    template <class Value, class Hash, class Pred, class Alloc>
    bool equal(unordered_set<Value, Hash, Pred, Alloc>& x,
               unordered_set<Value, Hash, Pred, Alloc>& y)
    {
        return x.size() == y.size()
            && std::equal(x.begin(), x.end(), y.begin());
    }

    void test_default_ctor()
    {
        unordered_set<int> s;
        assert(s.empty());
        assert(s.size() == 0);
        assert(s.begin() == s.end());
    }

    void test_range_ctor()
    {
        unordered_set<int> s(first_int, last_int);
        assert(std::set<int>(s.begin(), s.end())
               == std::set<int>(first_int, last_int));
    }

    void test_copy_ctor()
    {
        unordered_set<int> s(first_int, last_int), t(s);
        assert(equal(s, t));
    }

    void test_erase_absent_key()
    {
        typedef unordered_set<int> set_type;
        set_type s(first_int, last_int);
        set_type::size_type old_size = s.size();
        set_type::size_type count = s.erase(1000);
        assert(count == 0);
        assert(s.size() == old_size);
    }

    void test_erase_present_key()
    {
        typedef unordered_set<int> set_type;
        set_type s(first_int, last_int);
        set_type::size_type old_size = s.size();
        set_type::size_type count = s.erase(1337);
        assert(count == 1);
        assert(s.size() == old_size - count);
    }
}

int main()
{
    test_default_ctor();
    test_range_ctor();
    test_copy_ctor();
    test_erase_absent_key();
    test_erase_present_key();
    return 0;
}
