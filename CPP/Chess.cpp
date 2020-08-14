//#include "SFML/Graphics.hpp"
#include "Chess.hpp"
#include <algorithm>
#include <math.h>
#include <boost/range/combine.hpp>
#include <boost/range/irange.hpp>
#include <boost/range/algorithm_ext/push_back.hpp>
#include <boost/range/counting_range.hpp>
#include <boost/foreach.hpp>
#include <string>


void Chess::swap(){
	white= 1-white;
}

void Chess::print(){
	for (int i = 7; i >= 0; --i)
	{
		for (int j = 0; j < 8; ++j)
		{
			printf("%3d", board[i][j]);
		}
		printf("\n");
	}
}
/*
void Chess::play(){
	int px,py;
	bool piece_sel = false;
	int selection_x,selection_y;
   	sf::RenderWindow renderWindow(sf::VideoMode(610, 610), "Chess");
	sf::Event event;
	sf::Texture texture;
	texture.loadFromFile("icons/image.jpg");
	sf::Sprite sprite(texture);
	sprite.scale(0.25,0.25);
	sf::Texture textures[8][8];
	sf::Sprite sprites[8][8];
	char str[80];
	while (renderWindow.isOpen()){
	for (int i = 0; i < 8; ++i)
	{
		for (int j = 0; j < 8; ++j)
		{
			if (board[i][j]!=0){
				sprintf(str,"icons/%d.png",board[i][j]);
				textures[i][j].loadFromFile(str);
				sprites[i][j]=sf::Sprite(textures[i][j]);
				sprites[i][j].setPosition(sf::Vector2f(55+62*j,55+62*(7-i)));
			}
		}
	}
	while (renderWindow.pollEvent(event)){
		if (event.type == sf::Event::EventType::Closed) renderWindow.close();
		if (event.type == sf::Event::MouseButtonPressed){
			if(event.mouseButton.button == sf::Mouse::Left){
				py = (event.mouseButton.x-55)/62;
				px = 7- ((event.mouseButton.y-55)/62);
				if ((white and board[px][py]<0) or (!white and board[px][py]>0)){
					piece_sel=true;
					selection_x=px;
					selection_y=py;
				}
				if (piece_sel and move({selection_x,selection_y,px,py})){
					if (not check_mate()) make_a_move(2);
				}
			}
		}
	}
	renderWindow.clear();
	renderWindow.draw(sprite);
	for (int i = 0; i < 8; ++i)
	{
		for (int j = 0; j < 8; ++j)
		{
			if (board[i][j]!=0){
				renderWindow.draw(sprites[i][j]);
			}
		}
	}
	sf::Text text;
	sf::Font font;
	font.loadFromFile("BERNHC.TTF");
	std::string s = white ? "White " : "Black ";
	if (check_check()) s.append("Check");
	if (check_mate()) s.append("mate!");
	text.setString(s);
	text.setFont(font);
	text.setFillColor(sf::Color::Black);
	text.setPosition(300,590);
	text.setCharacterSize(20);
	renderWindow.draw(text);
	renderWindow.display();
	}
}
*/
std::vector<Move> Chess::get_reasonable_moves(Case c){
	std::vector<Move> moves;
	int type = board[c.x][c.y];
	if (abs(type)==4) return {{c,{c.x-1,c.y-1}},{c,{c.x-1,c.y}},{c,{c.x-1,c.y+1}},{c,{c.x,c.y-1}},{c,{c.x,c.y+1}},{c,{c.x+1,c.y-1}},{c,{c.x+1,c.y}},{c,{c.x+1,c.y+1}}};
	else if  (abs(type)==2) return {{c,{c.x-2,c.y-1}},{c,{c.x-1,c.y-2}},{c,{c.x-2,c.y+1}},{c,{c.x-1,c.y+2}},{c,{c.x+1,c.y-2}},{c,{c.x+2,c.y-1}},{c,{c.x+1,c.y+2}},{c,{c.x+2,c.y+1}}};
	else if (type==-6) return {{c,{c.x-1,c.y}},{c,{c.x-1,c.y+1}},{c,{c.x-1,c.y-1}},{c,{c.x-2,c.y}}};
	else if (type==6) return {{c,{c.x+1,c.y}},{c,{c.x+1,c.y+1}},{c,{c.x+1,c.y-1}},{c,{c.x+2,c.y}}};
	else{
		int inc_x[] = {c.x+1,c.x+2,c.x+3,c.x+4,c.x+5,c.x+6,c.x+7};
		int dec_x[] = {c.x-1,c.x-2,c.x-3,c.x-4,c.x-5,c.x-6,c.x-7};
		int const_x[] = {c.x,c.x,c.x,c.x,c.x,c.x,c.x};
		int inc_y[] = {c.y+1,c.y+2,c.y+3,c.y+4,c.y+5,c.y+6,c.y+7};
		int dec_y[] = {c.y-1,c.y-2,c.y-3,c.y-4,c.y-5,c.y-6,c.y-7};
		int const_y[] = {c.y,c.y,c.y,c.y,c.y,c.y,c.y};
		int this_x, this_y;
		if(abs(type)==1 or abs(type)==5){
			BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(inc_x,const_y)){
				if(this_x>7) break;
				moves.push_back({c,{this_x,this_y}});
			}
			BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(dec_x,const_y)){
				if(this_x<0) break;
				moves.push_back({c,{this_x,this_y}});
			}
			BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(const_x,inc_y)){
				if(this_y>7) break;
				moves.push_back({c,{this_x,this_y}});
			}
			BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(const_x,dec_y)){
				if(this_y<0) break;
				moves.push_back({c,{this_x,this_y}});
			}
		}
		if(abs(type)==3 or abs(type)==5){
			BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(inc_x,inc_y)){
				if(this_x>7 or this_y>7) break;
				moves.push_back({c,{this_x,this_y}});
			}
			BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(inc_x,dec_y)){
				if(this_x>7 or this_y<0) break;
				moves.push_back({c,{this_x,this_y}});
			}
			BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(dec_x,inc_y)){
				if(this_x<0 or this_y>7) break;
				moves.push_back({c,{this_x,this_y}});
			}
			BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(dec_x,dec_y)){
				if(this_x<0 or this_y<0) break;
				moves.push_back({c,{this_x,this_y}});
			}
		}
		return moves;
	}
}

