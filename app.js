document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = 'http://localhost/api/alumnos'; // URL de tu API

    const itemsTableBody = document.querySelector('#itemsTable tbody');
    const addItemForm = document.getElementById('addItemForm');
    const nombreInput = document.getElementById('nombre');
    const apellidoInput = document.getElementById('apellido');
    const cursoInput = document.getElementById('curso');

    // Función para obtener y mostrar los items
    function fetchItems() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                itemsTableBody.innerHTML = ''; // Limpiar la tabla
                data.forEach(item => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${item.id}</td>
                        <td>${item.nombre}</td>
                        <td>${item.apellido}</td>
                        <td>${item.curso}</td>
                        <td>
                            <button class="btn-edit" onclick="editItem(${item.id}, '${item.nombre}', '${item.apellido}', '${item.curso}')">Editar</button>
                            <button class="btn-delete" onclick="deleteItem(${item.id})">Eliminar</button>
                        </td>
                    `;
                    itemsTableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error al obtener los items:', error));
    }
    
    // Función para agregar un nuevo item
    addItemForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const newItem = {
            nombre: nombreInput.value,
            apellido: apellidoInput.value,
            curso: cursoInput.value
        };
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newItem)
        })
        .then(response => response.json())
        .then(data => {
            fetchItems(); // Actualizar la lista de items
            addItemForm.reset(); // Limpiar el formulario
        })
        .catch(error => console.error('Error al agregar el item:', error));
    });

    // Función para eliminar un item
    window.deleteItem = function(id) {
        fetch(`${apiUrl}/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                fetchItems(); // Actualizar la lista de items
            } else {
                console.error('Error al eliminar el item');
            }
        })
        .catch(error => console.error('Error al eliminar el item:', error));
    };

    // Función para editar un item
    window.editItem = function(id, nombre, apellido, curso ) {
        const newNombre = prompt('Editar nombre:', nombre);
        const newApellido = prompt('Editar apellido:', apellido);
        const newCurso = prompt('Editar apellido:', curso);
        if (newNombre !== null && newApellido !== null && newCurso !== null) {
            const updatedItem = {
                nombre: newNombre,
                apellido: newApellido,
                curso: newCurso
            };
            fetch(`${apiUrl}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedItem)
            })
            .then(response => response.json())
            .then(data => {
                fetchItems(); // Actualizar la lista de items
            })
            .catch(error => console.error('Error al actualizar el item:', error));
        }
    };

    // Obtener y mostrar los items al cargar la página
    fetchItems();
});
