from collections import defaultdict

def bit_xor(x):
    """Return the XOR of all bits in integer x."""
    result = 0
    while x:
        result ^= x & 1
        x >>= 1
    return result

def build_lat(n):
    """
    Construct the Linear Approximation Table (LAT) for n-bit modular addition.
    Returns a 3D dictionary: LAT[alpha][beta][gamma] = bias count.
    """
    from collections import defaultdict

    lat = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    max_val = 2 ** n

    for alpha in range(max_val):
        for beta in range(max_val):
            for gamma in range(max_val):
                for x in range(max_val):
                    for y in range(max_val):
                        z = (x + y) % max_val
                        temp_alpha = x & alpha
                        temp_beta = y & beta
                        temp_gamma = z & gamma

                        lhs = bit_xor(temp_alpha ^ temp_beta)
                        rhs = bit_xor(temp_gamma)

                        if lhs == rhs:
                            lat[alpha][beta][gamma] += 1
    return lat

def print_lat_for_fixed_gamma(lat, n, gamma_fixed):
    """Print LAT[alpha][beta][gamma_fixed] as a readable table."""
    max_val = 2 ** n
    print(f"Linear Approximation Table for γ = {gamma_fixed:0{n}b}:\n")

    # Header
    print("      ", end="")
    for beta in range(max_val):
        print(f"{beta:0{n}b} ", end="")
    print("\n" + "-" * (6 + (n + 1) * max_val))

    # Rows
    for alpha in range(max_val):
        print(f"{alpha:0{n}b} | ", end="")
        for beta in range(max_val):
            value = lat[alpha][beta][gamma_fixed]
            print(f"{value:>{n+1}}", end=" ")
        print()

def print_all_lat_tables(lat, n):
    """Print LAT raw count tables for all gamma values."""
    max_val = 2 ** n
    for gamma in range(max_val):
        print(f"\nLAT Table for γ = {gamma:0{n}b}:\n")
        print("      ", end="")
        for beta in range(max_val):
            print(f"{beta:0{n}b} ", end="")
        print("\n" + "-" * (6 + (n + 2) * max_val))
        for alpha in range(max_val):
            print(f"{alpha:0{n}b} | ", end="")
            for beta in range(max_val):
                count = lat[alpha][beta][gamma]
                print(f"{count:>3} ", end="")
            print()


def export_lat_to_latex(lat, n, filename="lat_tables.tex"):
    max_val = 2 ** n

    with open(filename, "w") as f:
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\usepackage{booktabs}" + "\n")
        f.write(r"\usepackage[margin=1in]{geometry}" + "\n")
        f.write(r"\begin{document}" + "\n\n")

        for gamma in range(max_val):
            f.write(r"\section*{LAT Table for $\gamma = " + f"{gamma:0{n}b}" + r"$}\n")
            f.write(r"\begin{center}" + "\n")
            f.write(r"\begin{tabular}{c|" + "c" * max_val + "}\n")
            # Header row
            header = " $\\beta$ "
            for beta in range(max_val):
                header += f"& ${beta:0{n}b}$ "
            f.write(header + r" \\" + "\n")
            f.write(r"\midrule" + "\n")

            # Table rows
            for alpha in range(max_val):
                row = f"${alpha:0{n}b}$ "
                for beta in range(max_val):
                    count = lat[alpha][beta][gamma]
                    row += f"& {count} "
                row += r" \\"
                f.write(row + "\n")

            f.write(r"\end{tabular}" + "\n")
            f.write(r"\end{center}" + "\n\n")

        f.write(r"\end{document}" + "\n")

def observe_lat_statistics(lat, n):
    max_val = 2 ** n
    total_entries = max_val ** 3

    max_count = float('-inf')
    min_count = float('inf')
    max_positions = []
    min_positions = []
    sum_counts = 0

    for gamma in range(max_val):
        for alpha in range(max_val):
            for beta in range(max_val):
                count = lat[alpha][beta][gamma]
                sum_counts += count

                if count > max_count:
                    max_count = count
                    max_positions = [(alpha, beta, gamma)]
                elif count == max_count:
                    max_positions.append((alpha, beta, gamma))

                if count < min_count:
                    min_count = count
                    min_positions = [(alpha, beta, gamma)]
                elif count == min_count:
                    min_positions.append((alpha, beta, gamma))

    avg = sum_counts / total_entries

    print("LAT Observation Report")
    print("=========================")
    print(f"n = {n}, Total Entries: {total_entries}")
    print(f"Max LAT Count   : {max_count}")
    print(f"At Positions    : {[f'(α={a:0{n}b}, β={b:0{n}b}, γ={g:0{n}b})' for a,b,g in max_positions]}")
    print(f"Min LAT Count   : {min_count}")
    print(f"At Positions    : {[f'(α={a:0{n}b}, β={b:0{n}b}, γ={g:0{n}b})' for a,b,g in min_positions]}")
    print(f"Average Count   : {avg:.2f}")
    print("=========================")


if __name__ == "__main__":

    n = 3  # Number of bits for the LAT
    gamma_example = 0b010  # Example fixed gamma value
    lat = build_lat(n)
    #print_lat_for_fixed_gamma(lat, n, gamma_example)
    print_all_lat_tables(lat, n)
    #export_lat_to_latex(lat, n, "lat_tables.tex")
    observe_lat_statistics(lat, n)