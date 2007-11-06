#ifndef SIBLINGS_RECTANGLE_2_HPP
#define SIBLINGS_RECTANGLE_2_HPP

#include "vector_2.hpp"
#include <algorithm>
#include <ostream>

namespace siblings {
    /// Geometric, axis-aligned rectangle in 2D.
    ///
    /// @invariant min().x() <= max().x()
    /// @invariant min().y() <= max().y()
    template <typename R>
    class rectangle_2 {
    public: 
        typedef R real_type;

        /// Construct rectangle with min and max at origin.
        rectangle_2() { }

        rectangle_2(const vector_2<R>& min, const vector_2<R>& max)
            : min_(std::min(min.x(), max.x()), std::min(min.y(), max.y())),
              max_(std::max(min.x(), max.x()), std::max(min.y(), max.y()))
        { }

        rectangle_2(R min_x, R min_y, R max_x, R max_y)
            : min_(std::min(min_x, max_x), std::min(min_y, max_y)),
              max_(std::max(min_x, max_x), std::max(min_y, max_y))
        { }

        const vector_2<R>& min() const { return min_; }
        const vector_2<R>& max() const { return max_; }

    private:
        vector_2<R> min_;
        vector_2<R> max_;
    };

    /// Output rectangle in format "[min_x, min_y; max_x, max_y]".
    template <typename R>
    std::ostream& operator<<(std::ostream& out, const rectangle_2<R>& r)
    {
        return out << "[" << r.min().x() << ", " << r.min().y() << "; "
                   << r.max().x() << ", " << r.max().y() << "]";
    }
}

#endif
