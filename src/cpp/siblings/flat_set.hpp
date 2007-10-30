#ifndef SIBLINGS_FLAT_SET_HPP
#define SIBLINGS_FLAT_SET_HPP

#include <algorithm>
#include <functional>
#include <utility>
#include <vector>
#include <boost/utility.hpp>

namespace siblings {
    /// The Sequence template argument models Random Access Container and
    /// Back Insertion Sequence, as e.g. std::vector does.
    template <typename Key, typename Compare = std::less<Key>,
              typename Sequence = std::vector<Key> >
    class flat_set {
    public:
        typedef Sequence sequence_type;
        typedef typename sequence_type::allocator_type allocator_type;
        typedef Key key_type;
        typedef key_type value_type;
        typedef Compare key_compare;
        typedef key_compare value_compare;
        typedef typename sequence_type::pointer pointer;
        typedef typename sequence_type::reference reference;
        typedef typename sequence_type::const_reference const_reference;
        typedef typename sequence_type::size_type size_type;
        typedef typename sequence_type::difference_type difference_type;
        typedef typename sequence_type::const_iterator const_iterator;
        typedef const_iterator iterator;
        typedef typename sequence_type::const_reverse_iterator
            const_reverse_iterator;
        typedef const_reverse_iterator reverse_iterator;
        typedef typename sequence_type::iterator mutable_iterator;

        iterator begin() const { return storage_.begin(); }
        iterator end() const { return storage_.end(); }
        reverse_iterator rbegin() const { return storage_.rbegin(); }
        reverse_iterator rend() const { return storage_.rend(); }
        size_type size() const { return storage_.size(); }
        size_type max_size() const { return storage_.max_size(); }
        bool empty() const { return storage_.empty(); }
        key_compare key_comp() const { return less_; }
        value_compare value_comp() const { return less_; }

        explicit flat_set(const key_compare& less = key_compare(),
                          const allocator_type& alloc = allocator_type())
            : less_(less), storage_(alloc)
        { }

        template <typename InputIterator>
        flat_set(InputIterator first, InputIterator last,
                 const key_compare& comp = key_compare(),
                 const allocator_type& alloc = allocator_type())
            : less_(comp), storage_(alloc)
        {
            insert(first, last);
        }

        flat_set(const flat_set& other)
            : less_(other.less_), storage_(other.storage_)
        { }

        flat_set& operator=(const flat_set& other)
        {
            flat_set(other).swap(*this);
        }

        void swap(flat_set& other)
        {
            std::swap(less_, other.less_);
            storage_.swap(other.storage_);
        }

        std::pair<iterator, bool> insert(const value_type& value)
        {
            mutable_iterator i = mutable_lower_bound(value);
            if (i == storage_.end() || less_(value, *i)) {
                i = storage_.insert(i, value);
                return std::make_pair(i, true);
            } else {
                // an equivalent key is already present
                return std::make_pair(i, false);
            }
        }

        iterator insert(iterator pos, const value_type& value)
        {
            if (empty() || pos == end() && less_(storage_.back(), value)
                || pos == begin() && less_(value, storage_.front()))
            {
                return storage_.insert(pos, value);
            } else {
                return insert(value).first;
            }
        }

        template <typename InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert(*first++);
            }
        }

        void erase(iterator pos)
        {
            storage_.erase(pos);
        }

        size_type erase(const key_type& key)
        {
            iterator i = lower_bound(key);
            if (i == end() || less_(key, *i)) {
                // nothing to erase
                return 0;
            } else {
                storage_.erase(i);
                return 1;
            }
        }

        void erase(iterator first, iterator last)
        {
            storage_.erase(first, last);
        }

        void clear()
        {
            storage_.clear();
        }

        iterator find(const key_type& key) const
        {
            iterator i = lower_bound(key);
            return (i == end() || less_(key, *i)) ? end() : i;
        }

        size_type count(const key_type& key)
        {
            iterator i = lower_bound(key);
            return (i == end() || less_(key, *i)) ? 0 : 1;
        }

        iterator lower_bound(const key_type& key) const
        {
            return std::lower_bound(begin(), end(), key, less_);
        }

        iterator upper_bound(const key_type& key) const
        {
            return std::upper_bound(begin(), end(), key, less_);
        }

        std::pair<iterator, iterator> equal_range(const key_type& key)
        {
            iterator i = lower_bound(key);
            return std::make_pair(i, (i == end()) ? i : boost::next(i));
        }

        friend bool operator==(const flat_set& left, const flat_set& right)
        {
            return left.size() == right.size()
                && std::equal(left.begin(), left.end(), right.begin(),
                              left.less_);
        }

        friend bool operator<(const flat_set& left, const flat_set& right)
        {
            return std::lexicographical_compare(left.begin(), left.end(),
                                                right.begin(), right.end(),
                                                left.less_);
        }

    private:
        key_compare less_;
        sequence_type storage_;

        mutable_iterator mutable_lower_bound(const key_type& key)
        {
            return std::lower_bound(storage_.begin(), storage_.end(), key,
                                    less_);
        }
    };
}

#endif
