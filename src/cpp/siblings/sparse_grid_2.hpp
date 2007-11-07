#ifndef SIBLINGS_SPARSE_GRID_2_HPP
#define SIBLINGS_SPARSE_GRID_2_HPP

#include "flat_set.hpp"
#include "geometry_2.hpp"
#include "unordered_map.hpp"
#include <cmath>
#include <cstddef>
#include <utility>
#include <vector>
#include <boost/foreach.hpp>

namespace siblings {
    template <typename K, typename S>
    class sparse_grid_2 {
    public:
        typedef K key_type;
        typedef S shape_type;
        typedef typename S::real_type real_type;
        typedef vector_2<real_type> vector_type;
        typedef std::size_t size_type;

    private:
        typedef unordered_map<key_type, shape_type> entry_map;
        typedef std::pair<int, int> grid_position;
        typedef flat_set<grid_position> grid_position_set;
        typedef unordered_map<grid_position, entry_map> tile_map;
        typedef unordered_map<key_type, grid_position_set> grid_position_map;

    public:
        explicit sparse_grid_2(real_type tile_side = real_type(1))
            : tile_side_(std::abs(tile_side))
        { }

        bool insert(key_type k, const shape_type& s)
        {
            const std::vector<grid_position>
                positions(to_grid_positions(s));
            if (grid_positions_.find(k) == grid_positions_.end()) {
                create_entry(k, s);
                return true;
            } else {
                update_entry(k, s);
                return false;
            }
        }

        bool erase(key_type k)
        {
            typename grid_position_map::const_iterator i
                = grid_positions_.find(k);
            if (i == grid_positions_.end()) {
                // nothing to erase
                return false;
            } else {
                BOOST_FOREACH(const grid_position& p, i->second) {
                    remove_entry_at_position(k, p);
                }
                grid_positions_.erase(k);
                return true;
            }
        }

        template <typename OutputIterator>
        void find(const shape_type& s, OutputIterator o) const
        {
            flat_set<key_type> found;
            BOOST_FOREACH(const grid_position& p, to_grid_positions(s)) {
                typename tile_map::const_iterator i = tiles_.find(p);
                if (i != tiles_.end()) {
                    BOOST_FOREACH(const typename entry_map::value_type& v,
                                  i->second)
                    {
                        if (intersects(s, v.second)) {
                            found.insert(v.first);
                        }
                    }
                }
            }
            std::copy(found.begin(), found.end(), o);
        }

        size_type size() const { return grid_positions_.size(); }
        size_type tile_count() const { return tiles_.size(); }

    private:
        real_type tile_side_;
        tile_map tiles_;
        grid_position_map grid_positions_;

        void create_entry(key_type k, const shape_type& s)
        {
            const std::vector<grid_position> positions = to_grid_positions(s);
            BOOST_FOREACH(const grid_position& p, positions) {
                add_entry_at_position(k, s, p);
            }
            grid_positions_[k] = grid_position_set(positions.begin(),
                                                   positions.end());
        }

        void update_entry(key_type k, const shape_type& s)
        {
            const grid_position_set old_positions = grid_positions_[k];
            const std::vector<grid_position> new_positions
                = to_grid_positions(s);

            std::vector<grid_position> removed_positions;
            std::set_difference(old_positions.begin(), old_positions.end(),
                                new_positions.begin(), new_positions.end(),
                                std::back_inserter(removed_positions));
            BOOST_FOREACH(const grid_position& p, removed_positions) {
                remove_entry_at_position(k, p);
            }

            std::vector<grid_position> added_positions;
            std::set_difference(new_positions.begin(), new_positions.end(),
                                old_positions.begin(), old_positions.end(),
                                std::back_inserter(added_positions));
            BOOST_FOREACH(const grid_position& p, added_positions) {
                add_entry_at_position(k, s, p);
            }

            grid_positions_[k] = grid_position_set(new_positions.begin(),
                                                   new_positions.end());
        }

        /// Returns a sorted vector.
        std::vector<grid_position> to_grid_positions(const shape_type& s) const
        {
            std::vector<grid_position> result;
            const vector_type radii = vector_type(s.radius());
            grid_position min = to_grid_position(s.center() - radii);
            grid_position max = to_grid_position(s.center() + radii);
            for (int x = min.first; x <= max.second; ++x) {
                for (int y = min.second; y <= max.second; ++y) {
                    result.push_back(grid_position(x, y));
                }
            }
            return result;
        }

        grid_position to_grid_position(const vector_type& v) const
        {
            return grid_position(int(v.x() / tile_side_),
                                 int(v.y() / tile_side_));
        }

        void add_entry_at_position(key_type k, const shape_type& s,
                                   const grid_position& p)
        {
            tiles_[p][k] = s;
        }

        void remove_entry_at_position(key_type k, const grid_position& p)
        {
            typename tile_map::iterator i = tiles_.find(p);
            assert(i != tiles_.end());
            i->second.erase(k);
            if (i->second.empty()) {
                tiles_.erase(i);
            }
        }
    };
}

#endif
