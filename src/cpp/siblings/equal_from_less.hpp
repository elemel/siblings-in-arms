// Copyright 2007 Mikael Lind.

#ifndef SIBLINGS_EQUAL_FROM_LESS_HPP
#define SIBLINGS_EQUAL_FROM_LESS_HPP

#include <functional>

namespace siblings {
    /// @brief Adapts an equal-to function from a less-than function.
    ///
    /// Compare is a model of Strict Weak Ordering.
    template <typename T, typename Compare = std::less<T> >
    struct equal_from_less {
        /// Comparison function.
        Compare less;

        /// Default constructor.
        explicit equal_from_less(const Compare& less = Compare())
            : less(less)
        { }

        /// Function call operator.
        bool operator()(const T& a, const T& b) const
        {
            return !less(a, b) && !less(b, a);
        }
    };
}

#endif
