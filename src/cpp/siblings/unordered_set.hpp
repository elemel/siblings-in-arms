// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_UNORDERED_SET_HPP
#define SIBLINGS_UNORDERED_SET_HPP

#include "unordered_container.hpp"

namespace siblings {
    // 23.4.3, class template unordered_set:
    template <class Value,
              class Hash = boost::hash<Value>,
              class Pred = std::equal_to<Value>,
              class Alloc = std::allocator<Value> >
    class unordered_set
        : public unordered_container<const Value, set_tag, unique_tag,
                                     Hash, Pred, Alloc>
    { };

    // 23.4.4, class template unordered_multiset:
    template <class Value,
              class Hash = boost::hash<Value>,
              class Pred = std::equal_to<Value>,
              class Alloc = std::allocator<Value> >
    class unordered_multiset
        : public unordered_container<const Value, set_tag, non_unique_tag,
                                     Hash, Pred, Alloc>
    { };

    template <class Value, class Hash, class Pred, class Alloc>
    void swap(unordered_set<Value, Hash, Pred, Alloc>& x,
              unordered_set<Value, Hash, Pred, Alloc>& y)
    {
        x.swap(y);
    }

    template <class Value, class Hash, class Pred, class Alloc>
    void swap(unordered_multiset<Value, Hash, Pred, Alloc>& x,
              unordered_multiset<Value, Hash, Pred, Alloc>& y)
    {
        x.swap(y);
    }
}

#endif
