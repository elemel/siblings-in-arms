// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_UNORDERED_MAP_HPP
#define SIBLINGS_UNORDERED_MAP_HPP

#include "get_first.hpp"
#include "detail/unordered_impl.hpp"

namespace siblings {
    /// @brief Unordered map.
    ///
    /// Implements of 23.4.1, class template unordered_map.
    template <class Key,
              class T,
              class Hash = boost::hash<Key>,
              class Pred = std::equal_to<Key>,
              class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_map
    {
    private:
        /// Pair type.
        typedef std::pair<const Key, T> pair_type;

        /// Implementation type.
        typedef detail::unordered_impl<Key, pair_type, get_first<pair_type>,
                                       Hash, Pred, Alloc>
        impl_type;
        
    public:
        /// @name Types
        /// @{
        
        /// @copydoc detail::unordered_impl::key_type
        typedef typename impl_type::key_type key_type;
        
        /// @copydoc detail::unordered_impl::value_type
        typedef typename impl_type::value_type value_type;

        /// Mapped type.
        typedef T mapped_type;

        /// @copydoc detail::unordered_impl::hasher
        typedef typename impl_type::hasher hasher;

        /// @copydoc detail::unordered_impl::key_equal
        typedef typename impl_type::key_equal key_equal;

        /// @copydoc detail::unordered_impl::allocator_type
        typedef typename impl_type::allocator_type allocator_type;

        /// @copydoc detail::unordered_impl::pointer
        typedef typename impl_type::pointer pointer;

        /// @copydoc detail::unordered_impl::const_pointer
        typedef typename impl_type::const_pointer const_pointer;

        /// @copydoc detail::unordered_impl::reference
        typedef typename impl_type::reference reference;

        /// @copydoc detail::unordered_impl::const_reference
        typedef typename impl_type::const_reference const_reference;

        /// @copydoc detail::unordered_impl::size_type
        typedef typename impl_type::size_type size_type;

        /// @copydoc detail::unordered_impl::difference_type
        typedef typename impl_type::difference_type difference_type;

        /// @copydoc detail::unordered_impl::iterator
        typedef typename impl_type::iterator iterator;

        /// @copydoc detail::unordered_impl::const_iterator
        typedef typename impl_type::const_iterator const_iterator;

        /// @copydoc detail::unordered_impl::local_iterator
        typedef typename impl_type::local_iterator local_iterator;

        /// @copydoc detail::unordered_impl::const_local_iterator
        typedef typename impl_type::const_local_iterator const_local_iterator;

        /// @}

        /// @name Construct/Destroy/Copy
        /// @{

        /// Default constructor.
        explicit unordered_map(size_type n = impl_type::default_bucket_count,
                               const hasher& hf = hasher(),
                               const key_equal& eql = key_equal(),
                               const allocator_type& a = allocator_type())
            : impl_(n,  typename impl_type::get_key(), hf, eql, a)
        { }

        /// Range constructor.
        template <class InputIterator>
        unordered_map(InputIterator f, InputIterator l,
                      size_type n = impl_type::default_bucket_count,
                      const hasher& hf = hasher(),
                      const key_equal& eql = key_equal(),
                      const allocator_type& a = allocator_type())
            : impl_(n, typename impl_type::get_key(), hf, eql, a)
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

        /// @copydoc detail::unordered_impl::get_allocator
        allocator_type get_allocator() const { impl_.get_allocator(); }

        /// @}

        /// @name Size and Capacity
        /// @{

        /// @copydoc detail::unordered_impl::empty
        bool empty() const { return impl_.empty(); }

        /// @copydoc detail::unordered_impl::size
        size_type size() const { return impl_.size(); }

        /// @copydoc detail::unordered_impl::max_size
        size_type max_size() const { return impl_.max_size(); }

        /// @}

        /// @name Iterators
        /// @{

        /// @copydoc detail::unordered_impl::begin
        iterator begin() { return impl_.begin(); }

        /// @copydoc detail::unordered_impl::begin
        const_iterator begin() const { return impl_.begin(); }

        /// @copydoc detail::unordered_impl::end
        iterator end() { return impl_.end(); }

        /// @copydoc detail::unordered_impl::end
        const_iterator end() const { return impl_.end(); }

        /// @copydoc detail::unordered_impl::cbegin
        const_iterator cbegin() const { return impl_.cbegin(); }

        /// @copydoc detail::unordered_impl::cbegin
        const_iterator cend() const { return impl_.cend(); }

        /// @}

        /// @name Modifiers
        /// @{

        /// @copydoc detail::unordered_impl::insert(const value_type&)
        std::pair<iterator, bool> insert(const value_type& obj)
        {
            return impl_.insert_unique(obj);
        }

        /// @copydoc
        /// detail::unordered_impl::insert(iterator,const value_type&)
        iterator insert(iterator hint, const value_type& obj)
        {
            return impl_.insert_unique(hint, obj);
        }

        /// @copydoc
        /// detail::unordered_impl::insert(const_iterator,const value_type&)
        const_iterator insert(const_iterator hint, const value_type& obj)
        {
            return impl_.insert_unique(hint, obj);
        }

        /// @copydoc
        /// detail::unordered_impl::insert(InputIterator,InputIterator)
        template <class InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            return impl_.insert_unique(first, last);
        }

