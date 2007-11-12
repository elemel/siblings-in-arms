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
    {
    private:
        typedef unordered_container<Key, std::pair<const Key, T>,
                                    Hash, Pred, Alloc>
        impl_type;

        impl_type impl_;

    public:
        // types //////////////////////////////////////////////////////////////

        typedef typename impl_type::key_type key_type;
        typedef typename impl_type::value_type value_type;
        typedef T mapped_type;
        typedef typename impl_type::hasher hasher;
        typedef typename impl_type::key_equal key_equal;
        typedef typename impl_type::allocator_type allocator_type;

        typedef typename impl_type::pointer pointer;
        typedef typename impl_type::const_pointer const_pointer;
        typedef typename impl_type::reference reference;
        typedef typename impl_type::const_reference const_reference;
        typedef typename impl_type::size_type size_type;
        typedef typename impl_type::difference_type difference_type;

        typedef typename impl_type::iterator iterator;
        typedef typename impl_type::const_iterator const_iterator;
        typedef typename impl_type::local_iterator local_iterator;
        typedef typename impl_type::const_local_iterator const_local_iterator;

        // construct/destroy/copy /////////////////////////////////////////////

        explicit unordered_map(size_type n = impl_type::default_bucket_count,
                               const hasher& hf = hasher(),
                               const key_equal& eql = key_equal(),
                               const allocator_type& a = allocator_type())
            : impl_(n, hf, eql, a)
        { }

        template <class InputIterator>
        unordered_map(InputIterator f, InputIterator l,
                      size_type n = impl_type::default_bucket_count,
                      const hasher& hf = hasher(),
                      const key_equal& eql = key_equal(),
                      const allocator_type& a = allocator_type())
            : impl_(n, hf, eql, a)
        {
            impl_.insert_unique(f, l);
        }

        // unordered_map(const unordered_map&);
        // ~unordered_map();
        // unordered_map& operator=(const unordered_map&);

        allocator_type get_allocator() const { impl_.get_allocator(); }

        // size and capacity //////////////////////////////////////////////////

        bool empty() const { return impl_.empty(); }
        size_type size() const { return impl_.size(); }
        size_type max_size() const { return impl_.max_size(); }

        // iterators //////////////////////////////////////////////////////////

        iterator begin() { return impl_.begin(); }
        const_iterator begin() const { return impl_.begin(); }
        iterator end() { return impl_.end(); }
        const_iterator end() const { return impl_.end(); }
        const_iterator cbegin() const { return impl_.cbegin(); }
        const_iterator cend() const { return impl_.cend(); }

        // modifiers //////////////////////////////////////////////////////////

        std::pair<iterator, bool> insert(const value_type& obj)
        {
            return impl_.insert_unique(obj);
        }

        iterator insert(iterator hint, const value_type& obj)
        {
            return impl_.insert_unique(hint, obj);
        }

        const_iterator insert(const_iterator hint, const value_type& obj)
        {
            return impl_.insert_unique(hint, obj);
        }

        template <class InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            return impl_.insert_unique(first, last);
        }

        iterator erase(iterator i) { return impl_.erase(i); }
        const_iterator erase(const_iterator i) { return impl_.erase(i); }
        size_type erase(const key_type& k) { return impl_.erase(k); }

        iterator erase(iterator first, iterator last)
        {
            return impl_.erase(first, last);
        }

        const_iterator erase(const_iterator first, const_iterator last)
        {
            return impl_.erase(first, last);
        }

        void clear() { impl_.clear(); }
        void swap(unordered_map& other) { impl_.swap(other.impl_); }

        // observers //////////////////////////////////////////////////////////

        hasher hash_function() const { return impl_.hash_function(); }
        key_equal key_eq() const { return impl_.key_eq(); }

        // lookup /////////////////////////////////////////////////////////////

        iterator find(const key_type& k) { return impl_.find(k); }
        const_iterator find(const key_type& k) const { return impl_.find(k); }
        size_type count(const key_type& k) const { return impl_.count(k); }

        std::pair<iterator, iterator>
        equal_range(const key_type& k) { return impl_.equal_range(k); }

        std::pair<const_iterator, const_iterator>
        equal_range(const key_type& k) const { return impl_.equal_range(k); }

        mapped_type& operator[](const key_type& k)
        {
            return impl_.insert_unique(value_type(k, T())).first->second;
        }

        // bucket interface ///////////////////////////////////////////////////

        size_type bucket_count() const { return impl_.bucket_count(); }
        size_type max_bucket_count() const { return impl_.max_bucket_count(); }

        size_type
        bucket_size(size_type i) const { return impl_.bucket_size(i); }

        size_type bucket(const key_type& k) const { return impl_.bucket(k); }
        local_iterator begin(size_type i) { return impl_.begin(i); }

        const_local_iterator
        begin(size_type i) const { return impl_.begin(i); }

        local_iterator end(size_type i) { return impl_.end(i); }
        const_local_iterator end(size_type i) const { return impl_.end(i); }

        // hash policy ////////////////////////////////////////////////////////

        float load_factor() const { return impl_.load_factor(); }
        float max_load_factor() const { return impl_.max_load_factor(); }
        void max_load_factor(float z) { impl_.max_load_factor(z); }
        void rehash(size_type n) { impl_.rehash(n); }
    };

    // 23.4.2, class template unordered_multimap:
    template <class Key,
              class T,
              class Hash = boost::hash<Key>,
              class Pred = std::equal_to<Key>,
              class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_multimap
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
