import random
from Game import Game


class Node:
    def __init__(self, grid_hash, ppn, typ, depth):
        self.grid_hash = grid_hash
        self.ppn = ppn
        # 0 is OR, 1 is AND
        self.typ = typ
        self.parent_nodes = []
        self.child_nodes = []
        self.depth = depth

    def add_parent(self, p_node):
        self.parent_nodes.append(p_node)

    def add_child(self, c_node):
        self.child_nodes.append(c_node)


class PPNS:
    def __init__(self, end_target=2048, simulation_num=60, simulation_target=128, theta=0.0001):
        self.end_target = end_target
        self.simulation_num = simulation_num
        self.simulation_target = simulation_target
        self.theta = theta
        self.existed_node = {}
        self.depth_set = [(16, 18*2),  (32, 31*2), (64, 57*2), (128, 109*2), (256, 201*2), (512, 388*2), (1024, 716*2)]

    def is_expand(self, new_grid_hash, depth):
        max_num = int(pow(2, ord(max(new_grid_hash)) - ord('A')))
        for k in self.depth_set:
            if max_num == k[0] and depth > k[1]:
                return False
        return True

    @staticmethod
    def selection(node):
        mpn = None
        if node.typ == 0:
            max_ppn = -100
            for child in node.child_nodes:
                if child.ppn == 1 or child.ppn == 0:
                    continue
                if child.ppn > max_ppn:
                    mpn = child
                    max_ppn = child.ppn
        else:
            min_ppn = 100
            for child in node.child_nodes:
                if child.ppn == 1 or child.ppn == 0:
                    continue
                if child.ppn < min_ppn:
                    mpn = child
                    min_ppn = child.ppn
        return mpn

    def expansion(self, node):
        grid_hash = node.grid_hash
        if node.typ == 0:
            action_list = {0: Game.up, 1: Game.left, 2: Game.down, 3: Game.right}
            for i in range(4):
                new_grid_hash = action_list[i](grid_hash)[0]
                if new_grid_hash != grid_hash:
                    if not self.is_expand(new_grid_hash, node.depth):
                        continue
                    if (new_grid_hash, 1) in self.existed_node:
                        child = self.existed_node[(new_grid_hash, 1)]
                    else:
                        child = Node(new_grid_hash, -1, 1, node.depth+1)
                        self.play_out(child)
                        self.existed_node[(new_grid_hash, 1)] = child
                    child.add_parent(node)
                    node.add_child(child)
                    if child.ppn == 1:
                        return
        else:
            lst = [i for i in range(16) if grid_hash[i] == "A"]
            for x in lst:
                for new_num in ["B", "C"]:
                    new_grid = list(grid_hash)
                    new_grid[x] = new_num
                    new_grid_hash = "".join(new_grid)
                    if (new_grid_hash, 0) in self.existed_node:
                        child = self.existed_node[(new_grid_hash, 0)]
                    else:
                        child = Node(new_grid_hash, -1, 0, node.depth+1)
                        self.play_out(child)
                        self.existed_node[(new_grid_hash, 0)] = child
                    child.add_parent(node)
                    node.add_child(child)
                    if child.ppn == 0:
                        return

    def play_out(self, node):
        grid_hash = node.grid_hash
        max_num = int(pow(2, ord(max(grid_hash)) - ord('A')))
        if max_num >= self.end_target or Game.is_end(grid_hash) > 0:
            if max_num >= self.end_target:
                node.ppn = 1
            else:
                node.ppn = 0
        else:
            win = 0
            simulation_target = self.simulation_target
            while max_num >= simulation_target:
                simulation_target *= 2
            for i in range(self.simulation_num):
                new_grid_hash = grid_hash
                if node.typ == 1:
                    new_grid_hash = Game.random_act_pc(new_grid_hash)
                    max_num = int(pow(2, ord(max(new_grid_hash)) - ord('A')))
                while max_num < simulation_target and Game.is_end(new_grid_hash) == 0:
                    new_grid_hash = Game.random_act_player(new_grid_hash)
                    new_grid_hash = Game.random_act_pc(new_grid_hash)
                    max_num = int(pow(2, ord(max(new_grid_hash)) - ord('A')))
                if max_num >= simulation_target:
                    win += 1
            R = win / self.simulation_num
            if R == 1:
                R = R - self.theta
            elif R == 0:
                R = R + self.theta
            node.ppn = R

    @staticmethod
    def back_propagation(node):
        ppn = 1
        if node.typ == 0:
            for child in node.child_nodes:
                ppn *= 1 - child.ppn
            node.ppn = 1 - ppn
        else:
            for child in node.child_nodes:
                ppn *= child.ppn
            node.ppn = ppn

    def back(self, node):
        self.back_propagation(node)
        if not node.parent_nodes:
            return
        else:
            for p in node.parent_nodes:
                self.back(p)

    def search(self, initial_hash):
        root_node = Node(initial_hash, -1, 0, 0)
        self.existed_node[(initial_hash, 0)] = root_node
        self.expansion(root_node)
        self.back_propagation(root_node)
        while root_node.ppn != 0 and root_node.ppn != 1:
            # selection
            selected_node = self.selection(root_node)
            while selected_node.child_nodes:
                selected_node = self.selection(selected_node)
            # expansion
            self.expansion(selected_node)
            # back_propagation
            self.back(selected_node)
        print("========================================")
        print(root_node.ppn)
        print("========================================")
        return root_node.ppn


if __name__ == '__main__':
    ppns = PPNS(32, 60, 32, 0.001)
    ppns.search("BBAAAAAAAAAAAAAA")



