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

        inline const vector_2& min() const { return min_; }
        inline const vector_2& max() const { return max_; }
        
        inline real min_x() const { return min_.x(); }
        inline real min_y() const { return min_.y(); }
        inline real max_x() const { return max_.x(); }
        inline real max_y() const { return max_.y(); }

        vector_2 center() const;

    private:
        vector_2 min_;
        vector_2 max_;
    };

    std::ostream& operator<<(std::ostream& out, const rectangle_2& r);
}

#endif
