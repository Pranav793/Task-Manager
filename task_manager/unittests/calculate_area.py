
def calculate_square_area(side):
    """
    Calculates the area of a square, given a side
    """
    # print(side)

    try:
        side == float(side)
    except Exception as e:
        print(e)
        return -1
    return side*side