        /// @copydoc detail::unordered_impl::erase(iterator)
        iterator erase(iterator i) { return impl_.erase(i); }

        /// @copydoc detail::unordered_impl::erase(const_iterator)
        const_iterator erase(const_iterator i) { return impl_.erase(i); }

        /// @copydoc detail::unordered_impl::erase(const key_type&)
        size_type erase(const key_type& k) { return impl_.erase_unique(k); }

        /// @copydoc detail::unordered_impl::erase(iterator,iterator)
        iterator erase(iterator first, iterator last)
        {
            return impl_.erase(first, last);
        }

        /// @copydoc
        /// detail::unordered_impl::erase(const_iterator,const_iterator)
        const_iterator erase(const_iterator first, const_iterator last)
        {
            return impl_.erase(first, last);
        }

        /// @copydoc detail::unordered_impl::clear
        void clear() { impl_.clear(); }

        /// @copydoc detail::unordered_impl::swap
        void swap(unordered_map& other) { impl_.swap(other.impl_); }

        /// @}

        /// @name Observers
        /// @{

        /// @copydoc detail::unordered_impl::hash_function
        hasher hash_function() const { return impl_.hash_function(); }

        /// @copydoc detail::unordered_impl::key_eq
        key_equal key_eq() const { return impl_.key_eq(); }

        /// @}

        /// @name Lookup
        /// @{

        /// @copydoc detail::unordered_impl::find
        iterator find(const key_type& k) { return impl_.find(k); }

        /// @copydoc detail::unordered_impl::find
        const_iterator find(const key_type& k) const { return impl_.find(k); }

        /// @copydoc detail::unordered_impl::count
        size_type
        count(const key_type& k) const { return impl_.count_unique(k); }

        /// @copydoc detail::unordered_impl::equal_range
        std::pair<iterator, iterator>
        equal_range(const key_type& k) { return impl_.equal_range_unique(k); }

        /// @copydoc detail::unordered_impl::equal_range
        std::pair<const_iterator, const_iterator>
        equal_range(const key_type& k) const
        {
            return impl_.equal_range_unique(k);
        }

        /// Index operator.
        ///
        /// Inserts an element with the specified key and a default-constructed
        /// mapped value. Returns a reference to the mapped value.
        ///
        /// @post m.find(k) != m.end()
        mapped_type& operator[](const key_type& k)
        {
            value_type v(k, mapped_type());
            return impl_.insert_unique(v).first->second;
        }

        /// @}

        /// @name Bucket Interface
        /// @{

        /// @copydoc detail::unordered_impl::bucket_count
        size_type bucket_count() const { return impl_.bucket_count(); }

        /// @copydoc detail::unordered_impl::max_bucket_count
        size_type max_bucket_count() const { return impl_.max_bucket_count(); }

        /// @copydoc detail::unordered_impl::bucket_size
        size_type
        bucket_size(size_type i) const { return impl_.bucket_size(i); }

        /// @copydoc detail::unordered_impl::bucket
        size_type bucket(const key_type& k) const { return impl_.bucket(k); }

        /// @copydoc detail::unordered_impl::begin(size_type)
        local_iterator begin(size_type i) { return impl_.begin(i); }

        /// @copydoc detail::unordered_impl::begin(size_type)
        const_local_iterator
        begin(size_type i) const { return impl_.begin(i); }

        /// @copydoc detail::unordered_impl::end(size_type)
        local_iterator end(size_type i) { return impl_.end(i); }

        /// @copydoc detail::unordered_impl::end(size_type)
        const_local_iterator end(size_type i) const { return impl_.end(i); }

        /// @}

        /// @name Hash Policy
        /// @{

        /// @copydoc detail::unordered_impl::load_factor
        float load_factor() const { return impl_.load_factor(); }

        /// @copydoc detail::unordered_impl::max_load_factor()
        float max_load_factor() const { return impl_.max_load_factor(); }

        /// @copydoc detail::unordered_impl::max_load_factor(float)
        void max_load_factor(float z) { impl_.max_load_factor(z); }

        /// @copydoc detail::unordered_impl::rehash
        void rehash(size_type n) { impl_.rehash(n); }

        /// @}

    private:        
        /// Implementation.
        impl_type impl_;
    };

    /// @brief Unordered multimap.
    ///
    /// Implements of 23.4.2, class template unordered_multimap.
    template <class Key,
              class T,
              class Hash = boost::hash<Key>,
              class Pred = std::equal_to<Key>,
              class Alloc = std::allocator<std::pair<const Key, T> > >
    class unordered_multimap
    {
    private:
        /// Pair type.
        typedef std::pair<const Key, T> pair_type;

        /// Implementation type.
        typedef detail::unordered_impl<Key, pair_type,
                                       get_first<pair_type>,
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
            : impl_(n, typename impl_type::get_key(), hf, eql, a)
        { }

        template <class InputIterator>
        unordered_multimap(InputIterator f, InputIterator l,
                           size_type n = impl_type::default_bucket_count,
                           const hasher& hf = hasher(),
                           const key_equal& eql = key_equal(),
                           const allocator_type& a = allocator_type())
            : impl_(n, typename impl_type::get_key(), hf, eql, a)
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
