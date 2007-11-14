// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_UNORDERED_SET_HPP
#define SIBLINGS_UNORDERED_SET_HPP

#include "identity.hpp"
#include "detail/unordered_impl.hpp"

namespace siblings {
    /// @brief Unordered set.
    ///
    /// Implements 23.4.3, class template unordered_set.
    ///
    /// @invariant s.load_factor() <= s.max_load_factor()
    template <class Value,
              class Hash = boost::hash<Value>,
              class Pred = std::equal_to<Value>,
              class Alloc = std::allocator<Value> >
    class unordered_set
    {
    private:
        /// Implementation type.
        typedef detail::unordered_impl<Value, Value, identity<Value>,
                                       Hash, Pred, Alloc>
        impl_type;
        
    public:
        // types //////////////////////////////////////////////////////////////

        /// @copydoc detail::unordered_impl::key_type
        typedef typename impl_type::key_type key_type;

        /// @copydoc detail::unordered_impl::value_type
        typedef typename impl_type::value_type value_type;

        /// @copydoc detail::unordered_impl::hasher
        typedef typename impl_type::hasher hasher;

        /// @copydoc detail::unordered_impl::key_equal
        typedef typename impl_type::key_equal key_equal;

        /// @copydoc detail::unordered_impl::allocator_type
        typedef typename impl_type::allocator_type allocator_type;

        /// @copydoc detail::unordered_impl::pointer
        typedef typename impl_type::const_pointer pointer;

        /// @copydoc detail::unordered_impl::const_pointer
        typedef typename impl_type::const_pointer const_pointer;

        /// @copydoc detail::unordered_impl::reference
        typedef typename impl_type::const_reference reference;

        /// @copydoc detail::unordered_impl::const_reference
        typedef typename impl_type::const_reference const_reference;

        /// @copydoc detail::unordered_impl::size_type
        typedef typename impl_type::size_type size_type;

        /// @copydoc detail::unordered_impl::difference_type
        typedef typename impl_type::difference_type difference_type;

        /// @copydoc detail::unordered_impl::iterator
        typedef typename impl_type::const_iterator iterator;

        /// @copydoc detail::unordered_impl::const_iterator
        typedef typename impl_type::const_iterator const_iterator;

        /// @copydoc detail::unordered_impl::local_iterator
        typedef typename impl_type::const_local_iterator local_iterator;

        /// @copydoc detail::unordered_impl::const_local_iterator
        typedef typename impl_type::const_local_iterator const_local_iterator;

        // construct/destroy/copy /////////////////////////////////////////////

        /// Default constructor.
        ///
        /// @post s.empty()
        explicit unordered_set(size_type n = impl_type::default_bucket_count,
                               const hasher& hf = hasher(),
                               const key_equal& eql = key_equal(),
                               const allocator_type& a = allocator_type())
            : impl_(n, typename impl_type::get_key(), hf, eql, a)
        { }

        /// Range constructor.
        template <class InputIterator>
        unordered_set(InputIterator f, InputIterator l,
                      size_type n = impl_type::default_bucket_count,
                      const hasher& hf = hasher(),
                      const key_equal& eql = key_equal(),
                      const allocator_type& a = allocator_type())
            : impl_(n, typename impl_type::get_key(), hf, eql, a)
        {
            impl_.insert_unique(f, l);
        }

        /// Copy constructor.
        unordered_set(const unordered_set& other) : impl_(other.impl_) { }

        /// Destructor.
        ~unordered_set() { }

        /// Copy assignment operator.
        unordered_set& operator=(const unordered_set& other)
        {
            impl_ = other.impl_;
            return *this;
        }

        /// @copydoc detail::unordered_impl::get_allocator
        allocator_type get_allocator() const { impl_.get_allocator(); }

        // size and capacity //////////////////////////////////////////////////

        /// @copydoc detail::unordered_impl::empty
        bool empty() const { return impl_.empty(); }

