#include "circle_2.hpp"
#include <cmath>
#include <ostream>

namespace siblings {
    real circle_2::min_x() const
    {
        return center_.x() - radius_;
    }

    real circle_2::min_y() const
    {
        return center_.y() - radius_;
    }

    real circle_2::max_x() const
    {
        return center_.x() + radius_;
    }

    real circle_2::max_y() const
    {
        return center_.y() + radius_;
    }

    std::ostream& operator<<(std::ostream& out, const circle_2& c)
    {
        return out << "((" << c.center().x() << ", " << c.center().y() << "); "
                   << c.radius() << ")";
    }
}
