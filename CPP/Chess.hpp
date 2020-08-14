//#include "SFML/Graphics.hpp"
#include <vector>
#include <tuple>
#include <string>
#include <stdexcept>

struct Case{
	int x,y;
};

struct Move{
	Case from,to;
};

class Chess
{
public:
    Chess(){
    	white = 0;
    	board[0][0] = 1;
    	board[0][1] = 2;
    	board[0][2] = 3;
    	board[0][3] = 4;
    	board[0][4] = 5;
    	board[0][5] = 3;
    	board[0][6] = 2;
    	board[0][7] = 1;
    	for (int j = 0; j < 8; ++j)
    	{
    		board[1][j] = 6;
    	}
    	for (int i = 2; i < 6; ++i)
    	{
    		for (int j = 0; j < 8; ++j)
    		{
    			board[i][j] = 0;
    		}
    	}
    	for (int j = 0; j < 8; ++j)
    	{
    		board[6][j] = -6;
    	}
    	board[7][0] = -1;
    	board[7][1] = -2;
    	board[7][2] = -3;
    	board[7][3] = -4;
    	board[7][4] = -5;
    	board[7][5] = -3;
    	board[7][6] = -2;
    	board[7][7] = -1;
    };
    ~Chess(){};
    int board[8][8];
    int white;
    int selection;
    //void play();
    void print();
    void swap();
    std::vector<Move> get_reasonable_moves(Case c);
    std::vector<Move> get_all_reasonable_moves();
    bool check_check();
    bool can_move(Move m);
    bool check_mate();
    bool move(Move m);
    int score_k_layers(Move m, int k);
    Move make_a_move(int k);
};