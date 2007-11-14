// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_UNORDERED_IMPL_HPP
#define SIBLINGS_UNORDERED_IMPL_HPP

#include "../nested_iterator.hpp"
#include <cassert>
#include <cstddef>
#include <functional>
#include <list>
#include <utility>
#include <vector>
#include <boost/bind.hpp>
#include <boost/functional/hash.hpp>
#include <boost/utility.hpp>

namespace siblings { namespace detail {

    /// @brief Unordered container implementation.
    ///
    /// @invariant size() <= max_size()
    ///
    /// @invariant bucket_count() <= max_bucket_count()
    ///
    /// @invariant load_factor() <= max_load_factor()
    template <class Key, class Value, class GetKey, class Hash, class Pred,
              class Alloc>
    class unordered_impl {
    private:
        /// Bucket type.
        typedef std::list<Value, Alloc> bucket_type;

        /// Bucket vector type.
        typedef std::vector<bucket_type> bucket_vector;

        /// Bucket iterator type.
        typedef typename bucket_vector::iterator bucket_iterator;

        /// Constant bucket iterator type.
        typedef typename bucket_vector::const_iterator const_bucket_iterator;

    public:
        /// @name Types
        /// @{

        /// Key type.
        typedef Key key_type;

        /// Value type.
        typedef Value value_type;

        /// Key retrieval function.
        typedef GetKey get_key;

        /// Hash function type.
        typedef Hash hasher;

        /// Key comparison type.
        typedef Pred key_equal;

        /// Allocator type.
        typedef Alloc allocator_type;

        /// Pointer type.
        typedef typename allocator_type::pointer pointer;

        /// Constant pointer type.
        typedef typename allocator_type::const_pointer const_pointer;

        /// Reference type.
        typedef typename allocator_type::reference reference;

        /// Constant reference type.
        typedef typename allocator_type::const_reference const_reference;

        /// Size type.
        typedef std::size_t size_type;

        /// Pointer difference type.
        typedef std::ptrdiff_t difference_type;

        /// Local iterator type.
        typedef typename bucket_type::iterator local_iterator;

        /// Constant local iterator type.
        typedef typename bucket_type::const_iterator const_local_iterator;

        /// Iterator type.
        typedef nested_iterator<value_type, bucket_iterator, local_iterator>
        iterator;

        /// Constant iterator type.
        typedef nested_iterator<const value_type, const_bucket_iterator,
                                const_local_iterator>
        const_iterator;

        /// @}

        /// @name Constants
        /// @{

        /// Default bucket type.
        static const size_type default_bucket_count = 3;

        /// @}

        /// @name Construct/Destroy/Copy
        /// @{

        /// Default constructor.
        explicit unordered_impl(size_type n, const get_key& k,
                                const hasher& hf, const key_equal& eql,
                                const allocator_type& a)
            : buckets_(n, bucket_type(a)), key_(k), hash_(hf), eq_(eql),
              alloc_(a), size_(0), max_load_factor_(1)
        { }

        // Use the compiler-generated copy constructor, destructor, and copy
        // assignment operator.
        //
        // unordered_map(const unordered_map&);
        //
        // ~unordered_map();
        //
        // unordered_map& operator=(const unordered_map&);

        /// @brief Returns the allocator.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw if the allocator's copy constructor is
        /// no-throw; strong otherwise.
        allocator_type get_allocator() const { return alloc_; }

        /// @}

        /// @name Size and Capacity
        /// @{

        /// @brief Returns true if there are no elements in the container;
        /// false otherwise.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        bool empty() const { return size_ == 0; }

        /// @brief Returns the number of elements in the container.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        size_type size() const { return size_; }

        /// @brief Returns the maximum number of elements that the container
        /// can hold.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        size_type max_size() const { return buckets_.max_size(); }

        /// @}

        /// @name Iterators
        /// @{

        /// @brief Returns an iterator to the beginning of the container.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        iterator begin()
        {
            return iterator(buckets_.begin(), buckets_.end());
        }

        /// @copydoc cbegin
        const_iterator begin() const
        {
            return const_iterator(buckets_.begin(), buckets_.end());
        }

