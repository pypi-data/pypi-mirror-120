from foo.constants import CATEGORY_COL
import pandas as pd

df = pd.DataFrame([['a', 1], ['b', None]], columns=[CATEGORY_COL, 'value'])

if __name__ == '__main__':
    print(df)