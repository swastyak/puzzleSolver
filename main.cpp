#include <iostream>
#include <string>
#include <queue>
#include "Node.hpp"
using namespace std;

int ** boardCreator(string);
void printBoard(int **);
void generalSearch(int**, string);

int main (int argc, char ** argv){


    cout << "Welcome to Bertie Woosters 8-puzzle solver." << endl <<
    "Type “1” to use a default puzzle, or “2” to enter your own puzzle." << endl;
    string response;
    cin >> response;
    int ** board = boardCreator(response);
    cout << "Enter choice of algorithm." << endl <<
    "1. Uniform Cost Search\n2. A* with the Misplaced Tile heuristic\n3. A* with the Manhattan distance heuristic." << endl;
    cin >> response;
    generalSearch(board, response);
    return 0;
}

void generalSearch(int**board, string queueingFunction){
    if (queueingFunction == "1"){

    }

}

int** boardCreator (string type){
    if (type=="goalState"){
        int** goalBoard = 0;
        goalBoard = new int*[3];
        int cnt = 1;
         for (int i = 0; i < 3; i++){
              goalBoard[i] = new int[3];
              for (int j = 0; j < 3; j++)
                   goalBoard[i][j] = cnt++;
         }
         goalBoard[2][2] = 0;
         return goalBoard;
    }
    if (type == "1"){
        int ** board = 0;
        board = new int*[3];
        board[0] = new int[3];
        board[1] = new int[3];
        board[2] = new int[3];
        board[0][0] = 4;
        board[0][1] = 1;
        board[0][2] = 2;
        board[1][0] = 5;
        board[1][1] = 3;
        board[1][2] = 0;
        board[2][0] = 7;
        board[2][1] = 8;
        board[2][2] = 6;
        return board;
    }
    if (type =="2"){
        string s1, s2, s3;
        cout << endl << "Enter your puzzle, use a zero to represent the blank. \nEnter the first row, use space or tabs between numbers. Press Enter when finished.\n";
        getline (cin,s1);
        getline (cin,s1);
        cout << endl << "Enter the second row, use space or tabs between numbers." << endl;
        getline (cin,s2);
        cout << "\nEnter the third row, use space or tabs between numbers." << endl;
        getline (cin,s3);
        Node *n = new Node(s1, s2, s3);
    }
}


// int board[3][3];
// board[0][0] = 4;
// board[0][1] = 1;
// board[0][2] = 2;
// board[1][0] = 5;
// board[1][1] = 3;
// board[1][2] = 0;
// board[2][0] = 7;
// board[2][1] = 8;
// board[2][2] = 6;
// for (int i = 0; i < 3; i++){
//     for (int j = 0; j < 3; j++){
//         cout << board[i][j] << " ";
//     }
//     cout << endl;
// }
