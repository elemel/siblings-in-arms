#include "geometry.hpp"
#include <boost/python.hpp>

using namespace siblings;
using namespace boost::python;

BOOST_PYTHON_MODULE(geometry)
{
    def("squared_distance", &squared_distance);
    def("distance", &distance);
}
