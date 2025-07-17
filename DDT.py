from collections import defaultdict

def compute_modular_addition_ddt(n):
    MOD = 2 ** n
    DDT = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for alpha in range(MOD):
        for beta in range(MOD):
            for x in range(MOD):
                for y in range(MOD):
                    z = (x + y) % MOD
                    zp = ((x ^ alpha) + (y ^ beta)) % MOD
                    gamma = z ^ zp
                    DDT[alpha][beta][gamma] += 1
    return DDT

def print_ddt_tables_in_grid_style(DDT, n):
    MOD = 2 ** n
    cell_width = 4  # Adjust spacing inside cells
    bin_fmt = lambda x: format(x, f"0{n}b")

    for gamma in range(MOD):
        print(f"\n DDT Table for γ = {bin_fmt(gamma)}\n")
        
        # Column header
        header = " " * (n + 2)
        for beta in range(MOD):
            header += f"{bin_fmt(beta):>{cell_width}}"
        print(header)

        # Separator
        print("-" * len(header))

        # Rows (alpha)
        for alpha in range(MOD):
            row = f"{bin_fmt(alpha)} |"
            for beta in range(MOD):
                count = DDT[alpha][beta][gamma]
                row += f"{count:>{cell_width}}"
            print(row)

def export_ddt_to_latex(DDT, n, filename="ddt_tables.tex"):
    MOD = 2 ** n
    bin_fmt = lambda x: format(x, f"0{n}b")

    with open(filename, "w") as f:
        for gamma in range(MOD):
            f.write(f"\\begin{{table}}[H]\n")
            f.write(f"\\centering\n")
            f.write(f"\\caption{{DDT Table for $\\gamma$ = {bin_fmt(gamma)}}}\n")
            f.write(f"\\begin{{tabular}}{{c|{'c' * MOD}}}\n")
            
            # Column header
            headers = " & " + " & ".join(bin_fmt(beta) for beta in range(MOD)) + " \\\\\n"
            f.write(headers)
            f.write("\\hline\n")
            
            # Rows
            for alpha in range(MOD):
                row = bin_fmt(alpha) + " & " + " & ".join(str(DDT[alpha][beta][gamma]) for beta in range(MOD)) + " \\\\\n"
                f.write(row)

            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n\n")


# Example usage
if __name__ == "__main__":
    n = 3  # For 3-bit modular addition
    ddt = compute_modular_addition_ddt(n)
    print_ddt_tables_in_grid_style(ddt, n)
