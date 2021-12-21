file = open("input.txt")
lines = list(map(lambda x : x.strip(), file.readlines()))

algorithm = lines.pop(0)
lines.pop(0)

height = len(lines)
width = len(lines[0])

def create_new_surface(algorithm, current_surface):
    if current_surface == '#':
        return algorithm[511]
    else:
        return algorithm[0]

def adjacents(x, y):
    return [
        (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
        (x, y - 1), (x, y), (x, y + 1),
        (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)
    ]

def to_zero_or_one(c):
    if c == '#':
        return '1'
    else:
        return '0'

def pixel(p: (int, int), image, surface):
    height = len(image)
    width = len(image[0])
    (x, y) = (p[0], p[1])
    if x < 0 or x >= height or y < 0 or y >= width:
        return surface
    else:
        return image[x][y]
    
def transform(p: (int, int), image, surface):
    chars = []
    for a in adjacents(p[0], p[1]):
        chars.append(to_zero_or_one(pixel(a, image, surface)))
    return int(''.join(chars), base=2)

def print_image(image):
    for line in image:
        print(''.join(line))

surface = '.'
new_image = lines
for step in range(50):
    old_image = new_image
    height = len(old_image)
    width = len(old_image[0])
    new_image = []
    for h in range(-1, height+1):
        new_image.append([])
        for w in range(-1,width+1):
            decimal_number = transform((h, w), old_image, surface)
            final_pixel = algorithm[decimal_number]
            new_image[h+1].append(final_pixel)
    print_image(new_image)
    print()
    surface = create_new_surface(algorithm, surface)


sum = 0
for row in new_image:
    sum += row.count('#')
print(sum)


