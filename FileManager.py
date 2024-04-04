from tkinter import Tk, Label, Button, Frame, messagebox, filedialog, PhotoImage, Canvas, Scrollbar
from PIL import Image, ImageTk
import os
import shutil

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ram's File Manager")

        # Set window size and center it on the screen
        window_width = 500
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Set background color
        self.root.configure(bg="#f0f0f0")

        # Load and resize icons
        icon_size = (25, 25)
        self.open_icon = self.load_and_resize_icon('icons/open.png', icon_size)
        self.copy_icon = self.load_and_resize_icon('icons/copy.png', icon_size)
        self.delete_icon = self.load_and_resize_icon('icons/delete.png', icon_size)
        self.rename_icon = self.load_and_resize_icon('icons/rename.png', icon_size)
        self.folder_icon = self.load_and_resize_icon('icons/folder.png', icon_size)
        self.remove_icon = self.load_and_resize_icon('icons/remove_folder.png', icon_size)
        self.list_icon = self.load_and_resize_icon('icons/list.png', icon_size)
        self.exit_icon = self.load_and_resize_icon('icons/exit.png', icon_size)
        self.search_icon = self.load_and_resize_icon('icons/search.png', icon_size)

        # Create frame for file operations
        self.file_operations_frame = Frame(root, bg="#f0f0f0")
        self.file_operations_frame.pack(pady=10, fill='both', expand=True)

        # Create canvas for scrolling
        self.canvas = Canvas(self.file_operations_frame, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)

        # Add scrollbar
        scrollbar = Scrollbar(self.file_operations_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create frame inside canvas
        self.inner_frame = Frame(self.canvas, bg="#f0f0f0")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Create labels and buttons for file operations
        Label(self.inner_frame, text="File Manager", font=("Helvetica", 20, "bold"), fg="#333", bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=(0, 5))

        self.create_button("Open", self.open_icon, self.open_file, row=1, column=0)
        self.create_button("Copy", self.copy_icon, self.copy_file, row=2, column=0)
        self.create_button("Delete", self.delete_icon, self.delete_file, row=3, column=0)
        self.create_button("Rename", self.rename_icon, self.rename_file, row=4, column=0)
        self.create_button("New Folder", self.folder_icon, self.make_folder, row=1, column=1)
        self.create_button("Remove Folder", self.remove_icon, self.remove_folder, row=2, column=1)
        self.create_button("List Files", self.list_icon, self.list_files, row=3, column=1)
        self.create_button("Search", self.search_icon, self.search_files, row=4, column=1)

        # Add exit button
        Button(self.inner_frame, text="Exit", font=("Helvetica", 12), command=root.quit).grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="ew")

    def load_and_resize_icon(self, path, size):
        image = Image.open(path)
        image = image.resize(size)
        return ImageTk.PhotoImage(image)

    def create_button(self, text, icon, command, row, column):
        button = Button(self.inner_frame, text=text, image=icon, compound="left", font=("Helvetica", 12), bg="#fff", fg="#333", bd=0, padx=10, pady=5, command=command)
        button.grid(row=row, column=column, padx=5, pady=5, sticky="ew")

    def open_window(self):
        return filedialog.askopenfilename()

    def open_file(self):
        file_path = self.open_window()
        if file_path:
            try:
                os.startfile(file_path)
            except:
                messagebox.showerror('Error', 'Failed to open file!')

    def copy_file(self):
        source_path = self.open_window()
        if source_path:
            destination_path = filedialog.askdirectory()
            if destination_path:
                try:
                    shutil.copy(source_path, destination_path)
                    messagebox.showinfo('Confirmation', 'File Copied!')
                except:
                    messagebox.showerror('Error', 'Failed to copy file!')

    def delete_file(self):
        file_path = self.open_window()
        if file_path:
            try:
                os.remove(file_path)
                messagebox.showinfo('Confirmation', 'File Deleted!')
            except:
                messagebox.showerror('Error', 'Failed to delete file!')

    def rename_file(self):
        chosen_file = self.open_window()
        if chosen_file:
            try:
                new_name = filedialog.asksaveasfilename(initialdir=os.path.dirname(chosen_file))
                os.rename(chosen_file, new_name)
                messagebox.showinfo('Confirmation', 'File Renamed!')
            except:
                messagebox.showerror('Error', 'Failed to rename file!')

    def make_folder(self):
        new_folder_path = filedialog.askdirectory()
        if new_folder_path:
            new_folder_name = filedialog.asksaveasfilename(initialdir=new_folder_path)
            if new_folder_name:
                try:
                    os.mkdir(new_folder_name)
                    messagebox.showinfo('Confirmation', 'Folder created!')
                except:
                    messagebox.showerror('Error', 'Failed to create folder!')

    def remove_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            try:
                os.rmdir(folder_path)
                messagebox.showinfo('Confirmation', 'Folder Deleted!')
            except:
                messagebox.showerror('Error', 'Failed to delete folder!')

    def list_files(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            file_list = os.listdir(folder_path)
            messagebox.showinfo('Files in Directory', '\n'.join(file_list))

    def search_files(self):
        search_query = filedialog.askstring("Search Files", "Enter file name:")
        if search_query:
            file_list = []
            for root_dir, dirs, files in os.walk(os.getcwd()):
                for file in files:
                    if search_query in file:
                        file_list.append(os.path.join(root_dir, file))
            if file_list:
                messagebox.showinfo("Search Results", "\n".join(file_list))
            else:
                messagebox.showinfo("Search Results", "No files found matching the query.")

if __name__ == "__main__":
    root = Tk()
    app = FileManagerApp(root)
    root.mainloop()
