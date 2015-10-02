#include <map>
#include <queue>
#include <chrono>
#include <thread>
#include <cstdio>
#include <iostream>
#include <cstdlib>
#include "search.h"

using namespace std;

shared_ptr<list<Action>> A_star(const A_StarState &start_state, unsigned long long (*heuristic) (const A_StarState &state)) {
	shared_ptr<list<Action>> actions(new list<Action>());

	map<A_StarState, tuple<shared_ptr<A_StarState>, Action, int>> visited;
	priority_queue<pair<unsigned long long, shared_ptr<A_StarState>>> pq;
	
	pq.push(make_pair(0, shared_ptr<A_StarState>(new A_StarState(start_state))));
	visited[start_state] = make_tuple(nullptr, FORWARD, 0);
	
	shared_ptr<A_StarState> goal_state;

	while (!pq.empty()) {
		pair<long long, shared_ptr<A_StarState>> _ = pq.top();
		pq.pop();

		shared_ptr<A_StarState> curr_state = get<1>(_);

		if (curr_state->is_goal()) {
			goal_state = curr_state;
			break;
		}

		tuple<shared_ptr<A_StarState>, Action, int> curr_cond = (visited.find(*curr_state)) -> second;
		int curr_cost = get<2>(curr_cond);

		shared_ptr<list<tuple<shared_ptr<A_StarState>, Action, int>>> children = curr_state->get_children();
		for (tuple<shared_ptr<A_StarState>, Action, int> child : *children) {
			shared_ptr<A_StarState> next_state = get<0>(child);
			Action action = get<1>(child);
			int transition_cost = get<2>(child);

			if (visited.find(*next_state) == visited.end()) {
				visited[*next_state] = make_tuple(curr_state, action, curr_cost - transition_cost);
				pq.push(make_pair(curr_cost - transition_cost - heuristic(*next_state), next_state));
			}
		}
	}

	shared_ptr<A_StarState> v = goal_state;
	while (*v != start_state) {
		tuple<shared_ptr<A_StarState>, Action, int> _ = (visited.find(*v))->second;
		v = get<0>(_);
		actions->push_front(get<1>(_));
	}

	return actions;
}

unsigned long long west_to_east(const A_StarState &state) {
	long long value = 0;
	for (int r = 1; r <= N_rows; ++r)
		for (int c = 1; c <= N_cols; ++c)
			if (!state.searched[r][c])
				//value += 4LL << (3 * (N_cols - c));
				value += 270 - 15 * c;
				//value += 1;
	return value;
}

void simulate(int pos_x, int pos_y, int dir, shared_ptr<list<Action>> actions) {
	for (Action action : *actions) {
		system("cls");

		switch (action) {
			case FORWARD:
				pos_x += dx[dir];
				pos_y += dy[dir];
				break;
			case TURN_RIGHT:
				dir = (dir + 1) % 4;
				break;
			case TURN_LEFT:
				dir = (dir + 3) % 4;
				break;
		}

		for (int r = N_rows; r >= 1; --r) {
			for (int c = 1; c <= N_cols; ++c) {
				if (r == pos_y && c == pos_x) {
					switch (dir) {
					case 0:
						putchar('^');
						break;
					case 1:
						putchar('>');
						break;
					case 2:
						putchar('v');
						break;
					case 3:
						putchar('<');
						break;
					}
				}
				else putchar('?');
			}
			puts("");
		}

		this_thread::sleep_for(chrono::milliseconds(100));
	}
}

shared_ptr<list<Action>> dijkstra(const BotState &start_state, const int &e_x, const int &e_y, const bool &ignore_unexplored = true) {
	shared_ptr<list<Action>> actions(new list<Action>());
	priority_queue<pair<int, shared_ptr<BotState>>> pq;
	map<BotState, tuple<shared_ptr<BotState>, Action, int>> visited;
	
	pq.push(make_pair(0, shared_ptr<BotState>(new BotState(start_state))));
	visited[start_state] = make_tuple(nullptr, FORWARD, 0);

	shared_ptr<BotState> goal_state;
	while (!pq.empty()) {
		pair<int, shared_ptr<BotState>> _ = pq.top();
		pq.pop();

		int curr_cost = get<0>(_);
		shared_ptr<BotState> curr_state = get<1>(_);

		if (curr_state->pos_x == e_x && curr_state->pos_y == e_y) {
			goal_state = curr_state;
			break;
		}

		shared_ptr<list<tuple<shared_ptr<BotState>, Action, int>>> children = curr_state->get_children(ignore_unexplored);
		for (tuple<shared_ptr<BotState>, Action, int> child : *children) {
			shared_ptr<BotState> next_state = get<0>(child);
			Action action = get<1>(child);
			int transition_cost = get<2>(child);

			if (visited.find(*next_state) == visited.end()) {
				visited[*next_state] = make_tuple(curr_state, action, curr_cost - transition_cost);
				pq.push(make_pair(curr_cost - transition_cost, next_state));
			}
		}
	}

	shared_ptr<BotState> v = goal_state;
	while (*v != start_state) {
		tuple<shared_ptr<BotState>, Action, int> _ = visited[*v];
		v = get<0>(_);
		actions->push_front(get<1>(_));
	}

	return actions;
}

int main(int argc, char ** argv) {
	if (argc == 5) {
		int s_x = atol(argv[1]) + 1,
			s_y = atol(argv[2]) + 1,
			s_dir = atol(argv[3]);

		char * flat_map = argv[4];
		update_knowledge(flat_map);

		A_StarState init_state(s_x, s_y, s_dir);

		init_state.mark_searched();
		//print(init_state);

		shared_ptr<list<Action>> actions = A_star(init_state, west_to_east);
		for (Action action : *actions) {
			switch (action) {
			case FORWARD:
				printf("F");
				break;
			case TURN_RIGHT:
				printf("R");
				break;
			case TURN_LEFT:
				printf("L");
				break;
			}
		}
		//puts("");

		//getchar();
		//simulate(2, 2, 0, actions);
	}
	else if (argc == 6) {
		int s_x = atol(argv[1]) + 1,
			s_y = atol(argv[2]) + 1,
			s_dir = atol(argv[3]),
			N_turn_lefts = atol(argv[5]);

		char * flat_map = argv[4];
		update_knowledge(flat_map);

		BotState init_state(s_x, s_y, s_dir);
		if (init_state.is_clear_left(false)) {
			printf("LF");
		}
		else if (init_state.is_clear_ahead(false)) {
			printf("F");
		}
		else printf("R");
	}
	else if (argc == 7) {
		int s_x = atol(argv[1]) + 1,
			s_y = atol(argv[2]) + 1,
			s_dir = atol(argv[3]),
			e_x = atol(argv[5]) + 1,
			e_y = atol(argv[6]) + 1;

		char * flat_map = argv[4];
		update_knowledge(flat_map);

		BotState init_state(s_x, s_y, s_dir);

		shared_ptr<list<Action>> actions = dijkstra(init_state, e_x, e_y, false);
		for (Action action : *actions) {
			switch (action) {
				case FORWARD:
					printf("F");
					break;
				case TURN_RIGHT:
					printf("R");
					break;
				case TURN_LEFT:
					printf("L");
					break;
			}
		}
		//puts("");

		//getchar();
		//simulate(2, 2, 0, actions);
	}

	return 0;
}
