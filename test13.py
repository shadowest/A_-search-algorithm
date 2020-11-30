# 去掉比较的启发式搜索
import numpy as np


map = [
    '############################################################',
    '#S............................#............#.....#.........#',
    '#..........#..................#......#.....#.....#.........#',
    '#..........#..................#......#.....#.....#.........#',
    '#..........#..................#......#.....#.....#.........#',
    '#..........#.........................#.....#.....#.........#',
    '#..........#..................#......#.....#...............#',
    '#..#########..................#......#.....#.....#.........#',
    '#..#..........................#......#.....#.....#.........#',
    '#..#..........................#......#.....#.....#.........#',
    '#..############################......#.....#.....#.........#',
    '#.............................#......#.....#.....#.........#',
    '#.............................#......#...........#.........#',
    '#######.##################################################.#',
    '#....#........#.................#.............#............#',
    '#....#........#........#........#.............#............#',
    '#....####.#####........#........#.............#............#',
    '#.........#............#........#.............#............#',
    '#.........#............#........#.............#............#',
    '#.........#............#........#.............#............#',
    '#.........#............#........#.............#............#',
    '#.........#............#........#.............#............#',
    '#.........#............#........####.#######.##............#',
    '#.........#............#........#....#.......#.............#',
    '#.........#............#........#....#.......#.............#',
    '#......................#........#....#.......#.............#',
    '#.........#............#........##.########..#.............#',
    '#.........#............#..................#..########.######',
    '#.........#............#..................#...............E#',
    '############################################################']


def get_Man_dis(node1, node2):      # 获得node2和node1之间的曼哈顿距离
    Man_dis = (node2[0] - node1[0]) + (node2[1] - node1[1])
    return Man_dis


def get_fn(node):       # 获得点node的启发性函数值f(n)
    global maze_gn, des_loc
    return get_Man_dis(node, des_loc) + maze_gn[node[0]][node[1]]


def get_avi_node(node):         # 查询某节点上下左右四个点，若可以走，则加入 avi_node 列表
    global maze
    avi_node = []
    if (maze[node[0] - 1][node[1]] == 1) or (maze[node[0] - 1][node[1]] == 9):
        avi_node.append((node[0] - 1, node[1]))
    if (maze[node[0]][node[1] - 1] == 1) or (maze[node[0]][node[1] - 1] == 9):
        avi_node.append((node[0], node[1] - 1))
    if (maze[node[0] + 1][node[1]] == 1) or (maze[node[0] + 1][node[1]] == 9):
        avi_node.append((node[0] + 1, node[1]))
    if (maze[node[0]][node[1] + 1] == 1) or (maze[node[0]][node[1] + 1] == 9):
        avi_node.append((node[0], node[1] + 1))
    return avi_node


if __name__ == '__main__':
    maze_line = list()
    start_loc = []      # 起点坐标
    des_loc = []        # 终点坐标

    for i in range(len(map)):       # 处理输入
        x = list()
        for j in range(len(map[i])):
            if map[i][j] == '#':
                x.append(0)
            elif map[i][j] == '.':
                x.append(1)
            elif map[i][j] == 'S':
                x.append(6)
                start_loc = (i, j)
            elif map[i][j] == 'E':
                x.append(9)
                des_loc = (i, j)
        maze_line.append(x)
    maze = np.array(maze_line)  # 将迷宫转化为numpy矩阵，0为墙，1可以走，6是起点，9是终点

    shape = maze.shape
    maze_gn = np.zeros((shape[0], shape[1]), dtype=np.int)
    list_from = []

    for i in range(shape[0]):
        list_from_line = []
        for j in range(shape[1]):
            list_from_line.append(0)
        list_from.append(list_from_line)

    road_open = [start_loc]
    road_close = []
    flag = 1

    while road_open[len(road_open) - 1] != des_loc:
        now_loc = road_open.pop()
        road_close.append(now_loc)
        all_avi_node = get_avi_node(now_loc)
        all_avi_node_copy = all_avi_node.copy()
        for x in all_avi_node_copy:
            if x in road_close:
                all_avi_node.remove(x)
        for x in all_avi_node:                              # 去掉比较后
            gn = maze_gn[now_loc[0]][now_loc[1]] + 1
            if x not in road_open:
                maze_gn[x[0]][x[1]] = gn
                road_open.append(x)
                list_from[x[0]][x[1]] = now_loc
        road_open.sort(key=get_fn, reverse=True)
        if len(road_open) == 0:
            flag = 0
            print("FAIL")
            break

    if flag == 1:
        road_list = []
        road_now = des_loc
        while road_now != start_loc:
            road_list.append(road_now)
            road_now = list_from[road_now[0]][road_now[1]]
        road_list.remove(des_loc)

        for i in range(shape[0]):
            for j in range(shape[1]):
                if maze[i][j] == 0:
                    print('#', end='')
                elif maze[i][j] == 6:
                    print('S', end='')
                elif maze[i][j] == 9:
                    print('E', end='')
                else:
                    if (i, j) in road_list:
                        print('*', end='')
                    elif (i, j) in road_close:
                        print('.', end='')
                    else:
                        print(' ', end='')
            print('\n')
