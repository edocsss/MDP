#include <memory>
#include <list>
#include <cstring>
#include <tuple>

using namespace std;

const int N_rows = 20;
const int N_cols = 15;
const int total_rows = N_rows + 2;
const int total_cols = N_cols + 2;

const int dy[4]{ 1, 0, -1, 0 };
const int dx[4]{ 0, 1, 0, -1 };

const int bot_size = 1;

enum Action {
	FORWARD, TURN_RIGHT, TURN_LEFT
};

const int action_cost[3]{ 1, 24, 24 };

enum GRID {
	EXPLORED = '.', UNEXPLORED = '?', WALL = '#'
};

// Input dependent knowledge
char knowledge[total_rows][total_cols + 1]{
	"#################",
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
	"#???????????????#",
	"#???????????????#",
	"#???????????????#",
	"#################"
};

pair<int, int> rotate(int _x, int _y, const int &n) {
	int temp;
	switch (n) {
		case 1:
			temp = _x;
			_x = _y;
			_y = -temp;
			break;
		case 2:
			_x = -_x;
			_y = -_y;
			break;
		case 3:
			temp = _x;
			_x = -_y;
			_y = temp;
			break;
	}
	return make_pair(_x, _y);
}

struct Sensor {
	int rel_x, rel_y, rel_dir, range;
	Sensor() {};
	Sensor(const int &rel_x, const int &rel_y, const int &rel_dir, const int &range) : rel_x(rel_x), rel_y(rel_y), rel_dir(rel_dir), range(range) {}
	tuple<int, int, int> get(const int &_x, const int &_y, const int &dir) {
		int abs_dir = (dir + rel_dir + 4) % 4;
		pair<int, int> temp_coord = rotate(rel_x, rel_y, dir);
		return make_tuple(_x + temp_coord.first, _y + temp_coord.second, abs_dir);
	}
};

const int N_sensors = 6;
Sensor sensors[N_sensors]{ Sensor(-1, 1, 0, 2), Sensor(0, 1, 0, 2), Sensor(1, 1, 0, 2), Sensor(-1, 1, -1, 2), Sensor(-1, 0, -1, 2), Sensor(1, 1, 1, 5) };

struct BotState {
	int pos_x, pos_y, dir;

	BotState() {}
	BotState(const int &pos_x, const int &pos_y, const int &dir) : pos_x(pos_x), pos_y(pos_y), dir(dir) {}

	const bool operator < (const BotState &other) const {
		return pos_x < other.pos_x
			|| pos_x == other.pos_x && pos_y < other.pos_y
			|| pos_x == other.pos_x && pos_y == other.pos_y && dir < other.dir;
	}

	const bool operator == (const BotState &other) const {
		return pos_x == other.pos_x && pos_y == other.pos_y && dir == other.dir;
	}

	const bool operator != (const BotState &other) const {
		return pos_x != other.pos_x || pos_y != other.pos_y || dir != other.dir;
	}

	bool is_clear_ahead(const bool &ignore_unexplored = true) {
		bool clear_ahead = true;
		for (int _x = -bot_size; _x <= bot_size && clear_ahead; ++_x) {
			int _y = bot_size + 1; // check only one grid ahead
			pair<int, int> temp_coord = rotate(_x, _y, dir);

			int abs_x = pos_x + temp_coord.first,
				abs_y = pos_y + temp_coord.second;
			clear_ahead = clear_ahead && knowledge[abs_y][abs_x] != WALL && (ignore_unexplored || !ignore_unexplored && knowledge[abs_y][abs_x] != UNEXPLORED);
		}
		return clear_ahead;
	}

