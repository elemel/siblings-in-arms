// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_GET_FIRST_HPP
#define SIBLINGS_GET_FIRST_HPP

namespace siblings {
    template <typename Pair>
    struct get_first {
        typedef Pair argument_type;
        typedef typename Pair::first_type result_type;

        result_type& operator()(Pair& p) const { return p.first; }
        const result_type& operator()(const Pair& p) const { return p.first; }
    };
}

#endif
