#ifndef SIBLINGS_CIRCLE_2_HPP
#define SIBLINGS_CIRCLE_2_HPP

#include "vector_2.hpp"
#include <ostream>

namespace siblings {
    /// Geometric circle in 2D.
    ///
    /// @invariant radius() >= 0
    template <typename T>
    class circle_2 {
    public:
        typedef T value_type;

        circle_2() : radius_(T(0)) { }

        circle_2(const vector_2<T>& center, T radius)
            : center_(center), radius_(radius)
        { }

        circle_2(T center_x, T center_y, T radius)
            : center_(center_x, center_y), radius_(radius)
        { }

        const vector_2<T>& center() const { return center_; }
        T radius() const { return radius_; }

    private:
        vector_2<T> center_;
        T radius_;
    };

    /// Output circle in format "(center_x, center_y; radius)".
    template <typename T>
    std::ostream& operator<<(std::ostream& out, const circle_2<T>& c)
    {
        return out << "(" << c.center().x() << ", " << c.center().y() << "; "
                   << c.radius() << ")";
    }
}

#endif
