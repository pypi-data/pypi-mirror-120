# This file is placed in the Public Domain.

import datetime
import getpass
import inspect
import os
import pwd
import queue
import sys
import threading
import time
import traceback
import types

from .obj import Db, Default, List, Object, cdir, get, update
from .obj import Cfg as ObjCfg

def __dir__():
    return ('Break', 'Bus', 'Client', 'Command', 'Db', 'Default',
            'Dispatcher', 'NotImplemented', 'Error', 'Event', 'Getter',
            'Handler', 'List', 'Loop', 'NoBot', 'NoTxt', 'Object', 'Option',
            'Output', 'Repeater', 'Restart', 'Runtime', 'Setter', 'Skip',
            'Stop', 'Table', 'Thr', 'Timer', 'Token', 'Url', 'Word', 'cdir',
            'day', 'elapsed', 'get_exception', 'getmain', 'getname', 'launch',
            'parse_txt', 'parse_ymd', 'spl', 'starttime')


starttime = time.time()


class NoBot(Exception):

    pass


class NoTxt(Exception):

    pass



class Restart(Exception):

    pass


class Stop(Exception):

    pass


class Break(Exception):

    pass


class NotImplemented(Exception):

    pass


class Thr(threading.Thread):

    def __init__(self, func, *args, thrname="", daemon=True):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self.name = thrname or getname(func)
        self.result = None
        self.queue = queue.Queue()
        self.queue.put_nowait((func, args))
        self.sleep = 0

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self.result

    def run(self):
        func, args = self.queue.get_nowait()
        if args:
            target = vars(args[0])
            if target and "txt" in dir(target):
                self.name = target.txt.split()[0]
        self.setName(self.name)
        self.result = func(*args)


def launch(func, *args, **kwargs):
    name = kwargs.get("name", getname(func))
    t = Thr(func, *args, thrname=name, daemon=True)
    t.start()
    return t


class Bus(Object):

    objs = []

    def __iter__(self):
        return iter(Bus.objs)

    @staticmethod
    def add(obj):
        if obj not in Bus.objs:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        for h in Bus.objs:
            if "announce" in dir(h):
                h.announce(txt)

    @staticmethod
    def byorig(orig):
        for o in Bus.objs:
            if o.__oqn__() == orig:
                return o
        return None

    @staticmethod
    def byfd(fd):
        for o in Bus.objs:
            if o.fd and o.fd == fd:
                return o
        return None

    @staticmethod
    def bytype(typ):
        for o in Bus.objs:
            if isinstance(o, typ):
                return o
        return None

    @staticmethod
    def first(otype=None):
        if Bus.objs:
            if not otype:
                return Bus.objs[0]
            for o in Bus.objs:
                if otype in str(type(o)):
                    return o
        return None

    @staticmethod
    def resume():
        for o in Bus.objs:
            o.resume()

    @staticmethod
    def say(orig, channel, txt):
        for o in Bus.objs:
            if o.__oqn__() == orig:
                o.say(channel, txt)

class Event(Object):

    def __init__(self):
        super().__init__()
        self.channel = None
        self.done = threading.Event()
        self.error = ""
        self.handler = None
        self.exc = None
        self.orig = None
        self.origin = None
        self.prs = Default()
        self.result = []
        self.thrs = []
        self.type = "event"
        self.txt = None

    def bot(self):
        return Bus.byorig(self.orig)

    def parse(self):
        parse_txt(self.prs, self.txt)

    def ready(self):
        self.done.set()

    def reply(self, txt):
        self.result.append(txt)

    def say(self, txt):
        Bus.say(self.orig, self.channel, txt)

    def show(self):
        bot = self.bot()
        if not bot:
            raise NoBot(self.orig)
        if bot.speed == "slow" and len(self.result) > 3:
            Output.append(self.channel, self.result)
            self.say("%s lines in cache, use !mre" % len(self.result))
            return
        for txt in self.result:
            self.say(txt)

    def wait(self, timeout=1.0):
        self.done.wait(timeout)
        for thr in self.thrs:
            thr.join(timeout)


