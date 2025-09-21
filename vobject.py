"""Mock vobject module for testing CLI changes"""

class MockVCard:
    def __init__(self):
        self.fn = MockProperty("Test User")
        self.uid = MockProperty("test-uid-123")
        self.n = MockProperty(MockName())
        
class MockName:
    def __init__(self):
        self.family = "User"
        self.given = "Test"

class MockProperty:
    def __init__(self, value):
        self.value = value

def readOne(content):
    return MockVCard()