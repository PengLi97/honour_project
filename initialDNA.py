import h5py
import numpy as np
# maximum size in group of DNA
#each gene size {hand_card,pre_player,next_player,Single,Pair,
#                Three,ThreeWithOne,Bomb,Chain,ChainPair,Airplane,
#                AirplaneWithWings,Rocket,score,k}
DNA_size = 20
Gene_size = 15
def initDNA():
    for i in range(3):
        DNA = np.random.random_sample((DNA_size, Gene_size))
        DNA[:, 13:15] = 0
        if i == 0:
            np.save('database/DNAup', DNA)
        elif i == 1:
            np.save('database/DNAlandlord', DNA)
        else:
            np.save('database/DNAdown', DNA)
def creat():
    # initDNA()
    print(np.load('database/DNAup.npy'))

creat()
