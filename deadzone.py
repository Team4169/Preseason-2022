def addDeadzone(x, y):
    newX = 1.1 * (x - 0.1)
    newY = 1.1 * (y - 0.1)
    if newX < 0:
        newX = 0
    if newY < 0:
        newY = 0
    return {
        "x": newX,
        "y": newY
    }