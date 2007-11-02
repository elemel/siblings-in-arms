#include "../hash_map.hpp"
#include <cassert>
#include <string>

using namespace siblings;

namespace {
    void test_default_ctor()
    {
        hash_map<int, std::string> m;
        assert(m.size() == 0);
        assert(m.empty());
    }

    void test_insert()
    {
        typedef hash_map<int, std::string> map_type;
        typedef std::pair<map_type::iterator, bool> status;

        map_type m;
        status s;

        s = m.insert(map_type::value_type(13, "Mikael"));
        assert(s.second);
        assert(m.size() == 1);

        s = m.insert(map_type::value_type(12, "Lind"));
        assert(s.second);
        assert(m.size() == 2);
        
        s = m.insert(map_type::value_type(13, "Mike"));
        assert(!s.second);
        assert(m.size() == 2);
    }

    void test_erase()
    {
        typedef hash_map<int, std::string> map_type;

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
}

int main()
{
    test_default_ctor();
    test_insert();
    test_erase();
    return 0;
}
