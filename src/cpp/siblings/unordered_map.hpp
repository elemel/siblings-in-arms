// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_UNORDERED_MAP_HPP
#define SIBLINGS_UNORDERED_MAP_HPP

#include "unordered_container.hpp"

namespace siblings {
    // 23.4.1, class template unordered_map:
    template <class Key,
              class T,
              class Hash = boost::hash<Key>,
              class Pred = std::equal_to<Key>,
              class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_map
        : public unordered_container<std::pair<const Key, T>,
                                     map_tag, unique_tag, Hash, Pred, Alloc>
    {
    public:
        /// Exception safety: Basic guarantee. This operation is implemented as
        /// an insert operation, which only offers the basic guarantee.
        T& operator[](const Key& k)
        {
            return insert(std::make_pair(k, T())).first->second;
        }
    };

    // 23.4.2, class template unordered_multimap:
    template <class Key,
              class T,
              class Hash = boost::hash<Key>,
              class Pred = std::equal_to<Key>,
              class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_multimap
        : public unordered_container<std::pair<const Key, T>,
                                     map_tag, non_unique_tag,
                                     Hash, Pred, Alloc>
    { };

    template <class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_map<Key, T, Hash, Pred, Alloc>& x,
              unordered_map<Key, T, Hash, Pred, Alloc>& y)
    {
        x.swap(y);
    }

    template <class Key, class T, class Hash, class Pred, class Alloc>
    void swap(unordered_multimap<Key, T, Hash, Pred, Alloc>& x,
              unordered_multimap<Key, T, Hash, Pred, Alloc>& y)
    {
        x.swap(y);
    }
}

#endif
