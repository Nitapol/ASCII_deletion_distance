import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
ax.set_xlim(0.5, 4.5)
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Prepare the data
x = np.linspace(0, 10, 100)

# Plot the data
plt.plot(x, x, label='linear')

# Add a legend
plt.legend()

# Show the plot
plt.show()


# from tkinter import *
# from PIL import ImageTk, Image
# root = Tk()
#
# canv = Canvas(root, width=80, height=80, bg="white")
# canv.pack(expand=YES, fill=BOTH)
#
# #s = "//Users//alex//Documents//17358441326_6b69db2561_o.jpg"
# img = ImageTk.PhotoImage(Image.open(
# "/Users/alex/Downloads/OpenSolitaire-1.0/Assets/original/2_of_clubs.png"))
# canv.create_image(20, 20, anchor=NW, image=img)
#
# mainloop()