        /// @brief Returns an iterator to the end of the container.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        iterator end()
        {
            return iterator(buckets_.end(), buckets_.end());
        }

        /// @copydoc cend
        const_iterator end() const
        {
            return const_iterator(buckets_.end(), buckets_.end());
        }

        /// @brief Returns a constant iterator to the beginning of the
        /// container.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        const_iterator cbegin() const { return begin(); }

        /// @brief Returns a constant iterator to the end of the container.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        const_iterator cend() const { return end(); }

        /// @}

        /// @name Modifiers
        /// @{

        /// @brief Inserts the specified value into the container.
        ///
        /// Complexity. Average case constant, worst case linear.
        ///
        /// Exception safety: Strong if the hash function is no-throw; basic
        /// otherwise.
        ///
        /// @post result.second
        std::pair<iterator, bool> insert(const value_type& obj)
        {
            bucket_iterator b = buckets_.begin() + bucket(key_(obj));
            local_iterator v = find_impl(*b, key_(obj));
            return std::make_pair(insert_impl(b, v, obj), true);
        }

        /// @brief Inserts a value using the specified iterator as a hint.
        ///
        /// Complexity. Average case constant, worst case linear.
        ///
        /// Exception safety: Strong if the hash function is no-throw; basic
        /// otherwise.
        iterator insert(iterator hint, const value_type& obj)
        {
            if (hint != end() && eq_(key_(*hint), key_(obj))) {
                return insert_impl(hint.current_outer(), hint.current_inner(),
                                   obj);
            } else {
                return insert_unique(obj).first;
            }
        }

        /// @brief Inserts a value using the specified constant iterator as a
        /// hint.
        ///
        /// Complexity. Average case constant, worst case linear.
        ///
        /// Exception safety: Strong if the hash function is no-throw; basic
        /// otherwise.
        const_iterator insert(const_iterator hint, const value_type& obj)
        {
            if (hint != end() && eq_(key_(*hint), key_(obj))) {
                return insert_impl(hint.current_outer(), hint.current_inner(),
                                   obj);
            } else {
                return insert_unique(obj).first;
            }
        }

        /// Inserts all values in the specified range.
        template <class InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert(*first++);
            }
        }

        /// @brief Inserts the specified value unless there is an element
        /// with an equivalent key.
        std::pair<iterator, bool> insert_unique(const value_type& obj)
        {
            bucket_iterator b = buckets_.begin() + bucket(key_(obj));
            local_iterator v = find_impl(b, key_(obj));
            if (v == b->end()) {
                return std::make_pair(insert_impl(b, v, obj), true);
            } else {
                return std::make_pair(iterator(b, buckets_.end(), v), false);
            }
        }
        
        /// Inserts value unless present; the iterator is used as a hint.
        iterator insert_unique(iterator hint, const value_type& obj)
        {
            if (hint != end() && eq_(key_(*hint), key_(obj))) {
                return hint;
            } else {
                return insert_unique(obj).first;
            }
        }
            
        /// Inserts value unless present; the iterator is used as a hint.
        const_iterator insert_unique(const_iterator hint,
                                     const value_type& obj)
        {
            if (hint != end() && eq_(key_(*hint), key_(obj))) {
                return hint;
            } else {
                return insert_unique(obj).first;
            }
        }

