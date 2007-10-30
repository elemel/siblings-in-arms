#ifndef SIBLINGS_VECTOR_2_HPP
#define SIBLINGS_VECTOR_2_HPP

#include "config.hpp"
#include <iosfwd>

namespace siblings {
    class vector_2 {
    public:
        vector_2();
        vector_2(real x, real y);

        vector_2& operator+=(const vector_2& other);
        vector_2& operator-=(const vector_2& other);
        vector_2& operator*=(real other);
        vector_2& operator/=(real other);

        inline real& x() { return x_; }
        inline real& y() { return y_; }
        inline real x() const { return x_; }
        inline real y() const { return y_; }
        real squared_length() const;
        real length() const;

    private:
        real x_;
        real y_;
    };

    vector_2 operator-(const vector_2& v);
    vector_2 operator+(const vector_2& left, const vector_2& right);
    vector_2 operator-(const vector_2& left, const vector_2& right);
    vector_2 operator*(const vector_2& left, real right);
    vector_2 operator*(real left, const vector_2& right);
    vector_2 operator/(const vector_2& left, real right);

    bool operator==(const vector_2& a, const vector_2& b);
    bool operator!=(const vector_2& a, const vector_2& b);

    std::ostream& operator<<(std::ostream& out, const vector_2& v);

    real abs(const vector_2& v);
    real dot(const vector_2& a, const vector_2& b);
    real cross(const vector_2& a, const vector_2& b);
}

#endif
