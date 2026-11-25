import os
os.makedirs("wrifi", exist_ok=True)


with open("wrifi/story.txt", "r") as wrf:
    reade = wrf.read() # yaha mn ne read kr doa
    splite= list(reade.split()) #Words mn takseen ker dia or list bna lia
#________________characters_____________________
    print(f"Total characters:{len(reade)}")
    print("="*30)

    print(f"Total number of Words:{len(splite)}")
    # print("="*30)

#=============== BIGGEST WORD ==================
    mostbig = splite[0]
    for wrd in splite:
        if len(wrd)>len(mostbig):
            mostbig=wrd
    print("="*30)

    print(f"Biggest Word: {mostbig}")
#++++++++++++ LINES  OF  FILE KI +++++++++++++++
    lines = reade.splitlines() # lines = reade.split(".")
    print("="*30)
    print(f"Total Lines: {len(lines)}")

#++++++++++++++++++ WORDS ++++++++++++++++++++
    print("="*30)
    print(f"Total words are: {len(splite)}")
