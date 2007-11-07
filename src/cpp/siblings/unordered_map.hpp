#ifndef SIBLINGS_UNORDERED_MAP_HPP
#define SIBLINGS_UNORDERED_MAP_HPP

#include <cassert>
#include <cstddef>
#include <functional>
#include <list>
#include <utility>
#include <vector>
#include <boost/foreach.hpp>
#include <boost/functional/hash.hpp>
#include <boost/iterator/iterator_facade.hpp>
#include <boost/utility.hpp>

namespace siblings {
    template <typename T, typename BucketIterator, typename LocalIterator>
    class unordered_map_iterator
        : public boost::iterator_facade<unordered_map_iterator<T,
                                                               BucketIterator,
                                                               LocalIterator>,
                                        T, boost::forward_traversal_tag>
    {
    public:
        typedef T value_type;
        typedef BucketIterator bucket_iterator;
        typedef LocalIterator local_iterator;

        unordered_map_iterator()
            : current_bucket_(), last_bucket_(),
              current_value_(), last_value_()
        { }

        unordered_map_iterator(bucket_iterator current_bucket,
                               bucket_iterator last_bucket)
            : current_bucket_(current_bucket), last_bucket_(last_bucket),
              current_value_(), last_value_()
        {
            skip_empty_buckets();
        }

        /// @pre current_bucket != last_bucket
        /// @pre current_value != current_bucket->end()
        /// @post i.current_bucket() == current_bucket
        /// @post i.last_bucket() == last_bucket
        /// @post i.current_value() == current_value
        /// @post i.last_value() == current_bucket->end()
        unordered_map_iterator(bucket_iterator current_bucket,
                               bucket_iterator last_bucket,
                               local_iterator current_value)
            : current_bucket_(current_bucket), last_bucket_(last_bucket),
              current_value_(current_value), last_value_(current_bucket->end())
        {
            assert(current_bucket != last_bucket);
            assert(current_value != current_bucket->end());
        }

        template <typename ConstIterator>
        unordered_map_iterator(const ConstIterator& other)
            : current_bucket_(other.current_bucket()),
              last_bucket_(other.last_bucket()),
              current_value_(other.current_value()),
              last_value_(other.last_value())
        { }

        bucket_iterator current_bucket() const { return current_bucket_; }
        bucket_iterator last_bucket() const { return last_bucket_; }
        local_iterator current_value() const { return current_value_; }
        local_iterator last_value() const { return last_value_; }

    private:
        friend class boost::iterator_core_access;

        bucket_iterator current_bucket_;
        bucket_iterator last_bucket_;
        local_iterator current_value_;
        local_iterator last_value_;

        /// @pre i.current_bucket() != i.last_bucket()
        /// @pre i.current_value() != i.last_value()
        void increment()
        {
            assert(current_bucket() != last_bucket());
            assert(current_value() != last_value());
            ++current_value_;
            if (current_value_ == last_value_) {
                ++current_bucket_;
                skip_empty_buckets();
            }
        }

        /// @pre i.last_bucket() == other.last_bucket()
        bool equal(const unordered_map_iterator& other) const
        {
            assert(last_bucket() == other.last_bucket());
            return current_bucket_ == other.current_bucket_
                && (current_bucket_ == last_bucket_
                    || current_value_ == other.current_value_);
        }
        
        /// @pre i.current_bucket() != i.last_bucket()
        /// @pre i.current_value() != i.last_value()
        value_type& dereference() const
        {
            assert(current_bucket() != last_bucket());
            assert(current_value() != last_value());
            return *current_value_;
        }

        void skip_empty_buckets()
        {
            while (current_bucket_ != last_bucket_ && current_bucket_->empty())
            {
                ++current_bucket_;
            }
            if (current_bucket_ != last_bucket_) {
                current_value_ = current_bucket_->begin();
                last_value_ = current_bucket_->end();
            } else {
                current_value_ = local_iterator();
                last_value_ = local_iterator();
            }
        }
    };
    
    /// @invariant m.load_factor() <= m.max_load_factor()
    template <typename K, typename T, typename H = boost::hash<K>,
              typename P = std::equal_to<K>,
              typename A = std::allocator<std::pair<const K, T> > >
    class unordered_map {
    public:
        // nested types ///////////////////////////////////////////////////////

        typedef K key_type;
        typedef T mapped_type;
        typedef H hasher;
        typedef P key_equal;
        typedef A allocator_type;
        typedef std::pair<const key_type, T> value_type;
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

        typedef unordered_map_iterator<value_type, bucket_iterator,
                                       local_iterator>
        iterator;

        typedef unordered_map_iterator<const value_type, const_bucket_iterator,
                                       const_local_iterator>
        const_iterator;

        // lifecycle //////////////////////////////////////////////////////////

