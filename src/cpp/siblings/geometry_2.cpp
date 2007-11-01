#include "geometry_2.hpp"
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

    bool contains(const circle_2& outer, const circle_2& inner)
    {
        return inner.radius() <= outer.radius()
            && squared_distance(outer.center(), inner.center())
            <= square(outer.radius() - inner.radius());
    }

    bool contains(const circle_2& outer, const rectangle_2& inner)
    {
        return contains(outer, inner.min()) && contains(outer, inner.max())
            && contains(outer, vector_2(inner.min_x(), inner.max_y()))
            && contains(outer, vector_2(inner.max_x(), inner.min_y()));
    }

    bool contains(const circle_2& outer, const vector_2& inner)
    {
        return squared_distance(outer.center(), inner)
            <= square(outer.radius());
    }

    bool contains(const rectangle_2& outer, const circle_2& inner)
    {
        return contains(outer, bounding_rectangle(inner));
    }

    bool contains(const rectangle_2& outer, const rectangle_2& inner)
    {
        return outer.min_x() <= inner.min_x()
            && inner.max_x() <= outer.max_x()
            && outer.min_y() <= inner.min_y()
            && inner.max_y() <= outer.max_y();
    }

    bool contains(const rectangle_2& outer, const vector_2& inner)
    {
        return outer.min_x() <= inner.x() && inner.x() <= outer.max_x()
                && outer.min_y() <= inner.y() && inner.y() <= outer.max_y();
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

    circle_2 bounding_circle(const rectangle_2& r)
    {
        return circle_2(r.center(), distance(r.center(), r.min()));
    }

    circle_2 bounding_circle(const vector_2& v)
    {
        return circle_2(v, real(0));
    }

    rectangle_2 bounding_rectangle(const circle_2& c)
    {
        return rectangle_2(c.center() - vector_2(c.radius()),
                           c.center() + vector_2(c.radius()));
    }

    rectangle_2 bounding_rectangle(const vector_2& v)
    {
        return rectangle_2(v, v);
    }
}