class Command(Event):

    def __init__(self):
        super().__init__()
        self.type = "cmd"


class Error(Event):

    pass


class Dispatcher(Object):

    def __init__(self):
        super().__init__()
        self.cbs = Object()

    def dispatch(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def register(self, k, v):
        self.cbs[str(k)] = v


class Loop(Object):

    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.speed = "normal"
        self.stopped = threading.Event()

    def do(self, e):
        Dispatcher.dispatch(self, e)

    def error(self, txt):
        pass

    def loop(self):
        dorestart = False
        self.stopped.clear()
        while not self.stopped.isSet():
            e = self.queue.get()
            try:
                self.do(e)
            except Restart:
                dorestart = True
                break
            except Stop:
                break
            except Exception:
                if Cfg.bork:
                    raise
                self.error(get_exception())
        if dorestart:
            self.restart()

    def restart(self):
        self.stop()
        self.start()

    def put(self, e):
        self.queue.put_nowait(e)

    def start(self):
        launch(self.loop)
        return self

    def stop(self):
        self.stopped.set()
        self.queue.put(None)


class Handler(Dispatcher, Loop):

    def __init__(self):
        Dispatcher.__init__(self)
        Loop.__init__(self)

    def event(self, txt):
        if txt is None:
            return None
        c = Command()
        c.txt = txt or ""
        c.orig = self.__oqn__()
        return c

    def handle(self, clt, e):
        Loop.put(self, e)

    def loop(self):
        while not self.stopped.isSet():
            try:
                txt = self.poll()
            except (ConnectionRefusedError, ConnectionResetError) as ex:
                self.error(str(ex))
                break
            if txt is None:
                self.error("%s stopped" % getname(self))
                break
            e = self.event(txt)
            if not e:
                self.error("%s stopped" % getname(self))
                return
            self.handle(self, e)

    def poll(self):
        return self.queue.get()

    def start(self):
        super().start()
        Bus.add(self)


class Client(Handler):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        Bus.add(self)

    def handle(self, clt, e):
        Runtime.put(self, e)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)


class Output(Object):

    cache = List()

    def __init__(self):
        Object.__init__(self)
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()

    @staticmethod
    def append(channel, txtlist):
        if channel not in Output.cache:
            Output.cache[channel] = []
        Output.cache[channel].extend(txtlist)

    def dosay(self, channel, txt):
        pass

    def oput(self, channel, txt):
        self.oqueue.put_nowait((channel, txt))

    def output(self):
        while not self.dostop.isSet():
            (channel, txt) = self.oqueue.get()
            if self.dostop.isSet() or channel is None:
                break
            self.dosay(channel, txt)

    @staticmethod
    def size(name):
        if name in Output.cache:
            return len(Output.cache[name])
        return 0

    def start(self):
        self.dostop.clear()
        launch(self.output)
        return self

    def stop(self):
        self.dostop.set()
        self.oqueue.put_nowait((None, None))


class Cfg(Default):

    console = False
    daemon = False
    debug = False
    systemd = False
    verbose = False


