'''
Created on 4 de dez de 2018

Implementation of MONIC, external clustering transitions detector.

Spiliopoulou, M., et al. (2006). MONIC - Modeling and Monitoring Cluster Transitions. 
KDD '06 (p. 706). New York, NY, USA: ACM Press. https://doi.org/10.1145/1150402.1150491

@author: guilherme.alves-da-silva@inria.fr
'''
import sys

def detect(old_clusters, current_clusters, tau = 0.7, tau_split = 0.35):
    
    dead_list = []
    split_list = []
    absorptions_survivals = []
    
    for x in old_clusters : # line 1
        split_candidates = [] # line 2
        split_union = set() # line 2
        survival_candidate = None # line 3
        
        best_m_cell = sys.float_info.min 
        
        for y in current_clusters : # line 4
            
            m_cell = overlap(x, y) # line 5
            
            if m_cell >= tau : # line 6 
                if m_cell > best_m_cell : # line 7
                    survival_candidate = y # line 8 
                    best_m_cell = m_cell
                    
            elif m_cell >= tau_split : # line 10 
                split_candidates.append(y) # line 11
                split_union.update(y) # line 12
        
        if survival_candidate == None and len(split_candidates) == 0 : # line 15
            dead_list.append(x) # line 16 ### DEAD 
        elif len(split_candidates) != 0 : # line 17 
            if overlap(x, split_union) >= tau : # line 18
                for y in split_candidates : # line 19
                    split_list.append((x,y)) # line 20 ### SPLIT CANDIDATES 
            else : 
                dead_list.append(x) # line 22
        else :
            absorptions_survivals.append((x,survival_candidate)) # line 24
    
    absorption_list = []
    survival_list = []
    
    for y in current_clusters : # line 27
        absorptions_candidates = make_list(absorptions_survivals,y) # line 28
        if len(absorptions_candidates) > 1 : # line 29
            for x in absorptions_candidates : # line 30
                absorption_list.append((x,y)) # line 31
                absorptions_survivals.remove((x,y)) # line 32
        elif len(absorptions_candidates) == 1: # line 34 
            x = absorptions_candidates[0]
            survival_list.append((x,y)) # line 35
            absorptions_survivals.remove((x,y)) # line 36

    return (dead_list,split_list,absorption_list,survival_list)

def overlap(cluster_a, cluster_b):
    
    num = len(cluster_a & cluster_b)
    den = len(cluster_a)
    
    if num == 0 or den == 0 :
        return 0
    else :
        return num / den

def make_list(absorptions_survivals,y):
    
    list = []
    
    for (cluster_a,cluster_b) in absorptions_survivals :
        if y == cluster_b :
            list.append(cluster_a)
    
    return list

Co1 = set([3, 4, 7, 8, 9, 12, 17, 18, 19, 26, 30, 34, 37, 38, 40, 41, 42, 48])
Co2 = set([2, 6, 13, 15, 20, 22, 25, 28, 29, 31, 35, 43, 44, 45, 46, 47])
Co3 = set([0, 5, 11, 14, 16, 24, 27, 32, 33, 36, 39])
Co4 = set([1, 10, 21, 23, 49])
Cc1 = set([2, 6, 10, 22, 23, 29, 35, 45, 49, 62, 72, 78, 83, 85, 88])
Cc2 = set([0, 1, 5, 7, 8, 11, 14, 16, 18, 21, 24, 25, 27, 31, 32, 33, 34, 36, 39, 43, 53, 55, 61, 63, 64, 65, 68, 70, 73, 75, 77, 79, 82, 84, 91, 92, 94, 98, 99]) 
Cc3 = set([3, 4, 9, 12, 17, 19, 26, 30, 37, 38, 40, 41, 42, 48, 52, 54, 69, 71, 76, 90, 95, 96, 97])
Cc4 = set([13, 15, 20, 28, 44, 46, 47, 50, 51, 56, 57, 58, 59, 60, 66, 67, 74, 80, 81, 86, 87, 89, 93])
    
def main():
    detect([Co1,Co2,Co3,Co4], [Cc1,Cc2,Cc3,Cc4])

if __name__== "__main__":
    main()
    
# m.overlap(m.Co1,m.Cc1)
# m.overlap(m.Co1,m.Cc2)
# m.overlap(m.Co1,m.Cc3)
# m.overlap(m.Co1,m.Cc4)
# m.overlap(m.Co2,m.Cc1)
# m.overlap(m.Co2,m.Cc2)
# m.overlap(m.Co2,m.Cc3)
# m.overlap(m.Co2,m.Cc4)
# m.overlap(m.Co3,m.Cc1)
# m.overlap(m.Co3,m.Cc2)
# m.overlap(m.Co3,m.Cc3)
# m.overlap(m.Co3,m.Cc4)
# m.overlap(m.Co4,m.Cc1)
# m.overlap(m.Co4,m.Cc2)
# m.overlap(m.Co4,m.Cc3)
# m.overlap(m.Co4,m.Cc4)
# 
# 
# Split
# ({Co2}, {Cc1}), 
# ({Co2}, {Cc4}), 
# ({Co4}, {Cc1}), 
# ({Co4}, {Cc2})
# 
# Survival
# ({Co3}, {Cc2}), 
# ({Co1}, {Cc3})