        /// Inserts those values in the specified range that are not present.
        template <class InputIterator>
        void insert_unique(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert_unique(*first++);
            }
        }

        /// Erases the element at the specified position.
        iterator erase(iterator i)
        {
            assert(i != end());
            iterator result = boost::next(i);
            i.current_outer()->erase(i.current_inner());
            --size_;
            return result;
        }

        /// Erases the element at the specified position.
        const_iterator erase(const_iterator i)
        {
            assert(i != end());
            const_iterator result = boost::next(i);
            i.current_outer()->erase(i.current_inner());
            --size_;
            return result;
        }

        /// @brief Erases all elements with key equal to @c k.
        ///
        /// Exception safety: No-throw if the hash and comparison functions are
        /// no-throw; strong if only the comparison function is no-throw; and
        /// basic otherwise.
        ///
        /// @post find(k) == end()
        /// 
        /// @post result == old(size()) - size()
        size_type erase(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator v = find_impl(b, k);
            if (v == b->end()) {
                return 0;
            } else {
                size_type old_size = size();
                do {
                    v = b->erase(v);
                    --size_;
                } while (v != b->end() && eq_(k, key_(*v)));
                return old_size - size();
            }
        }

        /// @brief Erases all elements in the range [first, last).
        ///
        /// Complexity: Linear in the size of the range.
        ///
        /// Exception safety: No-throw.
        iterator erase(iterator first, iterator last)
        {
            while (first != last) {
                first = erase(first);
            }
            return first;
        }

        /// @brief Erases all elements in the range [first, last).
        ///
        /// Complexity: Linear in the size of the range.
        ///
        /// Exception safety: No-throw.
        const_iterator erase(const_iterator first, const_iterator last)
        {
            while (first != last) {
                first = erase(first);
            }
            return first;
        }

        /// @brief Erases an element whose key is equivalent to the one
        /// specified.
        ///
        /// Exception safety: No-throw if the hash and comparison functions are
        /// no-throw; strong otherwise.
        ///
        /// @post result <= 1
        /// @post result == old(size()) - size()
        size_type erase_unique(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator v = find_impl(b, k);
            if (v == b->end()) {
                return 0;
            } else {
                b->erase(v);
                --size_;
                return 1;
            }
        }

        /// @brief Erases all elements in the container.
        ///
        /// Complexity: Linear in the number of elements plus the number of
        /// buckets.
        ///
        /// Exception safety: No-throw.
        ///
        /// @post empty()
        void clear()
        {
            for (bucket_iterator i = buckets_.begin(); i != buckets_.end();
                 ++i)
            {
                i->clear(); // no-throw
            }
            size_ = 0;
        }

        /// @brief Swaps this container with another.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw if the hash and comparison functions
        /// have no-throw swap operations; otherwise, no exception safety
        /// guarantee can be offered.
        void swap(unordered_impl& other)
        {
            buckets_.swap(other.buckets_);
            std::swap(key_, other.key_);
            std::swap(hash_, other.hash_);
            std::swap(eq_, other.eq_);
            std::swap(alloc_, other.alloc_);
            std::swap(size_, other.size_);
            std::swap(max_load_factor_, other.max_load_factor_);
        }

        /// @}

        /// @name Observers
        /// @{

        /// @brief Returns the hash function.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw if the copy constructor of the hash
        /// function is no-throw; strong otherwise.
        hasher hash_function() const { return hash_; }

        /// @brief Returns the key comparison function.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw if the copy constructor of the key
        /// comparison function is no-throw; strong otherwise.
        key_equal key_eq() const { return eq_; }

        /// @}

        /// @name Lookup
        /// @{

        /// @brief Finds an element with the specified key.
        ///
        /// Returns an iterator to an element whose key is equivalent to the
        /// one specified. If no such element was found, an iterator to the end
        /// of the container is returned instead.
        ///
        /// Complexity: Average case constant, worst case linear.
        ///
        /// Exception safety: No-throw if the hash and comparison functions are
        /// no throw; strong otherwise.
        iterator find(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator v = find_impl(b, k);
            return (v == b->end()) ? end() : iterator(b, buckets_.end(), v);
        }

        /// @brief Finds an element with the specified key.
        ///
        /// Returns a constant iterator to an element whose key is equivalent
        /// to the one specified. If no such element was found, a constant
        /// iterator to the end of the container is returned instead.
        ///
        /// Complexity: Average case constant, worst case linear.
        ///
        /// Exception safety: No-throw if the hash and comparison functions are
        /// no throw; strong otherwise.
        const_iterator find(const key_type& k) const
        {
            return const_cast<unordered_impl&>(*this).find(k);
        }

        /// @brief Counts all occurences of the specified key.
        ///
        /// Complexity: Average case linear in result, worst case linear in
        /// number of elements.
        ///
        /// Exception safety: No-throw if the hash and comparison functions are
        /// no throw; strong otherwise.
        size_type count(const key_type& k) const
        {
            const_bucket_iterator b = buckets_.begin() + bucket(k);
            const_local_iterator v = find_impl(b, k);
            if (v == b->end()) {
                return 0;
            }
            size_type result = 0;
            do {
                ++v;
                ++result;
            } while (v != b->end() && eq_(k, key_(*v)));
            return result;
        }

        /// @brief Counts at most one occurence of the specified key.
        ///
        /// Complexity: Average case constant, worst case linear.
        ///
        /// Exception safety: No-throw if the hash and comparison functions are
        /// no throw; strong otherwise.
        ///
        /// @post result <= 1
        size_type count_unique(const key_type& k) const
        {
            const_bucket_iterator b = buckets_.begin() + bucket(k);
            const_local_iterator v = find_impl(b, k);
            return (v == b->end()) ? 0 : 1;
        }

        /// @brief Returns a range of elements having keys equivalent to the
        /// specified key.
        std::pair<iterator, iterator> equal_range(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            std::pair<local_iterator, local_iterator> r
                = equal_range_impl(*b, k);
            if (r.first == b->end()) {
                return std::make_pair(end(), end());
            } else if (r.second == b->end()) {
                return std::make_pair(iterator(b, buckets_.end(), r.first),
                                      iterator(boost::next(b),
                                               buckets_.end()));
            } else {
                return std::make_pair(iterator(b, buckets_.end(), r.first),
                                      iterator(b, buckets_.end(), r.second));
            }
        }

        /// @brief Returns a constant range of elements having keys equivalent
        /// to the specified key.
        std::pair<const_iterator, const_iterator>
        equal_range(const key_type& k) const
        {
            return const_cast<unordered_impl&>(*this).equal_range(k);
        }

        /// @brief Returns a range of at most one element whose key is
        /// equivalent to the specified key.
        std::pair<iterator, iterator> equal_range_unique(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator v = find_impl(*b, k);
            if (v == b->end()) {
                return std::make_pair(end(), end());
            } else {
                return std::make_pair(iterator(b, buckets_.end(), v),
                                      iterator(b, buckets_.end(),
                                               boost::next(v)));
            }
        }

        /// @brief Returns a constant range of at most one element whose key
        /// is equivalent to the specified key.
        std::pair<const_iterator, const_iterator>
        equal_range_unique(const key_type& k) const
        {
            return const_cast<unordered_impl&>(*this)
                .equal_range_unique(k);
        }

        /// @}

        /// @name Bucket Interface
        /// @{

        /// @brief Returns the number of buckets in the container.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        size_type bucket_count() const { return buckets_.size(); }

        /// @brief Returns the maximum number of buckets that the container can
        /// hold.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        size_type max_bucket_count() const { return buckets_.max_size(); }

        /// @brief Returns the size of the specified bucket.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        ///
        /// @pre i < bucket_count()
        ///
        /// @post result <= size()
        size_type bucket_size(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].size();
        }

        /// @brief Returns the bucket index for the specified key.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw if the hash function is no-throw; strong
        /// otherwise.
        size_type bucket(const key_type& k) const
        {
            return hash_(k) % bucket_count();
        }

        /// @brief Returns an iterator to the beginning of the specified
        /// bucket.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        ///
        /// @pre i < bucket_count()
        local_iterator begin(size_type i)
        {
            assert(i < bucket_count());
            return buckets_[i].begin();
        }

        /// @brief Returns a constant iterator to the beginning of the
        /// specified bucket.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        ///
        /// @pre i < bucket_count()
        const_local_iterator begin(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].begin();
        }

        /// @brief Returns an iterator to the end of the specified bucket.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        ///
        /// @pre i < bucket_count()
        local_iterator end(size_type i)
        {
            assert(i < bucket_count());
            return buckets_[i].end();
        }

        /// @brief Returns a constant iterator to the end of the specified
        /// bucket.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        ///
        /// @pre i < bucket_count()
        const_local_iterator end(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].end();
        }

        /// @}

        /// @name Hash Policy
        /// @{

        /// @brief Returns the current load factor.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        ///
        /// @post result >= 0 && result <= max_load_factor()
        float load_factor() const
        {
            return load_factor(bucket_count());
        }

        /// @brief Returns the maximum load factor.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        ///
        /// @post result >= 0
        float max_load_factor() const { return max_load_factor_; }

        /// @brief Sets the maximum load factor.
        ///
        /// Complexity: Constant unless the new maximum load factor triggers a
        /// rehash, in which case the complexity is linear in the number of
        /// elements plus the number of buckets.
        ///
        /// Exception safety: Strong.
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
                throw;
            }
        }

        /// @brief Rehashes the container using the specified bucket count.
        ///
        /// Complexity: Linear in the number of elements plus the number of
        /// buckets in the container plus the specified number of buckets.
        ///
        /// Exception safety: Strong if the hash function is no-throw; basic
        /// otherwise.
        ///
        /// @pre n >= 1
        /// @post bucket_count() >= n
        /// @post size() <= old(size())
        void rehash(size_type n)
        {
            assert(n >= 1);
            if (load_factor(n) <= max_load_factor()) {
                bucket_vector v(n, bucket_type(alloc_));
                size_type old_size = size();
                for (bucket_iterator i = buckets_.begin(); i != buckets_.end();
                     ++i)
                {
                    while (!i->empty()) {
                        bucket_type& b = v[hash_(key_(i->front())) % n];
                        b.splice(b.end(), *i, i->begin());
                        --size_;
                    }
                }
                buckets_.swap(v);
                size_ = old_size;
            }
        }

        /// @}

    private:
        /// Bucket vector.
        bucket_vector buckets_;

        /// Key retrieval function.
        get_key key_;

        /// Hash function.
        hasher hash_;

        /// Key comparison function.
        key_equal eq_;

        /// Allocator.
        allocator_type alloc_;

        /// Size.
        size_type size_;

        /// Maximum load factor.
        float max_load_factor_;

        /// @brief Calculates the load factor using the specified bucket count.
        ///
        /// Complexity: Constant.
        ///
        /// Exception safety: No-throw.
        float load_factor(size_type n) const
        {
            assert(n >= 1);
            return float(size()) / float(n);
        }

        /// @brief Inserts a value at the specified position.
        ///
        /// Complexity: Constant unless the insertion triggers a rehash.
        ///
        /// Exception safety: Strong if the hash function is no-throw; basic
        /// otherwise.
        ///
        /// @param b Iterator to bucket.
        ///
        /// @param v Insertion point in bucket. Points to an element in the
        /// bucket or to its end.
        ///
        /// @return  An iterator to the inserted element.
        iterator insert_impl(bucket_iterator b, local_iterator v,
                             const value_type& obj)
        {
            v = b->insert(v, obj);
            ++size_;
            if (load_factor() <= max_load_factor()) {
                return iterator(b, buckets_.end(), v);
            } else {
                rehash(bucket_count() * 2 + 1);
                return find(key_(obj));
            }
        }

        /// @brief Searches the specified bucket for an element having the
        /// specified key.
        ///
        /// Exception safety: No-throw if the comparison function is no-throw;
        /// strong otherwise.
        ///
        /// Complexity: Average case constant, worst case linear.
        local_iterator find_impl(bucket_iterator b, const key_type& k) const
        {
            local_iterator first = b->begin();
            local_iterator last = b->end();
            while (first != last && !eq_(k, key_(*first))) {
                ++first;
            }
            return first;
        }

        /// @brief Returns the lower and upper bounds of the specified key in
        /// the specified bucket.
        ///
        /// Exception safety: No-throw if the comparison function is no-throw;
        /// strong otherwise.
        ///
        /// Complexity: Average case linear in size of range, worst case linear
        /// in total number of elements.
        std::pair<local_iterator, local_iterator>
        equal_range_impl(bucket_iterator b, const key_type& k) const
        {
            local_iterator first = find_impl(b, k);
            local_iterator last = first;
            while (last != b->end() && eq_(k, key_(*last))) {
                ++last;
            }
            return std::make_pair(first, last);
        }
    };

} }

#endif
