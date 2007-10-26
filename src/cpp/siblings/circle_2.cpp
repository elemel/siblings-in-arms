#include "circle_2.hpp"
#include <cmath>
#include <ostream>

namespace siblings {
    circle_2::circle_2() : radius_(0) { }

    circle_2::circle_2(const vector_2& center, real radius)
        : center_(center),
          radius_(std::abs(radius))
    { }

    const vector_2& circle_2::center() const { return center_; }
    real circle_2::radius() const { return radius_; }

    std::ostream& operator<<(std::ostream& out, const circle_2& c)
    {
        return out << "((" << c.center().x << ", " << c.center().y << "); "
                   << c.radius() << ")";
    }
}
