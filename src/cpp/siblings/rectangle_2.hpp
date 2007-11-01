#ifndef SIBLINGS_RECTANGLE_2_HPP
#define SIBLINGS_RECTANGLE_2_HPP

#include "config.hpp"
#include "vector_2.hpp"
#include <iosfwd>

namespace siblings {
    /// Geometric, axis-aligned rectangle in 2D.
    ///
    /// @invariant min().x() <= max().x()
    /// @invariant min().y() <= max().y()
    class rectangle_2 {
    public:
        /// Default constructor.
        rectangle_2();

        rectangle_2(const vector_2& min, const vector_2& max);
        rectangle_2(real min_x, real min_y, real max_x, real max_y);

        const vector_2& min() const;
        const vector_2& max() const;

    private:
        vector_2 min_;
        vector_2 max_;
    };

    /// Output rectangle in format "[min_x, min_y; max_x, max_y]".
    std::ostream& operator<<(std::ostream& out, const rectangle_2& r);
}

#endif
