import numpy as np 
import sympy as sp

from PixelMethods import OriginalPixels

def AdvMAME2x(image, index):
	A, C, pixel, B, D = [i[0] if i is not None else None 
		for i in OriginalPixels(image, allpixels=False, index=index)]

	p1 = A if C == A and C != D and A != B and A and C else pixel
	p2 = B if A == B and A != C and B != D and A and B else pixel
	p3 = C if D == C and D != B and C != A and C and D else pixel
	p4 = D if B == D and B != A and D != C and B and D else pixel

	return (p1,p2,p3,p4)

def FDM(image, index):
	A, C, pixel, B, D = [i[0] if i is not None else None 
		for i in OriginalPixels(image, allpixels=False, index=index)]

	A = A if A is not None else pixel
	B = B if B is not None else pixel
	C = C if C is not None else pixel
	D = D if D is not None else pixel

	p1, p2, p3, p4 = [], [], [], []

	for i in range(3):
		p1.append((A[i] + C[i] + 2*pixel[i]) / 4)
		p2.append((A[i] + B[i] + 2*pixel[i]) / 4)
		p3.append((D[i] + C[i] + 2*pixel[i]) / 4)
		p4.append((D[i] + B[i] + 2*pixel[i]) / 4)

	return (p1, p2, p3, p4)

def FEM(image, index):
	p1, p2, p3, p4, pixel, p6, p7, p8, p9 = [i[0] if i is not None else None 
		for i in OriginalPixels(image, index=index)]

	U2 = p2 if p2 else pixel
	U5 = p4 if p4 else pixel
	U8 = p6 if p6 else pixel
	U14 = p8 if p8 else pixel
	U3, U9, U12, U15 = U2, U5, U8, U14

	U1 = p1 if p1 else [(i+j)/2 for i,j in zip(U2,U5)]
	U4 = p3 if p3 else [(i+j)/2 for i,j in zip(U3,U8)]
	U13 = p7 if p7 else [(i+j)/2 for i,j in zip(U9,U14)]
	U16 = p9 if p9 else [(i+j)/2 for i,j in zip(U12,U15)]

	boundary_pixels = (U1, U2, U3, U4, U5, U8, U9, U12, U13, U14, U15, U16)

	red = [i[0] for i in boundary_pixels]
	green = [i[1] for i in boundary_pixels]
	blue = [i[2] for i in boundary_pixels]

	result_pixel = [(i,j,k) for i,j,k in zip(FEM_1color(red), 
		FEM_1color(green), FEM_1color(blue))]
	return result_pixel

def FEM_1color(boundary_conditions):
	m, n = 4, 4
	nds = m*n
	elmnts = 2*(n-1)*(m-1)

	U = {}

	def key(i,j,k=str()):
		return f'{i}|{j}|{k}'
	
	Nodes = {}
	for i in range(1, nds+1):
		x = (i-1) % n
		y = m - 1 - (i-1)//n
		Nodes[i] = (x, y)

	count = (i for i in range(1,n*(m-1)) if i%n)
	Elements = {}
	num = 0
	for i in count:
		num += 1
		Elements[num] = sorted([i, i+n, i+n+1])
		num += 1
		Elements[num] = sorted([i, i+1, i+1+n], reverse=True)

	def N(i,j,k):
		x, y = sp.var('x'), sp.var('y')
		alpha = Nodes[j][0]*Nodes[k][1] - Nodes[k][0]*Nodes[j][1]
		beta = Nodes[j][1] - Nodes[k][1]
		gamma = Nodes[k][0] - Nodes[j][0]
		return alpha + beta*x + gamma*y

	N_ei = {}
	for e in range(1, elmnts+1):
		i = Elements[e]
		N_ei[key(e,i[0])] = N(i[0], i[1], i[2])
		N_ei[key(e,i[1])] = N(i[1], i[2], i[0])
		N_ei[key(e,i[2])] = N(i[2], i[0], i[1])


	def K(e,l,m):
		x, y = sp.var('x'), sp.var('y')
		if key(e,m,l) in K_elm:
			return K_elm[key(e,m,l)]
		else:
			deposit = sp.diff(N_ei[key(e,l)],x)*sp.diff(N_ei[key(e,m)],x)
			deposit += sp.diff(N_ei[key(e,l)],y)*sp.diff(N_ei[key(e,m)],y)
			return deposit

	K_elm = {}
	for e in range(1, elmnts+1):
		for l in Elements[e]:
			for s in Elements[e]:
				K_elm[key(e,l,s)] = K(e,l,s)

	GlobalMatrix = {}
	for i in range(1, nds+1):
		for j in range(1, nds+1):
			for k in K_elm:
				if k.split('|')[1:] == [str(i), str(j)]:
					if key(i,j) not in GlobalMatrix:
						GlobalMatrix[key(i,j)] = K_elm[k]
					else:
						GlobalMatrix[key(i,j)] += K_elm[k]

	unknown_vars = [i for i in range(1, nds+1) if 0 not in Nodes[i] 
		and Nodes[i][0]!=n-1 and Nodes[i][1]!=m-1]

	U.update({i : j for i,j in zip(set(range(1,nds+1))-set(unknown_vars), 
		boundary_conditions)})

	A = []
	for i in unknown_vars:
		A.append([])
		for j in unknown_vars:
			A[-1].append(GlobalMatrix[key(i,j)] if key(i,j) in GlobalMatrix else 0)

	b = []
	for i in unknown_vars:
		var = 0
		for k in GlobalMatrix:
			if int(k.split('|')[1]) == i:
				if int(k.split('|')[0]) not in unknown_vars:
					var += -GlobalMatrix[k]*U[int(k.split('|')[0])]
		b.append(var)

	result = np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float))
	
	#U.update({i : j for i,j in zip(unknown_vars,result)})

	return result
