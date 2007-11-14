// Copyright 2007 Mikael Lind

#ifndef SIBLINGS_IDENTITY_HPP
#define SIBLINGS_IDENTITY_HPP

namespace siblings {
    template <typename T>
    struct identity {
        typedef T argument_type;
        typedef T result_type;

        T& operator()(T& t) const { return t; }
        const T& operator()(const T& t) const { return t; }
    };
}

#endif
