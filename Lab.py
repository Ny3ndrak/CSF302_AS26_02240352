# Example matrices
A = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

B = [[9, 8, 7],
     [6, 5, 4],
     [3, 2, 1]]

n = len(A)

c = [[0 for j in range(n)] for i in range(n)]
for i in range(n):
    for j in range(n):
        c[i][j] = 0
        for k in range(n):
            c[i][j] += A[i][k] * B[k][j]

print("Result matrix C:")
for row in c:
    print(row)

 