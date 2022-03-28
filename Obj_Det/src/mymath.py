
def count_new_coord(big0: int, small0: int, big1: int, small1: int, size_of_smaller_side: int) \
        -> tuple[int, int, int, int]:
    # 'big' according to a bigger side of the rectangle
    # 'small' - to a small one
    # example: rectangle with width bigger than height: big0: x0, big1: x1, small0: y0, small1: y1

    bigger_size, smaller_size = big1 - big0, small1 - small0

    dif = bigger_size - smaller_size
    sq_size = bigger_size
    if sq_size >= size_of_smaller_side:
        small0, small1 = 0, size_of_smaller_side
        razn = bigger_size - size_of_smaller_side
        big0 += razn/2
        big1 -= razn/2
    else:
        if (small0-dif/2) <= 0:
            razn = dif/2 - small0
            small0 = 0
            small1 += dif/2 + razn
            if small1 >= size_of_smaller_side:
                crop = (dif/2 + razn) - (size_of_smaller_side - small1)
                small1 = size_of_smaller_side
                big0 += crop/2
                big1 -= crop/2
        else:
            if (small1+dif/2) >= size_of_smaller_side:
                razn = dif/2 - (size_of_smaller_side - small1)
                small1 = size_of_smaller_side
                small0 -= dif/2 + razn
                if small0 <= 0:
                    crop = (dif/2 + razn) - small0
                    small0 = 0
                    big0 += crop/2
                    big1 -= crop/2
            else:
                small0 -= dif/2
                small1 += dif/2

    return big0, small0, big1, small1


def equalize(x0: float, y0: float, x1: float, y1: float) -> tuple[int, int, int, int]:
    resx0, resy0 = int(x0), int(y0)
    resx1, resy1 = int(x1), int(y1)
    res_h, res_w = resy1 - resy0, resx1 - resx0

    resx1 = resx1 - (res_w - res_h) if res_w > res_h else resx1
    resy1 = resy1 - (res_h - res_w) if res_h > res_w else resy1

    return resx0, resy0, resx1, resy1


def sq_from_rect(x0: float, y0: float, x1: float, y1: float, height: int, width: int) -> tuple[int, int, int, int]:
    def extra_side_check(x0, y0, x1, y1):
        x0 = 0 if x0 < 0 else x0
        y0 = 0 if y0 < 0 else y0
        x1 = width if x1 > width else x1
        y1 = height if y1 > height else y1

        return x0, y0, x1, y1

    x0, y0, x1, y1 = extra_side_check(x0, y0, x1, y1)
    rect_width, rect_height = x1 - x0, y1 - y0

    if rect_width > rect_height:
        x0, y0, x1, y1 = count_new_coord(big0=x0, small0=y0, big1=x1, small1=y1, size_of_smaller_side=height)
    elif rect_width < rect_height:
        y0, x0, y1, x1 = count_new_coord(big0=y0, small0=x0, big1=y1, small1=x1, size_of_smaller_side=width)

    x0, y0, x1, y1 = equalize(x0=x0, y0=y0, x1=x1, y1=y1)

    return x0, y0, x1, y1
