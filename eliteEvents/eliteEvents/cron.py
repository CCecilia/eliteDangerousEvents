from website.views import Utility


def dailyClean():
	Utility.cleanEndedEvents()

	return


def hourlyClean():
	Utility.cleanOldLfgPosts()

	return
