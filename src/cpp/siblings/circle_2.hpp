// Copyright 2007 Mikael Lind.

#ifndef SIBLINGS_CIRCLE_2_HPP
#define SIBLINGS_CIRCLE_2_HPP

#include "vector_2.hpp"
#include <ostream>

namespace siblings {
    /// @brief Geometric circle in 2D.
    ///
    /// @invariant radius() >= 0
    template <typename R>
    class circle_2 {
    public:
        typedef R real_type;

        circle_2() : radius_(R(0)) { }

        circle_2(const vector_2<R>& center, R radius)
            : center_(center), radius_(radius)
        { }

        circle_2(R center_x, R center_y, R radius)
            : center_(center_x, center_y), radius_(radius)
        { }

        const vector_2<R>& center() const { return center_; }
        R radius() const { return radius_; }

    private:
        vector_2<R> center_;
        R radius_;
    };

    /// Output circle in format "(center_x, center_y; radius)".
    template <typename R>
    std::ostream& operator<<(std::ostream& out, const circle_2<R>& c)
    {
        return out << "(" << c.center().x() << ", " << c.center().y() << "; "
                   << c.radius() << ")";
    }
}

#endif
