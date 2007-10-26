#include "rectangle_2.hpp"
#include <boost/python.hpp>
#include <sstream>

using namespace siblings;
using namespace boost::python;

namespace {
    std::string repr_rectangle_2(const rectangle_2& r) {
        std::ostringstream out;
        out << "Rectangle2(" << r.min_x() << ", " << r.min_y() << ", "
            << r.max_x() << ", " << r.max_y() << ")";
        return out.str();
    }
}

BOOST_PYTHON_MODULE(Rectangle2)
{
    class_<rectangle_2>("Rectangle2")
        // initializers
        .def(init<>())
        .def(init<const rectangle_2&>())
        .def(init<const vector_2&, const vector_2&>())
        .def(init<real, real, real, real>())

        // attributes
        .def("min", &rectangle_2::min, return_internal_reference<>())
        .def("max", &rectangle_2::max, return_internal_reference<>())
        .def("min_x", &rectangle_2::min_x)
        .def("min_y", &rectangle_2::min_y)
        .def("max_x", &rectangle_2::max_x)
        .def("max_y", &rectangle_2::max_y)

        // special methods
        .def(self_ns::str(self)) // workaround for ADL problems
        .def("__repr__", &repr_rectangle_2);
}
