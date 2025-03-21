import psycopg2
import creds
import tkinter as tk
from tkinter import messagebox

conn = psycopg2.connect(dbname=creds.dbname, user=creds.user, password=creds.password, host=creds.host, port=creds.port)
authors = []
books = []
users = []
statusies = []

def add_label(list2, id, parent, name,list1):
    if id not in list2:
        list2.append(id)
        list1.append(name)
        label_text = f"В сортировку добавлены следующие данные: {', '.join(map(str, list1))}"
    else:
        label_text = "Эти данные уже есть!"
    label = tk.Label(parent, text=label_text)
    label.pack(pady=10)
    return list2

def clear_lists(list1, list2):
    list1.clear()
    list2.clear()

def create_button(rows,frame,form,list1):
    names = [] 
    for row in rows:  
        item_id, item_name = row
        button = tk.Button(frame, text=item_name, command=lambda id=item_id,name=item_name: add_label(list1, id, form, name, names))
        button.pack(pady=5)
    
    button2 = tk.Button(form, text="Сбросить все значения", command=lambda:clear_lists(list1,names))
    button2.pack(pady=10)

    close_button1 = tk.Button(form, text="Выбрать значения", command=form.destroy)
    close_button1.pack(pady=10)

def open_form1(): #авторы
    form1 = tk.Toplevel(root)  
    form1.title("Авторы")

    label1 = tk.Label(form1, text="Выберите авторов, по которым надо сделать выборку!")
    label1.pack(pady=20)

    frame = tk.Frame(form1)
    frame.pack(pady=10)

    cursor = conn.cursor()
    cursor.execute("SELECT id_author, fio FROM authors") 
    rows = cursor.fetchall()
    #print(rows)
    create_button(rows,frame,form1,authors)
    cursor.close()

def open_form2():#читатели
    form2 = tk.Toplevel(root)  
    form2.title("Читатели")
    
    label1 = tk.Label(form2, text="Выберите читателей, по которым надо сделать выборку!")
    label1.pack(pady=20)

    frame = tk.Frame(form2)
    frame.pack(pady=10)

    cursor = conn.cursor()
    cursor.execute("SELECT id_user, fio FROM users") 
    rows = cursor.fetchall()
    #print(rows)
    create_button(rows,frame,form2,users)
    cursor.close()

def open_form3(): #книги
    form3 = tk.Toplevel(root)  
    form3.title("Книги")

    label1 = tk.Label(form3, text="Выберите книги, по которым надо сделать выборку!")
    label1.pack(pady=20)

    frame = tk.Frame(form3)
    frame.pack(pady=10)

    cursor = conn.cursor()
    cursor.execute("SELECT id_book, book_name FROM books") 
    rows = cursor.fetchall()
    #print(rows)
    create_button(rows,frame,form3,books)
    cursor.close()

def open_form4(): #статусы
    form4 = tk.Toplevel(root)  
    form4.title("Статусы")

    label1 = tk.Label(form4, text="Выберите статусы, по которым надо сделать выборку!")
    label1.pack(pady=20)

    frame = tk.Frame(form4)
    frame.pack(pady=10)

    cursor = conn.cursor()
    cursor.execute("SELECT id_status, stat_name FROM status") 
    rows = cursor.fetchall()
    #print(rows)
    create_button(rows,frame,form4,statusies)
    cursor.close()

# Создание главного окна
root = tk.Tk()
root.title("Главная Форма")


# Кнопки для открытия форм
button1 = tk.Button(root, text="Добавить фильтр по автору", command=open_form1)
button1.pack(pady=10)
button2 = tk.Button(root, text="Добавить фильтр по читателю", command=open_form2)
button2.pack(pady=10)
button3 = tk.Button(root, text="Добавить фильтр по книге", command=open_form3)
button3.pack(pady=10)
button4 = tk.Button(root, text="Добавить фильтр по статусу", command=open_form4)
button4.pack(pady=10)
button5 = tk.Button(root, text="Сформировать запрос", command=root.destroy)
button5.pack(pady=10)
# Запуск главного цикла
root.mainloop()