import time
import gmpy2
from gmpy2 import mpfr

class Harp:
    """
    ⚡ HARP Engine: High-Precision FFT-Backed Log-Space Solver
    With dynamic magnitude-aware bit allocation and robust initial guess.
    """
    def __init__(self, base=None, power=None, terms=None, nested=None, precision=1000, initial_guess=None):
        self.precision = precision
        self.initial_guess = initial_guess

        # --- Syntax Normalization for Power ---
        num, den = 1, 1
        if power is not None:
            if isinstance(power, str):
                if "/" in power:
                    p, q = power.split("/")
                    num, den = int(p.strip()), int(q.strip())
                else:
                    num, den = int(power.strip()), 1
            elif isinstance(power, (list, tuple)) and len(power) == 2:
                num, den = int(power[0]), int(power[1])
            elif isinstance(power, (int, float)):
                from fractions import Fraction
                f = Fraction(power).limit_denominator(100000)
                num, den = f.numerator, f.denominator

        # Preliminary rough estimation to check magnitude before locking precision bits
        rough_log = 0.0
        if terms is not None:
            for b, p, q in terms:
                rough_log += (p / q) * __import__('math').log(float(b))
        elif base is not None:
            rough_log += (num / den) * __import__('math').log(float(base))

        # Estimate required integer digits from log magnitude
        self.est_int_digits = max(0, int(rough_log / 2.302585092994046))
        total_required_digits = max(precision, self.est_int_digits + precision)

        # Dynamic bit allocation (3.3219 bits per decimal digit + 128 guard bits)
        bits = int(total_required_digits * 3.3219280948873626) + 128
        gmpy2.get_context().precision = bits

        total_log = mpfr(0, bits)

        # 1. Recursive Nested Intercept
        if base is not None and nested is not None:
            b_mp = mpfr(str(base), bits)
            if b_mp <= 0: raise ValueError("❌ Boundary Error: Base must be strictly positive (> 0).")
            s_base, s_num, s_den = nested
            sub_res = Harp.solve(s_base, power=(s_num, s_den), precision=precision)
            self.target_log = mpfr(str(sub_res), bits) * gmpy2.log(b_mp)
            return

        # 2. Multi-Term or Single Base Parsing
        if terms is not None:
            self.terms = terms
        elif base is not None:
            self.terms = [(base, num, den)]
        else:
            raise ValueError("❌ Boundary Error: Missing core operational parameters (base or terms).")

        for b, p, q in self.terms:
            if q == 0: raise ZeroDivisionError("❌ Boundary Error: Denominator 'q' cannot be zero.")
            b_mp = mpfr(str(b), bits)
            if b_mp <= 0: raise ValueError(f"❌ Boundary Error: Base '{b}' must be strictly positive (> 0).")
            total_log += (mpfr(p, bits) / mpfr(q, bits)) * gmpy2.log(b_mp)

        self.target_log = total_log

    @classmethod
    def solve(cls, base=None, power=None, terms=None, nested=None, precision=1000, initial_guess=None, return_dict=False):
        """Simplest one-liner wrapper to compute and return resolved root string or full report."""
        engine = cls(base=base, power=power, terms=terms, nested=nested, precision=precision, initial_guess=initial_guess)
        return engine.compute(return_dict=return_dict)

    def compute(self, max_iter=100, return_dict=False):
        """Core Newton-Raphson log-space expansion loop with automatic or custom starting guess."""
        bits = gmpy2.get_context().precision
        tolerance = mpfr(10, bits) ** (-self.precision)
        
        history = []
        
        # --- Initial Guess Logic: Custom if provided, else Automatic Heuristic ---
        if self.initial_guess is not None:
            x = mpfr(str(self.initial_guess), bits)
        elif abs(self.target_log) > 100:
            x = gmpy2.exp(self.target_log * mpfr('0.95', bits))
        else:
            x = gmpy2.exp(self.target_log * mpfr(0.5, bits))
            
        one = mpfr(1, bits)

        for i in range(max_iter):
            if x <= 0:
                raise RuntimeError(f"⚠️ Boundary Trigger: Domain violation x <= 0 at iteration {i}.")

            fx = gmpy2.log(x) - self.target_log
            err = abs(fx)
            history.append({'iteration': i, 'x': str(x), 'error': str(err)})

            if err < tolerance:
                formatted = f"{x:.{self.precision}f}"
                if return_dict:
                    return {
                        'status': 'HYPER_FFT_SUCCESS',
                        'root': x,
                        'formatted_root': formatted,
                        'iterations': i,
                        'history': history
                    }
                return formatted

            x_next = x * (one - fx)

            if i == 0 and x_next <= 0:
                raise ValueError(f"🚨 [BOUNDARY FIREWALL] First iteration yielded x1 = {x_next} (<= 0).")
            if x_next <= 0 or gmpy2.is_nan(x_next) or gmpy2.is_infinite(x_next):
                raise RuntimeError(f"⚠️ Boundary Trigger: Engine diverged or crossed zero at iteration {i}.")

            x = x_next

        raise TimeoutError("⚠️ Max iterations reached without convergence.")