def lingyang():
  '''宠物领养程序'''
  import random
  print('欢迎光临宠物店！')
  i=input('你想要领养一只宠物吗？输入‘y’（yes）或‘n’(no)：')
  name=''
  while 1:
    if i!='y':
        input('谢谢光临，再见！')
        break
    else:
        r=random.randint(1,100)
        if r<=80:
            name=random.choice(['小狗','小猫','小兔子','小猴子','鹦鹉','小鸡','小猪','小羊','小麻雀','小蚂蚁','小蜘蛛','小蝴蝶'])
            print('恭喜你领养了一只普通宠物：',name)
        elif r>=82:
            name=random.choice(['汉克狗','加菲猫','小樱兔','咕咕鸡','美羊羊','灰太狼','熊大','熊二','皮卡丘','小花'])
            print('恭喜你领养了一只稀有宠物：',name)
        else:
            name=random.choice(['火凤凰','哆啦A梦','精灵龙','孙悟空','提米','toby'])
            print('恭喜你领养了一只绝世神宠：',name)
        i=input('是否重新领养？输入‘y’(yes)或‘n’(no)：')



  print('你高高兴兴地带着你的宠物',name,'回家了！')
