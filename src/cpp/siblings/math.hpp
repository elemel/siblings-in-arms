#ifndef SIBLINGS_MATH_HPP
#define SIBLINGS_MATH_HPP

#include <algorithm>

namespace siblings {
    template <typename T>
    T square(const T& value) { return value * value; }

    template <typename T>
    const T& max_3(const T& a, const T& b, const T& c)
    {
        return std::max(std::max(a, b), c);
    }

    template <typename T>
    const T& min_3(const T& a, const T& b, const T& c)
    {
        return std::min(std::min(a, b), c);
    }
}

#endif
