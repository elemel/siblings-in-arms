#include "geometry.hpp"
#include "grid_2.hpp"
#include <cassert>
#include <cmath>
#include <boost/foreach.hpp>

namespace siblings {
    grid_2::grid_2(real tile_side) : tile_side_(std::abs(tile_side)) { }

    bool grid_2::insert(int key, const circle_2& bounds)
    {
        const std::vector<grid_position> positions(to_grid_positions(bounds));
        if (grid_positions_.find(key) == grid_positions_.end()) {
            create_entry(key, bounds);
            return true;
        } else {
            update_entry(key, bounds);
            return false;
        }
    }

    bool grid_2::erase(int key)
    {
        grid_position_map::const_iterator i = grid_positions_.find(key);
        if (i == grid_positions_.end()) {
            // nothing to erase
            return false;
        } else {
            BOOST_FOREACH(const grid_position& p, i->second) {
                remove_entry_at_position(key, p);
            }
            grid_positions_.erase(key);
            return true;
        }
    }

    std::vector<int> grid_2::find(const circle_2& bounds) const
    {
        std::set<int> found;
        BOOST_FOREACH(const grid_position& p, to_grid_positions(bounds)) {
            tile_map::const_iterator i = tiles_.find(p);
            if (i != tiles_.end()) {
                BOOST_FOREACH(const entry_map::value_type& v, i->second) {
                    if (intersects(bounds, v.second)) {
                        found.insert(v.first);
                    }
                }
            }
        }
        return std::vector<int>(found.begin(), found.end());
    }

    void grid_2::create_entry(int key, const circle_2& bounds)
    {
        const std::vector<grid_position> positions = to_grid_positions(bounds);
        BOOST_FOREACH(const grid_position& p, positions) {
            add_entry_at_position(key, bounds, p);
        }
        grid_positions_[key] = grid_position_set(positions.begin(),
                                                 positions.end());
    }

    void grid_2::update_entry(int key, const circle_2& bounds)
    {
        const grid_position_set old_positions = grid_positions_[key];
        const std::vector<grid_position> new_positions
            = to_grid_positions(bounds);

        std::vector<grid_position> removed_positions;
        std::set_difference(old_positions.begin(), old_positions.end(),
                            new_positions.begin(), new_positions.end(),
                            std::back_inserter(removed_positions));
        BOOST_FOREACH(const grid_position& p, removed_positions) {
            remove_entry_at_position(key, p);
        }

        std::vector<grid_position> added_positions;
        std::set_difference(new_positions.begin(), new_positions.end(),
                            old_positions.begin(), old_positions.end(),
                            std::back_inserter(added_positions));
        BOOST_FOREACH(const grid_position& p, added_positions) {
            add_entry_at_position(key, bounds, p);
        }

        grid_positions_[key] = grid_position_set(new_positions.begin(),
                                                 new_positions.end());
    }

    /// Returns a sorted vector.
    std::vector<grid_2::grid_position>
    grid_2::to_grid_positions(const circle_2& bounds) const
    {
        std::vector<grid_position> result;
        const vector_2 radii = vector_2(bounds.radius(), bounds.radius());
        grid_position min = to_grid_position(bounds.center() - radii);
        grid_position max = to_grid_position(bounds.center() + radii);
        for (int x = min.first; x <= max.second; ++x) {
            for (int y = min.second; y <= max.second; ++y) {
                result.push_back(grid_position(x, y));
            }
        }
        return result;
    }
    
    grid_2::grid_position grid_2::to_grid_position(const vector_2& v) const
    {
        return grid_position(int(v.x() / tile_side_), int(v.y() / tile_side_));
    }
    
    void grid_2::add_entry_at_position(int key, const circle_2& bounds,
                                       const grid_position& p)
    {
        tiles_[p][key] = bounds;
        
    }
    
    void grid_2::remove_entry_at_position(int key, const grid_position& p)
    {
        tile_map::iterator i = tiles_.find(p);
        assert(i != tiles_.end());
        i->second.erase(key);
        if (i->second.empty()) {
            tiles_.erase(i);
        }
    }
}
