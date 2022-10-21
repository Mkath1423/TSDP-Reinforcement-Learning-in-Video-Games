import logging

f = logging.FileHandler("a.log")

a = logging.getLogger("a")
a.setLevel(logging.DEBUG)

b = logging.getLogger("b")
b.setLevel(logging.DEBUG)


a.error("test error from a")
b.error("test error from b")