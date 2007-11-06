#include "geometry_2.hpp"
#include "math.hpp"
#include <algorithm>
#include <cmath>

namespace siblings {
    real squared_distance(const circle_2<real>& a, const circle_2<real>& b)
    {
        return std::max(squared_distance(a.center(), b.center())
                        - square(a.radius() + b.radius()), real(0));
    }

    real squared_distance(const circle_2<real>& c, const rectangle_2& r)
    {
        return std::max(squared_distance(r, c.center()) - square(c.radius()),
                        real(0));
    }

    real squared_distance(const circle_2<real>& c, const vector_2<real>& v)
    {
        return std::max(squared_distance(c.center(), v) - square(c.radius()),
                        real(0));
    }

    real squared_distance(const rectangle_2& r, const circle_2<real>& c)
    {
        return squared_distance(c, r);
    }

    real squared_distance(const rectangle_2& a, const rectangle_2& b)
    {
        return square(max_3(a.min().x() - b.max().x(),
                            b.min().x() - a.max().x(), real(0)))
            + square(max_3(a.min().y() - b.max().y(),
                           b.min().y() - a.max().y(), real(0)));
    }

    real squared_distance(const rectangle_2& r, const vector_2<real>& v)
    {
        return square(max_3(r.min().x() - v.x(), v.x() - r.max().x(), real(0)))
            + square(max_3(r.min().y() - v.y(), v.y() - r.max().y(), real(0)));
    }

    real squared_distance(const vector_2<real>& v, const circle_2<real>& c)
    {
        return squared_distance(c, v);
    }

    real squared_distance(const vector_2<real>& v, const rectangle_2& r)
    {
        return squared_distance(r, v);
    }

    real squared_distance(const vector_2<real>& a, const vector_2<real>& b)
    {
        return square(a.x() - b.x()) + square(a.y() - b.y());
    }

    bool contains(const circle_2<real>& outer, const circle_2<real>& inner)
    {
        return inner.radius() <= outer.radius()
            && squared_distance(outer.center(), inner.center())
            <= square(outer.radius() - inner.radius());
    }

    bool contains(const circle_2<real>& outer, const rectangle_2& inner)
    {
        return contains(outer, inner.min()) && contains(outer, inner.max())
            && contains(outer, vector_2<real>(inner.min().x(),
                                              inner.max().y()))
            && contains(outer, vector_2<real>(inner.max().x(),
                                              inner.min().y()));
    }

    bool contains(const circle_2<real>& outer, const vector_2<real>& inner)
    {
        return squared_distance(outer.center(), inner)
            <= square(outer.radius());
    }

    bool contains(const rectangle_2& outer, const circle_2<real>& inner)
    {
        return contains(outer, bounding_rectangle(inner));
    }

    bool contains(const rectangle_2& outer, const rectangle_2& inner)
    {
        return outer.min().x() <= inner.min().x()
            && inner.max().x() <= outer.max().x()
            && outer.min().y() <= inner.min().y()
            && inner.max().y() <= outer.max().y();
    }

    bool contains(const rectangle_2& outer, const vector_2<real>& inner)
    {
        return outer.min().x() <= inner.x()
            && inner.x() <= outer.max().x()
            && outer.min().y() <= inner.y()
            && inner.y() <= outer.max().y();
    }

    bool intersects(const circle_2<real>& a, const circle_2<real>& b)
    {
        return squared_distance(a.center(), b.center())
            < square(a.radius() + b.radius());
    }

    bool intersects(const circle_2<real>& c, const rectangle_2& r)
    {
        return squared_distance(r, c.center()) < square(c.radius());
    }

    bool intersects(const rectangle_2& r, const circle_2<real>& c)
    {
        return intersects(c, r);
    }

    bool intersects(const rectangle_2& a, const rectangle_2& b)
    {
        return a.min().x() < b.max().x() && b.min().x() < a.max().x()
            && a.min().y() < b.max().y() && b.min().y() < a.max().y();
    }

    const circle_2<real>& bounding_circle(const circle_2<real>& c)
    {
        return c;
    }

    circle_2<real> bounding_circle(const rectangle_2& r)
    {
        const vector_2<real> center = (r.min() + r.max()) / real(2);
        return circle_2<real>(center, distance(center, r.min()));
    }

    circle_2<real> bounding_circle(const vector_2<real>& v)
    {
        return circle_2<real>(v, real(0));
    }

    rectangle_2 bounding_rectangle(const circle_2<real>& c)
    {
        return rectangle_2(c.center() - vector_2<real>(c.radius()),
                           c.center() + vector_2<real>(c.radius()));
    }

    const rectangle_2& bounding_rectangle(const rectangle_2& r)
    {
        return r;
    }

    rectangle_2 bounding_rectangle(const vector_2<real>& v)
    {
        return rectangle_2(v, v);
    }
}
