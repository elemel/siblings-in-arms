#include "../unordered_map.hpp"
#include "../unordered_set.hpp"
#include <cassert>
#include <string>

using namespace siblings;

namespace {
    const int int_data[] = { 1972, 1974, 2004, 2007, 1337, 1984, 2001, 1999,
                             1939, 1945 };
    const std::size_t int_data_size = sizeof(int_data) / sizeof(int_data[0]);

    const std::string string_data[] = { "green", "yellow", "blue", "red",
                                        "orange", "black", "white", "gray",
                                        "brown", "pink" };
    int string_data_size = sizeof(string_data) / sizeof(string_data[0]);

    void test_default_ctor()
    {
        unordered_map<int, std::string> m;
        assert(m.size() == 0);
        assert(m.empty());
    }

    void test_insert_value()
    {
        typedef unordered_map<int, std::string> map_type;
        typedef map_type::value_type value_type;
        typedef std::pair<map_type::iterator, bool> insert_result;

        map_type m;
        for (int i = 0; i < 10; ++i) {
            assert(int(m.size()) == i);
            assert(m.find(int_data[i]) == m.end());
            insert_result r = m.insert(value_type(int_data[i],
                                                  string_data[i]));
            assert(r.second);
            assert(int(m.size()) == i + 1);
            assert(m.find(int_data[i]) != m.end());
        }
    }

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

    void test_index()
    {
        typedef unordered_map<int, std::string> map_type;

        map_type m;
        map_type::iterator i;

        assert(m.find(13) == m.end());
        m[13] = "black";
        i = m.find(13);
        assert(i != m.end());
        assert(i->first == 13);
        assert(i->second == "black");
        assert(m.find(17) == m.end());
    }
}

int main()
{
    // test_iteration();
    // test_const_iteration();
    // test_size();
    // test_max_size();
    // test_empty();
    // test_bucket_count();
    // test_resize();
    // test_hash_funct();
    // test_key_eq();
    test_default_ctor();
    // test_range_ctor();
    // test_copy_ctor();
    // test_assign();
    // test_swap();
    test_insert_value();
    // test_insert_range();
    // test_erase_iterator();
    test_erase_absent_key();
    test_erase_present_key();
    // test_erase_range();
    // test_clear();
    // test_const_find();
    // test_find();
    // test_count();
    // test_const_equal_range();
    // test_equal_range();
    test_index();
    // test_equal();
    return 0;
}
