from tkinter import ttk
from tkinter import *
import sqlite3


class Product:
	db = "database.db"

	def __init__(self, windows):
		self.wind = windows
		self.wind.title("Añadir Productos")
		# register title
		frame = LabelFrame(self.wind, text="Register a New Product")
		frame.grid(row=0, column=0, columnspan=3, pady=20)
		# name title
		Label(frame, text="Name: ").grid(row=1, column=0)
		self.name = Entry(frame)
		self.name.focus()
		self.name.grid(row=1, column=1)
		# price title
		Label(frame, text="Price: ").grid(row=2, column=0)
		self.price = Entry(frame)
		self.price.grid(row=2, column=1)
		# Description
		Label(frame, text="Descriptiññon: ").grid(row=3, column=0)
		self.description = Entry(frame)
		self.description.grid(row=3, column=1)
		# button
		ttk.Button(frame, text="Add Product", command=self.add_product).grid(row=4, columnspan=2, sticky=W + E)
		# message
		self.message = Label(text="", fg="white")
		self.message.grid(row=4, column=0, columnspan=2, sticky=W + E)
		# Table
		self.tree = ttk.Treeview(height=10, columns=('Name', 'Price', 'Description'))
		self.tree.grid(row=5, column=0, columnspan=3, sticky=E + W)
		self.tree.heading('#0', text="Name", anchor=CENTER)
		self.tree.heading('#1', text="Price", anchor=CENTER)
		self.tree.heading('#2', text="Description", anchor=CENTER)
		# botton
		ttk.Button(text='DELETE', command=self.delete_product).grid(row=6, column=0, sticky=W + E)
		ttk.Button(text='EDIT', command=self.edit_product).grid(row=6, column=1, sticky=W + E)
		self.get_all_product()

	def run_query(self, query, parameters=()):
		with sqlite3.connect(self.db) as conn:
			cursor = conn.cursor()
			result = cursor.execute(query, parameters)
			conn.commit()
			return result

	def get_all_product(self):
		# limpiar la tabla
		record = self.tree.get_children()
		for element in record:
			self.tree.delete(element)
		# query data
		query = 'SELECT * FROM product ORDER BY  name DESC'
		db_rows = self.run_query(query)
		# filling data
		for row in db_rows:
			# print(row)
			self.tree.insert('', 0, text=row[1], values=(row[2], row[3]))

	def validation(self):
		return (
				len(self.name.get()) != 0 and
				len(self.price.get()) != 0 and
				len(self.description.get()) != 0
		)

	def add_product(self):
		if self.validation():
			query = 'INSERT INTO product VALUES (NULL, ?, ?, ?)'
			parameters = (self.name.get(), self.price.get(), self.description.get())
			self.run_query(query, parameters)
			self.get_all_product()
			self.message['text'] = 'Product {} added successfully'.format(self.name.get())
			self.message['fg'] = 'green'
			self.name.delete(0, END)
			self.price.delete(0, END)
			self.description.delete(0, END)
			print("Product add successfully")
		else:
			self.message['text'] = 'No Product Selected'
			self.message['fg'] = 'red'
			self.get_all_product()

	def delete_product(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError as e:
			self.message['text'] = 'Select a Record'
			self.message['fg'] = 'red'
			print(e)
			return

		self.message['text'] = ''
		name = self.tree.item(self.tree.selection())['text']
		query = 'DELETE FROM product WHERE name = ?'
		self.run_query(query, (name,))
		self.message['text'] = 'Record {} deleted successfully'.format(name)
		self.message['fg'] = 'blue'
		self.get_all_product()

	def edit_product(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())
		except IndexError as e:
			self.message['text'] = 'Select a Record'
			self.message['fg'] = 'red'
			print(e)
			return
		self.message['text'] = ''
		name = self.tree.item(self.tree.selection())['text']
		old_price = self.tree.item(self.tree.selection())['values'][0]
		old_description = self.tree.item(self.tree.selection())['values'][1]
		#
		self.edit_wind = Toplevel()
		self.edit_wind.title("Edit Product")
		#
		Label(self.edit_wind, text="Old Name: ").grid(row=0, column=1)
		Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state="readonly").grid(row=0,
		                                                                                                 column=2)
		Label(self.edit_wind, text="New name").grid(row=1, column=1)
		new_name = Entry(self.edit_wind)
		new_name.grid(row=1, column=2)
		#
		Label(self.edit_wind, text="Old Price: ").grid(row=2, column=1)
		Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state="readonly").grid(row=2,
		                                                                                                      column=2)
		Label(self.edit_wind, text="New Price").grid(row=3, column=1)
		new_price = Entry(self.edit_wind)
		new_price.grid(row=3, column=2)
		#
		Label(self.edit_wind, text="Old Description: ").grid(row=4, column=1)
		Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_description), state="readonly").grid(
			row=4, column=2)
		Label(self.edit_wind, text="New Description").grid(row=5, column=1)
		new_description = Entry(self.edit_wind)
		new_description.grid(row=5, column=2)

		Button(self.edit_wind, text="UPDATE",
		       command=lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price, new_description.get(), old_description)).grid(row=6,
		                                                                                                       column=1, )

	def edit_records(self, name, new_name, old_price, new_price, old_description, new_description):
		query = 'UPDATE product SET name = ?, price = ?, description = ? WHERE name = ? AND price = ? AND description = ?'
		parameters = (new_name, new_price, new_description, name, old_price, old_description)
		self.run_query(query, parameters)
		self.edit_wind.destroy()
		self.message['text'] = 'Record {} update Succesfully'.format(name)
		self.get_all_product()


if __name__ == '__main__':
	windows = Tk()
	aplicacion = Product(windows)
	windows.mainloop()
