import numpy as np
  
def reJ(jj):
	jj = np.triu(jj) + np.triu(jj, k=1).T
	return jj

def Ei(qq,jj):
	EE = 0
	for i in range(len(qq)):
		EE += qq[i]*jj[i][i]
		EE += sum(qq[i]*qq[i+1:]*jj[i][i+1:])
	return EE

def q2i(jjj):
	jj = jjj
	nn = len(jj)
	for i in range(nn):
		for j in range(i+1,nn):
			jj[i][j] *= 0.25

	jj = np.triu(jj)+np.triu(jj,k=1).T

	for i in range(nn):
		sum = 0
		for j in range(nn):
			if i == j:
				sum += jj[i][i]*0.5
			else:
				sum += jj[i][j]
		jj[i][i] = sum

	return np.triu(jj)

class anneal:
	def __init__(self):
		self.Ts = 5
		self.Tf = 0.02

		self.Gs = 10
		self.Gf = 0.02
		self.tro = 8

		self.R = 0.95
		self.ite = 1000
		self.qubo = [[4,-4,-4],[0,4,-4],[0,0,4]]
		self.J = [[0,-1,-1],[0,0,-1],[0,0,0]]

	def sa(self):
		T = self.Ts
		self.J = q2i(self.qubo)
		J = reJ(self.J)
		N = len(J)
		q = np.random.choice([-1,1],N)
		while T>self.Tf:
			for i in range(self.ite):
				x = np.random.randint(N)
				dE = 0

				for j in range(N):
					if j == x:
						dE += -2*q[x]*J[x][x]
					else:
						dE += -2*q[j]*q[x]*J[j][x]

				if dE < 0 or np.exp(-dE/T) > np.random.random_sample():
					q[x] *= -1
			T *= self.R
		return q

	def sqa(self):
		G = self.Gs
		self.J = q2i(self.qubo)
		J = reJ(self.J)
		N = len(J)
		q = [np.random.choice([-1,1],N) for j in range(self.tro)]
		for i in range(self.tro):
			q[i] = np.random.choice([-1,1],N)
		while G>self.Gf:
			for i in range(self.ite*self.tro):
				x = np.random.randint(N)
				y = np.random.randint(self.tro)
				dE = 0

				for j in range(N):
					if j == x:
						dE += -2*q[y][x]*J[x][x]
					else:
						dE += -2*q[y][j]*q[y][x]*J[j][x]

				dE += q[y][x]*(q[(self.tro+y-1)%self.tro][x]+q[(y+1)%self.tro][x])*np.log(1/np.tanh(G/self.Tf/self.tro))/self.Tf;

				if dE < 0 or np.exp(-dE/self.Tf) > np.random.random_sample():
					q[y][x] *= -1
			G *= self.R
		return q
