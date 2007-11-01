#ifndef SIBLINGS_GEOMETRY_HPP
#define SIBLINGS_GEOMETRY_HPP

#include "circle_2.hpp"
#include "rectangle_2.hpp"
#include "vector_2.hpp"
#include <cmath>

namespace siblings {
    real squared_distance(const circle_2&, const circle_2&);
    real squared_distance(const circle_2&, const rectangle_2&);
    real squared_distance(const circle_2&, const vector_2&);
    real squared_distance(const rectangle_2&, const rectangle_2&);
    real squared_distance(const rectangle_2&, const vector_2&);
    real squared_distance(const vector_2&, const vector_2&);

    bool contains(const circle_2& outer, const circle_2& inner);
    bool contains(const circle_2& outer, const rectangle_2& inner);
    bool contains(const circle_2& outer, const vector_2& inner);
    bool contains(const rectangle_2& outer, const circle_2& inner);
    bool contains(const rectangle_2& outer, const rectangle_2& inner);
    bool contains(const rectangle_2& outer, const vector_2& inner);

    bool intersects(const circle_2&, const circle_2&);
    bool intersects(const circle_2&, const rectangle_2&);
    bool intersects(const rectangle_2&, const rectangle_2&);

    circle_2 bounding_circle(const rectangle_2& r);
    circle_2 bounding_circle(const vector_2& v);

    rectangle_2 bounding_rectangle(const circle_2& c);
    rectangle_2 bounding_rectangle(const vector_2& v);

    inline real squared_distance(const rectangle_2& r, const circle_2& c)
    {
        return squared_distance(c, r);
    }

    inline real squared_distance(const vector_2& v, const circle_2& c)
    {
        return squared_distance(c, v);
    }

    inline real squared_distance(const vector_2& v, const rectangle_2& r)
    {
        return squared_distance(r, v);
    }

    template <typename T, typename U>
    real distance(const T& a, const U& b)
    {
        return std::sqrt(squared_distance(a, b));
    }

    inline bool intersects(const rectangle_2& r, const circle_2& c)
    {
        return intersects(c, r);
    }

    inline const circle_2& bounding_circle(const circle_2& c)
    {
        return c;
    }

    inline const rectangle_2& bounding_rectangle(const rectangle_2& r)
    {
        return r;
    }
}

#endif
