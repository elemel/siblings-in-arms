#ifndef SIBLINGS_FLAT_SET_HPP
#define SIBLINGS_FLAT_SET_HPP

#include <algorithm>
#include <functional>
#include <utility>
#include <vector>
#include <boost/utility.hpp>

namespace siblings {
    /// The Sequence template argument models Random Access Container and
    /// Back Insertion Sequence.
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
        flat_set(InputIterator from, InputIterator to,
                 const key_compare& comp = key_compare(),
                 const allocator_type& alloc = allocator_type())
            : less_(comp), storage_(alloc)
        {
            insert(from, to);
        }

        flat_set(const flat_set& other)
            : storage_(other.storage_), less_(other.less_)
        { }

        flat_set& operator=(const flat_set& other)
        {
            storage_ = other.storage_;
            less_ = other.less_;
        }

        void swap(flat_set& other)
        {
            storage_.swap(other.storage_);
            std::swap(less_, other.less_);
        }

        std::pair<iterator, bool> insert(const value_type& value)
        {
            if (!storage_.empty() && !less_(value, storage_.back())) {
                if (less_(storage_.back(), value)) {
                    storage_.push_back(value);
                    return std::make_pair(boost::prior(storage_.end()), true);
                } else {
                    return std::make_pair(boost::prior(storage_.end()), false);
                }
            }
            typename sequence_type::iterator i
                = std::lower_bound(storage_.begin(), storage_.end(), value,
                                   less_);
            if (i == storage_.end() || less_(value, *i)) {
                return std::make_pair(storage_.insert(i, value), true);
            } else {
                return std::make_pair(i, false);
            }
        }

        template <typename InputIterator>
        void insert(InputIterator from, InputIterator to)
        {
            while (from != to)
            {
                insert(*from++);
            }
        }

    private:
        key_compare less_;
        sequence_type storage_;
    };
}

#endif
