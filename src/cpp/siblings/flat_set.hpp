// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_FLAT_SET_HPP
#define SIBLINGS_FLAT_SET_HPP

#include <algorithm>
#include <functional>
#include <utility>
#include <vector>
#include <boost/utility.hpp>

namespace siblings {
    /// @brief Set backed by a flat sequence.
    ///
    /// Compare is a model of Strict Weak Ordering. Sequence is a model of
    /// Random Access Container and Back Insertion Sequence, e.g. std::vector.
    ///
    /// @author Mikael Lind
    template <typename Key, typename Compare = std::less<Key>,
              typename Sequence = std::vector<Key> >
    class flat_set {
    public:
        /// Underlying sequence type.
        typedef Sequence sequence_type;

        /// Allocator type.
        typedef typename sequence_type::allocator_type allocator_type;

        /// Key type.
        typedef Key key_type;

        /// Value type.
        typedef key_type value_type;

        /// Key comparison function type.
        typedef Compare key_compare;

        /// Value comparison function type.
        typedef key_compare value_compare;

        /// Pointer type.
        typedef typename sequence_type::pointer pointer;

        /// Reference type.
        typedef typename sequence_type::reference reference;

        /// Constant reference type.
        typedef typename sequence_type::const_reference const_reference;

        /// Size type.
        typedef typename sequence_type::size_type size_type;

        /// Pointer difference type.
        typedef typename sequence_type::difference_type difference_type;

        /// Constant iterator type.
        typedef typename sequence_type::const_iterator const_iterator;

        /// Iterator type.
        typedef const_iterator iterator;

        /// Constant reverse iterator type.
        typedef typename sequence_type::const_reverse_iterator
            const_reverse_iterator;

        /// Reverse iterator type.
        typedef const_reverse_iterator reverse_iterator;

    private:
        /// Mutable iterator type.
        typedef typename sequence_type::iterator mutable_iterator;

    public:
        /// Returns a constant iterator to the first element.
        const_iterator begin() const { return seq_.begin(); }

        /// Returns a constant iterator just beyond the last element.
        const_iterator end() const { return seq_.end(); }

        /// Returns a constant reverse iterator to the first element.
        const_reverse_iterator rbegin() const { return seq_.rbegin(); }

        /// Returns a constant reverse iterator just beyond the last element.
        const_reverse_iterator rend() const { return seq_.rend(); }

        /// Returns the number of elements in the set.
        size_type size() const { return seq_.size(); }

        /// Returns the maximum number of elements that the set can hold.
        size_type max_size() const { return seq_.max_size(); }

        /// Returns true if there are no elements in the set; false otherwise.
        bool empty() const { return seq_.empty(); }

        /// Returns the key comparison function.
        key_compare key_comp() const { return less_; }

        /// Returns the value comparison function.
        value_compare value_comp() const { return less_; }

        /// Default constructor.
        explicit flat_set(const key_compare& less = key_compare(),
                          const allocator_type& alloc = allocator_type())
            : less_(less), seq_(alloc)
        { }

        /// Constructs a set from the specified range.
        template <typename InputIterator>
        flat_set(InputIterator first, InputIterator last,
                 const key_compare& comp = key_compare(),
                 const allocator_type& alloc = allocator_type())
            : less_(comp), seq_(alloc)
        {
            insert(first, last);
        }

        /// Copy constructor.
        flat_set(const flat_set& other)
            : less_(other.less_), seq_(other.seq_)
        { }

        /// Copy assignent operator.
        flat_set& operator=(const flat_set& other)
        {
            flat_set(other).swap(*this);
            return *this;
        }

        /// Swaps this instance with another.
        void swap(flat_set& other)
        {
            std::swap(less_, other.less_);
            seq_.swap(other.seq_);
        }

        /// Inserts the specified value.
        std::pair<iterator, bool> insert(const value_type& v)
        {
            mutable_iterator i = mutable_lower_bound(v);
            if (i == seq_.end() || less_(v, *i)) {
                i = seq_.insert(i, v);
                return std::make_pair(i, true);
            } else {
                // an equivalent key is already present
                return std::make_pair(i, false);
            }
        }

        /// Inserts a value using the specified position as a hint.
        const_iterator insert(iterator pos, const value_type& v)
        {
            if (empty() || pos == end() && less_(seq_.back(), v)
                || pos == begin() && less_(v, seq_.front()))
            {
                return seq_.insert(pos, v);
            } else {
                return insert(v).first;
            }
        }

        /// Inserts all values in the specified range.
        template <typename InputIterator>
        void insert(InputIterator first, InputIterator last)
        {
            while (first != last) {
                insert(*first++);
            }
        }

        /// Erases the element at the specified position.
        void erase(iterator pos)
        {
            seq_.erase(pos);
        }

        /// Erases any element equal to the specified key.
        size_type erase(const key_type& k)
        {
            const_iterator i = lower_bound(k);
            if (i == end() || less_(k, *i)) {
                // nothing to erase
                return 0;
            } else {
                seq_.erase(i);
                return 1;
            }
        }

