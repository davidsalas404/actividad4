import sqlite3
import datetime

class TaskManager:
    def __init__(self, db_name='tasks.db'):
        # Se inicializa la conexión a la base de datos SQLite y se crea el cursor
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        # Se crea la tabla de tareas si no existe
        self._create_table()

    def _create_table(self):
        # Método privado para crear la tabla de tareas en la base de datos
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY,
                            description TEXT NOT NULL,
                            priority TEXT NOT NULL,
                            due_date TEXT,
                            completed INTEGER
                          )''')
        self.conn.commit()

    def add_task(self, description, priority, due_date=None):
        # Método para agregar una nueva tarea a la base de datos
        # Se convierte la fecha de vencimiento a un objeto datetime si se proporciona
        if due_date:
            try:
                due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Formato de fecha y hora incorrecto. Utilice YYYY-MM-DD HH:MM.")
                return
        else:
            due_date = None
        # Se inserta la tarea en la base de datos
        self.c.execute('''INSERT INTO tasks (description, priority, due_date, completed)
                           VALUES (?, ?, ?, ?)''', (description, priority, due_date, 0))
        self.conn.commit()

    def list_tasks(self):
        # Método para listar todas las tareas de la base de datos
        self.c.execute('''SELECT * FROM tasks ORDER BY due_date''')
        tasks = self.c.fetchall()
        print("Lista de tareas:")
        # Se imprime cada tarea con su información relevante
        for task in tasks:
            completed = "Completada" if task[4] else "Pendiente"
            due_date = task[3] if task[3] else "No especificada"
            print(f"{task[0]}. {task[1]} - Prioridad: {task[2]} - Fecha de vencimiento: {due_date} - Estado: {completed}")

    def remove_task(self, task_id):
        # Método para eliminar una tarea de la base de datos por su ID
        self.c.execute('''DELETE FROM tasks WHERE id=?''', (task_id,))
        self.conn.commit()

    def complete_task(self, task_id):
        # Método para marcar una tarea como completada en la base de datos por su ID
        self.c.execute('''UPDATE tasks SET completed=1 WHERE id=?''', (task_id,))
        self.conn.commit()

    def __del__(self):
        # Método destructor para cerrar la conexión a la base de datos al finalizar
        self.conn.close()


def main():
    # Función principal del programa
    # Se crea una instancia de TaskManager para manejar las tareas
    task_manager = TaskManager()

    while True:
        # Menú principal de opciones
        print("\n1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Marcar tarea como completada")
        print("4. Eliminar tarea")
        print("5. Salir")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            # Opción para agregar una nueva tarea
            description = input("Descripción de la tarea: ")
            priority = input("Prioridad de la tarea (alta, media, baja): ")
            due_date = input("Fecha y hora de vencimiento (opcional - formato: YYYY-MM-DD HH:MM): ")
            task_manager.add_task(description, priority, due_date)
            print("Tarea agregada con éxito.")
        elif choice == "2":
            # Opción para listar todas las tareas
            task_manager.list_tasks()
        elif choice == "3":
            # Opción para marcar una tarea como completada
            task_id = int(input("Ingrese el número de la tarea a marcar como completada: "))
            task_manager.complete_task(task_id)
            print("Tarea marcada como completada.")
        elif choice == "4":
            # Opción para eliminar una tarea
            task_id = int(input("Ingrese el número de la tarea a eliminar: "))
            task_manager.remove_task(task_id)
            print("Tarea eliminada con éxito.")
        elif choice == "5":
            # Opción para salir del programa
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
