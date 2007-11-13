#ifndef SIBLINGS_EQUAL_FROM_LESS_HPP
#define SIBLINGS_EQUAL_FROM_LESS_HPP

#include <functional>

namespace siblings {
    /// Compare models Strict Weak Ordering.
    template <typename T, typename Compare = std::less<T> >
    struct equal_from_less {
        Compare less;

        explicit equal_from_less(const Compare& less = Compare())
            : less(less)
        { }

        bool operator()(const T& a, const T& b) const
        {
            return !less(a, b) && !less(b, a);
        }
    };
}

#endif
