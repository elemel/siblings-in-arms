#ifndef SIBLINGS_VECTOR_2_HPP
#define SIBLINGS_VECTOR_2_HPP

#include <cmath>
#include <ostream>

namespace siblings {
    /// Spatial vector in 2D.
    template <typename R>
    class vector_2 {
    public:
        typedef R real_type;

        /// Construct vector having x = y = 0.
        vector_2() : x_(R(0)), y_(R(0)) { }

        /// Construct vector having x = y = a.
        vector_2(R a) : x_(a), y_(a) { }

        /// Construct vector having the specified x and y components.
        vector_2(R x, R y) : x_(x), y_(y) { }

        vector_2& operator+=(const vector_2& other)
        {
            x() += other.x();
            y() += other.y();
            return *this;
        }

        vector_2& operator-=(const vector_2& other)
        {
            x() -= other.x();
            y() -= other.y();
            return *this;
        }

        vector_2& operator*=(R other)
        {
            x() *= other;
            y() *= other;
            return *this;
        }

        vector_2& operator/=(R other)
        {
            x() /= other;
            y() /= other;
            return *this;
        }

        vector_2 operator-() const
        {
            return vector_2(-x(), -y());
        }

        R& x() { return x_; }
        R& y() { return y_; }
        R x() const { return x_; }
        R y() const { return y_; }

        /// Compute squared magnitude of vector.
        R squared_magnitude() const { return dot(*this, *this); }

        /// Compute magnitude of vector. Prefer squared_magnitude where
        /// applicable; that operation is more efficient.
        ///
        /// @see squared_magnitude
        R magnitude() const { return std::sqrt(squared_magnitude()); }

    private:
        R x_;
        R y_;
    };

    template <typename R>
    vector_2<R> operator+(vector_2<R> left, const vector_2<R>& right)
    {
        left += right;
        return left;
    }

    template <typename R>
    vector_2<R> operator-(vector_2<R> left, const vector_2<R>& right)
    {
        left -= right;
        return right;
    }

    template <typename R>
    vector_2<R> operator*(vector_2<R> left, R right)
    {
        left *= right;
        return left;
    }

    template <typename R>
    vector_2<R> operator*(R left, vector_2<R> right)
    {
        right *= left;
        return right;
    }

    template <typename R>
    vector_2<R> operator/(vector_2<R> left, R right)
    {
        left /= right;
        return left;
    }

    /// Compare two vectors for equality.
    template <typename R>
    bool operator==(const vector_2<R>& a, const vector_2<R>& b)
    {
        return a.x() == b.x() && a.y() == b.y();
    }

    /// Compare two vectors for inequality.
    template <typename R>
    bool operator!=(const vector_2<R>& a, const vector_2<R>& b)
    {
        return !(a == b);
    }

    /// Output vector in format "[x, y]".
    template <typename R>
    std::ostream& operator<<(std::ostream& out, const vector_2<R>& v)
    {
        return out << '[' << v.x() << ',' << ' ' << v.y() << ']';
    }

    /// Compute magnitude of vector.
    ///
    /// @see vector_2::magnitude
    template <typename R>
    R abs(const vector_2<R>& v)
    {
        return v.magnitude();
    }

    /// Compute dot product of two vectors.
    template <typename R>
    R dot(const vector_2<R>& a, const vector_2<R>& b)
    {
        return a.x() * b.x() + a.y() * b.y();
    }

    /// Compute cross product of two vectors.
    template <typename R>
    R cross(const vector_2<R>& a, const vector_2<R>& b)
    {
        return a.x() * b.y() - a.y() * b.x();
    }
}

#endif
