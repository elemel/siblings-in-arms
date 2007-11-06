#ifndef SIBLINGS_VECTOR_2_HPP
#define SIBLINGS_VECTOR_2_HPP

#include <cmath>
#include <ostream>

namespace siblings {
    /// Spatial vector in 2D.
    template <typename T>
    class vector_2 {
    public:
        /// Construct vector having x = y = 0.
        vector_2() : x_(T(0)), y_(T(0)) { }

        /// Construct vector having x = y = a.
        vector_2(T a) : x_(a), y_(a) { }

        /// Construct vector having the specified x and y components.
        vector_2(T x, T y) : x_(x), y_(y) { }

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

        vector_2& operator*=(T other)
        {
            x() *= other;
            y() *= other;
            return *this;
        }

        vector_2& operator/=(T other)
        {
            x() /= other;
            y() /= other;
            return *this;
        }

        vector_2 operator-() const
        {
            return vector_2(-x(), -y());
        }

        T& x() { return x_; }
        T& y() { return y_; }
        T x() const { return x_; }
        T y() const { return y_; }

        /// Compute squared magnitude of vector.
        T squared_magnitude() const { return dot(*this, *this); }

        /// Compute magnitude of vector. Prefer squared_magnitude where
        /// applicable; that operation is more efficient.
        ///
        /// @see squared_magnitude
        T magnitude() const { return std::sqrt(squared_magnitude()); }

    private:
        real x_;
        real y_;
    };

    template <typename T>
    vector_2<T> operator+(vector_2<T> left, const vector_2<T>& right)
    {
        left += right;
        return left;
    }

    template <typename T>
    vector_2<T> operator-(vector_2<T> left, const vector_2<T>& right)
    {
        left -= right;
        return right;
    }

    template <typename T>
    vector_2<T> operator*(vector_2<T> left, T right)
    {
        left *= right;
        return left;
    }

    template <typename T>
    vector_2<T> operator*(T left, vector_2<T> right)
    {
        right *= left;
        return right;
    }

    template <typename T>
    vector_2<T> operator/(vector_2<T> left, T right)
    {
        left /= right;
        return left;
    }

    /// Compare two vectors for equality.
    template <typename T>
    bool operator==(const vector_2<T>& a, const vector_2<T>& b)
    {
        return a.x() == b.x() && a.y() == b.y();
    }

    /// Compare two vectors for inequality.
    template <typename T>
    bool operator!=(const vector_2<T>& a, const vector_2<T>& b)
    {
        return !(a == b);
    }

    /// Output vector in format "[x, y]".
    template <typename T>
    std::ostream& operator<<(std::ostream& out, const vector_2<T>& v)
    {
        return out << '[' << v.x() << ',' << ' ' << v.y() << ']';
    }

    /// Compute magnitude of vector.
    ///
    /// @see vector_2::magnitude
    template <typename T>
    T abs(const vector_2<T>& v)
    {
        return v.magnitude();
    }

    /// Compute dot product of two vectors.
    template <typename T>
    T dot(const vector_2<T>& a, const vector_2<T>& b)
    {
        return a.x() * b.x() + a.y() * b.y();
    }

    /// Compute cross product of two vectors.
    template <typename T>
    T cross(const vector_2<T>& a, const vector_2<T>& b)
    {
        return a.x() * b.y() - a.y() * b.x();
    }
}

#endif
