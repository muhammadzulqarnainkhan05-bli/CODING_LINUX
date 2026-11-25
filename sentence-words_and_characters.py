sentence = input("Write a sentence:") 
if sentence=="":
    sentence="HI g kase ho"

    
lengthofsen = len(sentence)

print(f"The Total Alphabets:{lengthofsen}")

wordssplit= sentence.split()

print(f"First word is:{wordssplit[0]}")

print(f"Total words are: {len(wordssplit)}")
