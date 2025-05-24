import tkinter as tk
from tkinter import messagebox
import copy

import generate
import solve


class SudokuGUI:
    """Tkinter GUI wrapper for the Sudoku generator/solver project."""

    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Sudoku")
        root.resizable(False, False)

        # --- State ---
        self.generated_board: list[list[int]] | None = None
        self.entries: list[list[tk.Entry]] = [[None] * 9 for _ in range(9)]  # type: ignore[arg-type]

        # --- Layout ---
        board_frame = tk.Frame(root, padx=10, pady=10)
        board_frame.pack()

        # Build 9×9 grid of Entry widgets
        for r in range(9):
            for c in range(9):
                ent = tk.Entry(
                    board_frame,
                    width=2,
                    font=("Helvetica", 20),
                    justify="center",
                    state="disabled",
                    disabledforeground="black",
                )

                pad_x = (2 if c % 3 == 0 else 0, 2 if (c + 1) % 3 == 0 else 0)
                pad_y = (2 if r % 3 == 0 else 0, 2 if (r + 1) % 3 == 0 else 0)

                ent.grid(row=r, column=c, padx=pad_x, pady=pad_y)
                self.entries[r][c] = ent

        # --- Control buttons ---
        btn_frame = tk.Frame(root, pady=10)
        btn_frame.pack()

        tk.Button(btn_frame, text="Generate", command=self.generate_puzzle).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Solve", command=self.solve_puzzle).pack(side="left", padx=5)

    def generate_puzzle(self) -> None:
        board = generate.create_puzzle_board()
        if not board:
            messagebox.showerror("Generation error", "Failed to generate a Sudoku puzzle.")
            return

        self.generated_board = board
        self._write_board_to_ui(board, readonly_clues=True, clue_color="black")
        messagebox.showinfo("Puzzle ready", "A new Sudoku puzzle has been generated!")

    def solve_puzzle(self) -> None:
        if self.generated_board is None:
            messagebox.showwarning("No puzzle", "Generate a puzzle first.")
            return

        board = self._read_board_from_ui()
        board_copy = copy.deepcopy(board)

        if not solve.solve(board_copy):
            messagebox.showerror("Unsolvable", "This Sudoku cannot be solved.")
            return

        self._write_board_to_ui(board_copy, readonly_clues=True, clue_color="black", fill_color="blue")
        messagebox.showinfo("Solved", "The Sudoku has been solved!")

    def _read_board_from_ui(self) -> list[list[int]]:
        board: list[list[int]] = []
        for r in range(9):
            row: list[int] = []
            for c in range(9):
                text = self.entries[r][c].get().strip()
                row.append(int(text) if text.isdigit() else 0)
            board.append(row)
        return board

    def _write_board_to_ui(
        self,
        board: list[list[int]],
        *,
        readonly_clues: bool,
        clue_color: str = "black",
        fill_color: str | None = None,
    ) -> None:
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                ent = self.entries[r][c]
                ent.config(state="normal", fg=clue_color)
                ent.delete(0, tk.END)

                if val:
                    ent.insert(0, str(val))
                    ent.config(state="disabled")
                else:
                    ent.delete(0, tk.END)
                    ent.config(state="disabled")
                    if fill_color is not None:
                        ent.config(fg=fill_color)


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
