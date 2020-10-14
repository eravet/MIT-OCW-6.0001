# Problem Set 4A
# Name: Eric Ravet
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    

    if len(sequence) == 1:
        return sequence
    else:
        first = sequence[0]
        remain = sequence[1:]
        temp_perm = get_permutations(remain)
        permutations = []
        
        for p in temp_perm:
            for i in range(len(p)+1):
                new_sequence = p[0:i] + first + p[i:]
                
                if new_sequence not in permutations:
                    permutations.append(new_sequence)
                    permutations.sort()
        return permutations

    #1. return base case if len of sequence equals 1
    #2. if len of the string is greater than 1
            #3. move the first character through the permutations of the remaining string

if __name__ == '__main__':
    #EXAMPLE
    example_input = 'abcd'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
    # Put three example test cases here (for your sanity, limit your inputs
    #to be three characters or fewer as you will have n! permutations for a 
    #sequence of length n)
