#ifndef SIBLINGS_GEOMETRY_HPP
#define SIBLINGS_GEOMETRY_HPP

#include "circle_2.hpp"
#include "config.hpp"
#include "rectangle_2.hpp"
#include "vector_2.hpp"
#include <cmath>

namespace siblings {
    real squared_distance(const circle_2<real>&, const circle_2<real>&);
    real squared_distance(const circle_2<real>&, const rectangle_2<real>&);
    real squared_distance(const circle_2<real>&, const vector_2<real>&);
    real squared_distance(const rectangle_2<real>&, const circle_2<real>&);
    real squared_distance(const rectangle_2<real>&, const rectangle_2<real>&);
    real squared_distance(const rectangle_2<real>&, const vector_2<real>&);
    real squared_distance(const vector_2<real>&, const circle_2<real>&);
    real squared_distance(const vector_2<real>&, const rectangle_2<real>&);
    real squared_distance(const vector_2<real>&, const vector_2<real>&);

    template <typename T, typename U>
    real distance(const T& a, const U& b)
    {
        return std::sqrt(squared_distance(a, b));
    }

    bool contains(const circle_2<real>& outer, const circle_2<real>& inner);
    bool contains(const circle_2<real>& outer, const rectangle_2<real>& inner);
    bool contains(const circle_2<real>& outer, const vector_2<real>& inner);
    bool contains(const rectangle_2<real>& outer, const circle_2<real>& inner);
    bool contains(const rectangle_2<real>& outer,
                  const rectangle_2<real>& inner);
    bool contains(const rectangle_2<real>& outer, const vector_2<real>& inner);

    bool intersects(const circle_2<real>&, const circle_2<real>&);
    bool intersects(const circle_2<real>&, const rectangle_2<real>&);
    bool intersects(const rectangle_2<real>&, const circle_2<real>&);
    bool intersects(const rectangle_2<real>&, const rectangle_2<real>&);

    const circle_2<real>& bounding_circle(const circle_2<real>&);
    circle_2<real> bounding_circle(const rectangle_2<real>&);
    circle_2<real> bounding_circle(const vector_2<real>&);

    rectangle_2<real> bounding_rectangle(const circle_2<real>&);
    const rectangle_2<real>& bounding_rectangle(const rectangle_2<real>&);
    rectangle_2<real> bounding_rectangle(const vector_2<real>&);
}

#endif