        /// @pre n >= 1
        /// @post m.bucket_count() >= n
        /// @post m.empty()
        explicit unordered_map(size_type n = 3, const hasher& h = hasher(),
                               const key_equal& eq = key_equal(),
                               const allocator_type& a = allocator_type())
            : buckets_(n, bucket_type(a)), hash_(h), eq_(eq),
              allocator_(a), size_(0), max_load_factor_(1)
        { }

        void swap(unordered_map& other)
        {
            buckets_.swap(other.buckets_);
            std::swap(hash_, other.hash_);
            std::swap(eq_, other.eq_);
            std::swap(allocator_, other.allocator_);
            std::swap(size_, other.size_);
            std::swap(max_load_factor_, other.max_load_factor_);
        }

        // iteration //////////////////////////////////////////////////////////
        
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

        // local iteration ////////////////////////////////////////////////////

        /// @pre i < m.bucket_count()
        local_iterator begin(size_type i)
        {
            assert(i < bucket_count());
            return buckets_[i].begin();
        }

        /// @pre i < m.bucket_count()
        const_local_iterator begin(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].begin();
        }

        /// @pre i < m.bucket_count()
        local_iterator end(size_type i)
        {
            assert(i < bucket_count());
            return buckets_[i].end();
        }

        /// @pre i < m.bucket_count()
        const_local_iterator end(size_type i) const
        {
            assert(i < bucket_count());
            return buckets_[i].end();
        }

        // insertion and removal //////////////////////////////////////////////

        // @post m.find(v.first) != m.end()
        std::pair<iterator, bool> insert(const value_type& v)
        {
            std::pair<iterator, bool> result;
            bucket_iterator b = buckets_.begin() + bucket(v.first);
            local_iterator i = std::find_if(b->begin(), b->end(),
                                            first_equal(v.first, eq_));
            if (i == b->end()) {
                b->push_back(v);
                ++size_;
                if (load_factor() > max_load_factor()) {
                    rehash(bucket_count() * 2 + 1);
                    result = std::make_pair(find(v.first), true);
                } else {
                    result = std::make_pair(iterator(b, buckets_.end(),
                                                     boost::prior(b->end())),
                                            true);
                }
            } else {
                // Update map element. If we use assignment, the data type must
                // model Assignable. Use erase and insert instead.
                b->erase(i++); // post-increment iterator to keep it valid
                i = b->insert(i, v);
                result = std::make_pair(iterator(b, buckets_.end(), i), false);
            }
            assert(find(v.first) != end());
            return result;
        }

        template <typename InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert(*first++);
            }
        }

        void erase(iterator i)
        {
            assert(i.current_bucket() != i.last_bucket());
            assert(i.current_value() != i.last_value());
            i.current_bucket()->erase(i.current_value());
            --size_;
        }

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

        void clear()
        {
            BOOST_FOREACH(bucket_type& b, buckets_) {
                b.clear();
            }
            size_ = 0;
        }

        mapped_type& operator[](const key_type& k)
        {
            return insert(value_type(k, mapped_type())).first->second;
        }

        // searching //////////////////////////////////////////////////////////

        /// @post result == m.end() || result->first == k
        iterator find(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator v = std::find_if(b->begin(), b->end(),
                                            first_equal(k, eq_));
            return (v == b->end()) ? end() : iterator(b, buckets_.end(), v);
        }

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

        /// @return The number of key-value pairs in the map.
        size_type size() const { return size_; }

        /// @return True if the map contains no key-value pairs; false
        ///         otherwise.
        bool empty() const { return size() == 0; }

        // partitioning ///////////////////////////////////////////////////////

        /// @return The number of buckets in the map.
        size_type bucket_count() const { return buckets_.size(); }

        /// @return The bucket index for the specified key.
        /// @post result < m.size()
        size_type bucket(const key_type& k) const
        {
            return hash_(k) % bucket_count();
        }

        size_type bucket_size(size_type i) const
        {
            assert(i <= bucket_count());
            return buckets_[i].size();
        }

        // @post result >= 0 && result <= m.max_load_factor()
        float load_factor() const
        {
            return load_factor(bucket_count());
        }

        // @post result >= 0
        float max_load_factor() const { return max_load_factor_; }

        /// @post m.bucket_count() >= n
        void rehash(size_type n)
        {
            if (n >= 1 && load_factor(n) <= max_load_factor()) {
                bucket_vector v(n, bucket_type(allocator_));
                BOOST_FOREACH(bucket_type& b, buckets_) {
                    while (b.begin() != b.end()) {
                        bucket_type& r = v[hash_(b.front().first) % n];
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
                return eq(key, v.first);
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
            return float(size()) / float(n);
        }
    };
}

#endif
