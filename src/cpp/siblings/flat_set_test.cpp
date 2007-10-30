#include "flat_set.hpp"
#include <cassert>
#include <cstddef>

using namespace siblings;

int main()
{
    int data[] = { 3, 9, 2, 1, 4, 7, 6, 0, 8, 5 };
    std::size_t data_size = sizeof(data) / sizeof(data[0]);

    flat_set<int> cont(data, data + data_size);
    assert(cont.size() == data_size);

    flat_set<int>::iterator i = cont.begin();
    for (int j = 0; j < 10; ++j)
    {
        assert(*i++ == j);
    }
    assert(i == cont.end());

    return 0;
}
