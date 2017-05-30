#coding=utf-8

for letter in 'abcdefg':
    print letter
    if letter == 'd':
        print 'break 了'
        break




def printMe( a):
    if a == 'aa':
        print '输入了 aa'
    else:
        print '没有输入 aa';


printMe( 'bb' );


fo = open("C:/Users/MacheNike/Desktop/aaaa.txt", "wb")
print "文件名: ", fo.name
print "是否已关闭 : ", fo.closed
print "访问模式 : ", fo.mode
print "末尾是否强制加空格 : ", fo.softspace
fo.write('IOTest')
fo.close();
