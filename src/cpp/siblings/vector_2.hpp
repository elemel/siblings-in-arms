#ifndef SIBLINGS_VECTOR_2_HPP
#define SIBLINGS_VECTOR_2_HPP

#include "config.hpp"
#include <iosfwd>

namespace siblings {
    /// Spatial vector in 2D.
    class vector_2 {
    public:
        inline vector_2() : x_(real(0)), y_(real(0)) { }
        inline vector_2(real r) : x_(r), y_(r) { }
        inline vector_2(real x, real y) : x_(x), y_(y) { }

        vector_2& operator+=(const vector_2& other);
        vector_2& operator-=(const vector_2& other);
        vector_2& operator*=(real other);
        vector_2& operator/=(real other);

        inline real& x() { return x_; }
        inline real& y() { return y_; }
        inline real x() const { return x_; }
        inline real y() const { return y_; }

        real squared_magnitude() const;
        real magnitude() const;

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

    inline bool operator!=(const vector_2& a, const vector_2& b)
    {
        return !(a == b);
    }

    /// Output vector in format "[x, y]".
    std::ostream& operator<<(std::ostream& out, const vector_2& v);

    inline real abs(const vector_2& v)
    {
        return v.magnitude();
    }

    real dot(const vector_2& a, const vector_2& b);
    real cross(const vector_2& a, const vector_2& b);
}

#endif
