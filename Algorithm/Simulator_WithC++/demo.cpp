#include <cstdio>
#include <chrono>
#include <thread>
#include <list>
#include <tuple>
#include <queue>
#include <map>
#include <windows.h>
#include <iostream>

using namespace std;

const int N_rows = 20, N_cols = 15;

char real_maze[N_rows + 2][N_cols + 3] = {
	"#################",
	"#.......###.....#",
	"#...............#",
	"#...............#",
	"#...............#",
	"#....######.....#",
	"#...............#",
	"#..#............#",
	"####...##.......#",
	"#......#....#####",
	"#......#........#",
	"#......#........#",
	"#...............#",
	"#..#............#",
	"####....###.....#",
	"#...............#",
	"#...............#",
	"#..............##",
	"##...##...##....#",
	"#...............#",
	"#...............#",
	"#################",
};

const int transition = -1; // cost
const int bot_length = 3;
const int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};

bool in_range(const int &a, const int &b, const int &c) { return a <= b && b <= c; }

struct Position {
	int x, y;
	Position(): x(0), y(0) {}
	Position(const int &x, const int &y): x(x), y(y) {}
	bool operator < (const Position &other) const { return x < other.x || x == other.x && y < other.y; }
	bool operator == (const Position &other) const { return x == other.x && y == other.y; }
	bool operator != (const Position &other) const { return x != other.x || y != other.y; }
	int operator - (const Position &other) const { return abs(x - other.x) + abs(y - other.y); }
	Position get(const int &dir, const int &step = 1) { return Position(x + dc[dir] * step, y + dr[dir] * step); }
};

struct Knowledge {
	char maze[N_rows + 2][N_cols + 3]{
		"#################",
		"#...????????????#",
		"#...????????????#",
		"#...????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#???????????????#",
		"#################",
	};
	
	Knowledge() {}
	Knowledge(const char flat_map[]) {
		for(int i = 1; i <= N_rows; ++i) {
			memcpy(maze[i] + 1, flat_map + (N_cols * i - N_cols), N_cols);
		}
	}
	
	bool operator < (const Knowledge &other) const {
		for(int i = 1; i <= N_rows; ++i)
			for(int j = 1; j <= N_cols; ++j)
				if(maze[i][j] != '?' && other.maze[i][j] == '?') return true;
				else if(maze[i][j] == '?' && other.maze[i][j] != '?') return false;
		return false;
	}
	
	bool operator != (const Knowledge &other) const {
		for(int i = 1; i <= N_rows; ++i)
			for(int j = 1; j <= N_cols; ++j)
				if(maze[i][j] != '?' && other.maze[i][j] == '?') return true;
				else if(maze[i][j] == '?' && other.maze[i][j] != '?') return true;
		return false;
	}
	
	bool operator == (const Knowledge &other) const {
		int left = 0, right = 0, matched = 0;
		for(int i = 1; i <= N_rows; ++i)
			for(int j = 1; j <= N_cols; ++j) {
				if(maze[i][j] == '?') ++left;
				if(other.maze[i][j] == '?') ++right;
				if(maze[i][j] == '?' && maze[i][j] == other.maze[i][j]) ++matched;
			}
		return left == matched && left == right;
	}
	
	int count() {
		int result = 0;
		for(int i = 1; i <= N_rows; ++i)
			for(int j = 1; j <= N_cols; ++j)
				if(maze[i][j] == '?')
					++result;
		return result;
	}
};

enum Action {
	FORWARD, TURN_LEFT, TURN_RIGHT
};

struct Robot {
	int dir;
	Position pos;
	Knowledge mem;
	Robot(): pos(1, 1), dir(0), mem() { this -> update(); }
	Robot(const int &x, const int &y, const int &dir, const char * flat_map): pos(x, y), dir(dir), mem(flat_map) {}
	
