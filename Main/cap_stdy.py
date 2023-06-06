import numpy as np
from scipy.sparse import lil_array, csr_array
from scipy.sparse.linalg import spsolve
from math import ceil, sqrt
from Main import MyLabel2

#Function definiton (uber function is at the bottom)
#Geometry init
def init_l(dx, width, geo): 
    l_water = 0.6089 #from wiki
    #Initialize the geometry array of l(i, j)
    #calculate total system height
    height = sum([sublist[0] for sublist in geo])
    l = np.zeros((int(height/dx), int(width/dx)))
    
    #Fill the geometry array
    lower_bound = 0
    for i in geo:
        l_height = int(i[0]/dx)
        l[lower_bound:(lower_bound+l_height)] = i[1]

        #Fill in capillary
        if len(i) == 3:
            cap_info = i[2]

            #Extract cap info and set vars
            r1 = cap_info[0]/dx
            r2 = cap_info[1]/dx
            cap_low = int(lower_bound + cap_info[2]/dx)
            cap_high = int(cap_low+2*r2)
            center = cap_low  + r2

            for ly in range(cap_low, cap_high+1):
                for lx in range(0, ceil(2*r2)+1):
                    dist = sqrt((ly-center)**2+lx**2)
                    
                    #Fudge coefficent, helps to fill all elements
                    eps = 0.2

                    #Set lambda in the Water zone
                    if dist <= r1:
                        l[ly,lx]= l_water

                    #Set capilar lambda
                    elif r1-eps < dist < r2+eps:
                        l[ly,lx] = cap_info[-1]

                    #Could turn this into closest elements for completeness

        lower_bound += l_height
    #Make water mask
    water_mask = l == l_water

    
    return l, water_mask
#l is the geometry
#water_mask is true only in the water region


###Linear system of eqs
def init_Ab(l, t_top, t_water, water_mask, q, dx):
    # Define the grid parameters
    ny, nx = l.shape

    # Create the coefficient matrix A and b vector
    A = lil_array((nx*ny, nx*ny))
    b = np.zeros((nx*ny))

    #Constants in b
    #top
    b[(len(b)-nx):] = t_top

    #water
    b[water_mask.flatten()] = t_water

    #bottom boundary
    b[:nx] = -(0.1/1000)*q/l[0,0] #h*q/lambda

    #A operator
    #Loop over A and fill in elements

    #Set coefficents for medium, but not for boundarys
    for i in range(1,ny-1):
        for j in range(1,nx-1):
            k = i*nx+j

            if not water_mask[i,j]:
                ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
                im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
                jp = 2/(1/l[i,j+1]+1/l[i,j]) #i,j+1
                jm = 2/(1/l[i,j-1]+1/l[i,j]) #i,j-1
                diagonal = -(ip+im+jp+jm)

                A[k,k] = diagonal
                A[k,k+nx] = ip
                A[k,k-nx] = im
                A[k,k+1] = jp
                A[k,k-1] = jm

            #constant for water
            else:
                A[k,k]=1 #this mises first elements of each row of water_mask

    #sides is 3 element average with k corrected coefficents
    for i in range(1,ny-1):
        #left
        if not water_mask[i,0]:

                k = i*nx
                ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
                im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
                jp = 2/(1/l[i,j+1]+1/l[i,j]) #i,j+1
                diagonal = -(ip+im+jp)

                A[k,k] = diagonal
                A[k,k+nx] = ip
                A[k,k-nx] = im
                A[k,k+1] = jp

        else:
            k = i*nx
            A[k,k] = 1 #water mask first element fix

        #right
        k = i*nx+nx-1
        ip = 2/(1/l[i+1,j]+1/l[i,j]) #i+1,j
        im = 2/(1/l[i-1,j]+1/l[i,j]) #i-1,j
        jm = 2/(1/l[i,j-1]+1/l[i,j]) #i,j-1
        diagonal = -(ip+im+jm)

        A[k,k] = diagonal
        A[k,k+nx] = ip
        A[k,k-nx] = im
        A[k,k-1] = jm

    #bottom is the derivative
    for j in range(0,nx):
        k = j
        A[k,k] = 1
        A[k,k+nx] = -1

        #top is constant
        k = (ny-1)*nx+j
        A[k,k] = 1

    A = A.tocsr()
    
    return A,b

#can be made much faster via matrix operations and scipy.sparse.diags


#Itterative temp fitter
def t_fit(self, A, b, l, t_to_fit, t_error, maxiter, water_mask):
    t = t_to_fit
    ny, nx = l.shape
    
    iteration = 0
    diff = 1
    b[water_mask.flatten()] = t_to_fit
    
    while abs(diff)>t_error and iteration < maxiter:
        
        # Solve the linear system
        T = spsolve(A, b)

        # Reshape the solution vector into a 2D array
        T = T.reshape((ny, nx))

        bot_t = T[1].mean()

        diff = t_to_fit - bot_t

        iteration+=1
        t += diff
        b[water_mask.flatten()] = t

    return T, t;


#Uber black box
def fit_water_t(self, geo, width, t_to_fit, q, t_top):
    try:
        dx = 0.1

        #init geometry
        l, water_mask = init_l(dx, width, geo)
    
        #init eq. system
        A, b = init_Ab(l, t_top, t_to_fit, water_mask, q, dx)
    
        print("init done")
     
        #fit t
        t_error = 0.001
        maxiter = 10

        T,t = t_fit(self, A, b, l, t_to_fit, t_error, maxiter, water_mask)
        return t
    except TypeError:
        return()