class Runtime(Dispatcher, Loop):

    cfg = Cfg()
    classes = Object()
    cmds = Object()
    opts = Object()
    prs = Default()

    def __init__(self):
        Dispatcher.__init__(self)
        Loop.__init__(self)
        self.register("cmd", Runtime.handle)

    def add(self, cmd):
        Table.add(cmd)

    @staticmethod
    def cmd(clt, txt):
        if not txt:
            return None
        e = clt.event(txt)
        e.origin = "root@shell"
        Runtime.handle(clt, e)
        e.wait()
        return None

    def do(self, e):
        self.dispatch(e)

    def error(self, txt):
        pass

    @staticmethod
    def handle(clt, obj):
        obj.parse()
        f = None
        mn = get(Table.modnames, obj.prs.cmd, None)
        if mn:
            mod = sys.modules.get(mn, None)
            if mod:
                f = getattr(mod, obj.prs.cmd, None)
        if not f:
            f = get(Runtime.cmds, obj.prs.cmd, None)
        if f:
            f(obj)
            obj.show()
        obj.ready()

    def init(self, mns, threaded=False):
        for mn in spl(mns):
            mod = sys.modules.get(mn, None)
            i = getattr(mod, "init", None)
            if i:
                self.log("init %s" % mn)
                if threaded:
                    launch(i, self)
                else:
                    i(self)

    def log(self, txt):
        pass

    @staticmethod
    def opt(ops):
        if not Runtime.opts:
            return False
        for opt in ops:
            if opt in Runtime.opts:
                return True
        return False

    def parse_cli(self):
        o = Default()
        txt = " ".join(sys.argv[1:])
        if txt:
            parse_txt(o, txt)
        if o.sets:
            update(self.cfg, o.sets)
        if o.index:
            self.cfg.index = o.index
        if o.opts:
            update(Runtime.opts, o.opts)
        update(self.prs, o)
        Cfg.console = Runtime.opt("c")
        Cfg.daemon = Runtime.opt("d")
        Cfg.debug = Runtime.opt("z")
        Cfg.systemd = Runtime.opt("s")
        Cfg.verbose = Runtime.opt("v")

    @staticmethod
    def privileges(name=None):
        if os.getuid() != 0:
            return None
        try:
            pwn = pwd.getpwnam(name)
        except (TypeError, KeyError):
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except (TypeError, KeyError):
                return None
        if name is None:
            try:
                name = getpass.getuser()
            except (TypeError, KeyError):
                pass
        try:
            pwn = pwd.getpwnam(name)
        except (TypeError, KeyError):
            return False
        try:
            os.chown(ObjCfg.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        os.setgroups([])
        os.setgid(pwn.pw_gid)
        os.setuid(pwn.pw_uid)
        os.umask(0o22)
        return True

    @staticmethod
    def root():
        if os.geteuid() != 0:
            return False
        return True

    @staticmethod
    def skel():
        assert ObjCfg.wd
        cdir(ObjCfg.wd+os.sep)
        cdir(os.path.join(ObjCfg.wd, "store", ""))

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)



class Table(Object):

    classes = Object()
    modnames = Object()
    names = List()

    @staticmethod
    def add(func):
        n = func.__name__
        Table.modnames[n] = func.__module__

    @staticmethod
    def addcls(cls):
        Table.classes[cls.__name__] = cls
        Table.names.append(
            cls.__name__.lower(), "%s.%s" % (cls.__module__, cls.__name__)
        )

    @staticmethod
    def addmod(mod):
        Table.introspect(mod)

    @staticmethod
    def introspect(mod):
        for _k, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1 and "event" in o.__code__.co_varnames:
                Table.add(o)
        for _k, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                Table.addcls(o)


class Timer(Object):

    def __init__(self, sleep, func, *args, name=None):
        super().__init__()
        self.args = args
        self.func = func
        self.sleep = sleep
        self.name = name or ""
        self.state = Object()
        self.timer = None

    def run(self):
        self.state.latest = time.time()
        launch(self.func, *self.args)

    def start(self):
        if not self.name:
            self.name = getname(self.func)
        timer = threading.Timer(self.sleep, self.run)
        timer.setName(self.name)
        timer.setDaemon(True)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def stop(self):
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    def run(self):
        thr = launch(self.start)
        super().run()
        return thr


class Token(Object):

    pass


class Word(Token):

    def __init__(self, txt=None):
        super().__init__()
        if txt is None:
            txt = ""
        self.txt = txt


class Option(Token):

    def __init__(self, txt):
        super().__init__()
        if txt.startswith("--"):
            self.opt = txt[2:]
        elif txt.startswith("-"):
            self.opt = txt[1:]


class Getter(Token):

    def __init__(self, txt):
        super().__init__()
        if "==" in txt:
            pre, post = txt.split("==", 1)
        else:
            pre = post = ""
        if pre:
            self[pre] = post


class Setter(Token):

    def __init__(self, txt):
        super().__init__()
        if "=" in txt:
            pre, post = txt.split("=", 1)
        else:
            pre = post = ""
        if pre:
            self[pre] = post


