#ifndef SIBLINGS_HASH_MAP_HPP
#define SIBLINGS_HASH_MAP_HPP

#include <cstddef>
#include <utility>
#include <vector>
#include <boost/foreach.hpp>
#include <boost/functional/hash.hpp>
#include <boost/iterator/iterator_facade.hpp>
#include <boost/utility.hpp>

namespace siblings {
    template <typename T, typename BucketIterator, typename ValueIterator>
    class hash_container_iterator
        : public boost::iterator_facade<hash_container_iterator<T,
                                                                BucketIterator,
                                                                ValueIterator>,
                                        T, boost::bidirectional_traversal_tag>
    {
    public:
        typedef T value_type;
        typedef BucketIterator bucket_iterator;
        typedef ValueIterator value_iterator;

        explicit hash_container_iterator(const bucket_iterator& b
                                         = bucket_iterator(),
                                         const value_iterator& v
                                         = value_iterator())
            : bucket_(b), value_(v)
        { }

    private:
        friend class boost::iterator_core_access;

        bucket_iterator bucket_;
        value_iterator value_;

        void increment()
        {
            ++value_;
            if (value_ == bucket_->end()) {
                ++bucket_;
                value_ = bucket_->begin();
            }
        }

        void decrement()
        {
            if (value_ == bucket_->begin()) {
                --bucket_;
                value_ = bucket_->end();
            }
            --value_;
        }
        
        bool equal(const hash_container_iterator& other) const
        {
            return bucket_ == other.bucket_ && value_ = other.value_;
        }

        value_type& dereference() const { return *value_; }
    };

    /// @invariant size() <= capacity()
    template <typename Key, typename Data, typename Hash = boost::hash<Key> >
    class hash_map {
    public:
        typedef Key key_type;
        typedef Data data_type;
        typedef Hash hash_function;
        typedef std::pair<key_type, data_type> value_type;
        typedef std::size_t size_type;

    private:
        typedef std::vector<value_type> bucket;
        typedef std::vector<bucket> bucket_vector;

    public:
        typedef hash_container_iterator<const value_type,
                                        typename bucket_vector::const_iterator,
                                        typename bucket::const_iterator>
            const_iterator;
        typedef const_iterator iterator;
        typedef hash_container_iterator<value_type,
                                        typename bucket_vector::iterator,
                                        typename bucket::iterator>
            mutable_iterator;

        /// @pre new_bucket_count >= 1
        /// @post bucket_count() == new_bucket_count
        /// @post empty()
        hash_map(size_type new_bucket_count = 11,
                 const hash_function& h = hash_function())
            : buckets_(new_bucket_count), hash_(h), size_(0)
        { }

        std::pair<iterator, bool> insert(const value_type& v)
        {
            bucket& b = buckets_[hash_(v.first) % buckets_.size()];
            typename bucket::iterator i
                = std::find_if(b.begin(), b.end(), key_equal(v.first));
            if (i == b.end()) {
                if (size() < capacity()) {
                    b.push_back(v);
                    ++size_;
                    return std::make_pair(iterator(buckets_.begin()
                                                   + (&b - &buckets_.front()),
                                                   boost::prior(b.end())),
                                          true);
                } else {
                    rehash();
                    return insert(v);
                }
            } else {
                i->second = v.second;
                return std::make_pair(iterator(buckets_.begin()
                                               + (&b - &buckets_.front()), i),
                                      false);
            }
        }

        template <typename InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert(*first++);
            }
        }

        /// @post find(k) == end()
        size_type erase(const key_type& k)
        {
            bucket& b = buckets_[hash_(k) % buckets_.size()];
            typename bucket::iterator i
                = std::find_if(b.begin(), b.end(), key_equal(k));
            if (i == b.end()) {
                return 0;
            } else {
                b.erase(i);
                --size_;
                return 1;
            }
        }

        /// @post result == end() || result->first == k
        const_iterator find(const key_type& k) const
        {
            const bucket& b = buckets_[hash_(k) % buckets_.size()];
            typename bucket::const_iterator i
                = std::find_if(b.begin(), b.end(), key_equal(k));
            return (i == b.end()) ? 0 : &*i;
        }

        /// @return The number of key-value pairs in the hash map.
        size_type size() const
        {
            return size_;
        }

        /// @return True if the hash map contains no key-value pairs; false
        ///         otherwise.
        bool empty() const
        {
            return size() == 0;
        }

        /// @return The number of buckets in the hash map.
        size_type bucket_count() const {
            return buckets_.size();
        }

        /// @return The maximum number of key-value pairs that the hash map can
        ///         contain before it is rehashed.
        size_type capacity() const {
            return bucket_count();
        }

        void rehash()
        {
            rehash(bucket_count() * 2 + 1);
        }

        /// @pre new_bucket_count >= 1
        /// @post bucket_count() == new_bucket_count
        void rehash(size_type new_bucket_count)
        {
            hash_map h(new_bucket_count, hash_);
            BOOST_FOREACH(const bucket& b, buckets_) {
                h.insert(b.begin(), b.end());
            }
            swap(h);
        }

        void swap(hash_map& other)
        {
            buckets_.swap(other.buckets_);
            std::swap(hash_, other.hash_);
            std::swap(size_, other.size_);
        }

    private:
        struct key_equal {
            key_type key;

            explicit key_equal(const key_type& key) : key(key) { }

            bool operator()(const value_type& v) { return key == v.first; }
        };

        bucket_vector buckets_;
        hash_function hash_;
        size_type size_;
    };
}

#endif
