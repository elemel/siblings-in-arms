// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_UNORDERED_CONTAINER_HPP
#define SIBLINGS_UNORDERED_CONTAINER_HPP

#include "nested_iterator.hpp"
#include <cassert>
#include <cstddef>
#include <functional>
#include <list>
#include <utility>
#include <vector>
#include <boost/bind.hpp>
#include <boost/foreach.hpp>
#include <boost/functional/hash.hpp>
#include <boost/utility.hpp>

namespace siblings {
    /// @invariant size() <= max_size()
    /// @invariant bucket_count() <= max_bucket_count()
    /// @invariant load_factor() <= max_load_factor()
    template <class Key, class Value, class Hash, class Pred, class Alloc>
    class unordered_container {
    private:
        typedef std::list<Value, Alloc> bucket_type;
        typedef std::vector<bucket_type> bucket_vector;
        typedef typename bucket_vector::iterator bucket_iterator;
        typedef typename bucket_vector::const_iterator const_bucket_iterator;

    public:
        // types //////////////////////////////////////////////////////////////

        typedef Key key_type;
        typedef Value value_type;
        typedef Hash hasher;
        typedef Pred key_equal;
        typedef Alloc allocator_type;

        typedef typename allocator_type::pointer pointer;
        typedef typename allocator_type::const_pointer const_pointer;
        typedef typename allocator_type::reference reference;
        typedef typename allocator_type::const_reference const_reference;
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;

        typedef typename bucket_type::iterator local_iterator;
        typedef typename bucket_type::const_iterator const_local_iterator;

        typedef nested_iterator<value_type, bucket_iterator, local_iterator>
        iterator;

        typedef nested_iterator<const value_type, const_bucket_iterator,
                                const_local_iterator>
        const_iterator;

        // constants //////////////////////////////////////////////////////////

        static const size_type default_bucket_count = 3;

    private:
        bucket_vector buckets_;
        hasher hash_;
        key_equal eq_;
        allocator_type alloc_;
        size_type size_;
        float max_load_factor_;

        float load_factor(size_type n) const
        {
            assert(n >= 1);
            return float(size()) / float(n);
        }

    public:
        // construct/destroy/copy /////////////////////////////////////////////

        explicit unordered_container(size_type n = 3,
                                     const hasher& hf = hasher(),
                                     const key_equal& eql = key_equal(),
                                     const allocator_type& a
                                     = allocator_type())
            : buckets_(n, bucket_type(a)), hash_(hf), eq_(eql),
              alloc_(a), size_(0), max_load_factor_(1)
        { }

        // unordered_map(const unordered_map&);
        // ~unordered_map();
        // unordered_map& operator=(const unordered_map&);

        allocator_type get_allocator() const { return alloc_; }

        // size and capacity //////////////////////////////////////////////////

        bool empty() const { return size_ == 0; }
        size_type size() const { return size_; }
        size_type max_size() const { return buckets_.max_size(); }

        // iterators //////////////////////////////////////////////////////////

        iterator begin()
        {
            return iterator(buckets_.begin(), buckets_.end());
        }

        const_iterator begin() const
        {
            return const_iterator(buckets_.begin(), buckets_.end());
        }

        iterator end()
        {
            return iterator(buckets_.end(), buckets_.end());
        }

        const_iterator end() const
        {
            return const_iterator(buckets_.end(), buckets_.end());
        }

        const_iterator cbegin() const { return begin(); }
        const_iterator cend() const { return end(); }

        // modifiers //////////////////////////////////////////////////////////

        std::pair<iterator, bool> insert(const value_type& obj)
        {
            std::pair<iterator, bool> result;
            bucket_iterator b = buckets_.begin() + bucket(key(obj));
            local_iterator i = find_local(*b, key(obj));
            i = b->insert(i, obj);
            ++size_;
            if (load_factor() > max_load_factor()) {
                rehash(bucket_count() * 2 + 1);
                result = std::make_pair(find(key(obj)), true);
            } else {
                result = std::make_pair(iterator(b, buckets_.end(), i),
                                        true);
            }
            assert(find(key(obj)) != end());
            return result;
        }

