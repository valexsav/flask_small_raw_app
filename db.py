from constants import DB_CONNECTION
from db_connect import DBConnect

db = DBConnect(**DB_CONNECTION)


def _add_cursor_wrapper(func):
    def wrapper(*args, **kwargs):
        with db.get_connection().cursor() as __cur:
            return func(__cur, *args, **kwargs)

    return wrapper


@_add_cursor_wrapper
def get_all_tasks(__cur):
    __cur.execute(
        'SELECT id, name, category, description, priority, status '
        'FROM tasks ORDER BY priority DESC, id ASC')
    return __cur.fetchall()


@_add_cursor_wrapper
def add_task_to_db(__cur, name, category, description, priority, status):
    __cur.execute(
        'INSERT INTO tasks '
        '(name, category, description, priority, status) '
        'VALUES (%s, %s, %s, %s, %s)',
        (name, category, description, priority, status)
    )


@_add_cursor_wrapper
def get_tasks_sorted_by_param(__cur, param):
    query = f'''
        SELECT * FROM tasks
        ORDER BY {param} DESC
    '''
    __cur.execute(query)
    return __cur.fetchall()


@_add_cursor_wrapper
def get_task_by_id(__cur, task_id):
    __cur.execute(
        'SELECT id, name, category, description, priority, status '
        'FROM tasks '
        'WHERE id = %s',
        (task_id,)
    )
    return __cur.fetchone()


@_add_cursor_wrapper
def get_task_contents(__cur, task_id):
    __cur.execute(
        'SELECT id, task_id, content '
        'FROM task_comments '
        'WHERE task_id = %s',
        (task_id,)
    )
    return __cur.fetchall()


@_add_cursor_wrapper
def delete_task_from_db(__cur, task_id):
    __cur.execute(
        'DELETE FROM tasks WHERE id = %s',
        (task_id,)
    )


@_add_cursor_wrapper
def edit_task_in_db(__cur, name, category, description, priority, status, task_id):
    __cur.execute(
        'UPDATE tasks '
        'SET name = %s, '
        'category = %s, '
        'description = %s, '
        'priority = %s, '
        'status = %s '
        'WHERE id = %s',
        (name, category, description, priority, status, task_id)
    )
