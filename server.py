
import socket             
import numpy as np
import pickle
import sys
import threading
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
    tmp = addingdata[0 : pickdata] 
   
    while (pickdata < len(addingdata)): 
   
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
    addingdata = data + '0'*(length-1)
    remainder = division(addingdata,key)
    return remainder
"""

def decrypted(decryptedmessage,A_inverse):
    val1 = np.dot(A_inverse,decryptedmessage)
    #print(val1)
    val1 = np.reshape(val1, (val1.shape[0] * val1.shape[1]), 'F')
    #print(val1)
    message = ""
    for values in val1:
        if values == 27:
            message+=" "
        else:
            val2 = values+65-1
            message+=chr(val2)
    message1 = message.rstrip()
    return message1     

def threaded(c):
    while(True):
        data = c.recv(50000)
        if(len(data) < 3):
            continue
        # print(data)
        val1 = data[:data[1:].find(b'\x80')]
        val1 += b'.'
        #print(val1)
        val2 = data[data[1:].find(b'\x80'):]
        val2 = val2[1:]      
        print ('Got data')
        #print(val1)
        decryptedmessage = pickle.loads(val1)
        #print(decryptedmessage)
        crcc = pickle.loads(val2)
        #print(crcc)
        recievedmessage = decrypted(decryptedmessage,A_inverse)
        print(recievedmessage)
        print("Message got from client" + " -"+" "+  str(recievedmessage))
        
        #crcc1 = CRC(recievedmessage)

        recievedmessage = ''.join(format(i, 'b') for i in bytearray(recievedmessage, encoding ='utf-8')) 
        crcc1 = Crc32.calc(bytearray(recievedmessage,encoding = 'utf-8'))

        #kyuki imbuilt crc key int me ata
        if int(crcc1) == int(crcc): 
            print("Received Message is correct")
        else:
            print("Wrong message Recieved")
        c.send('done'.encode()) 
        
def main():  
    s = socket.socket()
    port = sys.argv[1] 
    port = int(port)      
    print ("Socket successfully created") 
    s.bind(('', port))        
    print ("socket binded to %s" %(port))  
    s.listen(2)  
    print ("socket is listening")  
    while(True):          
        c, addr = s.accept()
        threading.Thread(target=threaded, args=(c,)).start()
    s.close()

if __name__ == '__main__':
    main()
