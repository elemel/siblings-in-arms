#ifndef SIBLINGS_CIRCLE_2_HPP
#define SIBLINGS_CIRCLE_2_HPP

#include "config.hpp"
#include "vector_2.hpp"
#include <iosfwd>

namespace siblings {
    /// Geometric circle in 2D.
    ///
    /// @invariant radius() >= 0
    class circle_2 {
    public:
        circle_2();
        circle_2(const vector_2<real>& center, real radius);
        circle_2(real center_x, real center_y, real radius);

        const vector_2<real>& center() const;
        real radius() const;

    private:
        vector_2<real> center_;
        real radius_;
    };

    /// Output circle in format "(center_x, center_y; radius)".
    std::ostream& operator<<(std::ostream& out, const circle_2& c);
}

#endif
