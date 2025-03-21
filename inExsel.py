
import creds
import pandas as pd
import panel

try:
    # Создаем соединение с базой данных
    conn = panel.conn
    cursor = conn.cursor()
    author = panel.authors
    books = panel.books
    users = panel.users
    statusies = panel.statusies

    # Начинаем формировать запрос
    query = f"""
        SELECT 
            id_library_card, 
            book_name, 
            authors.fio AS author_fio, 
            users.fio AS user_fio, 
            telephon, 
            address, 
            date_in, 
            date_out, 
            date_out_plan, 
            stat_name 
        FROM 
            library_card 
        JOIN 
            books ON book_id = id_book 
        JOIN 
            authors ON author_id = id_author 
        JOIN 
            users ON user_id = id_user 
        JOIN 
            status ON status_id = id_status 
        WHERE 
    """
    conditions = []
    params = []

    if author:
        id_author = ', '.join(['%s'] * len(author))
        conditions.append(f"id_author IN ({id_author})")
        params.extend(author)

    if books:
        id_books = ', '.join(['%s'] * len(books))
        conditions.append(f"id_book IN ({id_books})")
        params.extend(books)

    if users:
        id_users = ', '.join(['%s'] * len(users))
        conditions.append(f"id_user IN ({id_users})")
        params.extend(users)

    if statusies:
        id_statusies = ', '.join(['%s'] * len(statusies))
        conditions.append(f"id_status IN ({id_statusies})")
        params.extend(statusies)

    # Если нет условий, добавляем условие, чтобы запрос был корректным
    if not conditions:
        query += "1=1"  
    else:
        query += " AND ".join(conditions)

    # Выполняем SQL-запрос
    cursor.execute(query, params)

    df = pd.DataFrame(cursor.fetchall(), columns=[
            'Номер взятия книги', 
            'Название книги', 
            'Автор', 
            'Пользователь', 
            'Телефон', 
            'Адрес', 
            'Дата, когда взяли книгу', 
            'Дата, когда вернули книгу', 
            'Дата, когда предположительно должны вернуть книгу', 
            'Статус'
        ])
    
    # Сохраняем в Excel
    df.to_excel('kontrol.xlsx', index=False)

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()