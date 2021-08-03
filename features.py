import numpy as np 

class ErrorDisfluencyFeatures:
    def __init__(self, script, transcript):
        
        self.script = script.split(' ')
        self.transcript = transcript.split(' ')
        self.eds = self.run_dl()
            
        self.num_insertions = self.eds.count('I')
        self.num_deletions = self.eds.count('D')
        self.num_substitutions = self.eds.count('S')
        self.num_transpositions = self.eds.count('T')
        self.aligned_str = self.align() 
        
    def run_dl(self): 
        
        # set up penalties 
        ins_penalty = 1 
        del_penalty = 1 
        sub_penalty = 2 
        trans_penalty = 2 
        
        # initialize distance matrix with empty string comparisons
        # (empty string comparison --> row and column = 0)
        dist = np.zeros(((len(self.transcript) + 1), len(self.script) + 1))
        for i in range(len(self.transcript) + 1): 
            dist[i][0] = i*ins_penalty 
        for j in range(len(self.script) + 1): 
            dist[0][j] = j*del_penalty 
        
        # fill in the distance matrix 
        for i in range(1, len(self.transcript) + 1): 
            for j in range(1, len(self.script) + 1): 
                
                if self.script[j-1] == self.transcript[i-1]: 
                    dist[i][j] = dist[i-1][j-1] # correct 
                else: 
                    del_cost = dist[i][j-1] + del_penalty # deletion
                    ins_cost = dist[i-1][j] + ins_penalty # insertion
                    sub_cost = dist[i-1][j-1] + sub_penalty # substitution
                    # only calc trans cost if transposed words match
                    if i >=2 and j >=2 and self.script[j-2] == self.transcript[i-1] and self.script[j-1] == self.transcript[i-2]:
                        trans_cost = dist[i-2][j-2] + trans_penalty # transposition
                    else: 
                        trans_cost = None 

                    # word is not correct                    
                    # update cell with min cost of getting there
                    possible_costs = [del_cost, ins_cost, sub_cost, trans_cost]
                    dist[i][j] = min(cost for cost in possible_costs if cost is not None) 
                    
        # backtrack the distance matrix 
        # initialize i and j so that we start in bottom right of matrix 
        i = len(self.transcript) 
        j = len(self.script) 
        operations = [] 
        
        while i > 0 or j > 0: 
        
            # correct
            if self.script[j-1] == self.transcript[i-1] and dist[i-1][j-1] == dist[i][j]: 
                i -= 1 
                j -= 1
                operations.append('C')
        
            # get cost of getting to i,j for every operation that could have been used to get there
            del_cost = None 
            ins_cost = None 
            sub_cost = None 
            trans_cost = None 
            if i > 0 and dist[i-1][j] + ins_penalty == dist[i][j]: 
                ins_cost = dist[i-1][j]
            if j > 0 and dist[i][j-1] + del_penalty == dist[i][j]: 
                del_cost = dist[i][j-1] 
            if i > 0 and j > 0 and self.script[j-1] != self.transcript[i-1] and dist[i-1][j-1] + sub_penalty == dist[i][j]:
                sub_cost = dist[i-1][j-1]
            if i > 1 and j > 1 and self.script[j-2] == self.transcript[i-1] and self.script[j-1] == self.transcript[i-2] and dist[i-2][j-2] + trans_penalty == dist[i][j]: 
                trans_cost = dist[i-2][j-2]
            
            # pick an operation based on which ones were possible to get to i,j
            # priority for picking: transposition, substitution, insertion, deletion 
            if trans_cost is not None: 
                i -= 2
                j -= 2 
                operations.append('T') 
                operations.append('T') 
                continue
            if sub_cost is not None: 
                i -= 1
                j -= 1 
                operations.append('S') 
                continue
            if ins_cost is not None: 
                i -= 1
                operations.append('I') 
                continue 
            if del_cost is not None: 
                j -= 1 
                operations.append('D') 
        
        operations.reverse() 
        
        return operations
        
    def align(self): 
        
        # alignment: text + operations combined 
        # row0: script, with '*' when there was something inserted
        # row1: operations or error and disfluency sequence (eds)
        # row2: transcript, with '*' when there was something deleted
        alignment = np.empty((3, len(self.eds)), dtype=object)

        
        script_idx = 0 
        trans_idx = 0 
        # collect word lengths so we can pad words with spaces on both sides for readability 
        word_lens = [] 

        # loop through operations and update alignment 
        for idx, op in enumerate(self.eds): 
            if op in ['C', 'S', 'T']: 
                alignment[0][idx] = self.script[script_idx] 
                alignment[1][idx] = self.eds[idx] 
                alignment[2][idx] = self.transcript[trans_idx]
                word_lens.append(max(len(self.script[script_idx]), len(self.transcript[trans_idx])))
                script_idx += 1 
                trans_idx += 1
            elif op == 'I': 
                alignment[0][idx] = '*' 
                alignment[1][idx] = self.eds[idx] 
                alignment[2][idx] = self.transcript[trans_idx]
                word_lens.append(len(self.transcript[trans_idx]))
                trans_idx += 1 
            elif op == 'D': 
                alignment[0][idx] = self.script[script_idx]
                alignment[1][idx] = self.eds[idx] 
                alignment[2][idx] = '*'
                word_lens.append(len(self.script[script_idx]))
                script_idx += 1 
        
        # convert alignment to string 
        # pad each word on both sizes with ' ' so words line up 
        aligned_str = '\n'.join(' '.join([alignment[i][j].center(word_lens[j], ' ') for j in range(alignment.shape[1])]) for i in range(alignment.shape[0]))
        
        return aligned_str 
