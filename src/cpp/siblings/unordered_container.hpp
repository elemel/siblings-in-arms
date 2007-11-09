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

    template <typename T, typename Cont>
    struct unordered_key_traits {
        typedef T key_type;
        typedef T mapped_type;

        static const key_type& key(const key_type& k) { return k; }
    };

    template <typename T>
    struct unordered_key_traits<T, map_tag> {
        typedef typename T::first_type key_type;
        typedef typename T::second_type mapped_type;

        static const key_type& key(const key_type& k) { return k; }

        template <typename U>
        static const key_type& key(const U& v) { return v.first; }
    };

    template <typename Uniq>
    struct unordered_uniqueness_traits
    {
        static const bool unique = true;
    };

    template <>
    struct unordered_uniqueness_traits<non_unique_tag>
    {
        static const bool unique = false;
    };

    template <typename T, typename Cont, typename Uniq>
    struct unordered_traits
        : unordered_key_traits<T, Cont>, unordered_uniqueness_traits<Uniq>
    { };

    /// @invariant size() <= max_size()
    /// @invariant bucket_count() <= max_bucket_count()
    /// @invariant load_factor() <= max_load_factor()
    template <class T,
              class Cont,
              class Uniq,
              class Hash = boost::hash<
                  typename unordered_traits<T, Cont, Uniq>::key_type
              >,
              class Pred = std::equal_to<
                  typename unordered_traits<T, Cont, Uniq>::key_type
              >,
              class Alloc = std::allocator<T> >
    class unordered_container {
    private:
        typedef unordered_traits<T, Cont, Uniq> traits;
        typedef std::list<T, Alloc> bucket_type;
        typedef std::vector<bucket_type> bucket_vector;
        typedef typename bucket_vector::iterator bucket_iterator;
        typedef typename bucket_vector::const_iterator const_bucket_iterator;

    public:
        // types //////////////////////////////////////////////////////////////

        typedef typename traits::key_type key_type;
        typedef T value_type;
        typedef typename traits::mapped_type mapped_type;
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
        typedef nested_iterator<T, bucket_iterator, local_iterator> iterator;
        typedef nested_iterator<const T, const_bucket_iterator,
                                const_local_iterator> const_iterator;

    private:
        struct key_equal_to {
            const key_type k;
            key_equal eq;

            template <typename U>
            key_equal_to(const U& u, const key_equal& eq)
                : k(traits::key(u)), eq(eq)
            { }

            bool operator()(const value_type& v) const
            {
                return eq(k, traits::key(v));
            }
        };
        
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

        template <class InputIterator>
        unordered_container(InputIterator f, InputIterator l,
                            size_type n = 3,
                            const hasher& hf = hasher(),
                            const key_equal& eql = key_equal(),
                            const allocator_type& a = allocator_type())
            : buckets_(n, bucket_type(a)), hash_(hf), eq_(eql),
              alloc_(a), size_(0), max_load_factor_(1)
        {
            insert(f, l);
        }

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
            bucket_iterator b = buckets_.begin() + bucket(traits::key(obj));
            local_iterator i = std::find_if(b->begin(), b->end(),
                                            key_equal_to(obj, eq_));
            if (!traits::unique || i == b->end()) {
                i = b->insert(i, obj);
                ++size_;
                if (load_factor() > max_load_factor()) {
                    rehash(bucket_count() * 2 + 1);
                    result = std::make_pair(find(traits::key(obj)), true);
                } else {
                    result = std::make_pair(iterator(b, buckets_.end(), i),
                                            true);
                }
            } else {
                result = std::make_pair(iterator(b, buckets_.end(), i), false);
            }
            assert(find(traits::key(obj)) != end());
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
            local_iterator v = std::find_if(b->begin(), b->end(),
                                            key_equal_to(k, eq_));
            return (v == b->end()) ? end() : iterator(b, buckets_.end(), v);
        }

        const_iterator find(const key_type& k) const
        {
            const_bucket_iterator b = buckets_.begin() + bucket(k);
            const_local_iterator v = std::find_if(b->begin(), b->end(),
                                                  key_equal_to(k, eq_));
            return (v == b->end()) ? end()
                : const_iterator(b, buckets_.end(), v);
        }

        size_type count(const key_type& k) const;
        std::pair<iterator, iterator> equal_range(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator i = std::find_if(b->begin(), b->end(),
                                            key_equal_to(k, eq_));
            if (i == b->end()) {
                return std::make_pair(end(), end());
            } else {
                iterator first = iterator(b, buckets_.end(), i);
                iterator last = boost::next(first);
                if (!traits::unique) {
                    key_equal_to eq(*first, eq_);
                    while (last != end() && eq(*last)) {
                        ++last;
                    }
                }
                return std::make_pair(first, last);
            }
        }

        std::pair<const_iterator, const_iterator>
        equal_range(const key_type& k) const;

        mapped_type& operator[](const key_type& k);

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
                        bucket_type& r = v[hash_(traits::key(b.front())) % n];
                        r.splice(r.end(), b, b.begin());
                    }
                }
                buckets_.swap(v);
            }
        }

    private:
    };
}

#endif
