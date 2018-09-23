import scipy

# the parameters

points=500
grid_start = -5.0
grid_stop = 5.0
mass = 1.0

d = (grid_stop-grid_start)/(points-1)
grid = scipy.arange(grid_start, grid_stop+d, d)
print len(grid), points

f = lambda x: x**2
potential = scipy.array(map(f,grid))
plot (grid, potential)

H = scipy.zeros([points-2, points-2])
diagonal_prevalue = 1.0/(mass*d*d)
off_diagonal_value = -1.0/(2*mass*d*d)

for i in xrange(1,points-3):
    H[i,i-1] = off_diagonal_value
    H[i,i] = diagonal_prevalue + potential[i+1]
    H[i,i+1] = off_diagonal_value

H[0,0] = diagonal_prevalue + potential[1]
H[0,1] = off_diagonal_value
H[points-3,points-3] = diagonal_prevalue + potential[points-2]
H[points-3,points-4] = off_diagonal_value
print H

eigenvalues,eigenvectors = eig(H)

for i in xrange(1,10):
    plot(grid[1:points-1],transpose(eigenvectors)[i]+eigenvalues[i])
