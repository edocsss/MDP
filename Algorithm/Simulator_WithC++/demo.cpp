#include <cstdio>
#include <chrono>
#include <thread>
#include <list>
#include <tuple>
#include <queue>
#include <map>
#include <windows.h>
#include <iostream>
#include <cstring>

using namespace std;

const int N_rows = 20, N_cols = 15;
const int Real_rows = 22, Real_cols = 17;

char real_maze[Real_rows][Real_cols + 1]{
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
	"#################"
};

const int transition = -1; // cost

const int bot_sight = 2;
const int bot_length = 3;

const int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};

int goal_x, goal_y;

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
		for(int i = 1; i <= N_rows; ++i) {
			int cmp = memcmp(maze[i] + 1, other.maze[i] + 1, N_cols);
			if(cmp < 0) return true;
			else if(cmp > 0) return false;
		}
		return false;
	}
	
	bool operator != (const Knowledge &other) const {
		for(int i = 1; i <= N_rows; ++i) {
			int cmp = memcmp(maze[i] + 1, other.maze[i] + 1, N_cols);
			if(cmp != 0) return true;
		}
		return false;
	}
	
	bool operator == (const Knowledge &other) const {
		for(int i = 1; i <= N_rows; ++i) {
			int cmp = memcmp(maze[i] + 1, other.maze[i] + 1, N_cols);
			if(cmp != 0) return false;
		}
		return true;
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
	
	// OUTDATED
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
		switch(dir) {
			case 0:
				// EAST
				for(int i = 0; i < 3; ++i) {
					Position front = pos.get(dir, bot_length);
					
					front.y += i;
					for(int k = 0; k < bot_sight; ++k) {
						if(mem.maze[front.y][front.x] == '#') break;
						else if(mem.maze[front.y][front.x] == '?')
							mem.maze[front.y][front.x] = 'o';
						front = front.get(dir);
					}
				}
				// NORTH
				for(int i = 0; i < 3; i += 2) {
					Position front = pos.get(1, bot_length);
					
					front.x += i;
					for(int k = 0; k < 3; ++k) {
						if(mem.maze[front.y][front.x] == '#') break;
						else if(mem.maze[front.y][front.x] == '?')
							mem.maze[front.y][front.x] = 'o';
						front = front.get(1);
					}
				}
				break;
			case 1:
				// NORTH
				for(int i = 0; i < 3; ++i) {
					Position front = pos.get(dir, bot_length);
					
					front.x += i;
					for(int k = 0; k < 3; ++k) {
						if(mem.maze[front.y][front.x] == '#') break;
						else if(mem.maze[front.y][front.x] == '?')
							mem.maze[front.y][front.x] = 'o';
						front = front.get(dir);
					}
				}
				// WEST
				for(int i = 0; i < 3; i += 2) {
					Position front = pos.get(2);
					
					front.y += i;
					for(int k = 0; k < bot_sight; ++k) {
						if(mem.maze[front.y][front.x] == '#') break;
						else if(mem.maze[front.y][front.x] == '?')
							mem.maze[front.y][front.x] = 'o';
						front = front.get(2);
					}
				}
				break;
			case 2:
				// WEST
				for(int i = 0; i < 3; ++i) {
					Position front = pos.get(dir);
					
					front.y += i;
					for(int k = 0; k < bot_sight; ++k) {
						if(mem.maze[front.y][front.x] == '#') break;
						else if(mem.maze[front.y][front.x] == '?')
							mem.maze[front.y][front.x] = 'o';
						front = front.get(dir);
					}
				}
				// SOUTH
				for(int i = 0; i < 3; i += 2) {
					Position front = pos.get(3);
					
					front.x += i;
					for(int k = 0; k < bot_sight; ++k) {
						if(mem.maze[front.y][front.x] == '#') break;
						else if(mem.maze[front.y][front.x] == '?')
							mem.maze[front.y][front.x] = 'o';
						front = front.get(3);
					}
				}
				break;
			case 3:
				// SOUTH
				for(int i = 0; i < 3; ++i) {
					Position front = pos.get(dir);
					
					front.x += i;
					for(int k = 0; k < bot_sight; ++k) {
						if(mem.maze[front.y][front.x] == '#') break;
						else if(mem.maze[front.y][front.x] == '?')
							mem.maze[front.y][front.x] = 'o';
						front = front.get(dir);
					}
				}
				// EAST
				for(int i = 0; i < 3; i += 2) {
					Position front = pos.get(0, bot_length);
					
					front.y += i;
					for(int k = 0; k < bot_sight; ++k) {
						if(mem.maze[front.y][front.x] == '#') break;
						else if(mem.maze[front.y][front.x] == '?')
							mem.maze[front.y][front.x] = 'o';
						front = front.get(0);
					}
				}
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
				copy -> dir = (copy -> dir + 1) % 4;
				return copy;
			case TURN_RIGHT:
				copy -> dir = (copy -> dir + 3) % 4;
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
//				value += -288 + 16 * c;
				value += -(1 << (21 - c));
	
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
		backtrack -> push_front(action);
		v = prev;
	}
	
	return backtrack;
}

