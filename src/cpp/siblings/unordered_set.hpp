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
    {
    private:
        typedef unordered_container<Value, set_tag, unique_tag,
                                    Hash, Pred, Alloc>
        impl_type;

        impl_type impl_;

    public:
        // types //////////////////////////////////////////////////////////////

        typedef typename impl_type::key_type key_type;
        typedef typename impl_type::value_type value_type;
        typedef typename impl_type::hasher hasher;
        typedef typename impl_type::key_equal key_equal;
        typedef typename impl_type::allocator_type allocator_type;

        typedef typename impl_type::const_pointer pointer;
        typedef typename impl_type::const_pointer const_pointer;
        typedef typename impl_type::const_reference reference;
        typedef typename impl_type::const_reference const_reference;
        typedef typename impl_type::size_type size_type;
        typedef typename impl_type::difference_type difference_type;

        typedef typename impl_type::const_iterator iterator;
        typedef typename impl_type::const_iterator const_iterator;
        typedef typename impl_type::const_local_iterator local_iterator;
        typedef typename impl_type::const_local_iterator const_local_iterator;

        // construct/destroy/copy /////////////////////////////////////////////

        explicit unordered_set(size_type n = impl_type::default_bucket_count,
                               const hasher& hf = hasher(),
                               const key_equal& eql = key_equal(),
                               const allocator_type& a = allocator_type())
            : impl_(n, hf, eql, a)
        { }

        template <class InputIterator>
        unordered_set(InputIterator f, InputIterator l,
                      size_type n = impl_type::default_bucket_count,
                      const hasher& hf = hasher(),
                      const key_equal& eql = key_equal(),
                      const allocator_type& a = allocator_type())
            : impl_(f, l, n, hf, eql, a)
        { }

        // unordered_set(const unordered_set&);
        // ~unordered_set();
        // unordered_set& operator=(const unordered_set&);

        allocator_type get_allocator() const { impl_.get_allocator(); }

        // size and capacity //////////////////////////////////////////////////

        bool empty() const { return impl_.empty(); }
        size_type size() const { return impl_.size(); }
        size_type max_size() const { return impl_.max_size(); }

        // iterators //////////////////////////////////////////////////////////

        iterator begin() const { return impl_.begin(); }
        iterator end() const { return impl_.end(); }
        iterator cbegin() const { return impl_.cbegin(); }
        iterator cend() const { return impl_.cend(); }

        // modifiers //////////////////////////////////////////////////////////

        std::pair<iterator, bool> insert(const value_type& obj)
        {
            return impl_.insert(obj);
        }

        iterator insert(iterator hint, const value_type& obj)
        {
            return impl_.insert(hint, obj);
        }

        template <class InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            return impl_.insert(first, last);
        }

        iterator erase(iterator i) { return impl_.erase(i); }
        size_type erase(const key_type& k) { return impl_.erase(k); }

        iterator erase(iterator first, iterator last)
        {
            return impl_.erase(first, last);
        }

        void clear() { impl_.clear(); }
        void swap(unordered_set& other) { impl_.swap(other.impl_); }

        // observers //////////////////////////////////////////////////////////

        hasher hash_function() const { return impl_.hash_function(); }
        key_equal key_eq() const { return impl_.key_eq(); }

        // lookup /////////////////////////////////////////////////////////////

        iterator find(const key_type& k) const { return impl_.find(k); }
        size_type count(const key_type& k) const { return impl_.count(k); }

        std::pair<iterator, iterator>
        equal_range(const key_type& k) const { return impl_.equal_range(k); }

        // bucket interface ///////////////////////////////////////////////////

        size_type bucket_count() const { return impl_.bucket_count(); }
        size_type max_bucket_count() const { return impl_.max_bucket_count(); }

        size_type
        bucket_size(size_type i) const { return impl_.bucket_size(i); }

        size_type bucket(const key_type& k) const { return impl_.bucket(k); }
        local_iterator begin(size_type i) const { return impl_.begin(i); }
        local_iterator end(size_type i) const { return impl_.end(i); }

        // hash policy ////////////////////////////////////////////////////////

        float load_factor() const { return impl_.load_factor(); }
        float max_load_factor() const { return impl_.max_load_factor(); }
        void max_load_factor(float z) { impl_.max_load_factor(z); }
        void rehash(size_type n) { impl_.rehash(n); }
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
