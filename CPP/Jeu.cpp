#include "Chess.hpp"
#include <chrono>
#include <iostream>
using namespace std::chrono;

int main(int argc, char const *argv[])
{
	Chess a;
	Move m;
	for (int i = 0; i < 100; ++i)
	{
		m = a.make_a_move(3);
		printf("(%d,%d) -> (%d,%d)\n",m.from.x,m.from.y,m.to.x,m.to.y);
		if (a.check_check()){
			printf("FIN\n");
			break;
		}
	}
	a.print();
	return 0;
}