#include "vector_2.hpp"
#include <cmath>
#include <ostream>

namespace siblings {
    vector_2::vector_2()
        : x(),
          y()
    { }

    vector_2::vector_2(real x, real y)
        : x(x),
          y(y)
    { }

    vector_2& vector_2::operator+=(const vector_2& other)
    {
        x += other.x;
        y += other.y;
        return *this;
    }

    vector_2& vector_2::operator-=(const vector_2& other)
    {
        x -= other.x;
        y -= other.y;
        return *this;
    }

    vector_2& vector_2::operator*=(real other)
    {
        x *= other;
        y *= other;
        return *this;
    }
    
    vector_2& vector_2::operator/=(real other)
    {
        x /= other;
        y /= other;
        return *this;
    }

    real vector_2::squared_length() const
    {
        return x * x + y * y;
    }

    real vector_2::length() const
    {
        return std::sqrt(squared_length());
    }

    vector_2 operator-(const vector_2& v)
    {
        return vector_2(-v.x, -v.y);
    }

    vector_2 operator+(const vector_2& left, const vector_2& right)
    {
        return vector_2(left) += right;
    }

    vector_2 operator-(const vector_2& left, const vector_2& right)
    {
        return vector_2(left) -= right;
    }

    vector_2 operator*(const vector_2& left, real right)
    {
        return vector_2(left) *= right;
    }

    vector_2 operator*(real left, const vector_2& right)
    {
        return vector_2(right) *= left;
    }

    vector_2 operator/(const vector_2& left, real right)
    {
        return vector_2(left) /= right;
    }

    std::ostream& operator<<(std::ostream& out, const vector_2& v)
    {
        return out << '[' << v.x << ',' << ' ' << v.y << ']';
    }

    real abs(const vector_2& v)
    {
        return std::sqrt(v.squared_length());
    }

    real dot(const vector_2& a, const vector_2& b)
    {
        return a.x * b.x + a.y * b.y;
    }

    real cross(const vector_2& a, const vector_2& b)
    {
        return a.x * b.y - a.y * b.x;
    }
}