	bool operator < (const Robot &other) const {
		return pos < other.pos || pos == other.pos && dir < other.dir || pos == other.pos && dir == other.dir &&  mem < other.mem;
	}
	bool operator == (const Robot &other) const { return pos == other.pos && dir == other.dir && mem == other.mem; }
	bool operator != (const Robot &other) const { return dir != other.dir || pos != other.pos || mem != other.mem; }
	
	void update() {
		for(int i = 0; i < bot_length; ++i)
			for(int j = 0; j < bot_length; ++j)
				mem.maze[pos.y + i][pos.x + j] = '.';
		
		// near sighted
		Position front;
		switch(dir) {
			case 0: case 2:
				front = pos.get(dir, dir == 0 ? bot_length : 1);
				for(int i = 0; i < bot_length; ++i)
					if(mem.maze[front.y + i][front.x] == '?')
						mem.maze[front.y + i][front.x] = real_maze[front.y + i][front.x];
				break;
			case 1: case 3:
				front = pos.get(dir, dir == 1 ? bot_length : 1);
				for(int i = 0; i < bot_length; ++i)
					if(mem.maze[front.y][front.x + i] == '?')
						mem.maze[front.y][front.x + i] = real_maze[front.y][front.x + i];
				break;
		}
	}
	
	void weak_update() {
		// near sighted
		Position front;
		switch(dir) {
			case 0: case 2:
				front = pos.get(dir, dir == 0 ? bot_length : 1);
				for(int i = 0; i < bot_length; ++i)
					if(mem.maze[front.y + i][front.x] == '?')
						mem.maze[front.y + i][front.x] = 'o';
				break;
			case 1: case 3:
				front = pos.get(dir, dir == 1 ? bot_length : 1);
				for(int i = 0; i < bot_length; ++i)
					if(mem.maze[front.y][front.x + i] == '?')
						mem.maze[front.y][front.x + i] = 'o';
				break;
		}
	}
	
	shared_ptr<Robot> do_action(const Action &action) {
		shared_ptr<Robot> copy(new Robot(*this));
		Position front;
		switch(action) {
			case FORWARD:
				switch(dir) {
					case 0: case 2:
						front = pos.get(dir, dir == 0 ? bot_length : 1);
						for(int i = 0; i < bot_length; ++i)
							if(mem.maze[front.y + i][front.x] == '#')
								return nullptr;
						break;
					case 1: case 3:
						front = pos.get(dir, dir == 1 ? bot_length : 1);
						for(int i = 0; i < bot_length; ++i)
							if(mem.maze[front.y][front.x + i] == '#')
								return nullptr;
						break;
				}
				copy -> pos = pos.get(dir);
				return copy;
				
			case TURN_LEFT:
				copy -> dir = (copy -> dir + 3) % 4;
				return copy;
			case TURN_RIGHT:
				copy -> dir = (copy -> dir + 1) % 4;
				return copy;
		}
		return nullptr;
	}
};

struct State {
	shared_ptr<Robot> bot;
	State(): bot(new Robot()) {}
	State(Robot *bot): bot(bot) {}
	bool operator < (const State &other) const { return *bot < *other.bot; }
	bool operator == (const State &other) const { return *bot == *other.bot; }
	bool operator != (const State &other) const { return *bot != *other.bot; }
	
	shared_ptr<list<tuple<Action, shared_ptr<State> > > > get_children() {
		shared_ptr<list<tuple<Action, shared_ptr<State> > > > ptr_res(new list<tuple<Action, shared_ptr<State> > >());
		for(int i = FORWARD; i <= TURN_RIGHT; ++i) {
			Action action = static_cast<Action>(i);
			
			shared_ptr<Robot> temp(bot -> do_action(action));
			if(temp != nullptr) {
				temp -> weak_update();
				
				shared_ptr<State> next(new State(*this));
				next -> bot = temp;
				ptr_res -> push_back(make_tuple(action, next));
			}
		}
		return ptr_res;
	}
	
