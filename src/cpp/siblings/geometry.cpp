#include "geometry.hpp"
#include "math.hpp"
#include <algorithm>
#include <cmath>

namespace siblings {
    real squared_distance(const circle_2& a, const circle_2& b)
    {
        return std::max(squared_distance(a.center(), b.center())
                        - square(a.radius() + b.radius()), real(0));
    }

    real squared_distance(const vector_2& a, const vector_2& b)
    {
        return square(a.x - b.x) + square(a.y - b.y);
    }
    
    real squared_distance(const circle_2& c, const vector_2& v)
    {
        return std::max(squared_distance(c.center(), v) - square(c.radius()),
                        real(0));
    }

    real squared_distance(const rectangle_2& r, const vector_2& v)
    {
        return square(std::max(std::max(r.min_x() - v.x, v.x - r.max_x()),
                               0.0))
            + square(std::max(std::max(r.min_y() - v.y, v.y - r.max_y()),
                              0.0));
    }

    real distance(const vector_2& a, const vector_2& b)
    {
        return std::sqrt(squared_distance(a, b));
    }

    bool intersects(const circle_2& a, const circle_2& b)
    {
        return squared_distance(a.center(), b.center())
            < square(a.radius() + b.radius());
    }

    bool intersects(const circle_2& c, const rectangle_2& r)
    {
        return squared_distance(r, c.center()) < square(c.radius());
    }

    bool intersects(const rectangle_2& a, const rectangle_2& b)
    {
        return a.min_x() < b.max_x() && b.min_x() < a.max_x()
            && a.min_y() < b.max_y() && b.min_y() < a.max_y();
    }
}
