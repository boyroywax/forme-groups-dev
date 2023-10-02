"""The main application Init file.
which is being used temporarily as scratch code.
"""

import sys
import os


class App:
    """
    Holds the main application logic.
    """

    def __init__(self):
        """
        Constructor.
        """
        # get the python version
        print("\n"+sys.version)

        # get the python version info
        print("\n"+str(sys.version_info))

        # get the current working directory
        print("\n"+os.getcwd())

        # print the path of the current file
        print("\n"+__file__)

        # print the path of the current directory
        print("\n"+os.path.dirname(__file__))

        # print the path of the parent directory
        print("\n"+os.path.dirname(os.path.dirname(__file__)))

        # print the operating system name
        print("\n"+os.name)

        # print the environment variables
        print("\n"+repr(os.environ.items()))

    def run(self):
        """
        Runs the application.
        """
        print("\n"+"Hello world!")

    def create_types(self) -> bool:
        """
        Example of creating objects with different types
        """

        def create_a[T](value: T) -> T:
            print(value, type(value))
            return value

        if create_a(1) != 1:
            return False

        if create_a("1") != "1":
            return False

        if create_a(1.0) != 1.0:
            return False

        if isinstance(create_a(1), int) is not True:
            return False

        if isinstance(create_a("1"), str) is not True:
            return False

        if isinstance(create_a(1.0), float) is not True:
            return False

        return True
    
    def create_types2(self) -> bool:
        """
        Example of creating objects with different types
        """

        def create_a[T: (int, float)](value: T) -> T:
            assert isinstance(value, int | float)
            print(value, type(value))
            return value
        
        if create_a(1) != 1:
            return False
        
        if create_a(1.0) != 1.0:
            return False
        
        try:
            create_a("1")
        except AssertionError:
            print("AssertionError for type 'str' as expected")

        return True

            
        

