
def font(family, weight, size):
    return {
    'family': family,
    'weight': weight,
    'size': size,
    }

TimesNewRoman = lambda size=20, bold=False : font( 
    'Times New Roman',
    'bold' if bold else 'normal',
    size,
)

ComicSansMS = lambda size=20, bold=False : font( 
    'Comic Sans MS',
    'bold' if bold else 'normal',
    size,
)
