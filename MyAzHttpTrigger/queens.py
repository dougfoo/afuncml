def isValid(row,pos):
    if pos>=N or row>=N: return False
    if pos in sol: return False
    for i in range(len(sol)):
        if pos == sol[i]+row-i or pos == sol[i]-(row-i):
            return False
    return True

def solve(pos,Qc):
    Qc-=1
    sol.append(pos) 
    if Qc==0: return True 
    #Try
    for i in range(N):
        if(isValid(N-Qc,i)):
           if(solve(i,Qc)): return True
    sol.pop()
    Qc+=1
    return False

Queens = int(input().strip())
N=Queens
sol=[]
for i in range(Queens):
    if(solve(i,N)):
        print(sol)
    sol=[]