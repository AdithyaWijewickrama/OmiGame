from backend import StartFront

app=StartFront;

if __name__ == '__main__':
    # Creating the second widget window
    a = app.Widget1(0)  # Passing 0 to create a root Tk instance
    a.w1.mainloop()