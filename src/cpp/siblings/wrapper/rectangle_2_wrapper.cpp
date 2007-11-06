#include "../config.hpp"
#include "../rectangle_2.hpp"
#include <boost/python.hpp>
#include <sstream>

using namespace siblings;
using namespace boost::python;

namespace {
    vector_2<real> min_wrapper(const rectangle_2<real>& r)
    {
        return r.min();
    }

    vector_2<real> max_wrapper(const rectangle_2<real>& r)
    {
        return r.max();
    }

    std::string repr_wrapper(const rectangle_2<real>& r) {
        std::ostringstream out;
        out << "Rectangle2(" << r.min().x() << ", " << r.min().y() << ", "
            << r.max().x() << ", " << r.max().y() << ")";
        return out.str();
    }
}

BOOST_PYTHON_MODULE(Rectangle2)
{
    class_<rectangle_2<real> >("Rectangle2")
        // initializers
        .def(init<>())
        .def(init<const rectangle_2<real>&>())
        .def(init<const vector_2<real>&, const vector_2<real>&>())
        .def(init<real, real, real, real>())

        // attributes
        .add_property("min", &min_wrapper)
        .add_property("max", &max_wrapper)

        // special methods
        .def(self_ns::str(self)) // workaround for ADL problems
        .def("__repr__", &repr_wrapper);
}
