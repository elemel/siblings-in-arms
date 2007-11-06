#include "../config.hpp"
#include "../sparse_grid_2.hpp"
#include <cassert>
#include <iostream>

using namespace siblings;

namespace {
    typedef circle_2<real> circle_type;
    typedef sparse_grid_2<real, circle_type> grid_type;

    void test_size()
    {
        grid_type g;
        assert(g.size() == 0);
        for (int i = 1; i <= 10; ++i) {
            g.insert(i, circle_2<real>(i, i, i));
        }
        assert(g.size() == 10);
        for (int i = 1; i <= 5; ++i) {
            g.erase(i);
        }
        assert(g.size() == 5);
        for (int i = 6; i <= 10; ++i) {
            g.erase(i);
        }
        assert(g.size() == 0);
    }

    void test_tile_count()
    {
        grid_type g;
        assert(g.tile_count() == 0);
        g.insert(1, circle_2<real>(0.5, 0.5, 0.25));
        assert(g.tile_count() == 1);
        g.insert(2, circle_2<real>(0, 0, 0.5));
        assert(g.tile_count() == 4);
        g.erase(1);
        assert(g.tile_count() == 4);
        g.erase(2);
        assert(g.tile_count() == 0);
    }
}

int main()
{
    test_size();
    return 0;
}
