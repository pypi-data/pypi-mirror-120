import numpy as np
import sys
import pickle
import os
import io
from unittest.runner import _WritelnDecorator
import inspect
import colorama
import unittest
import time
import textwrap
from unitgrade import ActiveProgress
from unitgrade.utils import gprint, Capturing2
colorama.init(autoreset=True)  # auto resets your settings after every output

def setup_dir_by_class(C, base_dir):
    name = C.__class__.__name__
    return base_dir, name


class Report:
    title = "report title"
    version = None
    questions = []
    pack_imports = []
    individual_imports = []
    nL = 120  # Maximum line width
    _config = None  # Private variable. Used when collecting results from student computers. Should only be read/written by teacher and never used for regular evaluation.

    @classmethod
    def reset(cls):
        for (q, _) in cls.questions:
            if hasattr(q, 'reset'):
                q.reset()

    @classmethod
    def mfile(clc):
        return inspect.getfile(clc)

    def _file(self):
        return inspect.getfile(type(self))

    def _import_base_relative(self):
        if hasattr(self.pack_imports[0], '__path__'):
            root_dir = self.pack_imports[0].__path__._path[0]
        else:
            root_dir = self.pack_imports[0].__file__

        root_dir = os.path.dirname(root_dir)
        relative_path = os.path.relpath(self._file(), root_dir)
        modules = os.path.normpath(relative_path[:-3]).split(os.sep)
        return root_dir, relative_path, modules

    def __init__(self, strict=False, payload=None):
        working_directory = os.path.abspath(os.path.dirname(self._file()))
        self.wdir, self.name = setup_dir_by_class(self, working_directory)
        # self.computed_answers_file = os.path.join(self.wdir, self.name + "_resources_do_not_hand_in.dat")
        for (q, _) in self.questions:
            q.nL = self.nL  # Set maximum line length.

        if payload is not None:
            self.set_payload(payload, strict=strict)

    def main(self, verbosity=1):
        # Run all tests using standard unittest (nothing fancy).
        loader = unittest.TestLoader()
        for q, _ in self.questions:
            start = time.time()  # A good proxy for setup time is to
            suite = loader.loadTestsFromTestCase(q)
            unittest.TextTestRunner(verbosity=verbosity).run(suite)
            total = time.time() - start
            q.time = total

    def _setup_answers(self, with_coverage=False):
        if with_coverage:
            for q, _ in self.questions:
                q._with_coverage = True
                q._report = self

        from unitgrade import evaluate_report_student
        evaluate_report_student(self, unmute=True)

        # self.main()  # Run all tests in class just to get that out of the way...
        report_cache = {}
        for q, _ in self.questions:
            # print(self.questions)
            if hasattr(q, '_save_cache'):
                q()._save_cache()
                print("q is", q())
                # q()._cache_put('time', q.time) # = q.time
                report_cache[q.__qualname__] = q._cache2
            else:
                report_cache[q.__qualname__] = {'no cache see _setup_answers in framework.py': True}
        if with_coverage:
            for q, _ in self.questions:
                q._with_coverage = False
        return report_cache

    def set_payload(self, payloads, strict=False):
        for q, _ in self.questions:
            q._cache = payloads[q.__qualname__]
        self._config = payloads['config']


