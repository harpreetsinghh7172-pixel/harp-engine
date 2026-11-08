
import time
from harp import Harp

print("=" * 60)
print("⚡ HARP ENGINE: SYNTAX, TIMING, & ITERATION BENCHMARK SUITE")
print("=" * 60)

# ==========================================
# 1. SIMPLE BASE & POWER
# ==========================================
start = time.perf_counter()
report1 = Harp.solve(base=2, power="1/100", precision=50, return_dict=True)
elapsed = time.perf_counter() - start

print(f"\n1. Simple Base & Power:")
print(f"   - Result     : {report1['formatted_root']}")
print(f"   - Iterations : {report1['iterations']}")
print(f"   - Time Taken : {elapsed:.6f} seconds")


# ==========================================
# 2. BASE, POWER, & CUSTOM INITIAL GUESS
# ==========================================
start = time.perf_counter()
report2 = Harp.solve(base=2, power="1/100", precision=50, initial_guess=1.4, return_dict=True)
elapsed = time.perf_counter() - start

print(f"\n2. With Custom Initial Guess:")
print(f"   - Result     : {report2['formatted_root']}")
print(f"   - Iterations : {report2['iterations']}")
print(f"   - Time Taken : {elapsed:.6f} seconds")


# ==========================================
# 3. BASE, POWER, & CUSTOM PRECISION
# ==========================================
start = time.perf_counter()
report3 = Harp.solve(base=2, power="1/100", precision=50, return_dict=True)
elapsed = time.perf_counter() - start

print(f"\n3. With Custom Precision:")
print(f"   - Result     : {report3['formatted_root']}")
print(f"   - Iterations : {report3['iterations']}")
print(f"   - Time Taken : {elapsed:.6f} seconds")


# ==========================================
# 4. FULLY SPECIFIED (Precision + Guess)
# ==========================================
start = time.perf_counter()
report4 = Harp.solve(base=2, power="1/100", precision=50, initial_guess=1.4, return_dict=True)
elapsed = time.perf_counter() - start

print(f"\n4. Fully Specified (Precision + Guess):")
print(f"   - Result     : {report4['formatted_root']}")
print(f"   - Iterations : {report4['iterations']}")
print(f"   - Time Taken : {elapsed:.6f} seconds")


# ==========================================
# 5. OBJECT-ORIENTED INSTANCE SYNTAX
# ==========================================
start = time.perf_counter()
solver = Harp(base=10, power="1/3", precision=30, initial_guess=2.1)
# Using compute with return_dict to capture stats
report5 = solver.compute(return_dict=True)
elapsed = time.perf_counter() - start

print(f"\n5. OO Instance Syntax:")
print(f"   - Result     : {report5['formatted_root']}")
print(f"   - Iterations : {report5['iterations']}")
print(f"   - Time Taken : {elapsed:.6f} seconds")


# ==========================================
# 6. DICTIONARY REPORT OUTPUT
# ==========================================
start = time.perf_counter()
report6 = Harp.solve(base=2, power="1/10", precision=20, return_dict=True)
elapsed = time.perf_counter() - start

print(f"\n6. Dictionary Report Output:")
print(f"   - Status     : {report6['status']}")
print(f"   - Iterations : {report6['iterations']}")
print(f"   - Result     : {report6['formatted_root']}")
print(f"   - Time Taken : {elapsed:.6f} seconds")


# ==========================================
# 7. MULTI-TERM EXPRESSIONS SYNTAX
# ==========================================
start = time.perf_counter()
report7 = Harp.solve(terms=[(2, 1, 2), (3, 1, 3)], precision=40, return_dict=True)
elapsed = time.perf_counter() - start

print(f"\n7. Multi-Term Expression Result:")
print(f"   - Result     : {report7['formatted_root']}")
print(f"   - Iterations : {report7['iterations']}")
print(f"   - Time Taken : {elapsed:.6f} seconds")

print("\n" + "=" * 60)
print("Benchmark complete!")