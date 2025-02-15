import enum

class Ops(enum.Enum):
	add = 1
	subtract = 2
	multiply = 3
	divide = 4
	replace = 5
	square = 6


class Granularity(enum.Enum):
	day = 1
	hour = 2
	minute = 3
	second = 4