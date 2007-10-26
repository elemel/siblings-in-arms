#ifndef SIBLINGS_RECTANGLE_2_HPP
#define SIBLINGS_RECTANGLE_2_HPP

#include "config.hpp"
#include "vector_2.hpp"
#include <iosfwd>

namespace siblings {
    class rectangle_2 {
    public:
        rectangle_2();
        rectangle_2(const vector_2& min, const vector_2& max);
        rectangle_2(real min_x, real min_y, real max_x, real max_y);

        const vector_2& min() const;
        const vector_2& max() const;

        real min_x() const;
        real min_y() const;
        real max_x() const;
        real max_y() const;

    private:
        vector_2 min_;
        vector_2 max_;
    };

    std::ostream& operator<<(std::ostream& out, const rectangle_2& r);
}

#endif
