#include "../config.hpp"
#include "../sink_iterator.hpp"
#include "../sparse_grid_2.hpp"
#include <boost/bind.hpp>
#include <boost/foreach.hpp>
#include <boost/python.hpp>

using namespace siblings;
using namespace boost::python;

namespace {
    typedef circle_2<real> circle_type;
    typedef sparse_grid_2<int, circle_type> grid_type;

    void append(list& l, int i) { l.append(i); }
    
    list find_wrapper(const grid_type& g, const circle_type& c)
    {
        list result;
        g.find(c, sinker(boost::bind(&append, result, _1)));
        return result;
    }
}

BOOST_PYTHON_MODULE(SparseGrid2) {
    class_<grid_type>("SparseGrid2")
        // initializers
        .def(init<>())
        .def(init<const grid_type&>())
        .def(init<real>())

        // attributes
        .add_property("__len__", &grid_type::size)
        .add_property("tile_count", &grid_type::tile_count)

        // methods
        .def("insert", &grid_type::insert)
        .def("erase", &grid_type::erase)
        .def("find", &find_wrapper);
}
