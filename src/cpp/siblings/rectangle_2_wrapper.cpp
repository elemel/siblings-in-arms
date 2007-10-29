#include "rectangle_2.hpp"
#include <boost/python.hpp>
#include <sstream>

using namespace siblings;
using namespace boost::python;

namespace {
    vector_2 min_wrapper(const rectangle_2& r)
    {
        return r.min();
    }

    vector_2 max_wrapper(const rectangle_2& r)
    {
        return r.max();
    }

    std::string repr_wrapper(const rectangle_2& r) {
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
        .add_property("min", &min_wrapper)
        .add_property("max", &max_wrapper)
        .add_property("min_x", &rectangle_2::min_x)
        .add_property("min_y", &rectangle_2::min_y)
        .add_property("max_x", &rectangle_2::max_x)
        .add_property("max_y", &rectangle_2::max_y)

        // special methods
        .def(self_ns::str(self)) // workaround for ADL problems
        .def("__repr__", &repr_wrapper);
}