#include "grid_2.hpp"
#include <boost/bind.hpp>
#include <boost/foreach.hpp>
#include <boost/python.hpp>

using namespace siblings;
using namespace boost::python;

namespace {
    list find_wrapper(const grid_2& g, const circle_2& c)
    {
        list result;
        BOOST_FOREACH(int key, g.find(c)) {
            result.append(key);
        }
        return result;
    }
}

BOOST_PYTHON_MODULE(Grid2)
{
    class_<grid_2>("Grid2")
        // initializers
        .def(init<>())
        .def(init<const grid_2&>())
        .def(init<real>())

        // methods
        .def("add", &grid_2::add)
        .def("update", &grid_2::update)
        .def("remove", &grid_2::remove)
        .def("find", &find_wrapper);
}
