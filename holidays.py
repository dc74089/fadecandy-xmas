def get_holidays():
    specialdays = {}
    specialdays[(2, 14)] = ((255, 116, 140), (255, 0, 0), (255, 255, 175)) # Valentines Day
    specialdays[(2, 17)] = ((255, 0, 0), (255, 255, 175), (0, 0, 255))  # President's Day YEARLY
    specialdays[(3, 17)] = ((0, 255, 0), (255, 255, 175)) # St. Patrick's
    specialdays[(4, 2)] = ((0, 170, 255), (255, 255, 175))  # Light it up blue
    specialdays[(4, 12)] = ((255, 141, 161), (255, 255, 128), (192, 255, 244))  # Easter YEARLY
    specialdays[(5, 5)] = ((255, 0, 0), (0, 255, 0), (255, 255, 175))  # Cinco de Mayo
    specialdays[(5, 25)] = ((0, 0, 255), (255, 255, 175), (255, 0, 0)) # Memorial Day YEARLY
    specialdays[(7, 4)] = ((255, 0, 0), (255, 255, 175), (0, 0, 255))  # Independence Day
    specialdays[(7, 27)] = ((255, 107, 102), (255, 151, 74), (255, 233, 0), (142, 227, 213), (255, 99, 177))  # Mom's Bday
    specialdays[(10, 31)] = ((150, 0, 128), (255, 165, 0)) #Halloween
    specialdays[(11, 11)] = ((255, 0, 0), (255, 255, 175), (0, 0, 255)) # Veteran's Day
    specialdays[(11, 25)] = ((255, 165, 0), (255, 255, 0), (255, 0, 0)) # Thanksgiving Eve YEARLY
    specialdays[(11, 26)] = ((255, 165, 0), (255, 255, 0), (255, 0, 0)) # Thanksgiving YEARLY

    return specialdays
