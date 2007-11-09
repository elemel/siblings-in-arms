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
#include <boost/foreach.hpp>
#include <boost/functional/hash.hpp>
#include <boost/utility.hpp>

namespace siblings {
    struct set_tag { };
    struct map_tag { };

    struct unique_tag { };
    struct non_unique_tag { };

    template <typename T, typename C>
    struct unordered_key_traits {
        typedef T key_type;
        typedef boost::hash<key_type> hasher;
        typedef std::equal_to<key_type> key_equal;

        static const key_type& key(const key_type& k) { return k; }
    };

    template <typename T>
    struct unordered_key_traits<T, map_tag> {
        typedef typename T::first_type key_type;
        typedef boost::hash<key_type> hasher;
        typedef std::equal_to<key_type> key_equal;

        template <typename U>
        static const key_type& key(const U& v) { return v.first; }
    };

    template <typename U>
    struct unordered_uniqueness_traits
    {
        static const bool unique = true;
    };

    template <>
    struct unordered_uniqueness_traits<non_unique_tag>
    {
        static const bool unique = false;
    };

    template <typename T, typename C, typename U>
    struct unordered_traits
        : unordered_key_traits<T, C>, unordered_uniqueness_traits<U>
    { };

    /// @invariant m.bucket_count() >= 1
    /// @invariant m.load_factor() <= m.max_load_factor()
    template <typename T, typename C, typename U,
              typename H = typename unordered_traits<T, C, U>::hasher,
              typename P = typename unordered_traits<T, C, U>::key_equal,
              typename A = std::allocator<T> >
    class unordered_container {
    private:
        // nested types ///////////////////////////////////////////////////////

        typedef unordered_traits<T, C, U> traits;

    public:
        // nested types ///////////////////////////////////////////////////////

        typedef T value_type;
        typedef H hasher;
        typedef P key_equal;
        typedef A allocator_type;
        typedef typename traits::key_type key_type;
        typedef typename A::pointer pointer;
        typedef typename A::const_pointer const_pointer;
        typedef typename A::reference reference;
        typedef typename A::const_reference const_reference;
        typedef std::size_t size_type;

    private:
        // nested types ///////////////////////////////////////////////////////

        typedef std::list<value_type, allocator_type> bucket_type;
        typedef std::vector<bucket_type> bucket_vector;
        typedef typename bucket_vector::iterator bucket_iterator;
        typedef typename bucket_vector::const_iterator const_bucket_iterator;

    public:
        // nested types ///////////////////////////////////////////////////////

        typedef typename bucket_type::iterator local_iterator;
        typedef typename bucket_type::const_iterator const_local_iterator;

        typedef nested_iterator<value_type, bucket_iterator, local_iterator>
        iterator;

        typedef nested_iterator<const value_type, const_bucket_iterator,
                                const_local_iterator>
        const_iterator;

        // lifecycle //////////////////////////////////////////////////////////

        /// @pre n >= 1
        /// @post m.bucket_count() >= n
        /// @post m.empty()
        explicit unordered_container(size_type n = 3,
                                     const hasher& h = hasher(),
                                     const key_equal& eq = key_equal(),
                                     const allocator_type& a
                                     = allocator_type())
            : buckets_(n, bucket_type(a)), hash_(h), eq_(eq),
              allocator_(a), size_(0), max_load_factor_(1)
        { }

        /// Exception safety: No-throw guarantee.
        void swap(unordered_container& other)
        {
            buckets_.swap(other.buckets_);
            std::swap(hash_, other.hash_);
            std::swap(eq_, other.eq_);
            std::swap(allocator_, other.allocator_);
            std::swap(size_, other.size_);
            std::swap(max_load_factor_, other.max_load_factor_);
        }

        // iteration //////////////////////////////////////////////////////////
        
        /// Exception safety: No-throw guarantee.
        iterator begin()
        {
            return iterator(buckets_.begin(), buckets_.end());
        }

        /// Exception safety: No-throw guarantee.
        const_iterator begin() const
        {
            return const_iterator(buckets_.begin(), buckets_.end());
        }

        /// Exception safety: No-throw guarantee.
        iterator end()
        {
            return iterator(buckets_.end(), buckets_.end());
        }

        /// Exception safety: No-throw guarantee.
        const_iterator end() const
        {
            return const_iterator(buckets_.end(), buckets_.end());
        }

        // local iteration ////////////////////////////////////////////////////

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < m.bucket_count()
        local_iterator begin(size_type i)
        {
            assert(i < bucket_count());
            return buckets_[i].begin();
        }

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < m.bucket_count()
        const_local_iterator begin(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].begin();
        }

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < m.bucket_count()
        local_iterator end(size_type i)
        {
            assert(i < bucket_count());
            return buckets_[i].end();
        }

