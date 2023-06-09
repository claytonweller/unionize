import random

# TODO will need to increase the total number of posibilities here
adjectives = [
    'Amicable', 'Bouyant', 'Clever', 'Driven', 'Energized', 'Funny', 'Great', 'Honorable', 'Iconic',
    'Just', 'Kind', 'Lovable', 'Merry', 'Nice', 'Original', 'Peppy', 'Quick', 'Radiant', 'Super',
    'Terrific', 'Utmost', 'Vivacious', 'Wonderful', 'Xray', 'Young', 'Zippy'
]

nouns = [
    'Ant', 'Bird', 'Cat', 'Dog', 'Eagle', 'Fish', 'Goat', 'Horse', 'Ibex', 'Jaguar', 'Kiwi',
    'Lemur', 'Moose', 'Newt', 'Owl', 'Parrot', 'Quail', 'Rabbit', 'Snake', 'Tiger', 'Urial',
    'Vole', 'Whale', 'Xerus', 'Yak', 'Zebra'
]


def generate_pseydonym():
    return random.choice(adjectives)+random.choice(nouns)