        /// Erases all elements in the specified range.
        ///
        /// Exception safety: Basic.
        void erase(const_iterator first, const_iterator last)
        {
            seq_.erase(first, last);
        }

        /// Erases all elements in the set.
        ///
        /// Complexity: Linear.
        ///
        /// Exception safety: No-throw.
        void clear()
        {
            seq_.clear();
        }

        /// Finds any occurence of the specified key.
        ///
        /// Returns a constant iterator to the element, if found; returns a
        /// constant iterator to the end of the set otherwise.
        ///
        /// Complexity: Logarithmic.
        ///
        /// Exception safety: No-throw if the comparison function is no-throw;
        /// strong otherwise.
        const_iterator find(const key_type& k) const
        {
            const_iterator i = lower_bound(k);
            return (i == end() || less_(k, *i)) ? end() : i;
        }

        /// Counts the number of occurences of the specified key.
        ///
        /// Complexity: Logarithmic.
        ///
        /// Exception safety: No-throw if the comparison function is no-throw;
        /// strong otherwise.
        ///
        /// @post result <= 1
        size_type count(const key_type& k)
        {
            const_iterator i = lower_bound(k);
            return (i == end() || less_(k, *i)) ? 0 : 1;
        }

        /// Returns the lower bound of the specified key.
        ///
        /// Returns a constant iterator to the first element not less than the
        /// specified key. If no such element exists, a constant iterator to
        /// the end is returned instead.
        ///
        /// Complexity: Logarithmic.
        ///
        /// Exception safety: No-throw if the comparison function is no-throw;
        /// strong otherwise.
        ///
        /// @post result == s.end() || !s.key_comp()(*result, k)
        const_iterator lower_bound(const key_type& k) const
        {
            return std::lower_bound(begin(), end(), k, less_);
        }

        /// Returns the upper bound of the specified key.
        ///
        /// Returns a constant iterator to the first element greater than the
        /// specified key. If no such element exists, a constant iterator to
        /// the end is returned instead.
        ///
        /// Complexity: Logarithmic.
        ///
        /// Exception safety: No-throw if the comparison function is no-throw;
        /// strong otherwise.
        ///
        /// @post result == s.end() || s.key_comp()(k, *result)
        const_iterator upper_bound(const key_type& k) const
        {
            return std::upper_bound(begin(), end(), k, less_);
        }

        /// Returns a range of the elements equal to the specified key.
        ///
        /// Complexity: Logarithmic.
        ///
        /// Exception safety: No-throw if the comparison function is no-throw;
        /// strong otherwise.
        ///
        /// @post result.first == s.lower_bound(k)
        /// @post result.second == s.upper_bound(k)
        std::pair<const_iterator, const_iterator>
        equal_range(const key_type& k) const
        {
            const_iterator i = lower_bound(k);
            if (i == end() || less_(k, *i)) {
                return std::make_pair(i, i);
            } else {
                return std::make_pair(i, boost::next(i));
            }
        }

    private:
        /// Comparison function.
        key_compare less_;

        /// Underlying sequence.
        sequence_type seq_;

        /// Returns a mutable iterator to the lower bound of the specified key.
        ///
        /// Complexity: Logarithmic.
        ///
        /// Exception safety: No-throw if the comparison function is no-throw;
        /// strong otherwise.
        mutable_iterator mutable_lower_bound(const key_type& k)
        {
            return std::lower_bound(seq_.begin(), seq_.end(), k, less_);
        }
    };

    /// Equal-to operator.
    template <typename Key, typename Compare, typename Sequence>
    bool operator==(const flat_set<Key, Compare, Sequence>& left,
                    const flat_set<Key, Compare, Sequence>& right)
    {
        return left.size() == right.size()
            && std::equal(left.begin(), left.end(), right.begin());
    }

    /// Not-equal-to operator.
    template <typename Key, typename Compare, typename Sequence>
    bool operator!=(const flat_set<Key, Compare, Sequence>& left,
                    const flat_set<Key, Compare, Sequence>& right)
    {
        return !(left == right);
    }

    /// Less-than operator.
    template <typename Key, typename Compare, typename Sequence>
    bool operator<(const flat_set<Key, Compare, Sequence>& left,
                   const flat_set<Key, Compare, Sequence>& right)
    {
        return std::lexicographical_compare(left.begin(), left.end(),
                                            right.begin(), right.end());
    }

    /// Less-or-equal operator.
    template <typename Key, typename Compare, typename Sequence>
    bool operator<=(const flat_set<Key, Compare, Sequence>& left,
                    const flat_set<Key, Compare, Sequence>& right)
    {
        return !(right < left);
    }

    /// Greater-or-equal operator.
    template <typename Key, typename Compare, typename Sequence>
    bool operator>=(const flat_set<Key, Compare, Sequence>& left,
                    const flat_set<Key, Compare, Sequence>& right)
    {
        return !(left < right);
    }

    /// Greater-than operator.
    template <typename Key, typename Compare, typename Sequence>
    bool operator>(const flat_set<Key, Compare, Sequence>& left,
                   const flat_set<Key, Compare, Sequence>& right)
    {
        return right < left;
    }
}

#endif
