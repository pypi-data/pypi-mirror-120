#to conver given string is uppercase
def lowercase(string):
    b=""
    ls=[]
    st=''
    for i in string:
        #print(i)
        if ord(i)>=97 and ord(i)<=122:
            ls.append(i)
        elif ord(i)>=65 and ord(i)<=90: #caps
            temp=ord(i)+32
            ls.append(chr(temp))
        else:
            ls.append(i)
    for i in ls:
        st=st+str(i)
    return st

#to conver given string is lowercase
def uppercase(string):
    b=""
    ls=[]
    st=''
    for i in string:
        #print(i)
        if ord(i)>=97 and ord(i)<=122:
            temp=ord(i)-32
            ls.append(chr(temp))
        elif ord(i)>=65 and ord(i)<=90: #caps
            ls.append(i)
        else:
            ls.append(i)
    for i in ls:
        st=st+str(i)
    return st

#capitalize
def capitalize(string):
    ls=''
    temp=string[0].upper()
    ls=ls+temp
    for i in range(1,len(string)):
        ls=ls+string[i]
    return ls

#length
def length(string):
    cnt=0
    for i in string:
        cnt=cnt+1
    return cnt

#given string digit or not
def digit(string):
    cnt=0
    for i in string:
        if ord(i)>48 and ord(i)<57:
            cnt=cnt+1
    if cnt==len(string):
        return True
    else:
        return False

#minimum character in given string
def min(string):
    cnt=[]
    for i in string.strip():
        temp=int(ord(i))
        cnt.append(temp)
    cnt.sort()
    return chr(cnt[0])

#maximum character in given string
def max(string):
    cnt=[]
    for i in string.strip():
        temp=int(ord(i))
        cnt.append(temp)
    cnt.sort()
    return chr(cnt[len(string)-1])


#replace the given word in the string
def replace(string,original_word,replace_word):
    ls=string.split()
    temp=''
    for i in range(0,len(ls)):
        if ls[i]==original_word:
            ls[i]=replace_word
    for i in range(0,len(ls)):
        temp=temp+ls[i]
        temp=temp+" "
    return temp

#encode string
def encodeing(string):
    ls=[]
    for i in string:
        if ord(i)>=65 and ord(i)<=87:
            ls.append(chr(ord(i)+3))
        elif ord(i)>=97 and ord(i)<=119:
            ls.append(chr(ord(i)+3))
        else:
            if ord(i)==88:
                ls.append(chr(65))
            elif ord(i)==89:
                ls.append(chr(66))
            elif ord(i)==90:
                ls.append(chr(67))
            elif ord(i)==120:
                ls.append(chr(97))
            elif ord(i)==121:
                ls.append(chr(98))
            elif ord(i)==122:
                ls.append(chr(99))
    string1=''
    for i in ls:
        string1=string1+i
    return string1


#decode string
def decoding(string):
    ls=[]
    for i in string:
        if ord(i)>=69 and ord(i)<=90:
            ls.append(chr(ord(i)-3))
        elif ord(i)>=100 and ord(i)<=122:
            ls.append(chr(ord(i)-3))
        else:
            if ord(i)==65:
                ls.append(chr(88))
            elif ord(i)==66:
                ls.append(chr(89))
            elif ord(i)==67:
                ls.append(chr(90))
            elif ord(i)==97:
                ls.append(chr(120))
            elif ord(i)==98:
                ls.append(chr(121))
            elif ord(i)==99:
                ls.append(chr(122))
    string1=''
    for i in ls:
        string1=string1+i
    return string1

#split
def split(string):
    strtemp = ''
    string.strip()
    string=string+" "
    ls=[]
    for i in string:
        #print(i)
        if i!=' ':
            strtemp = strtemp+i
        else:
            ls.append(strtemp)
            strtemp=''
    return ls
#manual
def help():
    print('1.lowercase')
    print('2.uppercase')
    print('3.capitalize')
    print('4.length')
    print('5.digit')
    print('6.min')
    print('7.max')
    print('8.replace')
    print('9.encodeing')
    print('10.decoding')
    print('11.split')
    print('12.help')
    #trj08012002@gmail.com