std::vector<Move> Chess::get_all_reasonable_moves(){
	std::vector<Move> moves;
	for (int i = 0; i < 8; ++i)
	{
		for (int j = 0; j < 8; ++j)
		{
			if(board[i][j] != 0){
				Case c = {i,j};
				std::vector<Move> this_moves = get_reasonable_moves(c);
				moves.reserve(moves.size() + distance(this_moves.begin(),this_moves.end()));
				moves.insert(moves.end(),this_moves.begin(),this_moves.end());
			}
		}
	}
	return moves;
}


bool Chess::check_check(){
	int moi = white ? -1 : 1;
	int lui = moi * -1;
	int x,y;
	for (int i = 0; i < 8; ++i)
	{
		for (int j = 0; j < 8; ++j)
		{
			if (board[i][j]==4*moi){
				x=i; y=j; goto end;
			}
		}
	}
	end:
	if (white and (board[x-1][y-1]==6 or board[x-1][y+1]==6)) return true;
	if (!white and (board[x+1][y-1]==-6 or board[x+1][y+1]==-6)) return true;
	//bords
	Case cases_r[8]= {{x-1,y-1},{x-1,y},{x-1,y+1},{x,y-1},{x,y+1},{x+1,y-1},{x+1,y},{x+1,y+1}}; 
	for (int i = 0; i < 8; ++i)
	{
		if (board[cases_r[i].x][cases_r[i].y]==4*lui) return true;
	}
	Case cases_c[8]= {{x-1,y-2},{x-1,y-2},{x-2,y+1},{x-1,y+2},{x+1,y-2},{x+2,y-1},{x+1,y+2},{x+2,y+1}}; 
	for (int i = 0; i < 8; ++i)
	{
		if (board[cases_c[i].x][cases_c[i].y]==2*lui) return true;
	}
	int inc_x[] = {x+1,x+2,x+3,x+4,x+5,x+6,x+7};
	int dec_x[] = {x-1,x-2,x-3,x-4,x-5,x-6,x-7};
	int const_x[] = {x,x,x,x,x,x,x};
	int inc_y[] = {y+1,y+2,y+3,y+4,y+5,y+6,y+7};
	int dec_y[] = {y-1,y-2,y-3,y-4,y-5,y-6,y-7};
	int const_y[] = {y,y,y,y,y,y,y};
	int this_x, this_y;
	BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(inc_x,const_y)){
		if (this_x>7) break;
		if (board[this_x][this_y]==1*lui or board[this_x][this_y]==5*lui) return true;
		if (board[this_x][this_y]!=0) break;
	}
	BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(dec_x,const_y)){
		if (this_x<0) break;
		if (board[this_x][this_y]==1*lui or board[this_x][this_y]==5*lui) return true;
		if (board[this_x][this_y]!=0) break;
	}
	BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(const_x,inc_y)){
		if (this_y>7) break;
		if (board[this_x][this_y]==1*lui or board[this_x][this_y]==5*lui) return true;
		if (board[this_x][this_y]!=0) break;
	}
	BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(const_x,dec_y)){
		if (this_y<0) break;
		if (board[this_x][this_y]==1*lui or board[this_x][this_y]==5*lui) return true;
		if (board[this_x][this_y]!=0) break;
	}
	
	BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(inc_x,inc_y)){
		if (this_x>7 or this_y>7) break;
		if (board[this_x][this_y]==3*lui or board[this_x][this_y]==5*lui) return true;
		if (board[this_x][this_y]!=0) break;
	}
	BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(inc_x,dec_y)){
		if (this_x>7 or this_y<0) break;
		if (board[this_x][this_y]==3*lui or board[this_x][this_y]==5*lui) return true;
		if (board[this_x][this_y]!=0) break;
	}
	
	BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(dec_x,inc_y)){
		if (this_x<0 or this_y>7) break;
		if (board[this_x][this_y]==3*lui or board[this_x][this_y]==5*lui) return true;
		if (board[this_x][this_y]!=0) break;
	}
	BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(dec_x,dec_y)){
		if (this_x<0 or this_y<0) break;
		if (board[this_x][this_y]==3*lui or board[this_x][this_y]==5*lui) return true;
		if (board[this_x][this_y]!=0) break;
	}
	return false;
}

