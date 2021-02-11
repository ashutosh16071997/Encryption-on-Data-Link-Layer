
import sys
import numpy as np
import pickle
import socket
from crccheck.crc import Crc32, CrcXmodem
A = np.array([ [-3, -3, -4],
    [0, 1, 1],
    [4, 3, 4]
])
A_inverse = np.array([[1, 0, 1],
    [4, 4, 3],
    [-4, -3, -3]])

"""    
def xor(val1,val2):
    result1 = []
    i = 1
    while i < len(val2):
        if val1[i] == val2[i]: 
            result1.append('0') 
        else: 
            result1.append('1') 
        i = i+1
    return ''.join(result1)     

def division(addingdata,key):
    key = str(key)
    pickdata = len(key) 
    tmp = addingdata[0:pickdata] 
   
    while(pickdata < len(addingdata)): 
   
        if tmp[0] == '1': 
            tmp = xor(key, tmp) + addingdata[pickdata] 
   
        else:
            tmp = xor('0'*pickdata, tmp) + addingdata[pickdata] 
        pickdata = pickdata+1
    if tmp[0] == '1': 
        tmp = xor(key, tmp) 
    else: 
        tmp = xor('0'*pickdata, tmp) 
   
    result = tmp 
    return result 



def CRC(data):
    key = 1101
    length = len(data)
    data = str(data)
    addingdata = ""
    addingdata = data + '0'*(length-1)
    print(type(addingdata))
    remainder = division(addingdata,key)
    return remainder
"""

def encodedata(data,A):
    list1 = []
    data1 = []
    while len(data) % 3 != 0:
        data += ' '
    for values in (data):
        if values == " ":
            list1.append(27)
        else :
            #print(values)
            for tot in range(0,len(values)):
              tal = ord(values[tot])-65+1 
              list1.append(tal)   
    arr1 = np.array(list1)
    arr2 = np.reshape(arr1, (3, len(data)//3), 'F')
    val = np.dot(A,arr2)
    return val 
def main():
    while(True):
        data = input()
        #print(data)
        data = str(data)
        encryptedmessage = encodedata(data,A)
        #print(encryptedmessage)
        
        """
        crcgenerated = CRC(data)
        """

        #comde using inbuilt crc
        """
        1. pip3 install crccheck
        2. from crccheck.crc import Crc32, CrcXmodem
        """

        data = ''.join(format(i, 'b') for i in bytearray(data, encoding ='utf-8'))
        
        crcgenerated = Crc32.calc(bytearray(data,encoding = 'utf-8'))



        message = pickle.dumps(encryptedmessage)
        crcc = pickle.dumps(crcgenerated)
        s = socket.socket()
        port = 5001
        #ip = sys.argv[1]
        s.connect(('127.0.0.1',int(port)))
        print("Connection established to server")
        s.send(message)
        s.send(crcc)
        s.recv(1023)
    s.close()


if __name__ == '__main__':
    main()
