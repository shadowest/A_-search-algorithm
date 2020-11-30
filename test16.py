# 启发式搜索 fn+gn 有时间版本
import numpy as np
import time


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

    for i in range(len(map)):       # 处理输入，将map转化为numpy矩阵
        x = list()
        for j in range(len(map[i])):
            if map[i][j] == '#':    # 墙设为0
                x.append(0)
            elif map[i][j] == '.':  # 可以走的点设为1
                x.append(1)
            elif map[i][j] == 'S':  # 起点设为6
                x.append(6)
                start_loc = (i, j)  # 设置起点坐标
            elif map[i][j] == 'E':  # 终点设为9
                x.append(9)
                des_loc = (i, j)    # 设置终点坐标
        maze_line.append(x)
    maze = np.array(maze_line)      # 将迷宫转化为numpy矩阵，0为墙，1可以走，6是起点，9是终点

    shape = maze.shape
    maze_gn = np.zeros((shape[0], shape[1]), dtype=np.int)      # 初始化存储每个点g(n)值的矩阵
    list_from = []      # 记录每个节点父节点的坐标的矩阵list_from

    for i in range(shape[0]):   # 初始化list_from矩阵
        list_from_line = []
        for j in range(shape[1]):
            list_from_line.append(0)
        list_from.append(list_from_line)

    road_open = [start_loc]     # open表
    road_close = []             # close表
    flag = 1                    # flag为1则表示成功找到最优路径，若为0则表示不存在最优路径

    start = time.time()
    # A*算法
    while road_open[len(road_open) - 1] != des_loc:         # 若open表中fn最小的节点为终点，则搜索结束
        now_loc = road_open.pop()
        road_close.append(now_loc)
        all_avi_node = get_avi_node(now_loc)                # 获得某个点周围四个方向可以走的方向的坐标
        all_avi_node_copy = all_avi_node.copy()
        for x in all_avi_node_copy:                         # 若已在close表中，则删除
            if x in road_close:
                all_avi_node.remove(x)
        for x in all_avi_node:
            gn = maze_gn[now_loc[0]][now_loc[1]] + 1
            if x in road_open:
                if gn < maze_gn[x[0]][x[1]]:                # 若在open表里面但fn更小，则进行更新
                    maze_gn[x[0]][x[1]] = gn
                    list_from[x[0]][x[1]] = now_loc
            else:                                           # 若不在open表里面，则加进去
                maze_gn[x[0]][x[1]] = gn
                road_open.append(x)
                list_from[x[0]][x[1]] = now_loc
        road_open.sort(key=get_fn, reverse=True)            # 对open表进行排序，排序函数为get_fn即fn值，排序规则为降序
        if len(road_open) == 0:                             # 若搜索过程中出现open表为空的情况，则搜索失败
            flag = 0
            print("FAIL")
            break
    end = time.time()
    print("搜索时间为：", end - start, "s")

    if flag == 1:                                           # 若搜索成功，则进行输出
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
