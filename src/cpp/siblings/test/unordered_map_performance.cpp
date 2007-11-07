#include "../unordered_map.hpp"
#include <iostream>
#include <map>
#include <string>
#include <boost/progress.hpp>

namespace {
    void rehash(std::map<int, int>& m, int count) { }

    void rehash(siblings::unordered_map<int, int>& m, int count)
    {
        m.rehash(count);
    }

    template <typename T>
    void measure_insert(const std::string& type, int count,
                        bool prealloc = false)
    {
        std::cout << "Measuring " << count << (prealloc ? " preallocated" : "")
                  << " insertions into " << type << "... ";
        std::cout.flush();

        T m;
        if (prealloc) {
            rehash(m, count);
        }
        boost::progress_timer t;
        for (int i = 0; i < count; ++i) {
            m.insert(typename T::value_type(i, i));
        }
    }

    template <typename T>
    void measure_erase(const std::string& type, int count)
    {
        std::cout << "Measuring " << count << " removals from " << type
                  << "... ";
        std::cout.flush();

        T m;
        rehash(m, count);
        for (int i = 0; i < count; ++i) {
            m.insert(typename T::value_type(i, i));
        }

        boost::progress_timer t;
        for (int i = 0; i < count; ++i) {
            m.erase(i);
        }
    }

    template <typename T>
    void measure_find(const std::string& type, int count)
    {
        std::cout << "Measuring " << count << " lookups in " << type << "... ";
        std::cout.flush();

        T m;
        rehash(m, count);
        for (int i = 0; i < count; ++i) {
            m.insert(typename T::value_type(i, i));
        }

        boost::progress_timer t;
        for (int i = 0; i < count; ++i) {
            m.find(i);
        }
    }
}

int main()
{
    typedef std::map<int, int> ordered_map_type;
    typedef siblings::unordered_map<int, int> unordered_map_type;

    int count = 1000000;

    measure_insert<ordered_map_type>("std::map", count);
    measure_erase<ordered_map_type>("std::map", count);
    measure_find<ordered_map_type>("std::map", count);

    measure_insert<unordered_map_type>("siblings::unordered_map", count);
    measure_insert<unordered_map_type>("siblings::unordered_map", count,
                                       true);
    measure_erase<unordered_map_type>("siblings::unordered_map", count);
    measure_find<unordered_map_type>("siblings::unordered_map", count);

    return 0;
}
