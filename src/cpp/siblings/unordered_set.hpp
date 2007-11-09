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
        : public unordered_container<Value, set_tag, unique_tag,
                                     Hash, Pred, Alloc>
    {
    public:
        typedef unordered_container<Value, set_tag, unique_tag,
                                    Hash, Pred, Alloc> base;

        typedef typename base::size_type size_type;
        typedef typename base::hasher hasher;
        typedef typename base::key_equal key_equal;
        typedef typename base::allocator_type allocator_type;

        explicit unordered_set(size_type n = 3,
                               const hasher& hf = hasher(),
                               const key_equal& eql = key_equal(),
                               const allocator_type& a = allocator_type())
            : base(n, hf, eql, a)
        { }

        template <class InputIterator>
        unordered_set(InputIterator f, InputIterator l,
                      size_type n = 3,
                      const hasher& hf = hasher(),
                      const key_equal& eql = key_equal(),
                      const allocator_type& a = allocator_type())
            : base(f, l, n, hf, eql, a)
        { }
    };

    // 23.4.4, class template unordered_multiset:
    template <class Value,
              class Hash = boost::hash<Value>,
              class Pred = std::equal_to<Value>,
              class Alloc = std::allocator<Value> >
    class unordered_multiset
        : public unordered_container<Value, set_tag, non_unique_tag,
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
