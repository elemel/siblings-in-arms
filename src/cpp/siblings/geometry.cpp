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

    real squared_distance(const circle_2& c, const rectangle_2& r)
    {
        return std::max(squared_distance(r, c.center()) - square(c.radius()),
                        real(0));
    }

    real squared_distance(const circle_2& c, const vector_2& v)
    {
        return std::max(squared_distance(c.center(), v) - square(c.radius()),
                        real(0));
    }

    real squared_distance(const rectangle_2& a, const rectangle_2& b)
    {
        return square(max_3(a.min_x() - b.max_x(), b.min_x() - a.max_x(),
                            real(0)))
            + square(max_3(a.min_y() - b.max_y(), b.min_y() - a.max_y(),
                           real(0)));
    }

    real squared_distance(const rectangle_2& r, const vector_2& v)
    {
        return square(max_3(r.min_x() - v.x(), v.x() - r.max_x(), real(0)))
            + square(max_3(r.min_y() - v.y(), v.y() - r.max_y(), real(0)));
    }

    real squared_distance(const vector_2& a, const vector_2& b)
    {
        return square(a.x() - b.x()) + square(a.y() - b.y());
    }

    bool contains(const circle_2& outer, const vector_2& inner)
    {
        return squared_distance(outer.center(), inner)
            <= square(outer.radius());
    }

    bool contains(const rectangle_2& outer, const vector_2& inner)
    {
        return outer.min_x() <= inner.x() and inner.x() <= outer.max_x()
                and outer.min_y() <= inner.y() and inner.y() <= outer.max_y();
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
