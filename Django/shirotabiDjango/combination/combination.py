
import numpy as np
from abc import ABC,abstractmethod

class Combination(ABC):
  def __init__(self,horse_num):
    if type(horse_num) != list and not isinstance(horse_num,np.ndarray):
        horse_num = int(horse_num)
        horse_num = list(range(1, horse_num + 1))

    if type(horse_num) == list:
        horse_num = [int(num) for num in horse_num]
    else:
        horse_num = horse_num.astype(int)
    self.horse_num = np.array(horse_num)

  @abstractmethod
  def combination_ticket(self):
    pass

class CombinationBracketQuinella(Combination):
  def combination_ticket(self):
    if len(self.horse_num) <= 7:
      return False

    waku = [i for i in range(1,9)]
    combination = []
    for index,first in enumerate(waku):
      for second in waku[index:]:
        combination.append(str(first) + '-' + str(second))
    return combination

class CombinationQuinella(Combination):
  def combination_ticket(self):
    combination = []
    for first in self.horse_num:
      for second in  self.horse_num[first:]:
        combination.append(str(first) + '-' + str(second))
    return combination

class CombinationExacta(Combination):
  def combination_ticket(self):
    combination = []
    for _,first in enumerate(self.horse_num):
      for second in self.horse_num[self.horse_num != first]:
        combination.append(str(first) + '-' + str(second))
    return combination

class CombinationQuinellaPlace(CombinationQuinella):
  pass

class CombinationTrio(Combination):
  def combination_ticket(self):
    combination = []
    for first in self.horse_num:
      for second in self.horse_num[first:-1]:
        for third in self.horse_num[second:]:
          combination.append(str(first) + '-' + str(second) + '-' + str(third))
    return combination

class CombinationTrifecta(Combination):
  def combination_ticket(self):
    combination = []
    for _,first in  enumerate(self.horse_num):
      for _,second in enumerate(self.horse_num[self.horse_num != first]):
        for _,third in enumerate(self.horse_num[(self.horse_num != first) &(self.horse_num != second)]):
          combination.append(str(first) + '-' + str(second) + '-' + str(third))
    return combination

class MakeCombination(object):
    def _make_combination(self, obj):
        return obj.combination_ticket()

class TicketCombination(MakeCombination):

  def combination_bracket(self,horse_num):
    return self._make_combination(CombinationBracketQuinella(horse_num))

  def combination_exacta(self,horse_num):
    return self._make_combination(CombinationExacta(horse_num))

#combination_quinella and quinella place is same
  def combination_quinella(self,horse_num):
    return self._make_combination(CombinationQuinella(horse_num))

  def combination_quinella_place(self,horse_num):
    return self._make_combination(CombinationQuinella(horse_num))
  
  def combination_trio(self,horse_num):
    return self._make_combination(CombinationTrio(horse_num))
  
  def combination_trifecta(self,horse_num):
    return self._make_combination(CombinationTrifecta(horse_num))

