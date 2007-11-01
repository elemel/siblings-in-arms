#ifndef SIBLINGS_VECTOR_2_HPP
#define SIBLINGS_VECTOR_2_HPP

#include "config.hpp"
#include <iosfwd>

namespace siblings {
    /// Spatial vector in 2D.
    class vector_2 {
    public:
        /// Construct vector having x = y = 0.
        vector_2();

        /// Construct vector having x = y = r.
        vector_2(real r);

        /// Construct vector having the specified x and y components.
        vector_2(real x, real y);

        vector_2& operator+=(const vector_2& other);
        vector_2& operator-=(const vector_2& other);
        vector_2& operator*=(real other);
        vector_2& operator/=(real other);

        real& x();
        real& y();
        real x() const;
        real y() const;

        /// Compute squared magnitude of vector.
        real squared_magnitude() const;

        /// Compute magnitude of vector. Prefer squared_magnitude where
        /// applicable; that operation is more efficient.
        ///
        /// @see squared_magnitude
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

    /// Compare two vectors for equality.
    bool operator==(const vector_2& a, const vector_2& b);

    /// Compare two vectors for inequality.
    bool operator!=(const vector_2& a, const vector_2& b);

    /// Output vector in format "[x, y]".
    std::ostream& operator<<(std::ostream& out, const vector_2& v);

    /// Compute magnitude of vector.
    ///
    /// @see vector_2::magnitude
    real abs(const vector_2& v);

    /// Compute dot product of two vectors.
    real dot(const vector_2& a, const vector_2& b);

    /// Compute cross product of two vectors.
    real cross(const vector_2& a, const vector_2& b);
}

#endif
