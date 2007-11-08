// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_NESTED_ITERATOR_HPP
#define SIBLINGS_NESTED_ITERATOR_HPP

#include <boost/iterator/iterator_facade.hpp>

namespace siblings {
    /// Iterator suited for traversal of nested containers.
    template <typename T, typename OuterIterator, typename InnerIterator>
    class nested_iterator
        : public boost::iterator_facade<nested_iterator<T, OuterIterator,
                                                        InnerIterator>,
                                        T, boost::forward_traversal_tag>
    {
    public:
        typedef T value_type;
        typedef OuterIterator outer_iterator;
        typedef InnerIterator inner_iterator;

        nested_iterator()
            : current_outer_(), last_outer_(),
              current_inner_(), last_inner_()
        { }

        nested_iterator(outer_iterator current_outer,
                        outer_iterator last_outer)
            : current_outer_(current_outer), last_outer_(last_outer),
              current_inner_(), last_inner_()
        {
            skip();
        }

        /// @pre current_outer != last_outer
        /// @pre current_inner != current_outer->end()
        /// @post i.current_outer() == current_outer
        /// @post i.last_outer() == last_outer
        /// @post i.current_inner() == current_inner
        /// @post i.last_inner() == current_outer->end()
        nested_iterator(outer_iterator current_outer,
                        outer_iterator last_outer,
                        inner_iterator current_inner)
            : current_outer_(current_outer), last_outer_(last_outer),
              current_inner_(current_inner), last_inner_(current_outer->end())
        {
            assert(current_outer != last_outer);
            assert(current_inner != current_outer->end());
        }

        template <typename ConstIterator>
        nested_iterator(const ConstIterator& other)
            : current_outer_(other.current_outer()),
              last_outer_(other.last_outer()),
              current_inner_(other.current_inner()),
              last_inner_(other.last_inner())
        { }

        outer_iterator current_outer() const { return current_outer_; }
        outer_iterator last_outer() const { return last_outer_; }
        inner_iterator current_inner() const { return current_inner_; }
        inner_iterator last_inner() const { return last_inner_; }

    private:
        friend class boost::iterator_core_access;

        outer_iterator current_outer_;
        outer_iterator last_outer_;
        inner_iterator current_inner_;
        inner_iterator last_inner_;

        void skip()
        {
            while (current_outer_ != last_outer_
                   && current_outer_->begin() == current_outer_->end())
            {
                ++current_outer_;
            }

            if (current_outer_ == last_outer_) {
                current_inner_ = inner_iterator();
                last_inner_ = inner_iterator();
            } else {
                current_inner_ = current_outer_->begin();
                last_inner_ = current_outer_->end();
            }
        }

        // callbacks for boost::iterator_facade ///////////////////////////////

        /// @pre i.current_outer() != i.last_outer()
        /// @pre i.current_inner() != i.last_inner()
        void increment()
        {
            assert(current_outer() != last_outer());
            assert(current_inner() != last_inner());
            ++current_inner_;
            if (current_inner_ == last_inner_) {
                ++current_outer_;
                skip();
            }
        }

        /// @pre i.last_outer() == other.last_outer()
        bool equal(const nested_iterator& other) const
        {
            assert(last_outer() == other.last_outer());
            return current_outer_ == other.current_outer_
                && (current_outer_ == last_outer_
                    || current_inner_ == other.current_inner_);
        }
        
        /// @pre i.current_outer() != i.last_outer()
        /// @pre i.current_inner() != i.last_inner()
        value_type& dereference() const
        {
            assert(current_outer() != last_outer());
            assert(current_inner() != last_inner());
            return *current_inner_;
        }
    };
}

#endif
