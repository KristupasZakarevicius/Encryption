# Libraries
import random
import os, sys
from PIL import Image

# ***** Encryption / Decryption selection *****
def main():
   mode_selection = input("\n\nDo you want to encrypt or decrypt the communication?\nEnter [E] for the encryption and [D] for the decryption: ")

   if mode_selection.lower().startswith('e'):
      modeEncryption() # function is called

   elif mode_selection.lower().startswith('d'):
      Decryption() # class is called

   else:
      print("\nEntered input is invalid. Please, try again")
      main()

# *********** ENCRYPTION ************
# Encryption Object selection
def modeEncryption():
   print("\n*Encryption mode enabled*")
   mode_encr = input("Enter number to encrypt:\n[1] - Single message\n[2] - Text or csv file\n[3] - PNG Image\nSelection: ")

   try:
      mode_encr = int(mode_encr)
   except ValueError:
      inputInvalid()

   if int(mode_encr) == 1:
      singleMessage()

   elif int(mode_encr) == 2:
      txtFile() 

   elif int(mode_encr) == 3:
      imageFile()

   else:
      inputInvalid()

def inputInvalid():
      print("\nEntered input is invalid. Please, try again.")
      modeEncryption()

# Single message encryption mode
def singleMessage():
      Msg = input("\nEnter the message:\n")
      encryptedMsg = seedEncryption(Msg)
      print("\nEncrypted message:\n" + encryptedMsg)

# Text file encryption mode
def txtFile():
      fileName = input("\nEnter name of the file: ")

      # Relative path location is the directory in which script is located
      try:
         theFile = open(os.path.join(sys.path[0], fileName), "r")
      except FileNotFoundError:
         print("\n" + fileName + "file does not exist.")
         txtFile()
      
      content = theFile.read()
      theFile.close()

      # Initializes encryption Class Affine
      affine = Affine()
      encryptedContent = affine.encrypt(content) # Encrypts txt file content

      encryptedFileName = "[Encrypted] " + fileName     
      encryptedFile = open(os.path.join(sys.path[0], encryptedFileName), "w+") # w+ allows to create a file if it does not exist and write in it

      encryptedFile.write(encryptedContent) # Writes encrypted content into the created file
      encryptedFile.close()

      print('\nFile "' + encryptedFileName + '" was created with encrypted content in it.')

# Image encryption
# The images must be mutated in a lossless format. 
# So the encrypted/decrypted files will be saved as a .png image.
def imageFile():
   imageFileName = input("\nEnter name of the [PNG] image file: ")
   
   try:
      im = Image.open(os.path.join(sys.path[0], imageFileName + ".png"))
   except FileNotFoundError:
      print("\n" + imageFileName + "file does not exist.")
      imageFile()

   pixelMap = im.load()

   width = im.size[0]
   heigth = im.size[1]

   progress = 0
   for i in range(width):
      if i % (width/10) == 0:
         progress += 10
         print("Encrypting: " + str(progress) + " %")

         # Pick p < 256 prime, p != 2.
         # if a is even, take a + 1 (mod 256)
         # then a ^ 128+1 = a, (phi totient = 128) as # 129 = 43*3
      for j in range(heigth): # 
         pixel = pixelMap[i, j]
         coprime_pixel = ((c+1 if c % 2 == 0 else c) for c in pixel)
         pixelMap[i, j] = tuple(int(c**43 % 256) for c in coprime_pixel)

   im.save(os.path.join(sys.path[0], "[Encrypted] " + imageFileName + ".png"))
   print("\nImage saved as [Encrypted] " + imageFileName + ".png")

# ********** Encryption/Decryption Algorithms ***********

# *** Affine Algorithm
class Affine(object):

   # Modify encryption by changing coefficients
   K1 = 7 # Multiplies by K1
   K2 = 3 # Adds K2
   DIE = 128 # Mod by symbol set size
   KI = 55 # For decryption, multiply by mod inverse of K1
   KEY = (K1, K2, KI)
   
   def __init__(self):
      pass

   # Affine Encryption
   def encryptChar(self, char):
      K1, K2, KI = self.KEY
      return chr((K1 * ord(char) + K2) % self.DIE)
		
   def encrypt(self, string):
      encryptedMsg = "".join(map(self.encryptChar, string))  
      self.encryptedMsg = encryptedMsg
      return encryptedMsg

   # Affine Decryption
   def decryptChar(self, char):
      K1, K2, KI = self.KEY
      return chr(KI * (ord(char) - K2) % self.DIE)
   
   def decrypt(self, encryptedMsg):
      return "".join(map(self.decryptChar, encryptedMsg))

