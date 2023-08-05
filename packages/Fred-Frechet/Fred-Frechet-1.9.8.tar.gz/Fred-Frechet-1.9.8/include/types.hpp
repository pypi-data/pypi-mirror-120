/*
Copyright 2020-2021 Dennis Rohde

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#pragma once

#include <vector>
#include <cmath>
#include <limits>

typedef double distance_t;
typedef double coordinate_t;
typedef long double parameter_t;

typedef unsigned long dimensions_t;
typedef unsigned long curve_size_t;
typedef unsigned long curve_number_t;

class Point;
class Curve;
class Interval;

using Vector = Point;

using Intervals = std::vector<Interval>;
using Coordinates = std::vector<coordinate_t>;

template<typename T>
inline bool near_eq(T x, T y) {
  return std::abs(x - y) <= std::min(std::abs(x), std::abs(y)) * std::numeric_limits<T>::epsilon();
}


