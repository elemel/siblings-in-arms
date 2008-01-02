#ifndef SIBLINGS_HEX_GRAPH_HPP
#define SIBLINGS_HEX_GRAPH_HPP

#include <cstddef>

namespace siblings {
    /// Model of Vertex List Graph.
    template <typename R>
    class hex_graph {
    public:
        typedef R real_type;
        typedef std::size_t size_type;

        hex_graph(std::size_t width, std::size_t height, R distance = R(1))
            : width_(width), height_(height), distance_(distance)
        { }

        std::size_t width() const { return width_; }
        std::size_t height() const { return height_; }
        std::size_t size() const { return width_ * height_; }
        R distance() const { return distance_; }

    private:
        std::size_t width_, height_;
        R distance_;
    };

    

    template <typename R>
    std::pair<

    template <typename R>
    std::size_t num_vertices(const hex_graph<R>& g) {
        return g.size();
    }
}

namespace boost {
    template <typename R>
    struct graph_traits<siblings::hex_graph<R> > {
        typedef vertex_list_graph_tag traversal_category;
        // typedef ... vertex_iterator;
        typedef std::size_t vertices_size_type;
    };
}

#endif
