#include "../unordered_map.hpp"
#include "../unordered_set.hpp"
#include <cassert>
#include <string>

using namespace siblings;

namespace {
    int int_data[] = { 1972, 1974, 2004, 2007, 1337, 1984, 2001, 1999, 1939,
                       1945 };
    std::string string_data[] = { "green", "yellow", "blue", "red", "orange",
                                  "black", "white", "gray", "brown", "pink" };

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

    void test_erase_key()
    {
        typedef unordered_map<int, std::string> map_type;

        map_type m;
        std::size_t count;

        m.insert(map_type::value_type(13, "Mikael"));
        m.insert(map_type::value_type(12, "Lind"));

        count = m.erase(11);
        assert(count == 0);
        assert(m.size() == 2);

        count = m.erase(12);
        assert(count == 1);
        assert(m.size() == 1);

        count = m.erase(12);
        assert(count == 0);
        assert(m.size() == 1);

        count = m.erase(13);
        assert(count == 1);
        assert(m.empty());
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
    test_erase_key();
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
