/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

#include <map>
#include <vector>
#include <cmath>

#ifndef COMMON_TYPES_H
#define COMMON_TYPES_H

template<typename T>
struct XYWH
{
    T X;
    T Y;
    T W;
    T H;
    size_t POS;
    
    XYWH(size_t pos) : POS(pos), X(0), Y(0), W(0), H(0)
    {
    }
    
    bool operator<(const XYWH<T>& other) const
    { 
        return compare(*this, other) < 0; 
        //return X < other.X && Y <= other.Y && POS < other.POS;
        return POS < other.POS;
    }
    
    static int compare(const XYWH<T>& xy0, const XYWH<T>& xy1)
    {
        if (xy0.X == xy1.X && xy0.Y == xy1.Y)
        {
            return 0;
        }
        if (xy0.X > xy1.X)
        {
            if (xy0.Y >= xy1.Y)
            {
                return 1;
            }
        }
        if (xy0.X == xy1.X)
        {
            if (xy0.Y > xy0.Y)
            {
                return 1;
            }
        }
        return -1;
    }
};

typedef XYWH<double> XYWHf;

typedef std::map<XYWHf, std::string> TextLineMap;
typedef std::map<int, TextLineMap> TextBlockMap;

#endif