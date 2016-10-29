from gevent import monkey
monkey.patch_all()
import code, sys, enum

## CORE ##

def interactive():
    
    # exception trick to pick up the current frame
    try:
        raise None
    except:
        frame = sys.exc_info()[2].tb_frame.f_back

    # evaluate commands in current namespace
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)

    code.interact("======== Start Happypanda Debugging ========", local=namespace)
    print("======== END ========")

class Result:
    "Encapsulates return values from methods in the interface module"

    class ResultType(enum.Enum):
        Status = 1
        Gallery = 2

    def __init__(self):
        self._galleries = set()

    def toXML(self):
        ""
        pass

## DATABASE ##



## GALLERY ##

def fetchGallery(offset=None, from_gallery=None):
    """
    Fetch galleries from the database.
    Params:
        offset -- where to start fetching from, an int
        from_gallery -- which gallery id(index) to start fetching from, an int
    Returns:
        Gallery objects
    """
    pass

def addGallery(galleries=None, paths=None):
    """
    Add galleries to the database.
    Params:
        galleries -- list of gallery objects parsed from XML
        Returns: Status

        paths -- list of paths to the galleries
        Returns: Gallery objects
    """
    pass



