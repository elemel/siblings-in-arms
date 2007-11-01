#include "rectangle_2.hpp"
#include <algorithm>
#include <ostream>

namespace siblings {
    rectangle_2::rectangle_2() { }

    rectangle_2::rectangle_2(const vector_2& min, const vector_2& max)
        : min_(std::min(min.x(), max.x()), std::min(min.y(), max.y())),
          max_(std::max(min.x(), max.x()), std::max(min.y(), max.y()))
    { }

    rectangle_2::rectangle_2(real min_x, real min_y, real max_x, real max_y)
        : min_(std::min(min_x, max_x), std::min(min_y, max_y)),
          max_(std::max(min_x, max_x), std::max(min_y, max_y))
    { }

    const vector_2& rectangle_2::min() const { return min_; }
    const vector_2& rectangle_2::max() const { return max_; }

    std::ostream& operator<<(std::ostream& out, const rectangle_2& r)
    {
        return out << "[" << r.min().x() << ", " << r.min().y() << "; "
                   << r.max().x() << ", " << r.max().y() << "]";
    }
}
