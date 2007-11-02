#include "../sparse_grid_2.hpp"
#include <cassert>

using namespace siblings;

namespace {
    void test_entry_count()
    {
        sparse_grid_2 g;
        assert(g.entry_count() == 0);
        for (int i = 1; i <= 10; ++i) {
            g.insert(i, circle_2(i, i, i));
        }
        assert(g.entry_count() == 10);
        for (int i = 1; i <= 5; ++i) {
            g.erase(i);
        }
        assert(g.entry_count() == 5);
        for (int i = 6; i <= 10; ++i) {
            g.erase(i);
        }
        assert(g.entry_count() == 0);
    }

    void test_tile_count()
    {
        sparse_grid_2 g;
        assert(g.tile_count() == 0);
        g.insert(1, circle_2(0.5, 0.5, 0.25));
        assert(g.tile_count() == 1);
        g.insert(2, circle_2(0, 0, 0.5));
        assert(g.tile_count() == 4);
        g.erase(1);
        assert(g.tile_count() == 4);
        g.erase(2);
        assert(g.tile_count() == 0);
    }
}

int main()
{
    test_entry_count();
    return 0;
}