shared_ptr<list<Action>> dijkstra(const State &state, const int &goal_x, const int &goal_y) {
	shared_ptr<State> start_state(new State(state)), goal_state = nullptr;
	priority_queue<pair<int, shared_ptr<State>>> pq;
	
	pq.push(make_pair(0, shared_ptr<State>(start_state)));
	
	map<State, tuple<int, shared_ptr<State>, Action>> visited;
	visited[state] = make_tuple(0, nullptr, FORWARD);
	
	while(!pq.empty()) {
		pair<int, shared_ptr<State>> _ = pq.top();
		pq.pop();
		
		int current_cost = _.first;
		shared_ptr<State> current_state = _.second;
		
		if(current_state -> bot -> pos.x == goal_x && current_state -> bot -> pos.y == goal_y) {
			goal_state = current_state;
			break;
		}
		
		shared_ptr<list<tuple<Action, shared_ptr<State> > > > children = current_state -> get_children();
		for(tuple<Action, shared_ptr<State>> el: *children) {
			Action action = get<0>(el);
			shared_ptr<State> next_state = get<1>(el);
			
			if(visited.find(*next_state) == visited.end()) {
				visited[*next_state] = make_tuple(current_cost + transition, current_state, action);
				pq.push(make_pair(current_cost + transition, next_state));
			}
		}
	}
	
	shared_ptr<list<Action>> backtrack(new list<Action>());
	shared_ptr<State> v(goal_state);
	while(*v != *start_state) {
		tuple<int, shared_ptr<State>, Action> _ = visited[*v];
		shared_ptr<State> u = get<1>(_);
		Action action = get<2>(_);
		backtrack -> push_front(action);
		v = u;
	}
	
	return backtrack;
}

int main(int argc, char * argv[]) {
	// read from args
	if(argc >= 5) {
		int start_x = atol(argv[1]),
			start_y = atol(argv[2]),
			start_dir;
		
		switch(atol(argv[3])) {
			case 0:
				start_dir = 1;
				break;
			case 1:
				start_dir = 0;
				break;
			case 2:
				start_dir = 3;
				break;
			case 3:
				start_dir = 2;
				break;
		}
		
		State start(new Robot(start_x, start_y, start_dir, argv[4]));
		start.bot -> weak_update(); // ???
		
		if(argc == 7) {
			goal_x = atol(argv[5]);
			goal_y = atol(argv[6]);
			
			shared_ptr<list<Action>> actions = dijkstra(start, goal_x, goal_y);
			while(!actions -> empty()) {
				switch(actions -> front()) {
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
				actions -> pop_front();
			} puts("");
			
		} else {
			shared_ptr<list<Action>> actions = A_star(start);
			while(!actions -> empty()) {
				switch(actions -> front()) {
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
				actions -> pop_front();
			} puts("");
		}
	}

	return 0;
}