class Skip(Token):

    def __init__(self, txt):
        super().__init__()
        pre = ""
        if txt.endswith("-"):
            if "=" in txt:
                pre, _post = txt.split("=", 1)
            elif "==" in txt:
                pre, _post = txt.split("==", 1)
            else:
                pre = txt
        if pre:
            self[pre] = True


class Url(Token):

    def __init__(self, txt):
        super().__init__()
        self.url = ""
        if txt.startswith("http"):
            self.url = txt


def day():
    return str(datetime.datetime.today()).split()[0]


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    year = 365 * 24 * 60 * 60
    week = 7 * 24 * 60 * 60
    nday = 24 * 60 * 60
    hour = 60 * 60
    minute = 60
    years = int(nsec / year)
    nsec -= years * year
    weeks = int(nsec / week)
    nsec -= weeks * week
    nrdays = int(nsec / nday)
    nsec -= nrdays * nday
    hours = int(nsec / hour)
    nsec -= hours * hour
    minutes = int(nsec / minute)
    sec = nsec - minutes * minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def find(name, selector=None, index=None, timed=None):
    db = Db()
    for n in get(Table.names, name, [name,],):
        for fn, o in db.find(n, selector, index, timed):
            yield fn, o


def get_exception(txt="", sep=" "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        if elem[0].endswith(".py"):
            plugfile = elem[0][:-3].split(os.sep)
        else:
            plugfile = elem[0].split(os.sep)
        mod = []
        for element in plugfile[:-2:-1]:
            mod.append(element.split(".")[-1])
        ownname = ".".join(mod[::-1])
        result.append("%s:%s" % (ownname, elem[1]))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res


def getmain(name):
    return getattr(sys.modules["__main__"], name, None)


def getname(o):
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    if "__self__" in dir(o):
        return "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    if "__class__" in dir(o) and "__name__" in dir(o):
        return "%s.%s" % (o.__class__.__name__, o.__name__)
    if "__class__" in dir(o):
        return o.__class__.__name__
    if "__name__" in dir(o):
        return o.__name__
    return None


def listfiles(workdir):
    path = os.path.join(ObjCfg.wd, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def parse_txt(o, ptxt=None):
    if ptxt is None:
        raise NoTxt(o)
    o.txt = ptxt
    o.otxt = ptxt
    o.gets = Object()
    o.opts = Object()
    o.timed = []
    o.index = None
    o.sets = Object()
    o.skip = Object()
    args = []
    for t in [Word(txt) for txt in ptxt.rsplit()]:
        u = Url(t.txt)
        if u and "url" in u and u.url:
            args.append(u.url)
        s = Skip(t.txt)
        if s:
            update(o.skip, s)
            t.txt = t.txt[:-1]
        s = Setter(t.txt)
        if s:
            update(o.sets, s)
            continue
        g = Getter(t.txt)
        if g:
            update(o.gets, g)
            continue
        opt = Option(t.txt)
        if opt:
            try:
                o.index = int(opt.opt)
                continue
            except ValueError:
                pass
            if len(opt.opt) > 1:
                for op in opt.opt:
                    o.opts[op] = True
            else:
                o.opts[opt.opt] = True
            continue
        args.append(t.txt)
    if not args:
        o.args = []
        o.cmd = ""
        o.rest = ""
        o.txt = ""
        return o
    o.cmd = args[0]
    o.args = args[1:]
    o.txt = " ".join(args)
    o.rest = " ".join(args[1:])
    return o


def parse_ymd(daystr):
    valstr = ""
    val = 0
    total = 0
    for c in daystr:
        if c in "1234567890":
            vv = int(valstr)
        else:
            vv = 0
        if c == "y":
            val = vv * 3600 * 24 * 365
        if c == "w":
            val = vv * 3600 * 24 * 7
        elif c == "d":
            val = vv * 3600 * 24
        elif c == "h":
            val = vv * 3600
        elif c == "m":
            val = vv * 60
        else:
            valstr += c
        total += val
    return total


def spl(txt):
    return [x for x in txt.split(",") if x]
