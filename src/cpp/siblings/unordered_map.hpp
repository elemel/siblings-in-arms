#ifndef SIBLINGS_UNORDERED_MAP_HPP
#define SIBLINGS_UNORDERED_MAP_HPP

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

        explicit unordered_map_iterator(bucket_iterator current_bucket
                                        = bucket_iterator(),
                                        bucket_iterator last_bucket
                                        = bucket_iterator(),
                                        local_iterator current_value
                                        = local_iterator())

            : current_bucket_(current_bucket), last_bucket_(last_bucket),
              current_value_(current_value)
        { }

        template <typename ConstIterator>
        unordered_map_iterator(const ConstIterator& other)
            : current_bucket_(other.current_bucket()),
              last_bucket_(other.last_bucket()),
              current_value_(other.current_value())
        { }

        bucket_iterator current_bucket() const { return current_bucket_; }
        bucket_iterator last_bucket() const { return last_bucket_; }
        local_iterator current_value() const { return current_value_; }

    private:
        friend class boost::iterator_core_access;

        bucket_iterator current_bucket_;
        bucket_iterator last_bucket_;
        local_iterator current_value_;

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

        bool equal(const unordered_map_iterator& other) const
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
    
    /// @invariant m.size() <= m.bucket_count()
    template <typename Key, typename T, typename Hash = boost::hash<Key> >
    class unordered_map {
    public:
        typedef Key key_type;
        typedef T mapped_type;
        typedef Hash hasher;
        typedef std::pair<const key_type, mapped_type> value_type;
        typedef std::size_t size_type;

    private:
        typedef std::list<value_type> bucket_type;
        typedef std::vector<bucket_type> bucket_vector;
        typedef typename bucket_vector::iterator bucket_iterator;
        typedef typename bucket_vector::const_iterator const_bucket_iterator;

    public:
        typedef typename bucket_type::iterator local_iterator;
        typedef typename bucket_type::const_iterator const_local_iterator;

        typedef unordered_map_iterator<value_type, bucket_iterator,
                                       local_iterator>
        iterator;

        typedef unordered_map_iterator<const value_type, const_bucket_iterator,
                                       const_local_iterator>
        const_iterator;

        /// @pre new_bucket_count >= 1
        /// @post m.bucket_count() == new_bucket_count
        /// @post m.empty()
        explicit unordered_map(size_type new_bucket_count = 11,
                               const hasher& h = hasher())
            : buckets_(new_bucket_count), hash_(h), size_(0)
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
            return iterator(buckets_.end(), buckets_.end(), local_iterator());
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
                                  const_local_iterator());
        }

        // @post m.find(v.first) != m.end()
        std::pair<iterator, bool> insert(const value_type& v)
        {
            bucket_iterator b = buckets_.begin() + bucket(v.first);
            local_iterator i = std::find_if(b->begin(), b->end(),
                                            key_equal(v.first));
            if (i == b->end()) {
                b->push_back(v);
                if (++size_ > bucket_count()) {
                    rehash(bucket_count() * 2 + 1);
                    return std::make_pair(find(v.first), true);
                } else {
                    return std::make_pair(iterator(b, buckets_.end(),
                                                   boost::prior(b->end())),
                                          true);
                }
            } else {
                // Update map element. If we use assignment, the data type must
                // model Assignable. Use erase and insert instead.
                b->erase(i++); // post-increment iterator to keep it valid
                i = b->insert(i, v);
                return std::make_pair(iterator(b, buckets_.end(), i), false);
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
            i.current_bucket()->erase(i.current_value());
        }

        /// @post m.find(k) == m.end()
        size_type erase(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator i = std::find_if(b->begin(), b->end(),
                                            key_equal(k));
            if (i == b->end()) {
                return 0;
            } else {
                b->erase(i);
                --size_;
                return 1;
            }
        }

        /// @post result == m.end() || result->first == k
        iterator find(const key_type& k)
        {
            bucket_iterator b = buckets_.begin() + bucket(k);
            local_iterator i = std::find_if(b->begin(), b->end(),
                                            key_equal(k));
            return (i == b->end()) ? end() : iterator(b, buckets_.end(), i);
        }

        /// @post result == m.end() || result->first == k
        const_iterator find(const key_type& k) const
        {
            const_bucket_iterator b = buckets_.begin() + bucket(k);
            const_local_iterator i = std::find_if(b->begin(), b->end(),
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
        /// @post m.bucket_count() == new_bucket_count
        void rehash(size_type new_bucket_count)
        {
            unordered_map h(new_bucket_count, hash_);
            BOOST_FOREACH(const bucket_type& b, buckets_) {
                BOOST_FOREACH(const value_type& v, b) {
                    h.buckets_[h.bucket(v.first)].push_back(v);
                }
            }
            swap(h);
        }

        void swap(unordered_map& other)
        {
            buckets_.swap(other.buckets_);
            std::swap(hash_, other.hash_);
            std::swap(size_, other.size_);
        }

        mapped_type& operator[](const key_type& k)
        {
            return insert(value_type(k, mapped_type())).first->second;
        }

        size_type bucket(const key_type& k) const
        {
            return hash_(k) % bucket_count();
        }

    private:
        struct key_equal {
            key_type key;

            explicit key_equal(const key_type& k) : key(k) { }

            bool operator()(const value_type& v) { return key == v.first; }
        };

        bucket_vector buckets_;
        hasher hash_;
        size_type size_;
    };
}

#endif
