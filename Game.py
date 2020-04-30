import random
import os


class SimpleHash:
    alphabet_list = [chr(i) for i in range(65, 91)]
    num_list = [int(pow(2, i)) for i in range(26)]
    num_list[0] = 0
    hash_table = dict(zip(num_list, alphabet_list))
    hash_reverse_table = dict(zip(alphabet_list, num_list))

    @staticmethod
    def hash(grid):
        grid_hash = ""
        for x in range(4):
            for y in range(4):
                grid_hash += SimpleHash.hash_table[grid[x][y]]
        return grid_hash

    @staticmethod
    def reverse_hash(grid_hash):
        grid = []
        for i in range(4):
            line_i_hash = grid_hash[4*i: 4*i+4]
            line_i = []
            for j in range(4):
                line_i.append(SimpleHash.hash_reverse_table[line_i_hash[j]])
            grid.append(line_i)
        return grid


class Game:
    @staticmethod
    def random_act_pc(grid_hash):
        grid = list(grid_hash)
        lst = [i for i in range(16) if grid[i] == "A"]
        x = random.choice(lst)
        # Px(2)=0.8, Px(4)=0.2
        random_num = random.randint(1, 100)
        p = 80
        if random_num <= p:
            grid[x] = "B"
        else:
            grid[x] = "C"
        new_hash = "".join(grid)
        return new_hash

    @staticmethod
    def random_act_player(grid_hash):
        action_list = {0: Game.up, 1: Game.left, 2: Game.down, 3: Game.right}
        possible_grid = []
        for i in range(4):
            p_grid_hash = action_list[i](grid_hash)[0]
            if p_grid_hash != grid_hash:
                possible_grid.append(p_grid_hash)
        new_hash = random.choice(possible_grid)
        return new_hash

    @staticmethod
    def up(grid_hash):
        grid = SimpleHash.reverse_hash(grid_hash)
        add_score = 0
        col_list = []
        for k in range(4):
            col_k = [grid[0][k], grid[1][k], grid[2][k], grid[3][k]]
            col_list.append(col_k)
        for j in range(4):
            new_col = ([n for n in col_list[j] if n] + [0, 0, 0, 0])[:4]
            if new_col[0] and new_col[1] and new_col[0] == new_col[1]:
                add_score += new_col[0] + new_col[1]
                new_col[0] = new_col[0] + new_col[1]
                new_col[1] = 0
                new_col = ([n for n in new_col if n] + [0, 0, 0, 0])[:4]
            if new_col[1] and new_col[2] and new_col[1] == new_col[2]:
                add_score += new_col[1] + new_col[2]
                new_col[1] = new_col[1] + new_col[2]
                new_col[2] = 0
                new_col = ([n for n in new_col if n] + [0, 0, 0, 0])[:4]
            if new_col[2] and new_col[3] and new_col[2] == new_col[3]:
                add_score += new_col[2] + new_col[3]
                new_col[2] = new_col[2] + new_col[3]
                new_col[3] = 0
                new_col = ([n for n in new_col if n] + [0, 0, 0, 0])[:4]
            for i in range(4):
                grid[i][j] = new_col[i]
        new_hash = SimpleHash.hash(grid)
        return new_hash, add_score

    @staticmethod
    def down(grid_hash):
        grid = SimpleHash.reverse_hash(grid_hash)
        add_score = 0
        col_list = []
        for k in range(4):
            col_k = [grid[0][k], grid[1][k], grid[2][k], grid[3][k]]
            col_list.append(col_k)
        for j in range(4):
            new_col = ([0, 0, 0, 0] + [n for n in col_list[j] if n])[-4:]
            if new_col[-1] and new_col[-2] and new_col[-1] == new_col[-2]:
                add_score += new_col[-1] + new_col[-2]
                new_col[-1] = new_col[-1] + new_col[-2]
                new_col[-2] = 0
                new_col = ([0, 0, 0, 0] + [n for n in new_col if n])[-4:]
            if new_col[-2] and new_col[-2] and new_col[-2] == new_col[-3]:
                add_score += new_col[-2] + new_col[-3]
                new_col[-2] = new_col[-2] + new_col[-3]
                new_col[-3] = 0
                new_col = ([0, 0, 0, 0] + [n for n in new_col if n])[-4:]
            if new_col[-3] and new_col[-4] and new_col[-3] == new_col[-4]:
                add_score += new_col[-3] + new_col[-4]
                new_col[-3] = new_col[-3] + new_col[-4]
                new_col[-4] = 0
                new_col = ([0, 0, 0, 0] + [n for n in new_col if n])[-4:]
            for i in range(4):
                grid[i][j] = new_col[i]
        new_hash = SimpleHash.hash(grid)
        return new_hash, add_score

    @staticmethod
    def left(grid_hash):
        grid = SimpleHash.reverse_hash(grid_hash)
        add_score = 0
        new_grid = []
        for row in grid:
            new_row = ([n for n in row if n] + [0, 0, 0, 0])[:4]
            if new_row[0] and new_row[1] and new_row[0] == new_row[1]:
                add_score += new_row[0] + new_row[1]
                new_row[0] = new_row[0] + new_row[1]
                new_row[1] = 0
                new_row = ([n for n in new_row if n] + [0, 0, 0, 0])[:4]
            if new_row[1] and new_row[2] and new_row[1] == new_row[2]:
                add_score += new_row[1] + new_row[2]
                new_row[1] = new_row[1] + new_row[2]
                new_row[2] = 0
                new_row = ([n for n in new_row if n] + [0, 0, 0, 0])[:4]
            if new_row[2] and new_row[3] and new_row[2] == new_row[3]:
                add_score += new_row[2] + new_row[3]
                new_row[2] = new_row[2] + new_row[3]
                new_row[3] = 0
                new_row = ([n for n in new_row if n] + [0, 0, 0, 0])[:4]
            new_grid.append(new_row)
        new_hash = SimpleHash.hash(new_grid)
        return new_hash, add_score

    @staticmethod
    def right(grid_hash):
        grid = SimpleHash.reverse_hash(grid_hash)
        add_score = 0
        new_grid = []
        for row in grid:
            new_row = ([0, 0, 0, 0] + [n for n in row if n])[-4:]
            if new_row[-1] and new_row[-2] and new_row[-1] == new_row[-2]:
                add_score += new_row[-1] + new_row[-2]
                new_row[-1] = new_row[-1] + new_row[-2]
                new_row[-2] = 0
                new_row = ([0, 0, 0, 0] + [n for n in new_row if n])[-4:]
            if new_row[-2] and new_row[-3] and new_row[-2] == new_row[-3]:
                add_score += new_row[-2] + new_row[-3]
                new_row[-2] = new_row[-2] + new_row[-3]
                new_row[-3] = 0
                new_row = ([0, 0, 0, 0] + [n for n in new_row if n])[-4:]
            if new_row[-3] and new_row[-4] and new_row[-3] == new_row[-4]:
                add_score += new_row[-3] + new_row[-4]
                new_row[-3] = new_row[-3] + new_row[-4]
                new_row[-4] = 0
                new_row = ([0, 0, 0, 0] + [n for n in new_row if n])[-4:]
            new_grid.append(new_row)
        new_hash = SimpleHash.hash(new_grid)
        return new_hash, add_score

    @staticmethod
    def is_end(grid_hash):
        if "A" in grid_hash:
            return 0
        else:
            for i in range(4):
                row = grid_hash[i*4:i*4+4]
                if row[0] == row[1] or row[1] == row[2] or row[2] == row[3]:
                    return 0
            for j in range(4):
                col = grid_hash[j] + grid_hash[j+4] + grid_hash[j+8] + grid_hash[j+12]
                if col[0] == col[1] or col[1] == col[2] or col[2] == col[3]:
                    return 0
            max_value = int(pow(2, ord(max(grid_hash)) - ord('A')))
            return max_value


if __name__ == '__main__':
    pass
