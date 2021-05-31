import numpy
import matplotlib.pyplot as pptlt

from collections import deque
from sys import maxsize
import time
import random

from buckets import norm_bset , uni_bset

# BUCKET-SORT ---------------------------------------------------
def norm_bsort( arr ):

    mu    = numpy.mean( arr )
    sigma = numpy.std( arr )
    n     = len( arr )

    B = norm_bset( n , mu , sigma )
    for x in arr:
        B.add( x )
    return [ x for x in B ]

def uni_bsort( arr ):

    bottom = min( arr )
    top    = max( arr )
    n      = len( arr )

    B = uni_bset( n , bottom , top )
    for x in arr:
        B.add( x )
    return [ x for x in B ]

# Numpy Bsort --------------------------------------------------------

def np_bsort( arr ):

    bottom = min( arr )
    top    = max( arr ) + 1
    n      = len( arr )

    buckets = numpy.floor( n*( arr - bottom )/( top - bottom ) ).astype( int )
    # arr_prime = arr.copy()

    # m = numpy.ceil( numpy.log2( buckets.max() ) )
    # for _ in range( int( m ) ):
        
    #     seq = ( buckets%2 == 0 )
    #     x = len( seq[ seq ] )

    #     arr1 = arr_prime[ seq ]
    #     arr2 = arr_prime[ ~seq ]
    #     arr_prime[ :x ] = arr1
    #     arr_prime[ x: ] = arr2

    #     buck1 = buckets[ seq ]
    #     buck2 = buckets[ ~seq ]
    #     buckets[ :x ] = buck1//2
    #     buckets[ x: ] = buck2//2

    buck_val = numpy.zeros( buckets.max() + 1, dtype = int )
    for x in buckets:
        buck_val[ x ] += 1
    buck_val = numpy.cumsum( buck_val )

    arr_prime = numpy.zeros( n )
    for i in range( n - 1 , -1 , -1 ):
        x , buck = arr[ i ] , buckets[ i ]
        pos = buck_val[ buck ] -1
        arr_prime[ pos ] = x
        buck_val[ buck ] = pos

    for i in range( 1 , n ):
        j = i - 1
        while j > -1:
            if arr_prime[ j ] <= arr_prime[ j + 1 ]:
                break
            aux = arr_prime[ j + 1 ]
            arr_prime[ j + 1 ] = arr_prime[ j ]
            arr_prime[ j ] = aux
            j -= 1
    return arr_prime

# MERGE-SORT ---------------------------------------------------------
def intercal( A , B ):

    n = len( A ) + len( B )
    arr = [ None ]*n

    k , i , j = 0 , 0 , 0
    while k < n:

        xa = maxsize
        if i < len( A ):
            xa = A[ i ]
        
        xb = maxsize
        if j < len( B ):
            xb = B[ j ]

        x = xa if xa <= xb else xb
        arr[ k ] = x
        k += 1

        if x == xa:
            i += 1
        else:
            j += 1
    
    return arr

def merge_sort( arr ):

    queue = deque( [ [ x ] for x in arr ] )
    while len( queue ) > 1:
        A = queue.popleft()
        B = queue.popleft()
        C = intercal( A , B )
        queue.append( C )
    return queue.pop( )

# BENCHMARKING---------------------------------------------------------

def get_exec_time( fun , arr , repeats = 10 ):

    repeats = max( repeats , 1 ) 

    t = time.time( )
    for _ in range( repeats ):
        fun( arr )
    dt = ( time.time() - t )/repeats

    return dt

def is_sorted( arr ):

    result = True
    for i in range( len( arr ) -1 ):
        x1 = arr[ i ]
        x2 = arr[ i + 1 ]

        if x1 > x2:
            result = False
            break
    return result

def bench_marking( f1 , f2 , pool, max_size ):

    size = 8
    while size < max_size:
        
        size = min( 2*size , max_size )

        samp = numpy.random.choice( pool , size = int( size ) , replace = False )
        ord1 = is_sorted( f1( samp ) ) 
        ord2 = is_sorted( f2( samp ) )
        ord = ord1 and ord2
        t1 = get_exec_time( f1 , samp )
        t2 = get_exec_time( f2 , samp )

        yield size , ord , t1 , t2 

if __name__ == "__main__":

    f1 = uni_bsort
    f2 = np_bsort

    max_size = 1*10**6
    pool = numpy.random.random( size = maxsize )

    bench = bench_marking( f1 , f2 , pool , max_size )
    ns = []
    times1 = []
    times2 = []
    for size , ord , t1 , t2 in bench:

        print( "-"*25 )
        print( size , ord , t1 , t2 , sep = "\n")

        ns.append( size )
        times1.append( t1 )
        times2.append( t2 )
    
    
    pptlt.plot( ns , times1 , color = "blue" )
    pptlt.plot( ns , times2 , color = "red" )
    pptlt.show()

