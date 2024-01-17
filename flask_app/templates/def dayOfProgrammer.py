def dayOfProgrammer(year):
    months = [31, 28, 31, 30, 31, 30, 31, 31]
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 or year <= 1917 and year % 4 == 0:
        months[1] = 29
    sum = 0
    for mon in months:
        sum += mon
    day = 256 - sum
    if year == 1918:
        day += 13
    return f'{day}.09.{year}'


print(dayOfProgrammer(1918))