#include "circle_2.hpp"
#include <boost/python.hpp>
#include <sstream>

using namespace siblings;
using namespace boost::python;

namespace {
    std::string repr_circle_2(const circle_2& c) {
        std::ostringstream out;
        out << "Circle2(Vector2(" << c.center().x << ", " << c.center().y
            << "), " << c.radius() << ")";
        return out.str();
    }
}

BOOST_PYTHON_MODULE(Circle2)
{
    class_<circle_2>("Circle2")
        // initializers
        .def(init<>())
        .def(init<const circle_2&>())
        .def(init<const vector_2&, real>())

        // attributes
        .def("center", &circle_2::center, return_internal_reference<>())
        .def("radius", &circle_2::radius)

        // special methods
        .def(self_ns::str(self)) // workaround for ADL problems
        .def("__repr__", &repr_circle_2);
}