bool Chess::can_move(Move m){
	int moi = white ? -1 : 1;
	int x = m.from.x;
	int y = m.from.y;
	int nx = m.to.x;
	int ny = m.to.y;
	if(nx<0 or nx>7 or ny<0 or ny>7 or board[nx][ny]*moi >0 or board[x][y]*moi<=0) return false;
	if(abs(board[x][y])==6){
		if(board[x][y]>0){
			if(nx<=x or abs(ny-y)>1 or (nx-x>2 and x==1) or (nx-x>1 and x>1)) return false;
			if (ny==y and (board[nx][ny]!=0 or ((nx-x)==2 and board[nx-1][ny]!=0))) return false;
			if(ny!=y and (nx-x==2 or board[nx][ny]>=0)) return false;
		}
		else{
			if(nx>=x or abs(ny-y)>1 or (x-nx>2 and x==6) or (x-nx>1 and x<6)) return false;
			if (ny==y and (board[nx][ny]!=0 or ((x-nx)==2 and board[nx+1][ny]!=0))) return false;
			if(ny!=y and (x-nx==2 or board[nx][ny]<=0)) return false;
		}
	}
	else if(abs(board[x][y])==2){if(abs(nx-x)+abs(ny-y)!=3 or nx==x or ny==y) return false;}
	else if(abs(board[x][y])==4){if(abs(nx-x)>1 or abs(ny-y)>1) return false;}
	else {
		if(abs(board[x][y])==3){if(abs(nx-x) != abs(ny-y)) return false;}
		else if(abs(board[x][y])==1){if(nx!=x and ny!=y) return false;}
		else {if(abs(nx-x)!=abs(ny-y) and nx!=x and ny!=y) return false;}
		std::vector<int> x_range,y_range;
		
		if (nx>x) boost::range::push_back(x_range, boost::irange(x+1,nx));
		else if (nx<x) {
			boost::range::push_back(x_range, boost::irange(nx+1,x));
			std::reverse(x_range.begin(),x_range.end());
		}
		if (ny>y) boost::range::push_back(y_range, boost::irange(y+1,ny));
		else if (ny<y) {
			boost::range::push_back(y_range, boost::irange(ny+1,y));
			std::reverse(y_range.begin(),y_range.end());
		}
		if(nx==x) x_range.insert(x_range.end(),y_range.size(),x);
		if(ny==y) y_range.insert(y_range.end(),x_range.size(),y);
		int this_x, this_y;
		BOOST_FOREACH (boost::tie(this_x,this_y), boost::combine(x_range,y_range)){
			if(board[this_x][this_y]!=0) return false;
		}
	}
	bool serait_check = false;
	int pioch=board[nx][ny];
	board[nx][ny]=board[x][y];
	board[x][y]=0;
	if (check_check()){
		serait_check = true;
	}
	board[x][y]=board[nx][ny];
	board[nx][ny]=pioch;
	if (serait_check) return false;
	return true;
}

