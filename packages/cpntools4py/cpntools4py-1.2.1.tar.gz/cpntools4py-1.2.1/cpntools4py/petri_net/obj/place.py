class Place:
  def __init__(self, params):
    self.text = params['text']
    self.type = params['type']
    # self.__initmark = params['initmark']
    self._tokens = params['initmark']

  def __repr__(self):
    return f'<Place(text={self.text}, type={self.type}, tokens={self.tokens})>'

  def __str__(self):
    return str(self.__dict__)

  def __eq__(self, other):
    if not isinstance(other, Place):
        return False
    return self.text == other.text

  def __hash__(self):
      return hash(self.text)

  @property
  def tokens(self):
    if self._tokens is None:
      return

    if self.type == 'UNIT':
      token = self._tokens.replace('`()','')
      return int(token)
    else:
      tokens = []
      for text in self._tokens.replace('\n','').split('++'):
        token = text.split('`')
        tokens += [token[1]] * int(token[0])

      return tokens
  
  @tokens.setter
  def tokens(self, tokens):
    self._tokens = tokens