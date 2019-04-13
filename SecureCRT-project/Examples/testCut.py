s = '12345678'
maxx = 5
l = len(s)
loop = (l//maxx)
if(l%maxx!=0):
    loop=loop+1
print(loop)
head=0
tail=0
for i in range(loop):
    head=tail
    tail=(i+1)*maxx
    print(str(i)+":"+str(head)+str(tail)+": "+s[head:tail])
