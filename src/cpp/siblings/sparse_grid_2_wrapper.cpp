#include "sparse_grid_2.hpp"
#include <boost/bind.hpp>
#include <boost/foreach.hpp>
#include <boost/python.hpp>

using namespace siblings;
using namespace boost::python;

namespace {
    list find_wrapper(const sparse_grid_2& g, const circle_2& c)
    {
        list result;
        BOOST_FOREACH(int key, g.find(c)) {
            result.append(key);
        }
        return result;
    }
}

BOOST_PYTHON_MODULE(SparseGrid2)
{
    class_<sparse_grid_2>("SparseGrid2")
        // initializers
        .def(init<>())
        .def(init<const sparse_grid_2&>())
        .def(init<real>())

        // methods
        .def("insert", &sparse_grid_2::insert)
        .def("erase", &sparse_grid_2::erase)
        .def("find", &find_wrapper);
}