class UTextResult(unittest.TextTestResult):
    nL = 80
    number = -1  # HAcky way to set question number.
    show_progress_bar = True
    unmute = False # Whether to redirect stdout.
    cc = None
    setUpClass_time = 3 # Estimated time to run setUpClass in TestCase. Must be set externally. See key (("ClassName", "setUpClass"), "time") in _cache.

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.successes = []

    def printErrors(self) -> None:
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def addError(self, test, err):
        super(unittest.TextTestResult, self).addFailure(test, err)
        self.cc_terminate(success=False)

    def addFailure(self, test, err):
        super(unittest.TextTestResult, self).addFailure(test, err)
        self.cc_terminate(success=False)

    def addSuccess(self, test: unittest.case.TestCase) -> None:
        # test._get_outcome()

        msg = None
        if hasattr(test, '_get_outcome'):
            o = test._get_outcome()
            if isinstance(o, dict):
                key = (test.cache_id(), "return")
                if key in o:
                    msg = test._get_outcome()[key]

        self.successes.append((test, msg))  # (test, message) (to be consistent with failures and errors).
        self.cc_terminate()

    def cc_terminate(self, success=True):
        if self.show_progress_bar or True:
            tsecs = np.round(self.cc.terminate(), 2)
            self.cc.file.flush()
            ss = self.item_title_print

            state = "PASS" if success else "FAILED"

            dot_parts = ('.' * max(0, self.nL - len(state) - len(ss)))
            if self.show_progress_bar or True:
                print(self.item_title_print + dot_parts, end="", file=self.cc.file)
            else:
                print(dot_parts, end="", file=self.cc.file)

            if tsecs >= 0.5:
                state += " (" + str(tsecs) + " seconds)"
            print(state, file=self.cc.file)

    def startTest(self, test):
        name = test.__class__.__name__
        if self.testsRun == 0 and hasattr(test.__class__, '_cache2'): # Disable this if the class is pure unittest.TestCase
            # This is the first time we are running a test. i.e. we can time the time taken to call setupClass.
            if test.__class__._cache2 is None:
                test.__class__._cache2 = {}
            test.__class__._cache2[((name, 'setUpClass'), 'time')] = time.time() - self.t_start

        self.testsRun += 1
        item_title = test.shortDescription()  # Better for printing (get from cache).

        if item_title == None:
            # For unittest framework where getDescription may return None.
            item_title = self.getDescription(test)
        self.item_title_print = " * q%i.%i) %s" % (UTextResult.number + 1, self.testsRun, item_title)
        # estimated_time = 10

        # if self._previousTestClass == None:
        #     print("No prev. test class. ")
        if self.show_progress_bar or True:
            estimated_time = test.__class__._cache.get(((name, test._testMethodName), 'time'), 100) if hasattr(test.__class__, '_cache') else 4
            self.cc = ActiveProgress(t=estimated_time, title=self.item_title_print, show_progress_bar=self.show_progress_bar, file=sys.stdout)
        else:
            print(self.item_title_print + ('.' * max(0, self.nL - 4 - len(self.item_title_print))), end="")

        self._test = test
        # from unitgrade.unitgrade import Logger

        if not self.unmute:
            self._stdout = sys.stdout
            sys.stdout = io.StringIO()

    def stopTest(self, test):
        if not self.unmute:
            sys.stdout = self._stdout
        super().stopTest(test)

    def _setupStdout(self):
        if self._previousTestClass == None:
            self.t_start = time.time()
            # total_estimated_time = 1
            if hasattr(self.__class__, 'q_title_print'):
                q_title_print = self.__class__.q_title_print
            else:
                q_title_print = "<unnamed test. See unitgrade.framework.py>"

            # test.__class__._cache2[((name, 'setUpClass'), 'time')]

            cc = ActiveProgress(t=self.setUpClass_time, title=q_title_print, show_progress_bar=self.show_progress_bar)
            self.cc = cc

    def _restoreStdout(self):  # Used when setting up the test.
        if self._previousTestClass is None:
            q_time = self.cc.terminate()
            q_time = np.round(q_time, 2)
            sys.stdout.flush()
            if self.show_progress_bar:
                print(self.cc.title, end="")
            print(" " * max(0, self.nL - len(self.cc.title)) + (" (" + str(q_time) + " seconds)" if q_time >= 0.5 else ""))


class UTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        stream = io.StringIO()
        super().__init__(*args, stream=stream, **kwargs)

    def _makeResult(self):
        # stream = self.stream # not you!
        stream = sys.stdout
        stream = _WritelnDecorator(stream)
        return self.resultclass(stream, self.descriptions, self.verbosity)


def get_hints(ss):
    if ss == None:
        return None
    try:
        ss = textwrap.dedent(ss)
        ss = ss.replace('''"""''', "").strip()
        hints = ["hints:", "hint:"]
        j = np.argmax([ss.lower().find(h) for h in hints])
        h = hints[j]
        ss = ss[ss.lower().find(h) + len(h) + 1:]
        ss = "\n".join([l for l in ss.split("\n") if not l.strip().startswith(":")])
        ss = textwrap.dedent(ss).strip()
        return ss
    except Exception as e:
        print("bad hints", ss, e)


