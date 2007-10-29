#ifndef SIBLINGS_GRID_2_HPP
#define SIBLINGS_GRID_2_HPP

#include "circle_2.hpp"
#include "config.hpp"
#include <map>
#include <set>
#include <vector>

namespace siblings {
    /// @todo Use Boost.MultiIndex for the key-position map.
    /// @todo Optimize the update() member function.
    class grid_2 {
    public:
        explicit grid_2(real tile_side = real(1));

        bool insert(int key, const circle_2& bounds);
        bool erase(int key);

        std::vector<int> find(const circle_2& bounds) const;

    private:
        typedef std::map<int, circle_2> entry_map;
        typedef std::pair<int, int> grid_position;
        typedef std::set<grid_position> grid_position_set;
        typedef std::map<grid_position, entry_map> tile_map;
        typedef std::map<int, grid_position_set> grid_position_map;

        real tile_side_;
        tile_map tiles_;
        grid_position_map grid_positions_;

        void create_entry(int key, const circle_2& bounds);
        void update_entry(int key, const circle_2& bounds);

        std::vector<grid_position> to_grid_positions(const circle_2& bounds)
            const;

        grid_position to_grid_position(const vector_2& v) const;

        void add_entry_at_position(int key, const circle_2& bounds,
                                   const grid_position&);
        void remove_entry_at_position(int key, const grid_position&);
    };
}

#endif
