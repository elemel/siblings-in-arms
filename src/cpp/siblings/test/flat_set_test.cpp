#include "../flat_set.hpp"
#include <cassert>
#include <boost/array.hpp>

using namespace siblings;

namespace {
    const boost::array<int, 10> shuffled_ints
        = { { 3, 9, 2, 1, 4, 7, 6, 0, 8, 5 } };
    const boost::array<int, 10> sorted_ints
        = { { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 } };

    void test_default_ctor()
    {
        flat_set<int> ints;
        assert(ints.empty());
    }

    void test_iterators_ctor()
    {
        flat_set<int> ints(shuffled_ints.begin(), shuffled_ints.end());
        assert(ints.size() == shuffled_ints.size());
        assert(std::equal(ints.begin(), ints.end(), sorted_ints.begin()));
    }

    void test_lower_bound()
    {
        const flat_set<int> ints(shuffled_ints.begin(), shuffled_ints.end());

        assert(ints.lower_bound(-1) == ints.begin());
        assert(ints.lower_bound(10) == ints.end());

        flat_set<int>::iterator i = ints.lower_bound(5);
        assert(i != ints.end() && *i == 5);
    }

    void test_upper_bound()
    {
        const flat_set<int> ints(shuffled_ints.begin(), shuffled_ints.end());

        assert(ints.upper_bound(-1) == ints.begin());
        assert(ints.upper_bound(10) == ints.end());

        flat_set<int>::iterator i = ints.upper_bound(5);
        assert(i != ints.end() && *i == 6);
    }

    void test_equal_range()
    {
        const flat_set<int> ints(shuffled_ints.begin(), shuffled_ints.end());

        typedef flat_set<int>::iterator iterator;
        typedef std::pair<iterator, iterator> range;

        const range r = ints.equal_range(-1);
        assert(r.first == ints.begin() && r.second == ints.begin());

        const range r2 = ints.equal_range(10);
        assert(r2.first == ints.end() && r2.second == ints.end());

        const range r3 = ints.equal_range(5);
        assert(r3.first != ints.end() && *r3.first == 5);
        assert(r3.second != ints.end() && *r3.second == 6);
    }
}

int main()
{
    test_default_ctor();
    test_iterators_ctor();
    test_lower_bound();
    test_upper_bound();
    test_equal_range();
    return 0;
}
