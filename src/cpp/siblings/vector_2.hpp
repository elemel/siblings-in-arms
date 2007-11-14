// Copyright 2007 Mikael Lind.

#ifndef SIBLINGS_VECTOR_2_HPP
#define SIBLINGS_VECTOR_2_HPP

#include <cmath>
#include <ostream>

namespace siblings {
    /// Spatial vector in 2D.
    template <typename R>
    class vector_2 {
    public:
        /// Real type.
        typedef R real_type;

        /// @brief Default constructor.
        ///
        /// Constructs a vector where all components are equal to the specified
        /// number.
        ///
        /// @post v.x() == a
        /// @post v.y() == a
        vector_2(R a = R(0)) : x_(a), y_(a) { }

        /// @brief Constructs a vector having the specified components.
        ///
        /// @post v.x() == x
        /// @post v.y() == y
        vector_2(R x, R y) : x_(x), y_(y) { }

        /// Addition assignment operator.
        vector_2& operator+=(const vector_2& other)
        {
            x() += other.x();
            y() += other.y();
            return *this;
        }

        /// Subtraction assignment operator.
        vector_2& operator-=(const vector_2& other)
        {
            x() -= other.x();
            y() -= other.y();
            return *this;
        }

        /// Multiplication assignment operator.
        vector_2& operator*=(R other)
        {
            x() *= other;
            y() *= other;
            return *this;
        }

        /// Division assignment operator.
        vector_2& operator/=(R other)
        {
            x() /= other;
            y() /= other;
            return *this;
        }

        /// Negation operator.
        vector_2 operator-() const
        {
            return vector_2(-x(), -y());
        }

        /// Returns a reference to the <em>x</em> component.
        R& x() { return x_; }

        /// Returns the <em>x</em> component.
        R x() const { return x_; }

        /// Returns a reference to the <em>y</em> component.
        R& y() { return y_; }

        /// Returns the <em>y</em> component.
        R y() const { return y_; }

        /// Returns the squared magnitude of the vector.
        R squared_magnitude() const { return dot(*this, *this); }

        /// @brief Returns the magnitude of the vector.
        R magnitude() const { return std::sqrt(squared_magnitude()); }

    private:
        /// The <em>x</em> component.
        R x_;

        /// The <em>y</em> component.
        R y_;
    };

    /// Addition operator.
    template <typename R>
    vector_2<R> operator+(vector_2<R> left, const vector_2<R>& right)
    {
        left += right;
        return left;
    }

    /// Subtraction operator.
    template <typename R>
    vector_2<R> operator-(vector_2<R> left, const vector_2<R>& right)
    {
        left -= right;
        return right;
    }

    /// Multiplication operator.
    template <typename R>
    vector_2<R> operator*(vector_2<R> left, R right)
    {
        left *= right;
        return left;
    }

    /// Multiplication operator.
    template <typename R>
    vector_2<R> operator*(R left, vector_2<R> right)
    {
        right *= left;
        return right;
    }

    /// Division operator.
    template <typename R>
    vector_2<R> operator/(vector_2<R> left, R right)
    {
        left /= right;
        return left;
    }

    /// Equal-to operator.
    template <typename R>
    bool operator==(const vector_2<R>& a, const vector_2<R>& b)
    {
        return a.x() == b.x() && a.y() == b.y();
    }

    /// Not-equal-to operator.
    template <typename R>
    bool operator!=(const vector_2<R>& a, const vector_2<R>& b)
    {
        return !(a == b);
    }

    /// @brief Output operator.
    ///
    /// Writes the vector to the stream using the format "[x, y]".
    template <typename R>
    std::ostream& operator<<(std::ostream& out, const vector_2<R>& v)
    {
        return out << '[' << v.x() << ',' << ' ' << v.y() << ']';
    }

    /// @brief Returns the magnitude of the specified vector.
    ///
    /// @see vector_2::magnitude
    template <typename R>
    R abs(const vector_2<R>& v)
    {
        return v.magnitude();
    }

    /// Returns the dot product of two vectors.
    template <typename R>
    R dot(const vector_2<R>& a, const vector_2<R>& b)
    {
        return a.x() * b.x() + a.y() * b.y();
    }

    /// Returns the cross product of two vectors.
    template <typename R>
    R cross(const vector_2<R>& a, const vector_2<R>& b)
    {
        return a.x() * b.y() - a.y() * b.x();
    }
}

#endif
