#ifndef _COMPARISION_H
#define _COMPARISION_H

#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cstring>

template<class K, class V>
class Comparision {
private:
    K value;
public:
    Comparision(K newValue) {
        value = newValue;
    }

    bool operator()(std::pair<K, V> const &checkPair) {
        return (checkPair.first == value);
    }
};

#endif