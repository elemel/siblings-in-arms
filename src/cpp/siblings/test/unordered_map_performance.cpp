// Copyright 2007 Mikael Lind.

#include "../unordered_map.hpp"
#include <iostream>
#include <map>
#include <string>
#include <boost/progress.hpp>
#include <boost/lexical_cast.hpp>

namespace {
    typedef std::map<int, int> ordered_map_type;
    typedef siblings::unordered_map<int, int> unordered_map_type;

    void rehash(ordered_map_type& m, int count) { }

    void rehash(unordered_map_type& m, int count)
    {
        m.rehash(count);
    }

    template <typename T>
    void measure_insert(int count, bool prealloc = false)
    {
        if (prealloc) {
            std::cout << "insert (preallocated)... ";
        } else {
            std::cout << "insert... ";
        }
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
    void measure_erase(int count)
    {
        std::cout << "erase... ";
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
    void measure_find(int count)
    {
        std::cout << "find... ";
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

int main(int argc, char* argv[])
{
    int count = 1000000;

    if (argc == 2) {
        count = -1;
        try {
            count = boost::lexical_cast<int>(argv[1]);
        } catch (boost::bad_lexical_cast&) { }
        if (count < 0) {
            std::cerr << "Bad repeat count: " << argv[1] << std::endl;
            std::cerr << "The repeat count must be a positive integer."
                      << std::endl;
            std::cerr << "Usage: " << argv[0] << " [<repeats>]" << std::endl;
            return 2;
        }
    }

    std::cout << "\nmeasuring std::map with " << count << " repeats\n"
              << std::endl;
    measure_insert<ordered_map_type>(count);
    measure_erase<ordered_map_type>(count);
    measure_find<ordered_map_type>(count);

    std::cout << "\nmeasuring siblings::unordered_map with " << count
              << " repeats\n" << std::endl;
    measure_insert<unordered_map_type>(count);
    measure_insert<unordered_map_type>(count, true);
    measure_erase<unordered_map_type>(count);
    measure_find<unordered_map_type>(count);

    return 0;
}
