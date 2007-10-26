#ifndef SIBLINGS_GEOMETRY_HPP
#define SIBLINGS_GEOMETRY_HPP

#include "circle_2.hpp"
#include "rectangle_2.hpp"
#include "vector_2.hpp"

namespace siblings {
    real squared_distance(const vector_2& a, const vector_2& b);
    real distance(const vector_2& a, const vector_2& b);
}

#endif
