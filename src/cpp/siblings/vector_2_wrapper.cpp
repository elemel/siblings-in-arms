#include "vector_2.hpp"
#include <boost/python.hpp>
#include <sstream>

using namespace siblings;
using namespace boost::python;

namespace {
    std::string repr_vector_2(const vector_2& v) {
        std::ostringstream out;
        out << "Vector2(" << v.x << ", " << v.y << ")";
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
        .def_readwrite("x", &vector_2::x)
        .def_readwrite("y", &vector_2::y)
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
        .def("__repr__", &repr_vector_2)

        // other methods
        .def("dot", &dot)
        .def("cross", &cross);
}
