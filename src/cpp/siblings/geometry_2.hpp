// Copyright 2007 Mikael Lind.

#ifndef SIBLINGS_GEOMETRY_HPP
#define SIBLINGS_GEOMETRY_HPP

#include "circle_2.hpp"
#include "math.hpp"
#include "rectangle_2.hpp"
#include "vector_2.hpp"
#include <cmath>

namespace siblings {
    template <typename R>
    R squared_distance(const circle_2<R>& a, const circle_2<R>& b)
    {
        return std::max(squared_distance(a.center(), b.center())
                        - square(a.radius() + b.radius()), R(0));
    }

    template <typename R>
    R squared_distance(const circle_2<R>& c, const rectangle_2<R>& r)
    {
        return std::max(squared_distance(r, c.center()) - square(c.radius()),
                        R(0));
    }

    template <typename R>
    R squared_distance(const circle_2<R>& c, const vector_2<R>& v)
    {
        return std::max(squared_distance(c.center(), v) - square(c.radius()),
                        R(0));
    }

    template <typename R>
    R squared_distance(const rectangle_2<R>& r, const circle_2<R>& c)
    {
        return squared_distance(c, r);
    }

    template <typename R>
    R squared_distance(const rectangle_2<R>& a,
                          const rectangle_2<R>& b)
    {
        return square(max_3(a.min().x() - b.max().x(),
                            b.min().x() - a.max().x(), R(0)))
            + square(max_3(a.min().y() - b.max().y(),
                           b.min().y() - a.max().y(), R(0)));
    }

    template <typename R>
    R squared_distance(const rectangle_2<R>& r, const vector_2<R>& v)
    {
        return square(max_3(r.min().x() - v.x(), v.x() - r.max().x(), R(0)))
            + square(max_3(r.min().y() - v.y(), v.y() - r.max().y(), R(0)));
    }

    template <typename R>
    R squared_distance(const vector_2<R>& v, const circle_2<R>& c)
    {
        return squared_distance(c, v);
    }

    template <typename R>
    R squared_distance(const vector_2<R>& v, const rectangle_2<R>& r)
    {
        return squared_distance(r, v);
    }

    template <typename R>
    R squared_distance(const vector_2<R>& a, const vector_2<R>& b)
    {
        return square(a.x() - b.x()) + square(a.y() - b.y());
    }

    template <typename T, typename U>
    typename T::real_type distance(const T& a, const U& b)
    {
        return std::sqrt(squared_distance(a, b));
    }

    template <typename R>
    bool contains(const circle_2<R>& outer, const circle_2<R>& inner)
    {
        return inner.radius() <= outer.radius()
            && squared_distance(outer.center(), inner.center())
            <= square(outer.radius() - inner.radius());
    }

    template <typename R>
    bool contains(const circle_2<R>& outer, const rectangle_2<R>& inner)
    {
        return contains(outer, inner.min()) && contains(outer, inner.max())
            && contains(outer, vector_2<R>(inner.min().x(),
                                              inner.max().y()))
            && contains(outer, vector_2<R>(inner.max().x(),
                                              inner.min().y()));
    }

    template <typename R>
    bool contains(const circle_2<R>& outer, const vector_2<R>& inner)
    {
        return squared_distance(outer.center(), inner)
            <= square(outer.radius());
    }

    template <typename R>
    bool contains(const rectangle_2<R>& outer, const circle_2<R>& inner)
    {
        return contains(outer, bounding_rectangle(inner));
    }

    template <typename R>
    bool contains(const rectangle_2<R>& outer,
                  const rectangle_2<R>& inner)
    {
        return outer.min().x() <= inner.min().x()
            && inner.max().x() <= outer.max().x()
            && outer.min().y() <= inner.min().y()
            && inner.max().y() <= outer.max().y();
    }

    template <typename R>
    bool contains(const rectangle_2<R>& outer, const vector_2<R>& inner)
    {
        return outer.min().x() <= inner.x()
            && inner.x() <= outer.max().x()
            && outer.min().y() <= inner.y()
            && inner.y() <= outer.max().y();
    }

    template <typename R>
    bool intersects(const circle_2<R>& a, const circle_2<R>& b)
    {
        return squared_distance(a.center(), b.center())
            < square(a.radius() + b.radius());
    }

    template <typename R>
    bool intersects(const circle_2<R>& c, const rectangle_2<R>& r)
    {
        return squared_distance(r, c.center()) < square(c.radius());
    }

    template <typename R>
    bool intersects(const rectangle_2<R>& r, const circle_2<R>& c)
    {
        return intersects(c, r);
    }

    template <typename R>
    bool intersects(const rectangle_2<R>& a, const rectangle_2<R>& b)
    {
        return a.min().x() < b.max().x() && b.min().x() < a.max().x()
            && a.min().y() < b.max().y() && b.min().y() < a.max().y();
    }

    template <typename R>
    const circle_2<R>& bounding_circle(const circle_2<R>& c)
    {
        return c;
    }

    template <typename R>
    circle_2<R> bounding_circle(const rectangle_2<R>& r)
    {
        const vector_2<R> center = (r.min() + r.max()) / R(2);
        return circle_2<R>(center, distance(center, r.min()));
    }

    template <typename R>
    circle_2<R> bounding_circle(const vector_2<R>& v)
    {
        return circle_2<R>(v, R(0));
    }

    template <typename R>
    rectangle_2<R> bounding_rectangle(const circle_2<R>& c)
    {
        return rectangle_2<R>(c.center() - vector_2<R>(c.radius()),
                           c.center() + vector_2<R>(c.radius()));
    }

    template <typename R>
    const rectangle_2<R>& bounding_rectangle(const rectangle_2<R>& r)
    {
        return r;
    }

    template <typename R>
    rectangle_2<R> bounding_rectangle(const vector_2<R>& v)
    {
        return rectangle_2<R>(v, v);
    }
}

#endif
