#ifndef SIBLINGS_VECTOR_2_HPP
#define SIBLINGS_VECTOR_2_HPP

#include "config.hpp"
#include <iosfwd>

namespace siblings {
    class vector_2 {
    public:
        real x;
        real y;

        vector_2();
        vector_2(real x, real y);

        vector_2& operator+=(const vector_2& other);
        vector_2& operator-=(const vector_2& other);
        vector_2& operator*=(real other);
        vector_2& operator/=(real other);

        real squared_length() const;
        real length() const;
    };

    vector_2 operator-(const vector_2& v);
    vector_2 operator+(const vector_2& left, const vector_2& right);
    vector_2 operator-(const vector_2& left, const vector_2& right);
    vector_2 operator*(const vector_2& left, real right);
    vector_2 operator*(real left, const vector_2& right);
    vector_2 operator/(const vector_2& left, real right);

    std::ostream& operator<<(std::ostream& out, const vector_2& v);

    real abs(const vector_2& v);
    real dot(const vector_2& a, const vector_2& b);
    real cross(const vector_2& a, const vector_2& b);
}

#endif
