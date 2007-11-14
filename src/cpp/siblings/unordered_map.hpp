// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_UNORDERED_MAP_HPP
#define SIBLINGS_UNORDERED_MAP_HPP

#include "detail/unordered_container.hpp"

namespace siblings {
    /// Implementation of 23.4.1, class template unordered_map.
    ///
    /// @author Mikael Lind
    template <class Key,
              class T,
              class Hash = boost::hash<Key>,
              class Pred = std::equal_to<Key>,
              class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_map
    {
    private:
        /// Implementation type.
        typedef detail::unordered_container<Key, std::pair<const Key, T>,
                                            Hash, Pred, Alloc>
        impl_type;
        
    public:
        /// @name Types
        /// @{
        
        /// @copydoc unordered_container::key_type
        typedef typename impl_type::key_type key_type;
        
        /// @copydoc unordered_container::value_type
        typedef typename impl_type::value_type value_type;

        /// Mapped type.
        typedef T mapped_type;

        /// @copydoc unordered_container::hasher
        typedef typename impl_type::hasher hasher;

        /// @copydoc unordered_container::key_equal
        typedef typename impl_type::key_equal key_equal;

        /// @copydoc unordered_container::allocator_type
        typedef typename impl_type::allocator_type allocator_type;

        /// @copydoc unordered_container::pointer
        typedef typename impl_type::pointer pointer;

        /// @copydoc unordered_container::const_pointer
        typedef typename impl_type::const_pointer const_pointer;

        /// @copydoc unordered_container::reference
        typedef typename impl_type::reference reference;

        /// @copydoc unordered_container::const_reference
        typedef typename impl_type::const_reference const_reference;

        /// @copydoc unordered_container::size_type
        typedef typename impl_type::size_type size_type;

        /// @copydoc unordered_container::difference_type
        typedef typename impl_type::difference_type difference_type;

        /// @copydoc unordered_container::iterator
        typedef typename impl_type::iterator iterator;

        /// @copydoc unordered_container::const_iterator
        typedef typename impl_type::const_iterator const_iterator;

        /// @copydoc unordered_container::local_iterator
        typedef typename impl_type::local_iterator local_iterator;

        /// @copydoc unordered_container::const_local_iterator
        typedef typename impl_type::const_local_iterator const_local_iterator;

        /// @}

        /// @name Construct/Destroy/Copy
        /// @{

        /// Default constructor.
        explicit unordered_map(size_type n = impl_type::default_bucket_count,
                               const hasher& hf = hasher(),
                               const key_equal& eql = key_equal(),
                               const allocator_type& a = allocator_type())
            : impl_(n, hf, eql, a)
        { }

        /// Range constructor.
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

        /// Copy constructor.
        unordered_map(const unordered_map& other) : impl_(other.impl_) { }
        
        /// Destructor.
        ~unordered_map() { }

        /// Copy assignment operator.
        unordered_map& operator=(const unordered_map& other)
        {
            impl_ = other.impl_;
            return *this;
        }

        /// @copydoc unordered_container::get_allocator
        allocator_type get_allocator() const { impl_.get_allocator(); }

        /// @}

        /// @name Size and Capacity
        /// @{

        bool empty() const { return impl_.empty(); }
        size_type size() const { return impl_.size(); }
        size_type max_size() const { return impl_.max_size(); }

        /// @}

        /// @name Iterators
        /// @{

        iterator begin() { return impl_.begin(); }
        const_iterator begin() const { return impl_.begin(); }
        iterator end() { return impl_.end(); }
        const_iterator end() const { return impl_.end(); }
        const_iterator cbegin() const { return impl_.cbegin(); }
        const_iterator cend() const { return impl_.cend(); }

        /// @}

        /// @name Modifiers
        /// @{

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
        size_type erase(const key_type& k) { return impl_.erase_unique(k); }

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

        /// @}

        /// @name Observers
        /// @{

        hasher hash_function() const { return impl_.hash_function(); }
        key_equal key_eq() const { return impl_.key_eq(); }