        iterator insert(iterator hint, const value_type& obj)
        {
            return insert(obj).first;
        }

        const_iterator insert(const_iterator hint, const value_type& obj)
        {
            return insert(obj).first;
        }

        template <class InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert(*first++);
            }
        }

        std::pair<iterator, bool> insert_unique(const value_type& obj)
        {
            std::pair<iterator, bool> result;
            bucket_iterator b = buckets_.begin() + bucket(key(obj));
            local_iterator i = find_local(*b, key(obj));
            if (i == b->end()) {
                i = b->insert(i, obj);
                ++size_;
                if (load_factor() > max_load_factor()) {
                    rehash(bucket_count() * 2 + 1);
                    result = std::make_pair(find(key(obj)), true);
                } else {
                    result = std::make_pair(iterator(b, buckets_.end(), i),
                                            true);
                }
            } else {
                result = std::make_pair(iterator(b, buckets_.end(), i), false);
            }
            assert(find(key(obj)) != end());
            return result;
        }

        iterator insert_unique(iterator hint, const value_type& obj)
        {
            return insert_unique(obj).first;
        }

        const_iterator insert_unique(const_iterator hint,
                                     const value_type& obj)
        {
            return insert_unique(obj).first;
        }

        template <class InputIterator>
        void insert_unique(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert_unique(*first++);
            }
        }

        iterator erase(iterator i)
        {
            assert(i != end());
            iterator result = boost::next(i);
            i.current_outer()->erase(i.current_inner());
            --size_;
            return result;
        }

        const_iterator erase(const_iterator i)
        {
            assert(i != end());
            const_iterator result = boost::next(i);
            i.current_outer()->erase(i.current_inner());
            --size_;
            return result;
        }

        size_type erase(const key_type& k)
        {
            size_type old_size = size_;
            std::pair<iterator, iterator> r = equal_range(k);
            erase(r.first, r.second);
            assert(size_ <= old_size);
            return old_size - size_;
        }

        /// @todo Optimize.
        iterator erase(iterator first, iterator last)
        {
            while (first != last) {
                first = erase(first);
            }
            return first;
        }

        /// @todo Optimize.
        const_iterator erase(const_iterator first, const_iterator last)
        {
            while (first != last) {
                first = erase(first);
            }
            return first;
        }

        /// @todo Simplify this function if vector::clear is no-throw.
        void clear()
        {
            BOOST_FOREACH(bucket_type& b, buckets_) {
                size_ -= b.size();
                try {
                    b.clear();
                } catch (...) {
                    size_ += b.size();
                    throw;
                }
            }
        }

        void swap(unordered_container& other)
        {
            buckets_.swap(other.buckets_);
            std::swap(hash_, other.hash_);
            std::swap(eq_, other.eq_);
            std::swap(alloc_, other.alloc_);
            std::swap(size_, other.size_);
            std::swap(max_load_factor_, other.max_load_factor_);
        }

        // observers //////////////////////////////////////////////////////////

        hasher hash_function() const { return hash_; }
        key_equal key_eq() const { return eq_; }

        // lookup /////////////////////////////////////////////////////////////

        iterator find(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator v = find_local(*b, k);
            return (v == b->end()) ? end() : iterator(b, buckets_.end(), v);
        }

        const_iterator find(const key_type& k) const
        {
            return const_cast<unordered_container&>(*this).find(k);
        }

        size_type count(const key_type& k) const
        {
            const bucket_type& b = buckets_[bucket(k)];
            const_local_iterator v = find_local(b, k);
            if (v == b.end()) {
                return 0;
            }

            size_type result = 0;
            do {
                ++v;
                ++result;
            } while (v != b.end() && eq_(k, key(*v)));
            return result;
        }

        size_type count_unique(const key_type& k) const
        {
            const bucket_type& b = buckets_[bucket(k)];
            const_local_iterator v = find_local(b, k);
            return (v == b.end()) ? 0 : 1;
        }

        // @todo Optimization: use local iterators for searching.
        std::pair<iterator, iterator> equal_range(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator v = find_local(*b, k);
            if (v == b->end()) {
                return std::make_pair(end(), end());
            } else {
                iterator first = iterator(b, buckets_.end(), v);
                iterator last = boost::next(first);
                while (last != end() && eq_(key(*first), key(*last))) {
                    ++last;
                }
                return std::make_pair(first, last);
            }
        }

        std::pair<const_iterator, const_iterator>
        equal_range(const key_type& k) const
        {
            return const_cast<unordered_container&>(*this).equal_range(k);
        }

        // bucket interface ///////////////////////////////////////////////////

        /// Exception safety: No-throw guarantee.
        size_type bucket_count() const { return buckets_.size(); }

        /// Exception safety: No-throw guarantee.
        size_type max_bucket_count() const { return buckets_.max_size(); }

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < bucket_count()
        /// @post result <= size()
        size_type bucket_size(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].size();
        }

        /// Exception safety: No-throw guarantee if the hash function is
        /// no-throw; strong guarantee otherwise.
        size_type bucket(const key_type& k) const
        {
            return hash_(k) % bucket_count();
        }

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < bucket_count()
        local_iterator begin(size_type i)
        {
            assert(i < bucket_count());
            return buckets_[i].begin();
        }

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < bucket_count()
        const_local_iterator begin(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].begin();
        }

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < bucket_count()
        local_iterator end(size_type i)
        {
            assert(i < bucket_count());
            return buckets_[i].end();
        }

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < bucket_count()
        const_local_iterator end(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].end();
        }

        // hash policy ////////////////////////////////////////////////////////

        /// Exception safety: No-throw guarantee.
        ///
        // @post result >= 0 && result <= max_load_factor()
        float load_factor() const
        {
            return load_factor(bucket_count());
        }

        /// Exception safety: No-throw guarantee.
        ///
        /// @post result >= 0
        float max_load_factor() const { return max_load_factor_; }

        /// Exception safety: Strong guarantee.
        ///
        /// @pre z > 0
        void max_load_factor(float z)
        {
            assert(z > 0);
            float saved_max_load_factor = max_load_factor_;
            try {
                max_load_factor_ = z;
                if (load_factor() > max_load_factor()) {
                    rehash(size_type(std::ceil(size() / max_load_factor())));
                }
            } catch (...) {
                max_load_factor_ = saved_max_load_factor;
            }
        }

        /// Exception safety: Strong guarantee. Exceptions can only be thrown
        /// when constructing the new bucket vector. The container has not been
        /// modified at this point. Once the new bucket vector has been
        /// constructed, the rest of the rehashing is carried out using list
        /// splicing and vector swapping, which are no-throw operations.
        ///
        /// @post bucket_count() >= n
        void rehash(size_type n)
        {
            if (n >= 1 && load_factor(n) <= max_load_factor()) {
                bucket_vector v(n, bucket_type(alloc_));
                BOOST_FOREACH(bucket_type& b, buckets_) {
                    while (b.begin() != b.end()) {
                        bucket_type& r = v[hash_(key(b.front())) % n];
                        r.splice(r.end(), b, b.begin());
                    }
                }
                buckets_.swap(v);
            }
        }

    private:
        const key_type& key(const key_type& k) const { return k; }

        template <typename T> const key_type
        key(const std::pair<const key_type, T> p) const { return p.first; }

        local_iterator find_local(bucket_type& b, const key_type& k) const
        {
            local_iterator i = b.begin();
            local_iterator last = b.end();
            while (i != last && !eq_(k, key(*i))) {
                ++i;
            }
            return i;
        }

        const_local_iterator
        find_local(const bucket_type& b, const key_type& k) const
        {
            return find(const_cast<bucket_type&>(b), k);
        }

    };
}

#endif
