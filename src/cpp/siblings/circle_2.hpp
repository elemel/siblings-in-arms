#ifndef SIBLINGS_CIRCLE_2_HPP
#define SIBLINGS_CIRCLE_2_HPP

#include "config.hpp"
#include "vector_2.hpp"
#include <iosfwd>

namespace siblings {
    class circle_2 {
    public:
        circle_2();
        circle_2(const vector_2& center, real radius);

        const vector_2& center() const;
        real radius() const;

    private:
        vector_2 center_;
        real radius_;
    };

    std::ostream& operator<<(std::ostream& out, const circle_2& c);
}

#endif
