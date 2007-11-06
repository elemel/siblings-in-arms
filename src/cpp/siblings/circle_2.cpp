#include "circle_2.hpp"
#include <cmath>
#include <ostream>

namespace siblings {
    circle_2::circle_2() : radius_(real(0)) { }

    circle_2::circle_2(const vector_2<real>& center, real radius)
        : center_(center), radius_(radius)
    { }

    circle_2::circle_2(real center_x, real center_y, real radius)
        : center_(center_x, center_y), radius_(radius)
    { }

    const vector_2<real>& circle_2::center() const { return center_; }
    real circle_2::radius() const { return radius_; }

    std::ostream& operator<<(std::ostream& out, const circle_2& c)
    {
        return out << "(" << c.center().x() << ", " << c.center().y() << "; "
                   << c.radius() << ")";
    }
}
