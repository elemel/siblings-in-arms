#include "../circle_2.hpp"
#include <cassert>
#include <cstddef>
#include <string>
#include <boost/lexical_cast.hpp>

using namespace siblings;

namespace {
    void test_default_ctor()
    {
        circle_2 c;
        assert(c.center() == vector_2());
        assert(c.radius() == real(0));
    }

    /// This test also handles the center and radius properties.
    void test_center_radius_ctor()
    {
        circle_2 c(vector_2(1, 2), 3);
        assert(c.center() == vector_2(1, 2));
        assert(c.radius() == real(3));
    }

    void test_output()
    {
        circle_2 c(vector_2(1, 2), 3);
        assert(boost::lexical_cast<std::string>(c) == "(1, 2; 3)");
    }
}

int main()
{
    test_default_ctor();
    test_center_radius_ctor();
    test_output();
    return 0;
}
