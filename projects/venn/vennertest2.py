import matplotlib

from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles

'''
Let's make a Venn diagram.

http://matthiaseisen.com/pp/patterns/p0145/

In your virtualenv, you need:
matplotlib-venn==0.11.4

On a Mac, you need this:
$ cat ~/.matplotlib/matplotlibrc
backend: TkAgg

The above fixes the problem described in:
http://stackoverflow.com/questions/29433824/unable-to-import-matplotlib-pyplot-as-plt-in-virtualenv
'''

matplotlib.use('TkAgg')

s = (2, 3, 4, 3, 1, 0.5, 4)

v = venn3(subsets=s, set_labels=('A', 'B', 'C'))

# Subset labels
v.get_label_by_id('100').set_text('cowA1')
v.get_label_by_id('100').set_text('cowA2')
v.get_label_by_id('010').set_text('aBc')
v.get_label_by_id('110').set_text('ABc')
v.get_label_by_id('001').set_text('abC')
v.get_label_by_id('101').set_text('AbC')
v.get_label_by_id('011').set_text('aBC')
v.get_label_by_id('111').set_text('ABC')

# Subset colors
v.get_patch_by_id('100').set_color('c')
v.get_patch_by_id('010').set_color('#993333')
v.get_patch_by_id('110').set_color('blue')

# Subset alphas
v.get_patch_by_id('101').set_alpha(0.4)
v.get_patch_by_id('011').set_alpha(1.0)
v.get_patch_by_id('111').set_alpha(0.7)

# Border styles
c = venn3_circles(subsets=s, linestyle='solid')
c[0].set_ls('dotted')  # Line style
c[1].set_ls('dashed')
c[2].set_lw(1.0)       # Line width

plt.show()

