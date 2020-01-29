

a = [2,5,1,3,8,9,6]

def sort(arr):
    for i in range(1,len(arr)):
        v = arr[i]
        c = i
        for j in range(i-1,-1,-1):
#            print('ij v',c,j,v)
            if (v < arr[j]):
                tmp = arr[j]
                arr[j] = v
                arr[c] = tmp
                c = j
                print('swapped arr:',arr,i,j,c)
                       
    return arr

print(a)
print(sort(a))
