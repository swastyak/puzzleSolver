#ifndef NODE_H
#define NODE_H

#include <iostream>
#include <string>
#include <queue>
using namespace std;

class Node{
private:
    string data;
    int board[3][3];
public:

    Node();
    string matrixToString(int **);
    //Node(int**input);
    Node(string s1, string s2, string s3);
};

class Problem{
private:

public:
    int **start;
    int **goal;
    Problem();
    Problem(int**input);


};

#endif
