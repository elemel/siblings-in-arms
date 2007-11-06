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
    template <typename T>
    class rectangle_2 {
    public: 
        typedef T value_type;

        /// Construct rectangle with min and max at origin.
        rectangle_2() { }

        rectangle_2(const vector_2<T>& min, const vector_2<T>& max)
            : min_(std::min(min.x(), max.x()), std::min(min.y(), max.y())),
              max_(std::max(min.x(), max.x()), std::max(min.y(), max.y()))
        { }

        rectangle_2(T min_x, T min_y, T max_x, T max_y)
            : min_(std::min(min_x, max_x), std::min(min_y, max_y)),
              max_(std::max(min_x, max_x), std::max(min_y, max_y))
        { }

        const vector_2<T>& min() const { return min_; }
        const vector_2<T>& max() const { return max_; }

    private:
        vector_2<T> min_;
        vector_2<T> max_;
    };

    /// Output rectangle in format "[min_x, min_y; max_x, max_y]".
    template <typename T>
    std::ostream& operator<<(std::ostream& out, const rectangle_2<T>& r)
    {
        return out << "[" << r.min().x() << ", " << r.min().y() << "; "
                   << r.max().x() << ", " << r.max().y() << "]";
    }
}

#endif
