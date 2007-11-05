#ifndef SIBLINGS_HASH_MAP_HPP
#define SIBLINGS_HASH_MAP_HPP

#include <cassert>
#include <cstddef>
#include <list>
#include <utility>
#include <vector>
#include <boost/foreach.hpp>
#include <boost/functional/hash.hpp>
#include <boost/iterator/iterator_facade.hpp>
#include <boost/utility.hpp>

namespace siblings {
    template <typename T, typename BucketIterator, typename ValueIterator>
    class hash_map_iterator
        : public boost::iterator_facade<hash_map_iterator<T, BucketIterator,
                                                          ValueIterator>,
                                        T, boost::forward_traversal_tag>
    {
    public:
        typedef T value_type;
        typedef BucketIterator bucket_iterator;
        typedef ValueIterator value_iterator;

        explicit hash_map_iterator(bucket_iterator current_bucket
                                   = bucket_iterator(),
                                   bucket_iterator last_bucket
                                   = bucket_iterator(),
                                   value_iterator current_value
                                   = value_iterator())

            : current_bucket_(current_bucket), last_bucket_(last_bucket),
              current_value_(current_value)
        { }

        template <typename ConstIterator>
        hash_map_iterator(const ConstIterator& other)
            : current_bucket_(other.current_bucket()),
              last_bucket_(other.last_bucket()),
              current_value_(other.current_value())
        { }

        bucket_iterator current_bucket() const { return current_bucket_; }
        bucket_iterator last_bucket() const { return last_bucket_; }
        value_iterator current_value() const { return current_value_; }

    private:
        friend class boost::iterator_core_access;

        bucket_iterator current_bucket_;
        bucket_iterator last_bucket_;
        value_iterator current_value_;

        void increment()
        {
            assert(current_bucket_ != last_bucket_);
            if (++current_value_ == current_bucket_->end()) {
                do {
                    ++current_bucket_;
                } while (current_bucket_ != last_bucket_
                         && current_bucket_->empty());
                if (current_bucket_ != last_bucket_) {
                    current_value_ = current_bucket_->begin();
                }
            }
        }

        bool equal(const hash_map_iterator& other) const
        {
            return current_bucket_ == other.current_bucket_
                && (current_bucket_ == last_bucket_
                    || current_value_ == other.current_value_);
        }
        
        value_type& dereference() const
        {
            assert(current_bucket_ != last_bucket_);
            return *current_value_;
        }
    };
    
    /// @invariant size() <= bucket_count()
    template <typename Key, typename Data, typename Hasher = boost::hash<Key> >
    class hash_map {
    public:
        typedef Key key_type;
        typedef Data data_type;
        typedef Hasher hasher;
        typedef std::pair<const key_type, data_type> value_type;
        typedef std::size_t size_type;

    private:
        typedef std::list<value_type> bucket;
        typedef std::vector<bucket> bucket_vector;
        typedef typename bucket_vector::iterator bucket_iterator;
        typedef typename bucket_vector::const_iterator const_bucket_iterator;
        typedef typename bucket::iterator value_iterator;
        typedef typename bucket::const_iterator const_value_iterator;

    public:
        typedef hash_map_iterator<value_type, bucket_iterator, value_iterator>
            iterator;
        typedef hash_map_iterator<const value_type, const_bucket_iterator,
                                  const_value_iterator>
            const_iterator;

        /// @pre new_bucket_count >= 1
        /// @post bucket_count() == new_bucket_count
        /// @post empty()
        explicit hash_map(size_type new_bucket_count = 11,
                 const hasher& h = hasher())
            : buckets_(new_bucket_count), hasher_(h), size_(0)
        { }

        iterator begin()
        {
            // return iterator to first non-empty bucket
            for (bucket_iterator i = buckets_.begin();
                 i != buckets_.end(); ++i)
            {
                if (!i->empty()) {
                    return iterator(i, buckets_.end(), i->begin());
                }
            }
            return end();
        }

