#ifndef SIBLINGS_SINK_ITERATOR_HPP
#define SIBLINGS_SINK_ITERATOR_HPP

namespace siblings {
    template <typename F>
    class sink_iterator
    {
    public:
        explicit sink_iterator(F func) : func(func) { }

        template <typename T>
        sink_iterator& operator=(const T& value)
        {
            func(value);
            return *this;
        }

        template <typename T>
        const sink_iterator& operator=(const T& value) const
        {
            func(value);
            return *this;
        }

        sink_iterator& operator++() { return *this; }

        sink_iterator& operator*() { return *this; }
        const sink_iterator& operator*() const { return *this; }

    private:
        F func;
    };

    template <typename F>
    sink_iterator<F> sinker(F func) { return sink_iterator<F>(func); }
}

#endif