        /// Exception safety: No-throw guarantee.
        ///
        /// @pre i < m.bucket_count()
        const_local_iterator end(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].end();
        }

        // insertion and removal //////////////////////////////////////////////

        /// Complexity: Constant on average. Worst case is linear in size.
        ///
        /// Exception safety: Basic guarantee.
        ///
        /// @post m.find(v.first) != m.end()
        std::pair<iterator, bool> insert(const_reference t)
        {
            std::pair<iterator, bool> result;
            bucket_iterator b = buckets_.begin() + bucket(t.first);
            local_iterator i = std::find_if(b->begin(), b->end(),
                                            first_equal(traits::key(t), eq_));
            if (!traits::unique || i == b->end()) {
                i = b->insert(i, t);
                ++size_;
                if (load_factor() > max_load_factor()) {
                    rehash(bucket_count() * 2 + 1);
                    result = std::make_pair(find(traits::key(t)), true);
                } else {
                    result = std::make_pair(iterator(b, buckets_.end(), i),
                                            true);
                }
            } else {
                result = std::make_pair(iterator(b, buckets_.end(), i), false);
            }
            assert(find(traits::key(t)) != end());
            return result;
        }

        /// Exception safety: Basic guarantee.
        template <typename InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert(*first++);
            }
        }

        /// Exception safety: No-throw guarantee.
        void erase(iterator i)
        {
            assert(i.current_outer() != i.last_outer());
            assert(i.current_inner() != i.last_inner());
            i.current_outer()->erase(i.current_inner());
            --size_;
        }

        /// Exception safety: No-throw guarantee if this is offered by the hash
        /// and equal operations; strong guarantee otherwise.
        ///
        /// @post m.find(k) == m.end()
        size_type erase(const key_type& k)
        {
            size_type result = 0;
            bucket_type& b = buckets_[bucket(k)];
            local_iterator i = std::find_if(b.begin(), b.end(),
                                            first_equal(k, eq_));
            if (i != b.end()) {
                b.erase(i);
                --size_;
                result = 1;
            }
            assert(find(k) == end());
            return result;
        }

        /// Exception safety: No-throw guarantee.
        void clear()
        {
            BOOST_FOREACH(bucket_type& b, buckets_) {
                b.clear();
            }
            size_ = 0;
        }

        // searching //////////////////////////////////////////////////////////

        /// Exception safety: No-throw guarantee if this is offered by the hash
        /// and equal operations; strong guarantee otherwise.
        ///
        /// @post result == m.end() || result->first == k
        iterator find(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator v = std::find_if(b->begin(), b->end(),
                                            first_equal(k, eq_));
            return (v == b->end()) ? end() : iterator(b, buckets_.end(), v);
        }

        /// Exception safety: No-throw guarantee if this is offered by the hash
        /// and equal operations; strong guarantee otherwise.
        ///
        /// @post result == m.end() || result->first == k
        const_iterator find(const key_type& k) const
        {
            const_bucket_iterator b = buckets_.begin() + bucket(k);
            const_local_iterator v = std::find_if(b->begin(), b->end(),
                                                  first_equal(k, eq_));
            return (v == b->end()) ? end()
                : const_iterator(b, buckets_.end(), v);
        }

        // size ///////////////////////////////////////////////////////////////

        /// Exception safety: No-throw guarantee.
        ///
        /// @return The number of key-value pairs in the map.
        size_type size() const { return size_; }

        /// Exception safety: No-throw guarantee.
        ///
        /// @return True if the map contains no key-value pairs; false
        ///         otherwise.
        bool empty() const { return size() == 0; }

        // partitioning ///////////////////////////////////////////////////////

        /// Exception safety: No-throw guarantee.
        ///
        /// @return The number of buckets in the map.
        size_type bucket_count() const { return buckets_.size(); }

        /// Exception safety: No-throw guarantee if this is offered by the hash
        /// operation; strong guarantee otherwise.
        ///
        /// @return The bucket index for the specified key.
        /// @post result < m.bucket_count()
        size_type bucket(const key_type& k) const
        {
            return hash_(k) % bucket_count();
        }

        /// Exception safety: No-throw guarantee.
        ///
        size_type bucket_size(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].size();
        }

        /// Exception safety: No-throw guarantee.
        ///
        // @post result >= 0 && result <= m.max_load_factor()
        float load_factor() const
        {
            return load_factor(bucket_count());
        }

        /// Exception safety: No-throw guarantee.
        ///
        // @post result >= 0
        float max_load_factor() const { return max_load_factor_; }

        /// Exception safety: Strong guarantee. Exceptions can only be thrown
        /// when constructing the new bucket vector. The map instance has not
        /// been modified at this point. Once the new bucket vector has been
        /// constructed, the rest of the rehashing is carried out using list
        /// splicing and vector swapping, which are no-throw operations.
        ///
        /// @post m.bucket_count() >= n
        void rehash(size_type n)
        {
            if (n >= 1 && load_factor(n) <= max_load_factor()) {
                bucket_vector v(n, bucket_type(allocator_));
                BOOST_FOREACH(bucket_type& b, buckets_) {
                    while (b.begin() != b.end()) {
                        bucket_type& r = v[hash_(traits::key(b.front())) % n];
                        r.splice(r.end(), b, b.begin());
                    }
                }
                buckets_.swap(v);
            }
        }

    private:
        // nested types ///////////////////////////////////////////////////////

        struct first_equal {
            key_type key;
            key_equal eq;

            explicit first_equal(const key_type& k, const key_equal& eq)
                : key(k), eq(eq)
            { }

            bool operator()(const value_type& v) const
            {
                return eq(key, traits::key(v));
            }
        };

        // member variables ///////////////////////////////////////////////////

        bucket_vector buckets_;
        hasher hash_;
        key_equal eq_;
        allocator_type allocator_;
        size_type size_;
        float max_load_factor_;

        // member functions ///////////////////////////////////////////////////

        float load_factor(size_type n) const
        {
            assert(n >= 1);
            return float(size()) / float(n);
        }
    };
}

#endif
