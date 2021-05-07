import numpy as np

Nt = 21


def dist(_t1, _t2):
    _d = _t2 - _t1
    if _d < 0:
        _d += Nt - 1
    return _d


def half_of(_d):
    if _d in [1, 2]:
        _h = 1
    if _d in [3, 4]:
        _h = 2
    if _d in [5, 6]:
        _h = 3
    return _h


class Luvly:
    def __init__(self, rudder, adv_rudder=0, verbose=False):
        self.rudder = rudder
        self.adv_rudder = adv_rudder
        self.verbose = verbose
        self.pearl = 0
        self.coral = 0
        self.coral_levels = {3: 1, 10: 1, 15: 1}
        self.double = False
        self.double_coral = False
        self.backwards = False
        self.half = False
        self.t = 0

    def luvly_print(self, sth):
        if self.verbose:
            print(sth)

    def land_on(self, _t):
        for _ct, _cl in self.coral_levels.items():
            if (1 <= dist(self.t, _ct) <= 6) and (dist(_ct, _t) <= 6):
                if self.double_coral:
                    self.coral += 2 * (_cl + 2)
                    self.double_coral = False
                else:
                    self.coral += _cl + 2
                self.luvly_print(f"Get coral: {self.coral}")
                break

        self.t = _t
        self.luvly_print(f"Lands on: {self.t}")

        if _t in self.coral_levels.keys():
            if self.coral_levels[_t] < 3:
                self.coral_levels[_t] += 1
                self.luvly_print(f"Level up: {_t} {self.coral_levels[_t]}")

        if _t in [1, 11]:
            self.pearl += 10
            self.luvly_print(f"Get pearl: {self.pearl}")

        if _t in [6, 16]:
            self.pearl += 15
            self.luvly_print(f"Get pearl: {self.pearl}")

        if _t == 12:
            self.adv_rudder += 1
            self.luvly_print(f"Get adv rudder: {self.adv_rudder}")

        if _t == 17:
            self.rudder += 1
            self.luvly_print(f"Get rudder: {self.rudder}")

        if _t == 7:
            self.half = True
            self.luvly_print(f"Half: {self.half}")

        # Conch Block Effect:
        # 1 Gain an additional :rudder:  next turn.
        # 2 Teleport to starting point.
        # 3 Double the roll next turn.
        # 4 Randomly increase the level of a block by 1. If all are level 3, then no effect.
        # 5 Randomly decrease the level of a block by 1. If all are level 1, then no effect.
        # 6 Double the next :coral:  acquire.
        # 7 Get an :rescart:
        # 8 If next roll lands on a resource block, lose the corresponding resource.
        # 9 go backwards next turn
        if _t == 2:
            _conch = np.random.randint(1, 9 + 1)
            self.luvly_print(f"Conch: {_conch}")

            if _conch == 1:
                self.rudder += 1
                self.luvly_print(f"Get rudder: {self.rudder}")

            if _conch == 2:
                self.t = 0
                self.luvly_print(f"Restart: {self.t}")

            if _conch == 3:
                self.double = True
                self.luvly_print(f"Double: {self.double}")

            if _conch == 6:
                self.double_coral = True
                self.luvly_print(f"Double coral: {self.double_coral}")

            if _conch == 9:
                self.backwards = True
                self.luvly_print(f"Backwards: {self.backwards}")

    def assign(self, _d):
        if _d == 0:
            self.roll()
        elif self.adv_rudder < 1:
            self.luvly_print(f"No adv rudder: {self.adv_rudder}")
        else:
            self.adv_rudder -= 1
            self.advance(_d)

    def roll(self):
        if self.rudder < 1:
            self.luvly_print(f"No rudder: {self.rudder}")
            return
        _d = np.random.randint(1, 6 + 1)
        self.rudder -= 1
        self.advance(_d)

    def advance(self, _d):
        _dd = _d

        if self.double:
            _dd *= 2
            self.double = False
            self.luvly_print(f"Double: {self.double}")

        if self.half:
            _dd = half_of(_dd)
            self.half = False
            self.luvly_print(f"Half: {self.half}")

        if self.backwards:
            _dd = -_dd
            self.backwards = False
            self.luvly_print(f"Backwards: {self.backwards}")

        _nt = self.t + _dd
        if _nt >= Nt:
            _nt = _nt - Nt + 1
        if _nt <= 0:
            _nt = _nt + Nt - 1

        self.luvly_print(f"Advance: {_dd} \t Go to {_nt}")
        self.land_on(_nt)

    def keep_rolling(self, _strategy, verbose=False):
        self.verbose = verbose
        while self.rudder > 0 or self.adv_rudder > 0:
            self.assign(_strategy(self))

        # print(self.coral, self.pearl)
        return np.array([self.coral, self.pearl])


def benchmark(_l: Luvly):
    _d = dist(_l.t, 12)
    if (3 <= _d <= 6) and (not _l.half) and (_l.adv_rudder > 0):
        return _d
    if (_l.adv_rudder > 0) and (_l.rudder == 0):
        return 6
    return 0


# Luvly(78).keep_rolling(benchmark, True)
