#include "circle_2.hpp"
#include <cmath>
#include <ostream>

namespace siblings {
    std::ostream& operator<<(std::ostream& out, const circle_2& c)
    {
        return out << "(" << c.center().x() << ", " << c.center().y() << "; "
                   << c.radius() << ")";
    }
}