        /// @copydoc detail::unordered_impl::size
        size_type size() const { return impl_.size(); }

        /// @copydoc detail::unordered_impl::max_size
        size_type max_size() const { return impl_.max_size(); }

        // iterators //////////////////////////////////////////////////////////

        /// @copydoc detail::unordered_impl::begin
        iterator begin() const { return impl_.begin(); }

        /// @copydoc detail::unordered_impl::end
        iterator end() const { return impl_.end(); }

        /// @copydoc detail::unordered_impl::cbegin
        iterator cbegin() const { return impl_.cbegin(); }

        /// @copydoc detail::unordered_impl::cend
        iterator cend() const { return impl_.cend(); }

        // modifiers //////////////////////////////////////////////////////////

        /// @copydoc detail::unordered_impl::insert(const value_type&)
        std::pair<iterator, bool> insert(const value_type& obj)
        {
            return impl_.insert(obj);
        }

        /// @copydoc
        /// detail::unordered_impl::insert(iterator,const value_type&)
        iterator insert(iterator hint, const value_type& obj)
        {
            return impl_.insert(hint, obj);
        }

        /// @copydoc
        /// detail::unordered_impl::insert(InputIterator,InputIterator)
        template <class InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            return impl_.insert(first, last);
        }

        /// @copydoc detail::unordered_impl::erase(iterator)
        iterator erase(iterator i) { return impl_.erase(i); }

        /// @copydoc detail::unordered_impl::erase(const key_type&)
        size_type erase(const key_type& k) { return impl_.erase(k); }

        /// @copydoc detail::unordered_impl::erase(iterator,iterator)
        iterator erase(iterator first, iterator last)
        {
            return impl_.erase(first, last);
        }

        /// @copydoc detail::unordered_impl::clear
        void clear() { impl_.clear(); }

        /// @copydoc detail::unordered_impl::swap
        void swap(unordered_set& other) { impl_.swap(other.impl_); }

        // observers //////////////////////////////////////////////////////////

        /// @copydoc detail::unordered_impl::hash_function
        hasher hash_function() const { return impl_.hash_function(); }

        /// @copydoc detail::unordered_impl::key_eq
        key_equal key_eq() const { return impl_.key_eq(); }

        // lookup /////////////////////////////////////////////////////////////

        /// @copydoc detail::unordered_impl::find
        iterator find(const key_type& k) const { return impl_.find(k); }

        /// @copydoc detail::unordered_impl::count
        size_type count(const key_type& k) const { return impl_.count(k); }

        /// @copydoc detail::unordered_impl::equal_range
        std::pair<iterator, iterator>
        equal_range(const key_type& k) const { return impl_.equal_range(k); }

        // bucket interface ///////////////////////////////////////////////////

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
        local_iterator begin(size_type i) const { return impl_.begin(i); }

        /// @copydoc detail::unordered_impl::end(size_type)
        local_iterator end(size_type i) const { return impl_.end(i); }

        // hash policy ////////////////////////////////////////////////////////

        /// @copydoc detail::unordered_impl::load_factor
        float load_factor() const { return impl_.load_factor(); }

        /// @copydoc detail::unordered_impl::max_load_factor()
        float max_load_factor() const { return impl_.max_load_factor(); }

        /// @copydoc detail::unordered_impl::max_load_factor(float)
        void max_load_factor(float z) { impl_.max_load_factor(z); }

        /// @copydoc detail::unordered_impl::rehash
        void rehash(size_type n) { impl_.rehash(n); }

    private:
        /// Implementation.
        impl_type impl_;
    };

    /// @brief Unordered multiset.
    ///
    /// Implements 23.4.4, class template unordered_multiset:
    template <class Value,
              class Hash = boost::hash<Value>,
              class Pred = std::equal_to<Value>,
              class Alloc = std::allocator<Value> >
    class unordered_multiset
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
