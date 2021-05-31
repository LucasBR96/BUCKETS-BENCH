import math
import random
from scipy.stats import norm
import numpy
import time
import matplotlib.pyplot as pptlt 

class bucket_set:

    def __init__( self , n , foo ):

        self.n = n
        self.buckets = [ None ]*self.n
        self.foo = foo

    def __iter__( self ):

        for i in range( self.n ):
            bucket = self.buckets[ i ]
            if bucket is None: continue 
            for x in bucket:
                yield x
    
    def add( self , x ):

        prob = self.foo( x )
        idx = math.floor( prob*self.n )
        idx = min( idx , self.n - 1 )
        if self.buckets[ idx ] is None:
            self.buckets[ idx ] = [ x ]
            return

        bucket = self.buckets[ idx ]
        bucket.append( x )
        i = len( bucket ) - 1
        while i > 0:
            if bucket[ i ] > bucket[ i - 1 ]:
                break
            bucket[ i ] = bucket[ i - 1 ]
            bucket[ i - 1 ] = x
            i -= 1

def uni_bset( n , bottom = 0 , top = 1.):

    def foo( x ):
        if x < bottom or x > top:
            raise ValueError( "value of x is off limits" )
        num = x - bottom
        den = top - bottom
        return num/den
    
    return bucket_set( n , foo )

def norm_bset( n , mu = 0 , sigma = 1.):

    def foo( x ):
        z = ( x - mu )/sigma 
        return norm.cdf( z )
    
    return bucket_set( n , foo )

def test_1( ):

    n = 100
    B = norm_bset( n , 5 , 2 )
    for i in range( n ):
        x = random.normalvariate( 5 , 2 )
        B.add( x )
    
    w = lambda x : str( x )[ :6 ]
    for i , b in enumerate( B.buckets ):
        if b is None: continue

        s = " ".join( map( w , b ) )
        print( i , "|" , s )

def test_2():

    ns    = []
    times = []

    t = time.time()
    B = uni_bset( 10**5 )

    for i in range( 10**5 ):

        x = random.random()
        B.add( x )

        if not ( i )%( 10**2 ):
            ns.append( i )
            times.append( time.time() - t )

            print( ns[ -1 ] , times[ -1 ] )
    
    pptlt.plot( ns , times )
    pptlt.show()

if __name__ == "__main__":
    # test_1( )
    test_2( )