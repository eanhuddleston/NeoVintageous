from sublime import Region

import NeoVintageous.nv.ex.plat as plat
import NeoVintageous.nv.ex.plat.linux  # FIXME # noqa: F401
import NeoVintageous.nv.ex.plat.osx  # FIXME # noqa: F401
import NeoVintageous.nv.ex.plat.windows  # FIXME # noqa: F401


def run_and_wait(view, cmd):
    if plat.HOST_PLATFORM == plat.WINDOWS:
        plat.windows.run_and_wait(view, cmd)
    elif plat.HOST_PLATFORM == plat.LINUX:
        plat.linux.run_and_wait(view, cmd)
    elif plat.HOST_PLATFORM == plat.OSX:
        plat.osx.run_and_wait(view, cmd)
    else:
        raise NotImplementedError


def run_and_read(view, cmd):
    if plat.HOST_PLATFORM == plat.WINDOWS:
        return plat.windows.run_and_read(view, cmd)
    elif plat.HOST_PLATFORM == plat.LINUX:
        return plat.linux.run_and_read(view, cmd)
    elif plat.HOST_PLATFORM == plat.OSX:
        return plat.osx.run_and_read(view, cmd)
    else:
        raise NotImplementedError


def filter_thru_shell(view, edit, regions, cmd):
    # XXX: make this a ShellFilter class instead
    if plat.HOST_PLATFORM == plat.WINDOWS:
        filter_func = plat.windows.filter_region
    elif plat.HOST_PLATFORM == plat.LINUX:
        filter_func = plat.linux.filter_region
    elif plat.HOST_PLATFORM == plat.OSX:
        filter_func = plat.osx.filter_region
    else:
        raise NotImplementedError

    # Maintain text size delta as we replace each selection going forward.
    # We can't simply go in reverse because cursor positions will be incorrect.
    accumulated_delta = 0
    new_points = []
    for r in regions:
        r_shifted = Region(r.begin() + accumulated_delta, r.end() + accumulated_delta)
        rv = filter_func(view, view.substr(r_shifted), cmd).rstrip() + '\n'
        view.replace(edit, r_shifted, rv)
        new_points.append(r_shifted.a)
        accumulated_delta += len(rv) - r_shifted.size()

    # Switch to normal mode and move cursor(s) to beginning of replacement(s)
    view.run_command('_enter_normal_mode')
    view.sel().clear()
    view.sel().add_all(new_points)
