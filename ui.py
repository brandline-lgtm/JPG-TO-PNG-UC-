import tkinter as tk
from tkinter import filedialog, messagebox
from converter import convert_image


def _choose_file(var, save=False):
    if save:
        path = filedialog.asksaveasfilename(
            defaultextension=".jpg", filetypes=[("JPEG images", "*.jpg")]
        )
    else:
        path = filedialog.askopenfilename(
            filetypes=[("PNG images", "*.png"), ("All files", "*.*")]
        )
    if path:
        var.set(path)


def _run(input_var, output_var):
    inp, out = input_var.get(), output_var.get()
    if not inp or not out:
        messagebox.showerror("Error", "Please select input and output files")
        return
    try:
        convert_image(inp, out)
        messagebox.showinfo("Success", f"Saved to {out}")
    except Exception as exc:  # pragma: no cover - GUI feedback only
        messagebox.showerror("Error", str(exc))


def main() -> None:
    root = tk.Tk()
    root.title("PNG to JPG Converter")

    input_var = tk.StringVar()
    output_var = tk.StringVar()

    tk.Label(root, text="Input PNG:").grid(row=0, column=0, sticky="e")
    tk.Entry(root, textvariable=input_var, width=40).grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: _choose_file(input_var)).grid(
        row=0, column=2
    )

    tk.Label(root, text="Output JPG:").grid(row=1, column=0, sticky="e")
    tk.Entry(root, textvariable=output_var, width=40).grid(row=1, column=1)
    tk.Button(root, text="Browse", command=lambda: _choose_file(output_var, True)).grid(
        row=1, column=2
    )

    tk.Button(root, text="Convert", command=lambda: _run(input_var, output_var)).grid(
        row=2, column=1, pady=10
    )

    root.mainloop()


if __name__ == "__main__":
    main()
