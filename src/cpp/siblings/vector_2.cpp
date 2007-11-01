#include "math.hpp"
#include "vector_2.hpp"
#include <cmath>
#include <ostream>

namespace siblings {
    vector_2::vector_2() : x_(real(0)), y_(real(0)) { }
    vector_2::vector_2(real r) : x_(r), y_(r) { }
    vector_2::vector_2(real x, real y) : x_(x), y_(y) { }

    vector_2& vector_2::operator+=(const vector_2& other)
    {
        x_ += other.x_;
        y_ += other.y_;
        return *this;
    }

    vector_2& vector_2::operator-=(const vector_2& other)
    {
        x_ -= other.x_;
        y_ -= other.y_;
        return *this;
    }

    vector_2& vector_2::operator*=(real other)
    {
        x_ *= other;
        y_ *= other;
        return *this;
    }
    
    vector_2& vector_2::operator/=(real other)
    {
        x_ /= other;
        y_ /= other;
        return *this;
    }

    real& vector_2::x() { return x_; }
    real& vector_2::y() { return y_; }
    real vector_2::x() const { return x_; }
    real vector_2::y() const { return y_; }

    real vector_2::squared_magnitude() const
    {
        return square(x_) + square(y_);
    }

    real vector_2::magnitude() const
    {
        return std::sqrt(squared_magnitude());
    }

    vector_2 operator-(const vector_2& v)
    {
        return vector_2(-v.x(), -v.y());
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

    bool operator==(const vector_2& a, const vector_2& b)
    {
        return a.x() == b.x() && a.y() == b.y();
    }

    bool operator!=(const vector_2& a, const vector_2& b)
    {
        return !(a == b);
    }

    std::ostream& operator<<(std::ostream& out, const vector_2& v)
    {
        return out << '[' << v.x() << ',' << ' ' << v.y() << ']';
    }

    real abs(const vector_2& v)
    {
        return v.magnitude();
    }

    real dot(const vector_2& a, const vector_2& b)
    {
        return a.x() * b.x() + a.y() * b.y();
    }

    real cross(const vector_2& a, const vector_2& b)
    {
        return a.x() * b.y() - a.y() * b.x();
    }
}
