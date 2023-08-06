from typing import Type


class Transition:
  def __init__(self, params):
    self.text = params['text']
    self._time = params['time']

  def __repr__(self):
    return f'<Transition(text={self.text}, time={self.time})>'

  def __str__(self):
    return str(self.__dict__)

  def __eq__(self, other):
    if not isinstance(other, Transition):
        return False
    return self.text == other.text

  def __hash__(self):
      return hash(self.text)

  @property
  def time(self):
    if self._time is None:
      return

    time = int(self._time.replace('@+',''))
    return time

  @time.setter
  def time(self, time):
    if type(time) == int:
      raise TypeError('time attribute must be a string')

    self._time = time