bool Chess::check_mate(){
	auto moves = get_all_reasonable_moves();
	for(auto m:moves){
		if (can_move(m)) return false;
	}
	return true;
}

bool Chess::move(Move m){
	if(! can_move(m)) return false;
	int x = m.from.x;
	int y = m.from.y;
	int nx = m.to.x;
	int ny = m.to.y;
	int moi = white ? -1 : 1;
	board[nx][ny]=board[x][y];
	board[x][y]=0;
	if (abs(board[nx][ny])==6 and (nx==0 or nx==7)) board[nx][ny]=5*moi;
	swap();
	return true;
}

int Chess::score_k_layers(Move m, int k){
	int x = m.from.x;
	int y = m.from.y;
	int nx = m.to.x;
	int ny = m.to.y;
	int piece_piochee = board[nx][ny];
	int score;
	bool pion_promu;
	int moi = white ? -1 : 1;
	switch (abs(piece_piochee)){
		case 0:
			score=0;
			break;
		case 1:
			score=50;
			break;
		case 2:
			score=40;
			break;
		case 3:
			score=35;
			break;
		case 5:
			score=90;
			break;
		case 6:
			score=10;
			break;
	}
	pion_promu = (abs(board[nx][ny])==6 and (nx==0 or nx==7));
	if (pion_promu) score = score+100;
	

	assert(move(m));
	bool check = check_check();
	bool mate = check_mate();
	if (check) score=score+5;
	if (mate and check) score=score+1000000000;

	if(k!=1 and not mate){
		Move his_best_move;
		int his_best_score = INT_MIN;
		int this_score;
		for (auto m:get_all_reasonable_moves()){
			if (can_move(m)){
				this_score = score_k_layers(m,k-1);
				if(this_score > his_best_score){
					his_best_score = this_score;
					his_best_move = m;
				}
			}
		}
		score = k*score - his_best_score;
	}


	swap();
	board[x][y]=board[nx][ny];
	board[nx][ny]=piece_piochee;
	if (pion_promu){
		board[x][y]=6*moi;
	}
	return score;
}

Move Chess::make_a_move(int k){
	auto v = get_all_reasonable_moves();
	int score = INT_MIN;
	int this_score;
	Move m_dec;
	for (auto move:v){
		if (can_move(move)){
			this_score = score_k_layers(move,k);
			if (this_score>score){
				score = this_score;
				m_dec = move;
			}
		}
	}
	assert(move(m_dec));
	return(m_dec);
}