import tkinter as tk
from transport_app import TransportApp

def main():
    root = tk.Tk()
    app = TransportApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
