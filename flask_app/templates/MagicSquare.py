# def formingMagicSquare(s):
#     for key in matrix.keys():
#         matrix[key].sum = sum(matrix[key])
#     print(matrix)
    

def formMagicSquare(s):
    r1, r2, r3 = s[0], s[1], s[2]
    c1, c2, c3 = [r1[0], r2[0], r3[0]], [r1[1], r2[1], r3[1]], [r1[2], r2[2], r3[2]]
    matrix = locals()
    del matrix['s']
    class MagicRow:
        def __init__(self, name, sequence):
            self.name = name
            self.sequence = sequence
            self.sum = sum(sequence)
            self.good = False
    class MagicSquare:
        def __init__(self, data):
            self.r1 = data[0]
            self.r2 = data[1]
            self.r3 = data[2]
            self.c1 = data[3]
            self.c2 = data[4]
            self.c3 = data[5]
    data = []
    badrows = {}
    for key in matrix.keys():
        key = MagicRow(key, matrix[key])
        if key.sum == 15:
            key.good == True
        else:
            badrows[key.name] = key.sequence
        data.append(key)
    square = MagicSquare(data)

# calculate the difference between the square given and every possible solution
def calc_diff(a,b):
    diff = 0
    # for every row
    for row in range(3):
        #  for every column of every row
        for col in range(3):
            diff += abs(a[row][col]-b[row][col])
    return diff

def formingMagicSquare(s):
    # store every possible solution in a variable
    magicSquares = [
        [[4,3,8],[9,5,1],[2,7,6]],
        [[2,9,4],[7,5,3],[6,1,8]],
        [[6,7,2],[1,5,9],[8,3,4]],
        [[8,1,6],[3,5,7],[4,9,2]],
        [[8,3,4],[1,5,9],[6,7,2]],
        [[4,9,2],[3,5,7],[8,1,6]],
        [[2,7,6],[9,5,1],[4,3,8]],
        [[6,1,8],[7,5,3],[2,9,4]]
        ]
    # set the diff between the first solution as the minimum
    min_diff = calc_diff(s,magicSquares[0])
    # iterate over the rest of the list and update the minimum as needed
    for x in range(1,len(magicSquares)):
        current_diff = calc_diff(s,magicSquares[x])
        if(current_diff < min_diff):
            min_diff = current_diff
    return min_diff

print(formingMagicSquare([[4, 9, 2],
[3, 5, 7],
[8, 1, 5]]))


