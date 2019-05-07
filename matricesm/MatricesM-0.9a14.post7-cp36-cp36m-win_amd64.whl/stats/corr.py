def _corr(mat,col1=None,col2=None,population=1,temp=None):
    """
    Correlation of 2 columns
    col1,col2: integers>=1 or both None; column numbers. For correlation matrix give None to both
    population:1|0 ; 1 to calculate for the population or a 0 to calculate for a sample
    """
    if not (( isinstance(col1,int) and isinstance(col2,int) ) or (col1==None and col2==None)):
        raise TypeError("col1 and col2 should be integers or both None")
        
    if population not in [0,1]:
        raise ValueError("population should be 0 for samples, 1 for population")
    
    if not (col1==None and col2==None):
        if not (col1>=1 and col1<=mat.dim[1] and col2>=1 and col2<=mat.dim[1]):
            raise ValueError("col1 and col2 are not in the valid range")
    
    if col1==None and col2==None:
        sd = mat.sdev(population=population,asDict=0)
        for i in range(mat.dim[1]):
            for j in range(i+1,mat.dim[1]):
                cv = mat.cov(i+1,j+1,population=population)
                s = sd[i]*sd[j]
                if s == 0:
                    raise ZeroDivisionError("Standard deviation of 0")
                val =  cv/s
                temp._matrix[i][j] = val
                temp._matrix[j][i] = val
        return temp
    
    else:
        sd = mat.sdev(population=population,asDict=0)
        if 0 in sd:
            raise ZeroDivisionError("Standard deviation of 0")
        return mat.cov(col1,col2,population=population)/(sd[col1-1]*sd[col2-1])