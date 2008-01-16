#ifndef SIBLINGS_HEX_GRAPH_HPP
#define SIBLINGS_HEX_GRAPH_HPP

#include <cstddef>

namespace siblings {
    /// Model of Vertex List Graph.
    template <typename T>
    class hex_graph {
    private:
        typedef std::vector<T> vector_type;

    public:
        typedef std::size_t size_type;

        hex_graph(std::size_t width, std::size_t height, const T& value = T())
            : width_(width), height_(height), vector_(width * height, value)
        { }

        std::size_t width() const { return width_; }
        std::size_t height() const { return height_; }
        std::size_t size() const { return vector_.size(); }

    private:
        std::size_t width_, height_;
        vector_type vector_;
    };

    

    template <typename T>
    std::pair<hex_graph<T>::iterator, hex_graph<T>::iterator>
    vertices(hex_graph<T>& g) {
        
    }

    template <typename T>
    std::pair<hex_graph<T>::const_iterator, hex_graph<T>::const_iterator>
    vertices(const hex_graph<T>& g) {
        
    }

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