        /// @}

        /// @name Lookup
        /// @{

        iterator find(const key_type& k) { return impl_.find(k); }
        const_iterator find(const key_type& k) const { return impl_.find(k); }

        size_type
        count(const key_type& k) const { return impl_.count_unique(k); }

        std::pair<iterator, iterator>
        equal_range(const key_type& k) { return impl_.equal_range_unique(k); }

        std::pair<const_iterator, const_iterator>
        equal_range(const key_type& k) const
        {
            return impl_.equal_range_unique(k);
        }

        mapped_type& operator[](const key_type& k)
        {
            value_type v(k, mapped_type());
            return impl_.insert_unique(v).first->second;
        }

        /// @}

        /// @name Bucket Interface
        /// @{

        /// @copydoc unordered_container::bucket_count
        size_type bucket_count() const { return impl_.bucket_count(); }

        /// @copydoc unordered_container::max_bucket_count
        size_type max_bucket_count() const { return impl_.max_bucket_count(); }

        /// @copydoc unordered_container::bucket_size
        size_type
        bucket_size(size_type i) const { return impl_.bucket_size(i); }

        /// @copydoc unordered_container::bucket
        size_type bucket(const key_type& k) const { return impl_.bucket(k); }

        /// @copydoc unordered_container::begin(size_type)
        local_iterator begin(size_type i) { return impl_.begin(i); }

        /// @copydoc unordered_container::begin(size_type)
        const_local_iterator
        begin(size_type i) const { return impl_.begin(i); }

        /// @copydoc unordered_container::end(size_type)
        local_iterator end(size_type i) { return impl_.end(i); }

        /// @copydoc unordered_container::end(size_type)
        const_local_iterator end(size_type i) const { return impl_.end(i); }

        /// @}

        /// @name Hash Policy
        /// @{

        /// @copydoc unordered_container::load_factor
        float load_factor() const { return impl_.load_factor(); }

        /// @copydoc unordered_container::max_load_factor()
        float max_load_factor() const { return impl_.max_load_factor(); }

        /// @copydoc unordered_container::max_load_factor(float)
        void max_load_factor(float z) { impl_.max_load_factor(z); }

        /// @copydoc unordered_container::rehash
        void rehash(size_type n) { impl_.rehash(n); }

        /// @}

    private:        
        /// Implementation.
        impl_type impl_;
    };

    /// Implementation of 23.4.2, class template unordered_multimap.
    ///
    /// @author Mikael Lind
    template <class Key,
              class T,
              class Hash = boost::hash<Key>,
              class Pred = std::equal_to<Key>,
              class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_multimap
    {
    private:
        typedef detail::unordered_container<Key, std::pair<const Key, T>,
                                            Hash, Pred, Alloc>
        impl_type;

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

        explicit unordered_multimap(size_type n
                                    = impl_type::default_bucket_count,
                                    const hasher& hf = hasher(),
                                    const key_equal& eql = key_equal(),
                                    const allocator_type& a = allocator_type())
            : impl_(n, hf, eql, a)
        { }

        template <class InputIterator>
        unordered_multimap(InputIterator f, InputIterator l,
                           size_type n = impl_type::default_bucket_count,
                           const hasher& hf = hasher(),
                           const key_equal& eql = key_equal(),
                           const allocator_type& a = allocator_type())
            : impl_(n, hf, eql, a)
        {
            impl_.insert(f, l);
        }

        // unordered_multimap(const unordered_multimap&);
        // ~unordered_multimap();
        // unordered_multimap& operator=(const unordered_multimap&);

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
            return impl_.insert(obj);
        }

        iterator insert(iterator hint, const value_type& obj)
        {
            return impl_.insert(hint, obj);
        }

        const_iterator insert(const_iterator hint, const value_type& obj)
        {
            return impl_.insert(hint, obj);
        }

        template <class InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            return impl_.insert(first, last);
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
        void swap(unordered_multimap& other) { impl_.swap(other.impl_); }

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

    private:
        impl_type impl_;
    };

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
