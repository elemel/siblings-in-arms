#ifndef SIBLINGS_GEOMETRY_HPP
#define SIBLINGS_GEOMETRY_HPP

#include "circle_2.hpp"
#include "math.hpp"
#include "rectangle_2.hpp"
#include "vector_2.hpp"
#include <cmath>

namespace siblings {
    template <typename T>
    T squared_distance(const circle_2<T>& a, const circle_2<T>& b)
    {
        return std::max(squared_distance(a.center(), b.center())
                        - square(a.radius() + b.radius()), T(0));
    }

    template <typename T>
    T squared_distance(const circle_2<T>& c, const rectangle_2<T>& r)
    {
        return std::max(squared_distance(r, c.center()) - square(c.radius()),
                        T(0));
    }

    template <typename T>
    T squared_distance(const circle_2<T>& c, const vector_2<T>& v)
    {
        return std::max(squared_distance(c.center(), v) - square(c.radius()),
                        T(0));
    }

    template <typename T>
    T squared_distance(const rectangle_2<T>& r, const circle_2<T>& c)
    {
        return squared_distance(c, r);
    }

    template <typename T>
    T squared_distance(const rectangle_2<T>& a,
                          const rectangle_2<T>& b)
    {
        return square(max_3(a.min().x() - b.max().x(),
                            b.min().x() - a.max().x(), T(0)))
            + square(max_3(a.min().y() - b.max().y(),
                           b.min().y() - a.max().y(), T(0)));
    }

    template <typename T>
    T squared_distance(const rectangle_2<T>& r, const vector_2<T>& v)
    {
        return square(max_3(r.min().x() - v.x(), v.x() - r.max().x(), T(0)))
            + square(max_3(r.min().y() - v.y(), v.y() - r.max().y(), T(0)));
    }

    template <typename T>
    T squared_distance(const vector_2<T>& v, const circle_2<T>& c)
    {
        return squared_distance(c, v);
    }

    template <typename T>
    T squared_distance(const vector_2<T>& v, const rectangle_2<T>& r)
    {
        return squared_distance(r, v);
    }

    template <typename T>
    T squared_distance(const vector_2<T>& a, const vector_2<T>& b)
    {
        return square(a.x() - b.x()) + square(a.y() - b.y());
    }

    template <typename T, typename U>
    typename T::value_type distance(const T& a, const U& b)
    {
        return std::sqrt(squared_distance(a, b));
    }

    template <typename T>
    bool contains(const circle_2<T>& outer, const circle_2<T>& inner)
    {
        return inner.radius() <= outer.radius()
            && squared_distance(outer.center(), inner.center())
            <= square(outer.radius() - inner.radius());
    }

    template <typename T>
    bool contains(const circle_2<T>& outer, const rectangle_2<T>& inner)
    {
        return contains(outer, inner.min()) && contains(outer, inner.max())
            && contains(outer, vector_2<T>(inner.min().x(),
                                              inner.max().y()))
            && contains(outer, vector_2<T>(inner.max().x(),
                                              inner.min().y()));
    }

    template <typename T>
    bool contains(const circle_2<T>& outer, const vector_2<T>& inner)
    {
        return squared_distance(outer.center(), inner)
            <= square(outer.radius());
    }

    template <typename T>
    bool contains(const rectangle_2<T>& outer, const circle_2<T>& inner)
    {
        return contains(outer, bounding_rectangle(inner));
    }

    template <typename T>
    bool contains(const rectangle_2<T>& outer,
                  const rectangle_2<T>& inner)
    {
        return outer.min().x() <= inner.min().x()
            && inner.max().x() <= outer.max().x()
            && outer.min().y() <= inner.min().y()
            && inner.max().y() <= outer.max().y();
    }

    template <typename T>
    bool contains(const rectangle_2<T>& outer, const vector_2<T>& inner)
    {
        return outer.min().x() <= inner.x()
            && inner.x() <= outer.max().x()
            && outer.min().y() <= inner.y()
            && inner.y() <= outer.max().y();
    }

    template <typename T>
    bool intersects(const circle_2<T>& a, const circle_2<T>& b)
    {
        return squared_distance(a.center(), b.center())
            < square(a.radius() + b.radius());
    }

    template <typename T>
    bool intersects(const circle_2<T>& c, const rectangle_2<T>& r)
    {
        return squared_distance(r, c.center()) < square(c.radius());
    }

    template <typename T>
    bool intersects(const rectangle_2<T>& r, const circle_2<T>& c)
    {
        return intersects(c, r);
    }

    template <typename T>
    bool intersects(const rectangle_2<T>& a, const rectangle_2<T>& b)
    {
        return a.min().x() < b.max().x() && b.min().x() < a.max().x()
            && a.min().y() < b.max().y() && b.min().y() < a.max().y();
    }

    template <typename T>
    const circle_2<T>& bounding_circle(const circle_2<T>& c)
    {
        return c;
    }

    template <typename T>
    circle_2<T> bounding_circle(const rectangle_2<T>& r)
    {
        const vector_2<T> center = (r.min() + r.max()) / T(2);
        return circle_2<T>(center, distance(center, r.min()));
    }

    template <typename T>
    circle_2<T> bounding_circle(const vector_2<T>& v)
    {
        return circle_2<T>(v, T(0));
    }

    template <typename T>
    rectangle_2<T> bounding_rectangle(const circle_2<T>& c)
    {
        return rectangle_2<T>(c.center() - vector_2<T>(c.radius()),
                           c.center() + vector_2<T>(c.radius()));
    }

    template <typename T>
    const rectangle_2<T>& bounding_rectangle(const rectangle_2<T>& r)
    {
        return r;
    }

    template <typename T>
    rectangle_2<T> bounding_rectangle(const vector_2<T>& v)
    {
        return rectangle_2<T>(v, v);
    }
}

#endif
