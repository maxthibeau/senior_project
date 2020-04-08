# NOTE: this class will eventually be flushed into a UI
class PFTSelector():

  def select_pft(meteor_input, prev_pfts):
    print("possible PFTs:", end = ' ')
    poss_pfts = meteor_input.pfts(0,8)
    # convert to string to make pft datatype flexible
    poss_pfts = list(map(str, poss_pfts))
    for pft in poss_pfts:
      print(pft, end = ' ')
    if not prev_pfts:
        print()
    else:
        print(" Previously Optimized PFTs:",prev_pfts)

    pft_selected = input("Select a PFT: ")
    while pft_selected not in poss_pfts:
      print ("That's an invalid pft")
      pft_selected = input("Select a PFT:")
    return pft_selected
