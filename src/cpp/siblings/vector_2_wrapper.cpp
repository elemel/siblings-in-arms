#include "vector_2.hpp"
#include <boost/python.hpp>
#include <sstream>

using namespace siblings;
using namespace boost::python;

namespace {
    real get_x_wrapper(const vector_2& v)
    {
        return v.x();
    }

    void set_x_wrapper(vector_2& v, real x)
    {
        v.x() = x;
    }

    real get_y_wrapper(const vector_2& v)
    {
        return v.y();
    }

    void set_y_wrapper(vector_2& v, real y)
    {
        v.y() = y;
    }

    std::string repr_wrapper(const vector_2& v)
    {
        std::ostringstream out;
        out << "Vector2(" << v.x() << ", " << v.y() << ")";
        return out.str();
    }
}

BOOST_PYTHON_MODULE(Vector2)
{
    class_<vector_2>("Vector2")
        // initializers
        .def(init<>())
        .def(init<const vector_2&>())
        .def(init<real, real>())

        // attributes
        .add_property("x", &get_x_wrapper, &set_x_wrapper)
        .add_property("y", &get_y_wrapper, &set_y_wrapper)
        .add_property("squared_length", &vector_2::squared_length)
        .add_property("length", &vector_2::length)

        // operators
        .def(self += self)
        .def(self -= self)
        .def(self *= real())
        .def(self /= real())
        .def(-self)
        .def(self + self)
        .def(self - self)
        .def(self * real())
        .def(real() * self)
        .def(self / real())

        // other special methods
        .def(abs(self))
        .def(self_ns::str(self)) // workaround for ADL problems
        .def("__repr__", &repr_wrapper)

        // other methods
        .def("dot", &dot)
        .def("cross", &cross);
}
