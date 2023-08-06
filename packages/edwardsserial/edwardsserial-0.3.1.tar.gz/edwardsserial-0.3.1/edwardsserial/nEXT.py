from edwardsserial.serial_protocol import SerialProtocol


# make this as a descriptor that calls the owners pump start methods if available,
# since TIC does not forward some commands
class nEXT(SerialProtocol):
    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        pass
