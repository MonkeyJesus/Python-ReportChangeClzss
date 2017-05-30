#coding=utf-8

str = '123 呵呵 ad'

print (str);
print (str[1]);
print (str[3]);
print (str.decode('utf-8')[4]);
print ('呵');
print (str.decode('utf-8')[4:5]);
print (str + '多收到');