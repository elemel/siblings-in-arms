#ifndef SIBLINGS_SPARSE_GRID_2_HPP
#define SIBLINGS_SPARSE_GRID_2_HPP

#include "circle_2.hpp"
#include "config.hpp"
#include "flat_set.hpp"
#include "unordered_map.hpp"
#include <cstddef>
#include <vector>

namespace siblings {
    class sparse_grid_2 {
    public:
        explicit sparse_grid_2(real tile_side = real(1));

        bool insert(int key, const circle_2<real>& bounds);
        bool erase(int key);

        std::vector<int> find(const circle_2<real>& bounds) const;

        std::size_t entry_count() const;
        std::size_t tile_count() const;

    private:
        typedef unordered_map<int, circle_2<real> > entry_map;
        typedef std::pair<int, int> grid_position;
        typedef flat_set<grid_position> grid_position_set;
        typedef unordered_map<grid_position, entry_map> tile_map;
        typedef unordered_map<int, grid_position_set> grid_position_map;

        real tile_side_;
        tile_map tiles_;
        grid_position_map grid_positions_;

        void create_entry(int key, const circle_2<real>& bounds);
        void update_entry(int key, const circle_2<real>& bounds);

        std::vector<grid_position>
        to_grid_positions(const circle_2<real>& bounds) const;

        grid_position to_grid_position(const vector_2<real>& v) const;

        void add_entry_at_position(int key, const circle_2<real>& bounds,
                                   const grid_position&);
        void remove_entry_at_position(int key, const grid_position&);
    };
}

#endif
