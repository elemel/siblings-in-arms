// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_UNORDERED_MAP_HPP
#define SIBLINGS_UNORDERED_MAP_HPP

#include "unordered_container.hpp"

namespace siblings {
    /// @invariant m.bucket_count() >= 1
    /// @invariant m.load_factor() <= m.max_load_factor()
    template <typename K, typename T, typename H = boost::hash<K>,
              typename P = std::equal_to<K>,
              typename A = std::allocator<std::pair<const K, T> > >
    struct unordered_map : unordered_container<std::pair<const K, T>, true,
                                               true, H, P, A>
    {
        typedef K key_type;
        typedef T mapped_type;
        typedef std::pair<key_type, mapped_type> value_type;

        /// Exception safety: Basic guarantee. This operation is implemented as
        /// an insert operation, which only offers the basic guarantee.
        mapped_type& operator[](const key_type& k)
        {
            return insert(value_type(k, mapped_type())).first->second;
        }
    };
}

#endif