        iterator end()
        {
            // return past-the-end iterator for buckets
            return iterator(buckets_.end(), buckets_.end(), value_iterator());
        }

        const_iterator begin() const
        {
            // return iterator to first non-empty bucket
            for (const_bucket_iterator i = buckets_.begin();
                 i != buckets_.end(); ++i)
            {
                if (!i->empty()) {
                    return const_iterator(i, buckets_.end(), i->begin());
                }
            }
            return end();
        }

        const_iterator end() const
        {
            // return past-the-end iterator for buckets
            return const_iterator(buckets_.end(), buckets_.end(),
                                  const_value_iterator());
        }

        std::pair<iterator, bool> insert(const value_type& v)
        {
            bucket_iterator b = buckets_.begin()
                + hasher_(v.first) % buckets_.size();
            value_iterator i = std::find_if(b->begin(), b->end(),
                                            key_equal(v.first));
            bool inserting = (i == b->end());
            if (inserting) {
                b->push_back(v);
                ++size_;
            } else {
                b->erase(i);
                b->push_back(v);
            }
            if (inserting && size_ > bucket_count()) {
                rehash(bucket_count() * 2 + 1);
                return std::make_pair(find(v.first), true);
            } else {
                return std::make_pair(iterator(b, buckets_.end(),
                                               boost::prior(b->end())),
                                      inserting);
            }
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
            erase(i->first);
        }

        /// @post find(k) == end()
        size_type erase(const key_type& k)
        {
            bucket_iterator b = buckets_.begin()
                + hasher_(k) % buckets_.size();
            value_iterator i = std::find_if(b->begin(), b->end(),
                                            key_equal(k));
            if (i == b->end()) {
                return 0;
            } else {
                b->erase(i);
                --size_;
                return 1;
            }
        }

        /// @post result == end() || result->first == k
        iterator find(const key_type& k)
        {
            bucket_iterator b = buckets_.begin()
                + hasher_(k) % buckets_.size();
            value_iterator i = std::find_if(b->begin(), b->end(),
                                            key_equal(k));
            return (i == b->end()) ? end() : iterator(b, buckets_.end(), i);
        }

        /// @post result == end() || result->first == k
        const_iterator find(const key_type& k) const
        {
            const_bucket_iterator b = buckets_.begin()
                + hasher_(k) % buckets_.size();
            const_value_iterator i = std::find_if(b->begin(), b->end(),
                                                  key_equal(k));
            return (i == b->end()) ? end()
                : const_iterator(b, buckets_.end(), i);
        }

        /// @return The number of key-value pairs in the hash map.
        size_type size() const { return size_; }

        /// @return True if the hash map contains no key-value pairs; false
        ///         otherwise.
        bool empty() const { return size() == 0; }

        /// @return The number of buckets in the hash map.
        size_type bucket_count() const { return buckets_.size(); }

        /// @pre new_bucket_count >= 1
        /// @post bucket_count() == new_bucket_count
        void rehash(size_type new_bucket_count)
        {
            hash_map h(new_bucket_count, hasher_);
            BOOST_FOREACH(const bucket& b, buckets_) {
                BOOST_FOREACH(const value_type& v, b) {
                    h.buckets_[hasher_(v.first)
                               % new_bucket_count].push_back(v);
                }
            }
            swap(h);
        }

        void swap(hash_map& other)
        {
            buckets_.swap(other.buckets_);
            std::swap(hasher_, other.hasher_);
            std::swap(size_, other.size_);
        }

        data_type& operator[](const key_type& k)
        {
            return insert(value_type(k, data_type())).first->second;
        }

    private:
        struct key_equal {
            key_type key;

            explicit key_equal(const key_type& key) : key(key) { }

            bool operator()(const value_type& v) { return key == v.first; }
        };

        bucket_vector buckets_;
        hasher hasher_;
        size_type size_;
    };
}

#endif
