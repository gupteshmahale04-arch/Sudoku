from tabulate import tabulate
import numpy as np

alpha = np.array([
    ['A', 4, 2, 'B', 5, 'C', 'D', 'E', 6],
    [1, 9, 7, 'F', 'G', 'H', 'I', 4, 'J'],
    [5, 6, 'K', 4, 'L', 'M', 1, 'N', 9],
    
    [8, 'O', 1, 3, 'P', 'Q', 2, 6, 'R'],
    [9, 'S', 'T', 'U', 7, 1, 'V', 4, 5],
    ['W', 3, 'X', 2, 5, 6, 'Y', 'Z', 'AA'],
    
    ['AB', 5, 'AC', 3, 2, 'AD', 7, 'AE', 'AF'],
    ['AG', 4, 'AH', 5, 9, 'AI', 6, 'AJ', 'AK'],
    ['AL', 'AM', 7, 'AN', 6, 'AO', 'AP', 8, 'AQ']
])

print("👉 Use notebook and pen to solve:")
print(tabulate(alpha, tablefmt="grid"))

New = int(input("Enter 0 for play And For Exit 0 < : "))

while New == 0:
    # All Sudoku blank variables in a list
    arr = [
        "A","B","C","D","E","F","G","H","I","J",
        "K","L","M","N","O","P","Q","R","S","T",
        "U","V","W","X","Y","Z","AA","AB","AC","AD",
        "AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN",
        "AO","AP","AQ"
    ]
    
    d = {}
    for i in arr:
        d[i] = int(input(f"Enter the number for {i} And Pless {i} <10 : "))
        
        
            

    # Sudoku array with dictionary values
    sudoku_var = np.array([
        [d["A"], 4, 2, d["B"], 5, d["C"], d["D"], d["E"], 6],
        [1, 9, 7, d["F"], d["G"], d["H"], d["I"], 4, d["J"]],
        [5, 6, d["K"], 4, d["L"], d["M"], 1, d["N"], 9],
        
        [8, d["O"], 1, 3, d["P"], d["Q"], 2, 6, d["R"]],
        [9, d["S"], d["T"], d["U"], 7, 1, d["V"], 4, 5],
        [d["W"], 3, d["X"], 2, 5, 6, d["Y"], d["Z"], d["AA"]],
        
        [d["AB"], 5, d["AC"], 3, 2, d["AD"], 7, d["AE"], d["AF"]],
        [d["AG"], 4, d["AH"], 5, 9, d["AI"], 6, d["AJ"], d["AK"]],
        [d["AL"], d["AM"], 7, d["AN"], 6, d["AO"], d["AP"], 8, d["AQ"]]
    ])

    print("\n✅ Your Sudoku after filling inputs:")
    print(tabulate(sudoku_var, tablefmt="grid"))

    # Check rows and columns
    for i in range(9):
        if np.sum(sudoku_var[i, :]) != 45:
            print(f"⚠️ Problem in row {i+1}")
        if np.sum(sudoku_var[:, i]) != 45:
            print(f"⚠️ Problem in column {i+1}")

    New = int(input("\nEnter 0 for replay, any other number to exit: "))
