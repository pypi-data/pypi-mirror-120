class Donkey:
    def __init__( self, separator='__' ):
        self.separator = separator

    def key( self, *args ):
        """
        join the arguments in the format of donkey

        Arguments
        ---------
        args: list of string

        Examples
        --------
        >>>key( 'a', 'b', 'c' )
        'a__b__c'
        """
        return self.separator.join( args )


    def partion( self, key ):
        """
        split the key have the format of donkey

        Arguments
        ---------
        key: string

        Examples
        --------
        >>>partion( 'a__b__c' )
        [ 'a', 'b', 'c' ]
        """
        return key.split( self.separator )


    def init( self, key ):
        """
        get the first key

        Arguments
        ---------
        key: string

        Examples
        --------
        >>>init( 'a__b__c' )
        a__b
        """
        p = self.partion( key )
        if len( p ) > 1:
            return self.key( *p[:-1] )
        return self.key( *p )


    def last( self, key ):
        """
        get the last part of the key

        Arguments
        ---------
        key: string

        Examples
        --------
        >>>last( 'a__b__c' )
        c
        """
        return self.partion( key )[-1]


    def get( self, key, d ):
        """
        get the value from a dict

        Arguments
        ---------
        key: string
        d: dict

        Returns
        -------
        object
            the value of in the key

        Raises
        ------
        KeyError: if cannot find the key

        Examples
        --------
        >>>d = { 'c': { 'd': { 'f': 20 } }, }
        >>>get( 'c__d__f', d )
        20
        """
        keys = self.partion( key )
        value = d
        for k in keys:
            value = value[ k ]
        return value


    def setter( self, key, d, value ):
        """
        set the value in the dict in the key
        if no exitst the path is going to maked

        Arguments
        ---------
        key: string
        d: dict
        value: object

        Examples
        >>>d = { }
        >>>set( 'c__d__f', d, 20 )
        >>>d
        { 'c': { 'd': { 'f': 20 } } }
        """
        keys = self.partion( key )
        v = d
        for k in keys[:-1]:
            try:
                v = v[ k ]
            except KeyError:
                v[ k ] = {}
                v = v[ k ]
        v[ keys[-1] ] = value


    def inflate( self, d ):
        """
        inflate a dict

        Arguments
        ---------
        d: dict

        Returns
        -------
        dict

        Examples
        --------
        >>>inflate( { 'a': 10, 'b__c': 30 } )
        { 'a': 10, 'b': { 'c': 30 } }
        """
        result = {}
        for k, value in d.items():
            try:
                self.get( k, result )
                raise ValueError(
                    "Conflict with the donkey '{}' ".format( k ) )
            except KeyError:
                pass
            except TypeError:
                raise ValueError(
                    "Conflict with the donkey '{}' ".format( k ) )
            self.setter( k, result, value )
        return result


    def compress( self, d ):
        """
        compress a dict using donkey format

        Arguments
        ---------
        d: dict

        Returns
        -------
        dict

        Examples
        --------
        >>>inflate( { 'a': 10, 'b: { 'c': 30 } } )
        { 'a': 10, 'b__c': 30 }
        """
        result = {}
        for k, v in d.items():
            if isinstance( v, dict ):
                r = self._compress( k, v )
                result.update( r )
            else:
                result[ k ] = self._compress( k, v )
        return result


    def _compress( self, init_key, d ):
        """
        """
        if isinstance( d, dict ):
            result = {}
            for k, v in d.items():
                if init_key != '':
                    current_key = self.key( init_key, k )
                else:
                    current_key = k
                result[ current_key ] = self._compress( '', v )
            result = self.compress( result )
            return result
        elif isinstance( d, list ):
            return [ a for a in d ]
        elif isinstance( d, tuple ):
            return tuple( a for a in d )
        return d
