import matplotlib.pyplot as plt
from matplotlib.colors import colors
from matplotlib import cm


class MidpointNormalize(colors.Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        result, is_scalar = self.process_value(value)
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.array(np.interp(value, x, y), mask=result.mask, copy=False)


def error_plot(fig, ax, x, y, xerr=None, yerr=None, title='', xlabel='',
               ylabel='Counts', legend=True, label='', drawstyle='steps-mid'):

    ax.errorbar(x, y, xerr=xerr, yerr=yerr, label=label, drawstyle=drawstyle)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if legend:
        ax.legend()


def image_plot(fig, ax, data, cmap=cm.viridis, vmin=None, vmax=None, title='',
               xlabel='Frequency (Mhz)', ylabel='Time Pair',
               cbar_label=None, xticks=None, yticks=None,
               xticklabels=None, yticklabels=None, zero_mask=False,
               mask_color='white', freq_array=None, aspect=None, grid=None):

    if zero_mask:
        data = np.ma.masked_equal(data, 0)

    if vmin is None:
        vmin = np.amin(data)
    if vmax is None:
        vmax = np.amax(data)

    if cmap is cm.coolwarm:
        cax = ax.imshow(data, cmap=cmap, clim=(vmin, vmax),
                        norm=MidpointNormalize(midpoint=0, vmin=vmin, vmax=vmax))
    else:
        cax = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax)

    cmap.set_bad(color=mask_color)
    cbar = fig.colorbar(cax, ax=ax)
    cbar.set_label(cbar_label)

    ax.set_title(title)

    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
    if xticklabels is not None:
        ax.set_xticklabels(xticklabels)
    elif xlabel is 'Frequency (Mhz)':
        xticklabels = ['%.2f' % (freq_array[tick] * 10 ** (-6)) for tick in ax.get_xticks()]
    elif xlabel is '$\lambda u$':
        xticklabels = ['%.0f' % (grid[tick]) for tick in ax.get_xticks()]
    if yticklabels is not None:
        ax.set_yticklabels(yticklabels)
    elif xlabel is '$\lambda v$':
        yticklabels = ['%.0f' % (grid[tick]) for tick in ax.get_yticks()]
    if aspect is not None:
        ax.set_aspect(aspect)
    else:
        ax.set_aspect(data.shape[1] / (data.shape[0] * 2.5))
