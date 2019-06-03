import random
k=['石头','剪刀','布']
i=int(input('你的宠物要和你玩猜拳游戏，你要出的手势是（1.石头，2.剪刀，3.布）：'))   
while 1:    
    print('你出的是:',k[i-1])
    j=random.randint(1,3)
    print('你的宠物出的是:',k[j-1])
    if i==j:
        print('平局！')
    elif (i==1 and j==2)or(i==2 and j==3)or(i==3 and j==1):
        print("你赢了！")
    elif (i==2 and j==1)or(i==3 and j==2)or(i==1 and j==3):
        print('你输了！')
    i=int(input('继续玩吗？（1.石头，2.剪刀，3.布，0.不玩了）:'))
    if i!=1 and i!=2 and i!=3:
        input('你的宠物睡觉去了，再见！')
        break
    
