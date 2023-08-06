class ByteReader:
  def __init__(self, file_input):
    self.file_input = file_input

  def readByte(self):
    return self.file_input.read(1)

  def readByteAsInt(self):
    return int.from_bytes(self.readByte(), "big")

  def readString(self):
    length = int.from_bytes(self.readByte(), "big")
    return self.readStringLength(length if (length < 0xff) else self.readShort())

  def readStringLength(self, length):
    return self.file_input.read(length).decode('utf-8')

  def readInt(self):
    bytes = self.file_input.read(4)
    return ((bytes[3] & 0xff) << 24) | ((bytes[2] & 0xff) << 16) | ((bytes[1] & 0xff) << 8) | (bytes[0] & 0xff)

  def readShort(self):
    bytes = self.file_input.read(2)
    return ((bytes[1] & 0xff) << 8) | (bytes[0] & 0xff)

  def readBoolean(self):
    bool = int.from_bytes(self.readByte(), "big") > 0
    return bool

  def skip(self, bytes):
    self.file_input.read(bytes)

