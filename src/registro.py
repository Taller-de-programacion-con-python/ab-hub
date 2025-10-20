usuarios = []

def registrar_usuario(nombre, correo, contraseña):
    """Agrega un nuevo usuario a la lista"""
    usuario = {
        "nombre": nombre,
        "correo": correo,
        "contraseña": contraseña
    }
    usuarios.append(usuario)
    print(f"✅ Usuario {nombre} agregado!")

def mostrar_usuarios():
    """Muestra todos los usuarios en la lista"""
    print("\n--- Lista de usuarios ---")
    for u in usuarios:
        print(f"{u['nombre']} - {u['correo']}")
    print("--------------------------\n")

def buscar_usuario(correo):
    """Busca un usuario por su correo"""
    for u in usuarios:
        if u["correo"] == correo:
            return u
    return None

# Ejemplos
# registrar_usuario("Ana", "ana@mail.com", "1234")
# registrar_usuario("Luis", "luis@mail.com", "abcd")
# registrar_usuario("María", "maria@mail.com", "pass123")

registrar_usuario(input("Ingrese el nombre de usuario: "), input("Ingresa el correo: "), input("Ingresa tu contraseña: "))
mostrar_usuarios()

correo_busqueda = input("Ingresa un correo a buscar: ")
resultado = buscar_usuario(correo_busqueda)

print(f"🔎 Usuario encontrado: {resultado['nombre']}")