	shared_ptr<list<tuple<shared_ptr<BotState>, Action, int>>> get_children(const bool &ignore_unexplored = true) {
		shared_ptr<list<tuple<shared_ptr<BotState>, Action, int>>> children(new list<tuple<shared_ptr<BotState>, Action, int>>());
		for (int i = FORWARD; i <= TURN_LEFT; ++i) {
			Action action = static_cast<Action>(i);

			shared_ptr<BotState> next_state(new BotState(*this));
			switch (action) {
			case FORWARD:
				if (is_clear_ahead(ignore_unexplored)) {
					next_state->pos_x += dx[dir];
					next_state->pos_y += dy[dir];
				}
				break;
			case TURN_RIGHT:
				next_state->dir = (next_state->dir + 1) % 4;
				break;
			case TURN_LEFT:
				next_state->dir = (next_state->dir + 3) % 4;
				break;
			}
			children->push_back(make_tuple(next_state, action, action_cost[i]));
		}

		return children;
	}
};

struct A_StarState {
	BotState bot;
	bool searched[total_rows][total_cols];

	A_StarState() {}
	A_StarState(const int &pos_x, const int &pos_y, const int &dir) {
		bot = BotState(pos_x, pos_y, dir);
		for (int i = 0; i < total_rows; ++i) {
			for (int j = 0; j < total_cols; ++j) {
				if (knowledge[i][j] == UNEXPLORED) {
					searched[i][j] = false;
				}
				else searched[i][j] = true;
			}
		}
	}

	const bool operator < (const A_StarState &other) const {
		return bot < other.bot || bot == other.bot && memcmp(searched, other.searched, sizeof searched) < 0;
	}
	
	const bool operator != (const A_StarState &other) const {
		return bot != other.bot || memcmp(searched, other.searched, sizeof searched) != 0;
	}

	void mark_searched() {
		for (int _x = -bot_size; _x <= bot_size; ++_x)
			for (int _y = -bot_size; _y <= bot_size; ++_y)
				searched[bot.pos_y + _y][bot.pos_x + _x] = true;

		for (int i = 0; i < N_sensors; ++i) {
			tuple<int, int, int> _ = sensors[i].get(bot.pos_x, bot.pos_y, bot.dir);
			int s_x = get<0>(_),
				s_y = get<1>(_),
				s_dir = get<2>(_);

			for (int j = 1, g_x, g_y; j <= sensors[i].range; ++j) {
				g_x = s_x + j * dx[s_dir];
				g_y = s_y + j * dy[s_dir];
				if (knowledge[g_y][g_x] != WALL) {
					searched[g_y][g_x] = true;
				}
				else break;
			}
		}
	}

	shared_ptr<list<tuple<shared_ptr<A_StarState>, Action, int>>> get_children() {
		shared_ptr<list<tuple<shared_ptr<A_StarState>, Action, int>>> children(new list<tuple<shared_ptr<A_StarState>, Action, int>>());
		for (int i = FORWARD; i <= TURN_LEFT; ++i) {
			Action action = static_cast<Action>(i);

			shared_ptr<A_StarState> next_state(new A_StarState(*this));
			switch (action) {
				case FORWARD:
					if (bot.is_clear_ahead()) {
						next_state->bot.pos_x += dx[bot.dir];
						next_state->bot.pos_y += dy[bot.dir];
					}
					break;
				case TURN_RIGHT:
					next_state->bot.dir = (next_state->bot.dir + 1) % 4;
					break;
				case TURN_LEFT:
					next_state->bot.dir = (next_state->bot.dir + 3) % 4;
					break;
			}
			next_state->mark_searched();
			children->push_back(make_tuple(next_state, action, action_cost[i]));
		}

		return children;
	}

	bool is_goal() {
		bool searched_all = true;
		for (int i = 1; searched_all && i <= N_rows; ++i)
			for (int j = 1; searched_all && j <= N_cols; ++j)
				searched_all = searched_all && searched[i][j];
		return searched_all;
	}
};

void print(const A_StarState & state) {
	system("cls");

	for (int i = total_rows - 1; i >= 0; --i) {
		puts(knowledge[i]);
	}

	puts("");
	for (int i = total_rows - 1; i >= 0; --i) {
		for (int j = 0; j < total_cols; ++j) {
			if (state.searched[i][j]) {
				putchar('1');
			}
			else putchar('0');
		}
		puts("");
	}
}
