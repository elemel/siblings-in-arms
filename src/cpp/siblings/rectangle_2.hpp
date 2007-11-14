// Copyright 2007 Mikael Lind.

#ifndef SIBLINGS_RECTANGLE_2_HPP
#define SIBLINGS_RECTANGLE_2_HPP

#include "vector_2.hpp"
#include <algorithm>
#include <ostream>

namespace siblings {
    /// @brief Geometric, axis-aligned rectangle in 2D.
    ///
    /// @invariant min().x() <= max().x()
    ///
    /// @invariant min().y() <= max().y()
    template <typename R>
    class rectangle_2 {
    public:
        /// Real type.
        typedef R real_type;

        /// @brief Default constructor.
        ///
        /// Constructs a rectangle with mininum and maximum points at origin.
        rectangle_2() { }

        /// @brief Constructs a rectangle with the specified minumim and
        /// maximum points.
        rectangle_2(const vector_2<R>& min, const vector_2<R>& max)
            : min_(std::min(min.x(), max.x()), std::min(min.y(), max.y())),
              max_(std::max(min.x(), max.x()), std::max(min.y(), max.y()))
        { }

        /// @brief Constructs a rectangle with the specified minumim and
        /// maximum points.
        rectangle_2(R min_x, R min_y, R max_x, R max_y)
            : min_(std::min(min_x, max_x), std::min(min_y, max_y)),
              max_(std::max(min_x, max_x), std::max(min_y, max_y))
        { }

        /// Returns the minimum point.
        const vector_2<R>& min() const { return min_; }

        /// Returns the maximum point.
        const vector_2<R>& max() const { return max_; }

    private:
        /// Minimum point.
        vector_2<R> min_;

        /// Maximum point.
        vector_2<R> max_;
    };

    /// @brief Output operator.
    ///
    /// Writes the rectangle to the stream using the format <em>[min_x, min_y;
    /// max_x, max_y]</em>.
    template <typename R>
    std::ostream& operator<<(std::ostream& out, const rectangle_2<R>& r)
    {
        return out << "[" << r.min().x() << ", " << r.min().y() << "; "
                   << r.max().x() << ", " << r.max().y() << "]";
    }
}

#endif