class UTestCase(unittest.TestCase):
    _outcome = None  # A dictionary which stores the user-computed outcomes of all the tests. This differs from the cache.
    _cache = None  # Read-only cache. Ensures method always produce same result.
    _cache2 = None  # User-written cache.
    _with_coverage = False
    _covcache = None # Coverage cache. Written to if _with_coverage is true.
    _report = None  # The report used. This is very, very hacky and should always be None. Don't rely on it!


    def capture(self):
        if hasattr(self, '_stdout') and self._stdout is not None:
            file = self._stdout
        else:
            # self._stdout = sys.stdout
            # sys._stdout = io.StringIO()
            file = sys.stdout
        return Capturing2(stdout=file)

    @classmethod
    def question_title(cls):
        """ Return the question title """
        if cls.__doc__ is not None:
            title = cls.__doc__.strip().splitlines()[0].strip()
            if not (title.startswith("Hints:") or title.startswith("Hint:") ):
                return title
        return cls.__qualname__

    @classmethod
    def reset(cls):
        print("Warning, I am not sure UTestCase.reset() is needed anymore and it seems very hacky.")
        cls._outcome = None
        cls._cache = None
        cls._cache2 = None



    def _callSetUp(self):
        if self._with_coverage:
            if self._covcache is None:
                self._covcache = {}
            import coverage
            self.cov = coverage.Coverage(data_file=None)
            self.cov.start()
        self.setUp()

    def _callTearDown(self):
        self.tearDown()
        if self._with_coverage:
            from pathlib import Path
            from snipper import snipper_main
            self.cov.stop()
            data = self.cov.get_data()
            base, _, _ = self._report._import_base_relative()
            for file in data.measured_files():
                file = os.path.normpath(file)
                root = Path(base)
                child = Path(file)
                if root in child.parents:
                    with open(child, 'r') as f:
                        s = f.read()
                    lines = s.splitlines()
                    garb = 'GARBAGE'
                    lines2 = snipper_main.censor_code(lines, keep=True)
                    assert len(lines) == len(lines2)
                    for l in data.contexts_by_lineno(file):
                        if lines2[l].strip() == garb:
                            rel = os.path.relpath(child, root)
                            cc = self._covcache
                            j = 0
                            for j in range(l, -1, -1):
                                if "def" in lines2[j] or "class" in lines2[j]:
                                    break
                            from snipper.legacy import gcoms
                            fun = lines2[j]
                            comments, _ = gcoms("\n".join(lines2[j:l]))
                            if rel not in cc:
                                cc[rel] = {}
                            cc[rel][fun] = (l, "\n".join(comments))
                            self._cache_put((self.cache_id(), 'coverage'), self._covcache)

    def shortDescriptionStandard(self):
        sd = super().shortDescription()
        if sd is None or sd.strip().startswith("Hints:") or sd.strip().startswith("Hint:"):
            sd = self._testMethodName
        return sd

    def shortDescription(self):
        sd = self.shortDescriptionStandard()
        title = self._cache_get((self.cache_id(), 'title'), sd)
        return title if title is not None else sd

    @property
    def title(self):
        return self.shortDescription()

    @title.setter
    def title(self, value):
        self._cache_put((self.cache_id(), 'title'), value)

    def _get_outcome(self):
        if not (self.__class__, '_outcome') or self.__class__._outcome is None:
            self.__class__._outcome = {}
        return self.__class__._outcome

    def _callTestMethod(self, testMethod):
        t = time.time()
        self._ensure_cache_exists()  # Make sure cache is there.
        if self._testMethodDoc is not None:
            self._cache_put((self.cache_id(), 'title'), self.shortDescriptionStandard())

        self._cache2[(self.cache_id(), 'assert')] = {}
        res = testMethod()
        elapsed = time.time() - t
        self._get_outcome()[ (self.cache_id(), "return") ] = res
        self._cache_put((self.cache_id(), "time"), elapsed)


    def cache_id(self):
        c = self.__class__.__qualname__
        m = self._testMethodName
        return c, m

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_cache()
        self._assert_cache_index = 0

    def _ensure_cache_exists(self):
        if not hasattr(self.__class__, '_cache') or self.__class__._cache == None:
            self.__class__._cache = dict()
        if not hasattr(self.__class__, '_cache2') or self.__class__._cache2 == None:
            self.__class__._cache2 = dict()

    def _cache_get(self, key, default=None):
        self._ensure_cache_exists()
        return self.__class__._cache.get(key, default)

    def _cache_put(self, key, value):
        self._ensure_cache_exists()
        self.__class__._cache2[key] = value

    def _cache_contains(self, key):
        self._ensure_cache_exists()
        return key in self.__class__._cache

    def wrap_assert(self, assert_fun, first, *args, **kwargs):
        key = (self.cache_id(), 'assert')
        if not self._cache_contains(key):
            print("Warning, framework missing", key)
            self.__class__._cache[
                key] = {}  # A new dict. We manually insert it because we have to use that the dict is mutable.
        cache = self._cache_get(key)
        id = self._assert_cache_index
        if not id in cache:
            print("Warning, framework missing cache index", key, "id =", id)
        _expected = cache.get(id, f"Key {id} not found in cache; framework files missing. Please run deploy()")

        # The order of these calls is important. If the method assert fails, we should still store the correct result in cache.
        cache[id] = first
        self._cache_put(key, cache)
        self._assert_cache_index += 1
        assert_fun(first, _expected, *args, **kwargs)

    def assertEqualC(self, first, msg=None):
        self.wrap_assert(self.assertEqual, first, msg)

    def _shape_equal(self, first, second):
        a1 = np.asarray(first).squeeze()
        a2 = np.asarray(second).squeeze()
        msg = None
        msg = "" if msg is None else msg
        if len(msg) > 0:
            msg += "\n"
        self.assertEqual(a1.shape, a2.shape, msg=msg + "Dimensions of input data does not agree.")
        diff = np.abs(a1 - a2)
        return diff


    def assertLinf(self, first, second=None, tol=1e-5, msg=None):
        if second is None:
            return self.wrap_assert(self.assertLinf, first, tol=tol, msg=msg)
        else:
            diff = self._shape_equal(first, second)
            if max(diff.flat) >= tol:
                self.assertEqual(first, second, msg=msg + f"Not equal within tolerance {tol}")

    def assertL2(self, first, second=None, tol=1e-5, msg=None):
        if second is None:
            return self.wrap_assert(self.assertL2, first, tol=tol, msg=msg)
        else:
            # We first test using numpys build-in testing method to see if one coordinate deviates a great deal.
            # This gives us better output, and we know that the coordinate wise difference is lower than the norm difference.
            np.testing.assert_allclose(first, second, atol=tol)
            diff = self._shape_equal(first, second)
            diff = ( ( np.asarray( diff.flatten() )**2).sum() )**.5
            if max(diff.flat) >= tol:
                self.assertEqual(first, second, msg=msg + f"Not equal within tolerance {tol}")

    def _cache_file(self):
        return os.path.dirname(inspect.getabsfile(type(self))) + "/unitgrade_data/" + self.__class__.__name__ + ".pkl"

    def _save_cache(self):
        # get the class name (i.e. what to save to).
        cfile = self._cache_file()
        if not os.path.isdir(os.path.dirname(cfile)):
            os.makedirs(os.path.dirname(cfile))

        if hasattr(self.__class__, '_cache2'):
            with open(cfile, 'wb') as f:
                pickle.dump(self.__class__._cache2, f)

    # But you can also set cache explicitly.
    def _load_cache(self):
        if self._cache is not None:  # Cache already loaded. We will not load it twice.
            return
            # raise Exception("Loaded cache which was already set. What is going on?!")
        cfile = self._cache_file()
        if os.path.exists(cfile):
            try:
                # print("\ncache file", cfile)
                with open(cfile, 'rb') as f:
                    data = pickle.load(f)
                self.__class__._cache = data
            except Exception as e:
                print("Bad cache", cfile)
                print(e)
        else:
            print("Warning! data file not found", cfile)

    def _feedErrorsToResult(self, result, errors):
        """ Use this to show hints on test failure. """
        if not isinstance(result, UTextResult):
            er = [e for e, v in errors if v != None]

            if len(er) > 0:
                hints = []
                key = (self.cache_id(), 'coverage')
                if self._cache_contains(key):
                    CC = self._cache_get(key)
                    cl, m = self.cache_id()
                    gprint(f"> An error occured while solving: {cl}.{m}. The files/methods you need to edit are:")  # For the test {id} in {file} you should edit:")
                    for file in CC:
                        rec = CC[file]
                        gprint(f">   * {file}")
                        for l in rec:
                            _, comments = CC[file][l]
                            hint = get_hints(comments)

                            if hint != None:
                                hints.append((hint, file, l) )
                            gprint(f">      - {l}")

                er = er[0]
                doc = er._testMethodDoc
                # print("doc", doc)
                if doc is not None:
                    hint = get_hints(er._testMethodDoc)
                    if hint is not None:
                        hints = [(hint, None, self.cache_id()[1] )] + hints
                if len(hints) > 0:
                    # print(hints)
                    for hint, file, method in hints:
                        s = (f"'{method.strip()}'" if method is not None else "")
                        if method is not None and file is not None:
                            s += " in "
                        try:
                            s += (file.strip() if file is not None else "")
                            gprint(">")
                            gprint("> Hints (from " + s + ")")
                            gprint(textwrap.indent(hint, ">   "))
                        except Exception as e:
                            print("Bad stuff in hints. ")
                            print(hints)

        super()._feedErrorsToResult(result, errors)

    def startTestRun(self):
        super().startTestRun()

# 817, 705