# *** Random Random seed algorithm
# Random seed encryption
def seedEncryption(Msg):
    encryptedMsg = ''
    # List which contains is just every ASCII character (32-126) in order
    characters_in_order = [chr(x) for x in range(32,127)]

    # Change r_seed in order to provide different encryption value for each element
    r_seed = input("\nEnter an integer to use as seed: ")

   # 'random' is used to shuffle the characters in order according to a seed.
   # As long as this seed is the same on the encryption and decryption,
   # it will produce the same shuffled list and the result.
    random.seed(r_seed)
    shuffled_list = [chr(x) for x in range(32,127)]
    random.shuffle(shuffled_list)

    for i in range(0, len(Msg)):
      encryptedMsg += shuffled_list[characters_in_order.index(Msg[i])]
         
    return encryptedMsg

# Random seed decryption
def seedDecryption(Msg):
      decryptedMsg = ''
      characters_in_order = [chr(x) for x in range(32,127)] # List which is just every ASCII character (32-126) in order

      r_seed = input('\nEnter an integer to use as a seed (the same one used to encrypt): ')
      random.seed(r_seed)
      shuffled_list = [chr(x) for x in range(32,127)]
      random.shuffle(shuffled_list)

      for i in range(0, len(Msg)):
         decryptedMsg += characters_in_order[shuffled_list.index(Msg[i])]

      return decryptedMsg
      
# ************ Decryption *************
class Decryption:
   def __init__(self):
      print("\nDecryption mode enabled\n")
      mode = input("Enter number to decrypt:\n[1] - Single message\n[2] - Text file\n[3] - PNG Image\nSelection: ")
      
      self.mode = int(mode)
      self.modeDecryption(self.mode)

   def modeDecryption(self, mode):
      if self.mode == 1:
         self.decryptMsg()
         
      elif self.mode == 2:
         self.decryptTxtFile()
 
      elif self.mode == 3:
         self.decryptImage()

      else:
         print("\nEntered input is invalid. Please, try again")
         self.modeDecryption(self.mode)

   def decryptMsg(self):
      Msg = input("\nEnter the message:\n")
      decryptedMsg = seedDecryption(Msg)
      print("\nEncrypted message: \n" + decryptedMsg)

   def decryptTxtFile(self):
      fileName = input("\nEnter name of the file without the [Encrypted] label: ")

      encryptedFileName = os.path.join(sys.path[0], ("[Encrypted] " + fileName))
      encryptedFile = open(encryptedFileName, "r")
      encryptedContent = encryptedFile.read()
      encryptedFile.close()

      encryptedFile = open(os.path.join(sys.path[0], encryptedFileName), "w")
      affine = Affine()
      dencryptedContent = affine.decrypt(encryptedContent)
      encryptedFile.write(dencryptedContent)
      encryptedFile.close()

      decryptedFileName = os.path.join(sys.path[0], ("[Decrypted] " + fileName))

      os.rename(encryptedFileName, decryptedFileName) # Renames label [Encrypted] to [Decrypted]
      print('\nText file decrypted and placed in: ' + decryptedFileName)
 
   def decryptImage(self):
      fileName = input("\nEnter name of the encrypted image file (without the [Encrypted] label): ")
      encryptedImageName = os.path.join(sys.path[0], ("[Encrypted] " + fileName + ".png"))

      try:
         im = Image.open(encryptedImageName)
      except FileNotFoundError:
         print("\n" + encryptedImageName + "file does not exist.")
         imageFile()

      pixelMap = im.load()
      width = im.size[0]
      heigth = im.size[1]

      progress = 0

      # iterates through each pixel
      for i in range(width): 
         if i % (width/10) == 0: # Prints out progress every 10 % do.
            progress += 10
            print("Decrypting: " + str(progress) + " %")

         for j in range(heigth):
            pixel = pixelMap[i, j]
            pixelMap[i, j] = tuple(int(c**3 % 256) for c in pixel)

      decryptedImageName = os.path.join(sys.path[0], ("[Decrypted] " + fileName + ".png"))
      im.save(os.path.join(sys.path[0], encryptedImageName))

      os.rename(encryptedImageName, decryptedImageName) # Renames label [Encrypted] to [Decrypted]
      print('\nImage decrypted and located in:' + decryptedImageName)

########### Main ############
if __name__ == '__main__':
    main()