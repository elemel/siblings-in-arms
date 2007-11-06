#include "../geometry_2.hpp"
#include <boost/python.hpp>

using namespace siblings;
using namespace boost::python;

typedef const circle_2& c;
typedef const rectangle_2& r;
typedef const vector_2<real>& v;

BOOST_PYTHON_MODULE(geometry_2)
{
    def("squared_distance", (real (*)(c, c)) &squared_distance);
    def("squared_distance", (real (*)(c, r)) &squared_distance);
    def("squared_distance", (real (*)(c, v)) &squared_distance);
    def("squared_distance", (real (*)(r, c)) &squared_distance);
    def("squared_distance", (real (*)(r, r)) &squared_distance);
    def("squared_distance", (real (*)(r, v)) &squared_distance);
    def("squared_distance", (real (*)(v, c)) &squared_distance);
    def("squared_distance", (real (*)(v, r)) &squared_distance);
    def("squared_distance", (real (*)(v, v)) &squared_distance);

    def("distance", distance<circle_2, circle_2>);
    def("distance", distance<circle_2, rectangle_2>);
    def("distance", distance<circle_2, vector_2<real> >);
    def("distance", distance<rectangle_2, circle_2>);
    def("distance", distance<rectangle_2, rectangle_2>);
    def("distance", distance<rectangle_2, vector_2<real> >);
    def("distance", distance<vector_2<real>, circle_2>);
    def("distance", distance<vector_2<real>, rectangle_2>);
    def("distance", distance<vector_2<real>, vector_2<real> >);

    def("contains", (bool (*)(c, c)) &contains);
    def("contains", (bool (*)(c, r)) &contains);
    def("contains", (bool (*)(c, v)) &contains);
    def("contains", (bool (*)(r, c)) &contains);
    def("contains", (bool (*)(r, r)) &contains);
    def("contains", (bool (*)(r, v)) &contains);

    def("intersects", (bool (*)(c, c)) &intersects);
    def("intersects", (bool (*)(c, r)) &intersects);
    def("intersects", (bool (*)(r, c)) &intersects);
    def("intersects", (bool (*)(r, r)) &intersects);

    def("bounding_circle", (c (*)(c)) &bounding_circle,
        return_value_policy<copy_const_reference>());
    def("bounding_circle", (circle_2 (*)(r)) &bounding_circle);
    def("bounding_circle", (circle_2 (*)(v)) &bounding_circle);

    def("bounding_rectangle", (rectangle_2 (*)(c)) &bounding_rectangle);
    def("bounding_rectangle", (r (*)(r)) &bounding_rectangle,
        return_value_policy<copy_const_reference>());
    def("bounding_rectangle", (rectangle_2 (*)(v)) &bounding_rectangle);
}
