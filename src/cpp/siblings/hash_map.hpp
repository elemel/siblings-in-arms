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
    template <typename T, typename BucketSequence>
    class bucket_sequence_iterator
        : public boost::iterator_facade<bucket_sequence_iterator<T,
                                                               BucketSequence>,
                                        T, boost::bidirectional_traversal_tag>
    {
    public:
        typedef T value_type;
        typedef BucketSequence bucket_sequence;
        typedef typename bucket_sequence::size_type size_type;

        explicit bucket_sequence_iterator(bucket_sequence* s = 0,
                                          size_type bucket_index = 0,
                                          size_type value_index = 0)
            : buckets_(s), bucket_index_(bucket_index),
              value_index_(value_index)
        { }

    private:
        friend class boost::iterator_core_access;

        bucket_sequence* buckets_;
        size_type bucket_index_;
        size_type value_index_;

        void increment()
        {
            if (++value_index_ == (*buckets_)[bucket_index_].size()) {
                value_index_ = 0;
                do {
                    ++bucket_index_;
                } while (bucket_index_ < buckets_->size()
                         && (*buckets_)[bucket_index_].empty());
            }
        }

        void decrement()
        {
            if (value_index_ == 0) {
                --bucket_index_;
                value_index_ = (*buckets_)[bucket_index_].size() - 1;
            }
        }
        
        bool equal(const bucket_sequence_iterator& other) const
        {
            return buckets_ == other.buckets_
                && bucket_index_ == other.bucket_index_
                && value_index_ == other.value_index_;
        }
        
        value_type& dereference() const
        {
            return (*buckets_)[bucket_index_][value_index_];
        }
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
        typedef bucket_sequence_iterator<const value_type, const bucket_vector>
            const_iterator;
        typedef const_iterator iterator;
        typedef bucket_sequence_iterator<value_type, bucket_vector>
            mutable_iterator;

        /// @pre new_bucket_count >= 1
        /// @post bucket_count() == new_bucket_count
        /// @post empty()
        hash_map(size_type new_bucket_count = 11,
                 const hash_function& h = hash_function())
            : buckets_(new_bucket_count), hash_(h), size_(0)
        { }

        const_iterator begin() const { return const_iterator(&buckets_); }

        const_iterator end() const
        {
            return const_iterator(&buckets_, bucket_count());
        }

        std::pair<iterator, bool> insert(const value_type& v)
        {
            bucket& b = buckets_[hash_(v.first) % buckets_.size()];
            typename bucket::iterator i
                = std::find_if(b.begin(), b.end(), key_equal(v.first));
            if (i == b.end()) {
                b.push_back(v);
                if (++size_ > capacity()) {
                    rehash(bucket_count() * 2 + 1);
                    return std::make_pair(find(v.first), true);
                } else {
                    return std::make_pair(iterator(&buckets_,
                                                   &b - &buckets_.front(),
                                                   b.size() - 1), true);
                }
            } else {
                i->second = v.second;
                return std::make_pair(iterator(&buckets_,
                                               &b - &buckets_.front(),
                                               i - b.begin()), false);
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
            const bucket& b = buckets_[hash_(k) % bucket_count()];
            typename bucket::const_iterator i
                = std::find_if(b.begin(), b.end(), key_equal(k));
            if (i == b.end()) {
                return end();
            } else {
                return const_iterator(&buckets_, &b - &buckets_.front(),
                                      i - b.begin());
            }
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

        /// @pre new_bucket_count >= 1
        /// @post bucket_count() == new_bucket_count
        void rehash(size_type new_bucket_count)
        {
            hash_map h(new_bucket_count, hash_);
            BOOST_FOREACH(const bucket& b, buckets_) {
                BOOST_FOREACH(const value_type& v, b) {
                    h.buckets_[hash_(v.first) % new_bucket_count].push_back(v);
                }
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