	bool update(const Action &action) {
		shared_ptr<Robot> temp = bot -> do_action(action);
		
		// Action invalid
		if(temp == nullptr)
			return false;
		
		bot = temp;
		bot -> update();
		return true;
	}
	
	bool is_terminal() {
		return bot -> mem.count() == 0;
	}
};

void gotoxy(const int &x, const int &y) {
	static HANDLE h = GetStdHandle(STD_OUTPUT_HANDLE);
	COORD c = {x, y};
	SetConsoleCursorPosition(h, c);
}

void print(const State &state) {
	for(int i = N_rows + 1; i >= 0; --i)
		puts(state.bot -> mem.maze[i]);
	
	int x = state.bot -> pos.x,
		y = N_rows - state.bot -> pos.y - 1;
	
	char display;
	
	switch(state.bot -> dir) {
		case 0:
			display = '>';
			break;
		case 1:
			display = '^';
			break;
		case 2:
			display = '<';
			break;
		case 3:
			display = 'v';
			break;
	}
	
	for(int i = 0; i < bot_length; ++i)
		for(int j = 0; j < bot_length; ++j) {
			gotoxy(x + i, y + j);
			putchar(display);
		}
	gotoxy(0, N_rows + 2);
}

int west_east(const State &state) {
	const Knowledge * temp = &state.bot -> mem; // temporary knowledge
	
	int value = 0;
	for(int r = 1; r <= N_rows; ++r)
		for(int c = 1; c <= N_cols; ++c)
			if(temp -> maze[r][c] == '?')
				value += -288 + 16 * c;
	
	return value;
}

shared_ptr<list<Action>> A_star(const State &current) {
	priority_queue<pair<int, shared_ptr<State>>> pq; // max heap
	map<State, tuple<int, shared_ptr<State>, Action>> visited;
	
	shared_ptr<State> start(new State(current)), goal = nullptr;
	pq.push(make_pair(0, shared_ptr<State>(start) ));
	visited[*start] = make_tuple(0, nullptr, FORWARD);
	
	while(!pq.empty()) {
		pair<int, shared_ptr<State>> _ = pq.top();
		pq.pop();
		
		shared_ptr<State> curr = _.second;
		int cost = get<0>(visited[*curr]);
		
		if(curr -> is_terminal()) {
			goal = curr;
			break;
		}
		
		shared_ptr<list<tuple<Action, shared_ptr<State> > > > children = curr -> get_children();
		for(tuple<Action, shared_ptr<State>> el: *children) {
			Action action = get<0>(el);
			shared_ptr<State> next = get<1>(el);
			
			if(visited.find(*next) == visited.end()) {
				visited[*next] = make_tuple(cost + transition, curr, action);
				pq.push(make_pair(cost + transition + west_east(*next), next ));
			}
		}
	}
	
	shared_ptr<list<Action>> backtrack(new list<Action>());
	shared_ptr<State> v = goal;
	while(*v != *start) {
		tuple<int, shared_ptr<State>, Action> _ = visited[*v];
		shared_ptr<State> prev = get<1>(_);
		Action action = get<2>(_);
		backtrack -> push_back(action);
		v = prev;
	}
	
	return backtrack;
}

int main(int argc, char * argv[]) {
	system("cls");
	
	int start_x = atol(argv[1]),
		start_y = atol(argv[2]),
		start_dir = atol(argv[3]);
	
	State start(new Robot(start_x - 1, start_y - 1, start_dir, argv[4]));
//	print(start);
	
	shared_ptr<list<Action>> actions = A_star(start);
	while(!actions -> empty()) {
		switch(actions -> back()) {
			case FORWARD:
				printf("F");
				break;
			case TURN_LEFT:
				printf("L");
				break;
			case TURN_RIGHT:
				printf("R");
				break;
		}
		actions -> pop_back();
	} puts("");
	
	this_thread::sleep_for(chrono::seconds(1));
	
	return 0;
}

